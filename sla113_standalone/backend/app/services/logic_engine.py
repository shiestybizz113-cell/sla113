"""SLA113 Logic Engine Service — AI Game Math & Mechanics Generation"""
import os
import json
import time
import uuid
import logging
from typing import Dict, Any, Optional

from emergentintegrations.llm.chat import LlmChat, UserMessage

logger = logging.getLogger(__name__)

LOGIC_TEMPLATES = {
    "fish_shooter": {"mechanics": ["weapon_types", "fish_values", "hit_detection", "multipliers", "boss_mechanics"], "rtp": {"target": 96.5, "variance": "medium-high"}, "economy": ["coin_earn_rates", "weapon_costs", "upgrade_paths"]},
    "slot_machine": {"mechanics": ["reel_config", "paylines", "wild_mechanics", "scatter_trigger", "bonus_rounds", "free_spins"], "rtp": {"target": 96.0, "variance": "medium"}, "paytable": ["symbol_values", "combo_multipliers", "jackpot_tiers"]},
    "crash_game": {"mechanics": ["multiplier_curve", "crash_probability", "cashout_mechanics", "auto_cashout"], "rtp": {"target": 97.0, "variance": "high"}, "economy": ["min_max_bets", "house_edge", "payout_limits"]},
    "platformer": {"mechanics": ["physics_config", "jump_params", "enemy_ai", "collision_rules", "power_up_effects"], "levels": ["difficulty_curve", "spawn_rates", "checkpoint_spacing"], "scoring": ["point_values", "combo_system", "time_bonuses"]},
    "puzzle": {"mechanics": ["match_rules", "board_generation", "cascade_logic", "special_pieces", "objectives"], "levels": ["difficulty_progression", "move_limits", "star_thresholds"], "scoring": ["base_points", "combo_multipliers", "time_bonus"]},
}


async def generate_logic(
    project: Dict[str, Any], logic_type: str = "mechanics",
    difficulty: str = "medium", custom_requirements: Optional[str] = None,
) -> Dict[str, Any]:
    start = time.time()
    api_key = os.environ.get("EMERGENT_LLM_KEY")
    if not api_key:
        raise ValueError("EMERGENT_LLM_KEY not configured")

    game_type = project.get("game_type", "platformer")
    templates = LOGIC_TEMPLATES.get(game_type, {})
    type_refs = templates.get(logic_type, [])

    system_prompt = f"""You are SLA113, an expert game mathematician and mechanics designer.
You generate precise, balanced game logic specifications with real numbers.
Always respond with valid JSON only, no markdown.

Game Type: {project.get('game_type_info', {}).get('name', game_type)}
Difficulty: {difficulty}
Project: {project.get('name', 'Untitled')}"""

    prompts_by_type = {
        "mechanics": f"Generate complete game mechanics specification for this {game_type} game.\nReference areas: {json.dumps(type_refs)}\n\nReturn JSON.",
        "rtp": f"Generate RTP mathematical proof for this {game_type} game.\nTarget RTP: {templates.get('rtp', {}).get('target', 96.0)}%\nReturn JSON.",
        "paytable": f"Generate a complete paytable for this {game_type} game.\nReturn JSON.",
        "scoring": f"Generate a scoring system for this {game_type} game.\nReturn JSON.",
        "levels": f"Generate level design specifications for this {game_type} game with difficulty={difficulty}.\nReturn JSON.",
        "economy": f"Generate in-game economy design for this {game_type} game.\nReference: {json.dumps(templates.get('economy', []))}\nReturn JSON.",
        "rng": f"Generate RNG specification for this {game_type} game.\nReturn JSON.",
    }

    user_prompt = custom_requirements or prompts_by_type.get(logic_type, prompts_by_type["mechanics"])

    chat = LlmChat(api_key=api_key, session_id=f"sla113-logic-{uuid.uuid4().hex[:8]}", system_message=system_prompt)
    chat.with_model("openai", "gpt-4o-mini")
    raw = await chat.send_message(UserMessage(text=user_prompt))

    try:
        cleaned = raw.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("\n", 1)[1].rsplit("```", 1)[0]
        specs = json.loads(cleaned)
    except json.JSONDecodeError:
        specs = {"raw_output": raw, "logic_type": logic_type}

    elapsed = round(time.time() - start, 2)
    return {"project_id": project.get("id", ""), "logic_type": logic_type, "difficulty": difficulty, "specs": specs, "generation_time": elapsed}
