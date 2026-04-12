"""SLA113 Factory — Build Pipeline Engine"""
from fastapi import APIRouter, HTTPException
from datetime import datetime, timezone
import uuid
import random
import logging

from app.core.database import get_database
from app.models.schemas import CreateBuildRequest

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/sla113", tags=["sla113-factory"])


def projects_collection():
    return get_database()["sla113_projects"]

def builds_collection():
    return get_database()["sla113_builds"]


@router.post("/builds")
async def create_build(req: CreateBuildRequest):
    project = await projects_collection().find_one({"id": req.project_id}, {"_id": 0})
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    now = datetime.now(timezone.utc).isoformat()
    build = {
        "id": f"BLD-{uuid.uuid4().hex[:8].upper()}",
        "project_id": req.project_id, "project_name": project.get("name", "Unknown"),
        "game_type": project.get("game_type", "unknown"), "target": req.target,
        "optimization": req.optimization, "include_assets": req.include_assets,
        "include_logic": req.include_logic, "status": "queued", "progress": 0,
        "stages": [
            {"name": "Asset Compilation", "status": "pending", "progress": 0},
            {"name": "Logic Binding", "status": "pending", "progress": 0},
            {"name": "Shader Compilation", "status": "pending", "progress": 0},
            {"name": "Bundle Packaging", "status": "pending", "progress": 0},
            {"name": "Optimization Pass", "status": "pending", "progress": 0},
        ],
        "output": None, "size_mb": None,
        "logs": [f"[{now}] Build queued. Target: {req.target}, Optimization: {req.optimization}"],
        "created_at": now, "updated_at": now,
    }
    await builds_collection().insert_one(build)
    build.pop("_id", None)
    return build


@router.get("/builds")
async def list_builds():
    cursor = builds_collection().find({}, {"_id": 0}).sort("created_at", -1)
    builds = await cursor.to_list(100)
    return {"builds": builds, "total": len(builds)}


@router.post("/builds/{build_id}/advance")
async def advance_build(build_id: str):
    build = await builds_collection().find_one({"id": build_id}, {"_id": 0})
    if not build:
        raise HTTPException(status_code=404, detail="Build not found")
    if build["status"] == "completed":
        return build
    stages = build["stages"]
    now = datetime.now(timezone.utc).isoformat()
    current_stage_idx = next((i for i, s in enumerate(stages) if s["status"] != "completed"), len(stages))
    if current_stage_idx < len(stages):
        stage = stages[current_stage_idx]
        new_progress = min(stage["progress"] + random.randint(30, 60), 100)
        stage["progress"] = new_progress
        if new_progress >= 100:
            stage["status"] = "completed"
            log_msg = f"[{now}] Stage '{stage['name']}' completed."
        else:
            stage["status"] = "processing"
            log_msg = f"[{now}] Stage '{stage['name']}' at {new_progress}%..."
    else:
        log_msg = f"[{now}] All stages completed."
    total_progress = sum(s["progress"] for s in stages) // len(stages)
    all_done = all(s["status"] == "completed" for s in stages)
    new_status = "completed" if all_done else "building"
    output, size_mb = None, None
    if all_done:
        target = build["target"]
        output = f"sla113_{build['project_name'].lower().replace(' ', '_')}_{build['id']}.{'apk' if target == 'apk' else 'zip'}"
        size_mb = round(random.uniform(12.5, 185.0), 1)
        log_msg += f"\n[{now}] Build artifact: {output} ({size_mb} MB)"
    await builds_collection().update_one(
        {"id": build_id},
        {"$set": {"stages": stages, "progress": total_progress, "status": new_status,
                  "output": output, "size_mb": size_mb, "updated_at": now},
         "$push": {"logs": log_msg}}
    )
    return await builds_collection().find_one({"id": build_id}, {"_id": 0})


@router.delete("/builds/{build_id}")
async def delete_build(build_id: str):
    result = await builds_collection().delete_one({"id": build_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Build not found")
    return {"deleted": True}
