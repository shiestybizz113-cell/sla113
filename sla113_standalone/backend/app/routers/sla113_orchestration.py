"""SLA113 Orchestration — Night Queue Worker, Jobs CRUD, Dependencies"""
from fastapi import APIRouter, HTTPException
from datetime import datetime, timezone
from typing import Optional
import uuid
import random
import asyncio
import logging

from app.core.database import get_database
from app.core.sla113_constants import JOB_STAGES, DEFAULT_JOB_STAGES
from app.models.schemas import CreateJobRequest

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/sla113", tags=["sla113-orchestration"])

_worker_running = False
_worker_task = None


def jobs_collection():
    return get_database()["sla113_jobs"]


# ─── Jobs CRUD ───
@router.post("/jobs")
async def create_job(req: CreateJobRequest):
    now = datetime.now(timezone.utc).isoformat()
    stage_names = JOB_STAGES.get(req.preset, DEFAULT_JOB_STAGES)
    stages = [{"name": s, "status": "pending", "progress": 0} for s in stage_names]

    deps = req.depends_on or []
    for dep_id in deps:
        dep = await jobs_collection().find_one({"id": dep_id})
        if not dep:
            raise HTTPException(status_code=400, detail=f"Dependency job {dep_id} not found")

    has_unfinished_deps = False
    if deps:
        for dep_id in deps:
            dep = await jobs_collection().find_one({"id": dep_id}, {"_id": 0})
            if dep and dep.get("status") != "completed":
                has_unfinished_deps = True
                break

    initial_status = "blocked" if has_unfinished_deps else "pending"
    job = {
        "id": f"JOB-{uuid.uuid4().hex[:6].upper()}",
        "preset": req.preset, "status": initial_status, "progress": 0,
        "priority": req.priority, "config": req.config or {},
        "stages": stages, "depends_on": deps, "dependents": [],
        "logs": [f"[{now}] Job queued. Preset: {req.preset}. Dependencies: {len(deps)}. Status: {initial_status}"],
        "created_at": now, "updated_at": now,
    }
    await jobs_collection().insert_one(job)
    job.pop("_id", None)

    for dep_id in deps:
        await jobs_collection().update_one({"id": dep_id}, {"$addToSet": {"dependents": job["id"]}})
    return job


@router.get("/jobs")
async def list_jobs():
    cursor = jobs_collection().find({}, {"_id": 0}).sort("created_at", -1)
    jobs = await cursor.to_list(100)
    return {"jobs": jobs, "total": len(jobs)}


@router.delete("/jobs/{job_id}")
async def delete_job(job_id: str):
    result = await jobs_collection().delete_one({"id": job_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"deleted": True}


@router.put("/jobs/{job_id}/progress")
async def update_job_progress(job_id: str, progress: int, status: Optional[str] = None):
    update = {"progress": progress, "updated_at": datetime.now(timezone.utc).isoformat()}
    if status:
        update["status"] = status
    if progress >= 100:
        update["status"] = "completed"
    result = await jobs_collection().update_one({"id": job_id}, {"$set": update})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Job not found")
    return await jobs_collection().find_one({"id": job_id}, {"_id": 0})


@router.post("/jobs/{job_id}/process")
async def process_job(job_id: str):
    job = await jobs_collection().find_one({"id": job_id}, {"_id": 0})
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if job["status"] == "completed":
        return job
    return await _advance_job(job)


@router.post("/jobs/{job_id}/link")
async def link_dependency(job_id: str, depends_on_id: str):
    job = await jobs_collection().find_one({"id": job_id}, {"_id": 0})
    parent = await jobs_collection().find_one({"id": depends_on_id}, {"_id": 0})
    if not job or not parent:
        raise HTTPException(status_code=404, detail="Job not found")
    if job_id in (parent.get("depends_on") or []):
        raise HTTPException(status_code=400, detail="Circular dependency detected")
    now = datetime.now(timezone.utc).isoformat()
    await jobs_collection().update_one(
        {"id": job_id},
        {"$addToSet": {"depends_on": depends_on_id}, "$push": {"logs": f"[{now}] Linked dependency: {depends_on_id}"}}
    )
    await jobs_collection().update_one({"id": depends_on_id}, {"$addToSet": {"dependents": job_id}})
    if parent.get("status") != "completed":
        await jobs_collection().update_one({"id": job_id}, {"$set": {"status": "blocked", "updated_at": now}})
    return {"linked": True, "job": job_id, "depends_on": depends_on_id}


@router.delete("/jobs/{job_id}/link/{dep_id}")
async def unlink_dependency(job_id: str, dep_id: str):
    now = datetime.now(timezone.utc).isoformat()
    await jobs_collection().update_one({"id": job_id}, {"$pull": {"depends_on": dep_id}})
    await jobs_collection().update_one({"id": dep_id}, {"$pull": {"dependents": job_id}})
    job = await jobs_collection().find_one({"id": job_id}, {"_id": 0})
    if job and job.get("status") == "blocked":
        deps = job.get("depends_on", [])
        all_met = True
        for d in deps:
            parent = await jobs_collection().find_one({"id": d}, {"_id": 0})
            if parent and parent.get("status") != "completed":
                all_met = False
                break
        if all_met:
            await jobs_collection().update_one(
                {"id": job_id},
                {"$set": {"status": "pending", "updated_at": now}, "$push": {"logs": f"[{now}] All dependencies met. Unblocked."}}
            )
    return {"unlinked": True}


@router.get("/jobs/graph")
async def get_dependency_graph():
    cursor = jobs_collection().find({}, {"_id": 0}).sort("created_at", -1)
    jobs = await cursor.to_list(200)
    nodes, edges = [], []
    for j in jobs:
        nodes.append({
            "id": j["id"], "preset": j.get("preset", ""), "status": j.get("status", "pending"),
            "progress": j.get("progress", 0), "depends_on": j.get("depends_on", []),
            "dependents": j.get("dependents", []),
        })
        for dep_id in j.get("depends_on", []):
            edges.append({"from": dep_id, "to": j["id"]})
    return {"nodes": nodes, "edges": edges}


# ─── Background Worker ───
async def _advance_job(job):
    now = datetime.now(timezone.utc).isoformat()
    stages = job.get("stages", [])

    if not stages:
        new_progress = min(job["progress"] + 25, 100)
        new_status = "completed" if new_progress >= 100 else "processing"
        log_msg = f"[{now}] Progress: {new_progress}% — {'Complete.' if new_status == 'completed' else 'Processing...'}"
        await jobs_collection().update_one(
            {"id": job["id"]},
            {"$set": {"progress": new_progress, "status": new_status, "updated_at": now}, "$push": {"logs": log_msg}}
        )
        return await jobs_collection().find_one({"id": job["id"]}, {"_id": 0})

    current_idx = next((i for i, s in enumerate(stages) if s["status"] != "completed"), len(stages))
    if current_idx < len(stages):
        stage = stages[current_idx]
        increment = random.randint(20, 45)
        new_stage_progress = min(stage["progress"] + increment, 100)
        stage["progress"] = new_stage_progress
        if new_stage_progress >= 100:
            stage["status"] = "completed"
            log_msg = f"[{now}] Stage '{stage['name']}' DONE."
        else:
            stage["status"] = "processing"
            log_msg = f"[{now}] {stage['name']}: {new_stage_progress}%"
    else:
        log_msg = f"[{now}] All stages complete."

    total_progress = sum(s["progress"] for s in stages) // len(stages) if stages else 100
    all_done = all(s["status"] == "completed" for s in stages)
    new_status = "completed" if all_done else "processing"
    if all_done:
        log_msg = f"[{now}] ALL STAGES COMPLETE. Job finished."

    await jobs_collection().update_one(
        {"id": job["id"]},
        {"$set": {"stages": stages, "progress": total_progress, "status": new_status, "updated_at": now},
         "$push": {"logs": log_msg}}
    )

    if all_done:
        for dep_id in job.get("dependents", []):
            dep_job = await jobs_collection().find_one({"id": dep_id}, {"_id": 0})
            if dep_job and dep_job.get("status") == "blocked":
                all_deps_met = True
                for parent_id in dep_job.get("depends_on", []):
                    parent = await jobs_collection().find_one({"id": parent_id}, {"_id": 0})
                    if parent and parent.get("status") != "completed":
                        all_deps_met = False
                        break
                if all_deps_met:
                    await jobs_collection().update_one(
                        {"id": dep_id},
                        {"$set": {"status": "pending", "updated_at": now},
                         "$push": {"logs": f"[{now}] Dependencies met. Auto-unblocked by {job['id']}."}}
                    )
                    logger.info(f"Auto-unblocked {dep_id} after {job['id']} completed")

    return await jobs_collection().find_one({"id": job["id"]}, {"_id": 0})


async def night_queue_worker():
    global _worker_running
    _worker_running = True
    logger.info("Night Queue Worker started")
    while _worker_running:
        try:
            active_jobs = await jobs_collection().find(
                {"status": {"$in": ["pending", "processing"]}}, {"_id": 0}
            ).sort("priority", -1).to_list(10)
            for job in active_jobs:
                if not _worker_running:
                    break
                await _advance_job(job)
        except Exception as e:
            logger.error(f"Worker error: {e}")
        await asyncio.sleep(3)
    logger.info("Night Queue Worker stopped")


def start_worker():
    global _worker_task, _worker_running
    if _worker_task and not _worker_task.done():
        return
    _worker_running = True
    _worker_task = asyncio.create_task(night_queue_worker())


def stop_worker():
    global _worker_running
    _worker_running = False


@router.get("/worker/status")
async def worker_status():
    active = await jobs_collection().count_documents({"status": {"$in": ["pending", "processing"]}})
    blocked = await jobs_collection().count_documents({"status": "blocked"})
    completed = await jobs_collection().count_documents({"status": "completed"})
    total = await jobs_collection().count_documents({})
    return {
        "running": _worker_running and _worker_task is not None and not _worker_task.done(),
        "active_jobs": active, "blocked_jobs": blocked, "completed_jobs": completed, "total_jobs": total,
    }


@router.post("/worker/toggle")
async def toggle_worker():
    global _worker_running
    if _worker_running and _worker_task and not _worker_task.done():
        stop_worker()
        return {"status": "stopped"}
    else:
        start_worker()
        return {"status": "started"}
