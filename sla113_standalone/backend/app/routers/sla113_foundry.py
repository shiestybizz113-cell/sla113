"""SLA113 Foundry — Vision Smith Image Generation (Gemini 3 Pro)"""
from fastapi import APIRouter, HTTPException
import os
import uuid
import logging

from emergentintegrations.llm.chat import LlmChat, UserMessage
from app.core.sla113_constants import ASSET_TYPE_PROMPTS, STYLE_PROMPTS
from app.models.schemas import ImageGenRequest

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/sla113", tags=["sla113-foundry"])


@router.post("/vision/generate-image")
async def generate_image(req: ImageGenRequest):
    """Generate AAA-quality game art assets using Gemini 3 Pro Image Generation."""
    gemini_key = os.environ.get("GEMINI_API_KEY")
    if not gemini_key:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY not configured")

    asset_prefix = ASSET_TYPE_PROMPTS.get(req.asset_type, ASSET_TYPE_PROMPTS["concept_art"])
    style_suffix = STYLE_PROMPTS.get(req.style, STYLE_PROMPTS["pixel_art"])

    full_prompt = (
        f"{asset_prefix}"
        f"Subject: {req.prompt}. "
        f"Art Direction: {style_suffix} "
        f"Render at maximum detail and clarity. Professional game studio production quality. "
        f"Absolutely no watermarks, no text overlays, no signatures, no logos, no borders, no labels."
    )

    try:
        session_id = f"vision-smith-{uuid.uuid4().hex[:8]}"
        chat = LlmChat(
            api_key=gemini_key, session_id=session_id,
            system_message="You are an elite AAA game art director. Generate exactly what is requested with maximum quality."
        )
        chat.with_model("gemini", "gemini-3-pro-image-preview").with_params(modalities=["image", "text"])

        msg = UserMessage(text=full_prompt)
        text_response, images = await chat.send_message_multimodal_response(msg)

        if images and len(images) > 0:
            image_base64 = images[0]['data']
            return {"image_base64": image_base64, "prompt": req.prompt, "style": req.style, "asset_type": req.asset_type}

        raise HTTPException(status_code=500, detail="No image generated")
    except Exception as e:
        logger.error(f"Gemini image generation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Image generation failed: {str(e)}")


@router.get("/vision/styles")
async def list_vision_styles():
    return {"styles": list(STYLE_PROMPTS.keys()), "asset_types": list(ASSET_TYPE_PROMPTS.keys())}
