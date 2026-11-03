from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field

from agent_video_studio.creation.models import SceneEdit
from agent_video_studio.publishing.models import PublishRequest


class ProjectCreateRequest(BaseModel):
    title: str = Field(min_length=1, max_length=180)
    mode: Literal["prompt", "repurpose"]
    brief: str = Field(default="", max_length=12000)
    language: str = Field(default="en", max_length=40)
    aspect_ratios: list[Literal["9:16", "16:9", "1:1"]] = Field(default_factory=lambda: ["9:16"], max_length=3)


class ProjectUpdateRequest(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=180)
    brief: str | None = Field(default=None, max_length=12000)
    language: str | None = Field(default=None, max_length=40)
    aspect_ratios: list[Literal["9:16", "16:9", "1:1"]] | None = Field(default=None, max_length=3)


class ScriptRequest(BaseModel):
    language: str | None = Field(default=None, max_length=40)
    target_duration_seconds: int = Field(default=60, ge=10, le=3600)
    platform: str = Field(default="short-form social video", max_length=100)


class AnalyzeRequest(BaseModel):
    model: str = Field(default="small", max_length=80)


class HighlightSelectionRequest(BaseModel):
    selected_ids: list[str] = Field(min_length=1, max_length=30)


class RenderRequest(BaseModel):
    aspect_ratios: list[Literal["9:16", "16:9", "1:1"]] | None = Field(default=None, max_length=3)
    include_captions: bool = True
    use_tts: bool = True


class ProjectDocumentUpdate(BaseModel):
    music_asset_id: str | None = None
    hashtags: list[str] | None = None
    brand: dict[str, Any] | None = None


class SceneEditRequest(SceneEdit):
    pass


class PublishExportRequest(BaseModel):
    render_id: str = Field(min_length=8, max_length=40, pattern=r"^[a-f0-9]+$")
    aspect_ratio: Literal["9:16", "16:9", "1:1"]
    platform: Literal["youtube", "instagram", "tiktok"]
    title: str = Field(min_length=1, max_length=500)
    description: str = Field(default="", max_length=5000)
    privacy_level: str = Field(default="private", max_length=60)
    confirm: bool = False
    share_to_feed: bool = True
    ai_generated: bool = True

    def to_publish_request(self, project_id: str) -> PublishRequest:
        privacy = self.privacy_level
        if self.platform == "tiktok" and privacy == "private":
            privacy = "SELF_ONLY"
        return PublishRequest(
            project_id=project_id,
            render_id=self.render_id,
            aspect_ratio=self.aspect_ratio,
            platform=self.platform,
            title=self.title,
            description=self.description,
            privacy_level=privacy,
            confirm=self.confirm,
            share_to_feed=self.share_to_feed,
            ai_generated=self.ai_generated,
        )

\n