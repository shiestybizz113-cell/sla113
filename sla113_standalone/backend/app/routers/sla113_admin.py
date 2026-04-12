"""SLA113 Admin — Tenant Management (White Label Mint)"""
from fastapi import APIRouter, HTTPException
from datetime import datetime, timezone
import uuid
import logging

from app.core.database import get_database
from app.models.schemas import CreateTenantRequest

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/sla113", tags=["sla113-admin"])


def tenants_collection():
    return get_database()["sla113_tenants"]


@router.post("/tenants")
async def create_tenant(req: CreateTenantRequest):
    now = datetime.now(timezone.utc).isoformat()
    existing = await tenants_collection().find_one({"subdomain": req.subdomain}, {"_id": 0})
    if existing:
        raise HTTPException(status_code=409, detail=f"Subdomain '{req.subdomain}' already exists")
    tenant = {
        "id": str(uuid.uuid4()), "name": req.name, "subdomain": req.subdomain,
        "status": "provisioning", "credits": 0, "rtp_mode": 92,
        "config": req.config or {}, "created_at": now, "updated_at": now,
    }
    await tenants_collection().insert_one(tenant)
    tenant.pop("_id", None)
    await tenants_collection().update_one(
        {"id": tenant["id"]}, {"$set": {"status": "active", "updated_at": datetime.now(timezone.utc).isoformat()}}
    )
    tenant["status"] = "active"
    return tenant


@router.get("/tenants")
async def list_tenants():
    cursor = tenants_collection().find({}, {"_id": 0})
    tenants = await cursor.to_list(100)
    return {"tenants": tenants, "total": len(tenants)}


@router.delete("/tenants/{tenant_id}")
async def delete_tenant(tenant_id: str):
    result = await tenants_collection().delete_one({"id": tenant_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return {"deleted": True}


@router.put("/tenants/{tenant_id}/credits")
async def update_tenant_credits(tenant_id: str, amount: int):
    result = await tenants_collection().update_one(
        {"id": tenant_id},
        {"$inc": {"credits": amount}, "$set": {"updated_at": datetime.now(timezone.utc).isoformat()}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return await tenants_collection().find_one({"id": tenant_id}, {"_id": 0})


@router.put("/tenants/{tenant_id}/rtp")
async def update_tenant_rtp(tenant_id: str, rtp: int):
    if rtp < 80 or rtp > 99:
        raise HTTPException(status_code=400, detail="RTP must be between 80 and 99")
    await tenants_collection().update_one(
        {"id": tenant_id}, {"$set": {"rtp_mode": rtp, "updated_at": datetime.now(timezone.utc).isoformat()}}
    )
    return await tenants_collection().find_one({"id": tenant_id}, {"_id": 0})
