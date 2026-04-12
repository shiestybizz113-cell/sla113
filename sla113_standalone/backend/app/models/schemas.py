"""SLA113 Pydantic Models"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


# ─── Projects ───
class CreateProjectRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    game_type: str = Field(..., description="One of the supported game types")
    description: Optional[str] = None
    theme: Optional[str] = Field(None, description="Visual theme: cyberpunk, fantasy, ocean, space, etc.")
    target_platform: str = Field(default="web", description="web, mobile, or both")


# ─── Vision Engine ───
class VisionGenerateRequest(BaseModel):
    project_id: str
    asset_type: str = Field(default="sprites", description="sprites, backgrounds, ui, animations, effects")
    style: Optional[str] = Field(None, description="pixel_art, vector, 3d_render, hand_drawn, anime")
    count: int = Field(default=5, ge=1, le=20)
    custom_prompt: Optional[str] = None


class ImageGenRequest(BaseModel):
    prompt: str
    style: str = "pixel_art"
    asset_type: str = "concept_art"
    size: str = "1024x1024"
    quality: str = "high"


# ─── Logic Engine ───
class LogicGenerateRequest(BaseModel):
    project_id: str
    logic_type: str = Field(default="mechanics", description="mechanics, rtp, paytable, rng, scoring, levels, economy")
    difficulty: str = Field(default="medium", description="easy, medium, hard, progressive")
    custom_requirements: Optional[str] = None


# ─── Composer Engine ───
class ComposeRequest(BaseModel):
    project_id: str
    include_vision: bool = True
    include_logic: bool = True
    output_format: str = Field(default="json", description="json, html5, specification")


# ─── Terminal ───
class TerminalRequest(BaseModel):
    command: str
    session_id: Optional[str] = "default"


# ─── Tenants ───
class CreateTenantRequest(BaseModel):
    name: str
    subdomain: str
    config: Optional[dict] = None


# ─── Jobs (Night Queue) ───
class CreateJobRequest(BaseModel):
    preset: str
    config: Optional[dict] = None
    priority: str = "normal"
    depends_on: Optional[List[str]] = None


# ─── Pipelines ───
class CreatePipelineRequest(BaseModel):
    name: str
    type: str = "Automation"
    lane: int = 1


# ─── Build Pipeline ───
class CreateBuildRequest(BaseModel):
    project_id: str
    target: str = "webgl"  # webgl | apk | both
    optimization: str = "balanced"  # speed | balanced | size
    include_assets: bool = True
    include_logic: bool = True


# ─── Compliance ───
class ComplianceCheckRequest(BaseModel):
    project_id: str
    jurisdiction: str = "GLI"  # GLI | MGA | UKGC | CURACAO | INTERNAL
    check_type: str = "full"  # full | rtp_only | rng_only | fairness


# ─── Deploy ───
class DeployRequest(BaseModel):
    build_id: str
    target_cdn: str = "cloudflare"  # cloudflare | aws | gcp | custom
    region: str = "us-west"
    auto_ssl: bool = True
