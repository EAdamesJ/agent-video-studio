from __future__ import annotations

from pydantic import BaseModel, Field


class SceneDraft(BaseModel):
    id: str = ""
    title: str = Field(min_length=1, max_length=120)
    narration: str = Field(min_length=1, max_length=4000)
    visual_direction: str = Field(default="", max_length=1000)
    asset_search_query: str = Field(default="", max_length=300)
    duration_seconds: float = Field(default=6, ge=1, le=60)
    caption_text: str = Field(default="", max_length=2000)


class ScriptDocument(BaseModel):
    title: str = Field(min_length=1, max_length=180)
    hook: str = Field(default="", max_length=500)
    call_to_action: str = Field(default="", max_length=500)
    language: str = Field(default="en", max_length=40)
    scenes: list[SceneDraft] = Field(min_length=1, max_length=80)


class SceneEdit(BaseModel):
    title: str | None = Field(default=None, max_length=120)
    narration: str | None = Field(default=None, max_length=4000)
    visual_direction: str | None = Field(default=None, max_length=1000)
    asset_search_query: str | None = Field(default=None, max_length=300)
    duration_seconds: float | None = Field(default=None, ge=1, le=60)
    caption_text: str | None = Field(default=None, max_length=2000)
