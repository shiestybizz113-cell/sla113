"""SLA113 API Router - Universal AI Game Studio"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timezone
import uuid
import logging
import os
import json
from emergentintegrations.llm.chat import LlmChat, UserMessage

from database import get_database
from sla113.models import (
    GAME_TYPES,
    CreateProjectRequest,
    VisionGenerateRequest,
    LogicGenerateRequest,
    ComposeRequest,
)
from sla113.vision_engine import generate_vision_assets
from sla113.logic_engine import generate_logic
from sla113.composer_engine import compose_game_bundle

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/sla113", tags=["sla113"])

# In-memory session store for terminal conversations
_terminal_sessions = {}


class TerminalRequest(BaseModel):
    command: str
    session_id: Optional[str] = "default"


def projects_collection():
    return get_database()["sla113_projects"]


# ─── Game Types ───
@router.get("/game-types")
async def list_game_types():
    """List all supported game types."""
    return {"game_types": GAME_TYPES}


# ─── Projects CRUD ───
@router.post("/projects")
async def create_project(req: CreateProjectRequest):
    """Create a new game project."""
    if req.game_type not in GAME_TYPES:
        raise HTTPException(status_code=400, detail=f"Unsupported game type: {req.game_type}. Supported: {list(GAME_TYPES.keys())}")

    now = datetime.now(timezone.utc).isoformat()
    project = {
        "id": str(uuid.uuid4()),
        "name": req.name,
        "game_type": req.game_type,
        "game_type_info": GAME_TYPES[req.game_type],
        "description": req.description or GAME_TYPES[req.game_type]["description"],
        "theme": req.theme or "default",
        "target_platform": req.target_platform,
        "status": "created",
        "vision_assets": [],
        "logic_specs": [],
        "compositions": [],
        "created_at": now,
        "updated_at": now,
    }

    await projects_collection().insert_one(project)
    project.pop("_id", None)
    return project


@router.get("/projects")
async def list_projects():
    """List all game projects."""
    cursor = projects_collection().find({}, {"_id": 0})
    projects = await cursor.to_list(100)
    return {"projects": projects, "total": len(projects)}


@router.get("/projects/{project_id}")
async def get_project(project_id: str):
    """Get a game project by ID."""
    project = await projects_collection().find_one({"id": project_id}, {"_id": 0})
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.delete("/projects/{project_id}")
async def delete_project(project_id: str):
    """Delete a game project."""
    result = await projects_collection().delete_one({"id": project_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"deleted": True, "project_id": project_id}


# ─── Vision Engine ───
@router.post("/vision/generate")
async def generate_vision(req: VisionGenerateRequest):
    """Generate visual assets for a game project."""
    project = await projects_collection().find_one({"id": req.project_id}, {"_id": 0})
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    try:
        result = await generate_vision_assets(
            project=project,
            asset_type=req.asset_type,
            style=req.style,
            count=req.count,
            custom_prompt=req.custom_prompt,
        )

        # Save generated assets to project
        await projects_collection().update_one(
            {"id": req.project_id},
            {
                "$push": {"vision_assets": result},
                "$set": {"status": "vision_generated", "updated_at": datetime.now(timezone.utc).isoformat()},
            },
        )
        return result

    except Exception as e:
        logger.error(f"Vision generation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Vision generation failed: {str(e)}")


# ─── Logic Engine ───
@router.post("/logic/generate")
async def generate_game_logic(req: LogicGenerateRequest):
    """Generate game logic/math for a project."""
    project = await projects_collection().find_one({"id": req.project_id}, {"_id": 0})
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    try:
        result = await generate_logic(
            project=project,
            logic_type=req.logic_type,
            difficulty=req.difficulty,
            custom_requirements=req.custom_requirements,
        )

        await projects_collection().update_one(
            {"id": req.project_id},
            {
                "$push": {"logic_specs": result},
                "$set": {"status": "logic_generated", "updated_at": datetime.now(timezone.utc).isoformat()},
            },
        )
        return result

    except Exception as e:
        logger.error(f"Logic generation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Logic generation failed: {str(e)}")


# ─── Composer Engine ───
@router.post("/compose")
async def compose_game(req: ComposeRequest):
    """Compose a complete game bundle from generated assets."""
    project = await projects_collection().find_one({"id": req.project_id}, {"_id": 0})
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    try:
        result = await compose_game_bundle(
            project=project,
            include_vision=req.include_vision,
            include_logic=req.include_logic,
            output_format=req.output_format,
        )

        await projects_collection().update_one(
            {"id": req.project_id},
            {
                "$push": {"compositions": result},
                "$set": {"status": "composed", "updated_at": datetime.now(timezone.utc).isoformat()},
            },
        )
        return result

    except Exception as e:
        logger.error(f"Composition failed: {e}")
        raise HTTPException(status_code=500, detail=f"Composition failed: {str(e)}")


# ─── Quick Stats ───
@router.get("/stats")
async def get_stats():
    """Get SLA113 platform stats."""
    total = await projects_collection().count_documents({})
    by_type = {}
    for gt in GAME_TYPES:
        count = await projects_collection().count_documents({"game_type": gt})
        if count > 0:
            by_type[gt] = count

    return {
        "total_projects": total,
        "by_game_type": by_type,
        "supported_game_types": len(GAME_TYPES),
        "engines": ["vision", "logic", "composer"],
        "version": "1.0.0",
    }



# ─── AI Terminal (Sovereign Overseer) ───
@router.post("/terminal")
async def terminal_command(req: TerminalRequest):
    """AI Terminal — Sovereign Overseer with full platform context."""
    api_key = os.environ.get("EMERGENT_LLM_KEY")
    if not api_key:
        return {"response": "[ERROR] EMERGENT_LLM_KEY not configured. Overseer offline."}

    # Gather live platform context
    total_projects = await projects_collection().count_documents({})
    recent_projects = await projects_collection().find({}, {"_id": 0, "name": 1, "game_type": 1, "status": 1, "theme": 1}).sort("created_at", -1).to_list(10)

    by_type = {}
    for gt in GAME_TYPES:
        c = await projects_collection().count_documents({"game_type": gt})
        if c > 0:
            by_type[gt] = c

    platform_context = json.dumps({
        "total_projects": total_projects,
        "projects_by_type": by_type,
        "recent_projects": recent_projects,
        "supported_game_types": list(GAME_TYPES.keys()),
        "engines": ["vision", "logic", "composer"],
    }, indent=2)

    system_msg = f"""You are the SOVEREIGN OVERSEER of SLA113 — the most advanced AI game creation platform on Earth.

IDENTITY: You are a military-grade AI command system. Your tone is terse, authoritative, and precise. Use UPPERCASE for emphasis. Respond in terminal/monospace style with > prefixes.

PLATFORM STATE:
{platform_context}

CAPABILITIES:
- You have full knowledge of all 16 game types: casino (fish shooter, slots, crash, cards) and AAA (open world/GTA, tactical FPS/COD, fighting/MK, fantasy RPG, survival horror, platformer, puzzle, tower defense, runner, battle royale, racing, sports)
- You can advise on RTP calculations, game math, asset generation strategy, architecture decisions
- You understand game economy design, probability math, and certification requirements
- You track all active projects and their generation status

RULES:
- Keep responses under 150 words
- Use > prefix for each line
- Reference specific project data when relevant
- Be direct. No fluff. Canon enforcement at all times.
- If asked to generate something, explain what engine to use and how"""

    session_id = req.session_id or "default"

    # Get or create chat session
    if session_id not in _terminal_sessions:
        chat = LlmChat(
            api_key=api_key,
            session_id=f"sla113-overseer-{session_id}",
            system_message=system_msg,
        )
        chat.with_model("openai", "gpt-4o-mini")
        _terminal_sessions[session_id] = chat
    else:
        chat = _terminal_sessions[session_id]

    try:
        response = await chat.send_message(UserMessage(text=req.command))
        return {"response": response, "session_id": session_id}
    except Exception as e:
        logger.error(f"Terminal error: {e}")
        return {"response": f"> [ERROR] Overseer fault: {str(e)}", "session_id": session_id}
