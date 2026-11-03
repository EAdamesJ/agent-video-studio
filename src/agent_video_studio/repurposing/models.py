from __future__ import annotations

from pydantic import BaseModel, Field


class TranscriptSegment(BaseModel):
    start_seconds: float = Field(ge=0)
    end_seconds: float = Field(gt=0)
    text: str = Field(min_length=1, max_length=10000)
    speaker: str | None = Field(default=None, max_length=100)


class TranscriptDocument(BaseModel):
    language: str = "und"
    duration_seconds: float = Field(ge=0)
    segments: list[TranscriptSegment]


class Highlight(BaseModel):
    id: str = ""
    title: str = Field(min_length=1, max_length=180)
    start_seconds: float = Field(ge=0)
    end_seconds: float = Field(gt=0)
    hook: str = Field(default="", max_length=500)
    reason: str = Field(default="", max_length=1000)
    transcript_excerpt: str = Field(default="", max_length=4000)
