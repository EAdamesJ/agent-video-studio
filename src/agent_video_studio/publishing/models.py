from __future__ import annotations

from pydantic import BaseModel, Field


class PublishRequest(BaseModel):
    project_id: str
    render_id: str = Field(min_length=8, max_length=40, pattern=r"^[a-f0-9]+$")
    aspect_ratio: str = Field(pattern=r"^(9:16|16:9|1:1)$")
    platform: str = Field(pattern=r"^(youtube|instagram|tiktok)$")
    title: str = Field(min_length=1, max_length=500)
    description: str = Field(default="", max_length=5000)
    privacy_level: str = "private"
    confirm: bool = False
    share_to_feed: bool = True
    ai_generated: bool = True
