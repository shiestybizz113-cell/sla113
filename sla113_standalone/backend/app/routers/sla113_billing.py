"""SLA113 Billing — Revenue Pipelines"""
from fastapi import APIRouter, HTTPException
from datetime import datetime, timezone
import uuid
import random
import logging

from app.core.database import get_database
from app.core.sla113_constants import DEFAULT_PIPELINES
from app.models.schemas import CreatePipelineRequest

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/sla113", tags=["sla113-billing"])


def pipelines_collection():
    return get_database()["sla113_pipelines"]


@router.post("/pipelines")
async def create_pipeline(req: CreatePipelineRequest):
    now = datetime.now(timezone.utc).isoformat()
    pipeline = {
        "id": str(uuid.uuid4()), "name": req.name, "type": req.type, "lane": req.lane,
        "status": "active", "heartbeat": "idle", "executions": 0, "revenue": 0,
        "created_at": now, "updated_at": now,
    }
    await pipelines_collection().insert_one(pipeline)
    pipeline.pop("_id", None)
    return pipeline


@router.get("/pipelines")
async def list_pipelines():
    cursor = pipelines_collection().find({}, {"_id": 0})
    pipelines = await cursor.to_list(100)
    total_revenue = sum(p.get("revenue", 0) for p in pipelines)
    return {"pipelines": pipelines, "total": len(pipelines), "total_revenue": total_revenue}


@router.put("/pipelines/{pipeline_id}/pulse")
async def pulse_pipeline(pipeline_id: str):
    rev = random.randint(50, 500)
    now = datetime.now(timezone.utc).isoformat()
    result = await pipelines_collection().update_one(
        {"id": pipeline_id},
        {"$set": {"heartbeat": "active", "updated_at": now}, "$inc": {"executions": 1, "revenue": rev}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Pipeline not found")
    return await pipelines_collection().find_one({"id": pipeline_id}, {"_id": 0})


@router.delete("/pipelines/{pipeline_id}")
async def delete_pipeline(pipeline_id: str):
    result = await pipelines_collection().delete_one({"id": pipeline_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Pipeline not found")
    return {"deleted": True}


async def seed_default_pipelines():
    count = await pipelines_collection().count_documents({})
    if count == 0:
        now = datetime.now(timezone.utc).isoformat()
        for d in DEFAULT_PIPELINES:
            await pipelines_collection().insert_one({
                "id": str(uuid.uuid4()), **d, "status": "active", "heartbeat": "idle",
                "executions": 0, "revenue": 0, "created_at": now, "updated_at": now,
            })
        logger.info("Seeded 6 default pipelines")
