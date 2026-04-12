"""SLA113 Universe Registry — Auto-discover all mounted universe routers"""
from fastapi import APIRouter, HTTPException
from datetime import datetime, timezone
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/sla113", tags=["sla113-universes"])

_universe_registry = {}


def register_universe(uid: str, name: str, description: str, prefix: str, engine: str = "internal", product: str = None, status: str = "online"):
    """Register a universe into the SLA113 sovereign registry."""
    _universe_registry[uid] = {
        "id": uid,
        "name": name,
        "description": description,
        "prefix": prefix,
        "engine": engine,
        "product": product,
        "status": status,
        "registered_at": datetime.now(timezone.utc).isoformat(),
    }


# Auto-register known universes on import
register_universe("sla113", "SLA113 Core", "Sovereign Operator OS — Game Studio Platform", "/api/sla113", engine="fastapi+mongodb", product="SLA113 Operator OS")
register_universe("empire1", "Empire 1", "Hybrid Intelligence Core — 19 AI Engines", "/api/empire1", engine="emergent-llm", product="Hybrid Intelligence SaaS")
register_universe("southern", "Southern Lifestyle", "SouthernLifestyle Game OS", "/api/southern", engine="internal", product="Southern Game OS")
register_universe("soulfire", "Soulfire Ecosystem", "ASW + El Coro + Sentinel + SL Universal", "/api/soulfire", engine="vertex-ai", product="Lyrica 3 Pro — AI Music Creation")


@router.get("/universes")
async def list_universes():
    """Auto-discover all registered universes and their live status."""
    return {
        "universes": list(_universe_registry.values()),
        "total": len(_universe_registry),
        "sovereign": "SLA113",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@router.get("/universes/{universe_id}")
async def get_universe(universe_id: str):
    if universe_id not in _universe_registry:
        raise HTTPException(status_code=404, detail=f"Universe '{universe_id}' not found")
    return _universe_registry[universe_id]


@router.post("/universes/register")
async def register_universe_endpoint(uid: str, name: str, description: str, prefix: str, engine: str = "internal", product: str = None):
    """Dynamically register a new universe at runtime."""
    register_universe(uid, name, description, prefix, engine, product)
    return {"registered": True, "universe": _universe_registry[uid]}


@router.delete("/universes/{universe_id}")
async def deregister_universe(universe_id: str):
    if universe_id not in _universe_registry:
        raise HTTPException(status_code=404, detail=f"Universe '{universe_id}' not found")
    removed = _universe_registry.pop(universe_id)
    return {"deregistered": True, "universe": removed}
