"""SLA113 Factory / Deploy Engine — CDN Deployment"""
from fastapi import APIRouter, HTTPException
from datetime import datetime, timezone
import uuid
import random
import logging

from app.core.database import get_database
from app.models.schemas import DeployRequest

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/sla113", tags=["sla113-deploy"])


def builds_collection():
    return get_database()["sla113_builds"]

def deployments_collection():
    return get_database()["sla113_deployments"]


@router.post("/deploy")
async def deploy_build(req: DeployRequest):
    build = await builds_collection().find_one({"id": req.build_id}, {"_id": 0})
    if not build:
        raise HTTPException(status_code=404, detail="Build not found")
    if build["status"] != "completed":
        raise HTTPException(status_code=400, detail="Build must be completed before deployment")
    now = datetime.now(timezone.utc).isoformat()
    deployment = {
        "id": f"DPL-{uuid.uuid4().hex[:8].upper()}", "build_id": req.build_id,
        "project_name": build.get("project_name", "Unknown"), "target_cdn": req.target_cdn,
        "region": req.region, "auto_ssl": req.auto_ssl, "status": "deploying", "progress": 0,
        "url": None, "ssl_status": "pending" if req.auto_ssl else "disabled",
        "logs": [f"[{now}] Deployment initiated. CDN: {req.target_cdn}, Region: {req.region}"],
        "created_at": now, "updated_at": now,
    }
    await deployments_collection().insert_one(deployment)
    deployment.pop("_id", None)
    return deployment


@router.post("/deploy/{deploy_id}/advance")
async def advance_deployment(deploy_id: str):
    deploy = await deployments_collection().find_one({"id": deploy_id}, {"_id": 0})
    if not deploy:
        raise HTTPException(status_code=404, detail="Deployment not found")
    if deploy["status"] == "live":
        return deploy
    now = datetime.now(timezone.utc).isoformat()
    new_progress = min(deploy["progress"] + random.randint(25, 50), 100)
    new_status = "live" if new_progress >= 100 else "propagating"
    url, ssl_status = None, deploy.get("ssl_status", "pending")
    if new_progress >= 100:
        slug = deploy["project_name"].lower().replace(" ", "-")
        cdn = deploy["target_cdn"]
        url = f"https://{slug}.{'cdn.cloudflare.com' if cdn == 'cloudflare' else 'd2x.amazonaws.com' if cdn == 'aws' else 'storage.googleapis.com' if cdn == 'gcp' else 'custom-cdn.io'}"
        ssl_status = "active" if deploy.get("auto_ssl") else "disabled"
    log_msg = f"[{now}] {'LIVE — CDN propagation complete.' if new_progress >= 100 else f'Propagating... {new_progress}%'}"
    await deployments_collection().update_one(
        {"id": deploy_id},
        {"$set": {"progress": new_progress, "status": new_status, "url": url,
                  "ssl_status": ssl_status, "updated_at": now},
         "$push": {"logs": log_msg}}
    )
    return await deployments_collection().find_one({"id": deploy_id}, {"_id": 0})


@router.get("/deployments")
async def list_deployments():
    cursor = deployments_collection().find({}, {"_id": 0}).sort("created_at", -1)
    deploys = await cursor.to_list(100)
    return {"deployments": deploys, "total": len(deploys)}


@router.delete("/deploy/{deploy_id}")
async def delete_deployment(deploy_id: str):
    result = await deployments_collection().delete_one({"id": deploy_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Deployment not found")
    return {"deleted": True}
