from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from typing import Any, Literal
from uuid import uuid4

ProjectMode = Literal["prompt", "repurpose"]
ProjectStatus = Literal["draft", "processing", "ready", "failed"]
JobStatus = Literal["queued", "running", "completed", "failed", "cancelled"]


def utc_now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds")


def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:12]}"


@dataclass(slots=True)
class Project:
    id: str
    title: str
    mode: ProjectMode
    status: ProjectStatus
    created_at: str
    updated_at: str
    document: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class Asset:
    id: str
    project_id: str
    path: str
    kind: str
    name: str
    mime_type: str
    size_bytes: int
    duration_seconds: float | None
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=utc_now)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class Job:
    id: str
    project_id: str
    kind: str
    status: JobStatus
    progress: float
    message: str
    payload: dict[str, Any]
    result: dict[str, Any] | None
    error: str | None
    created_at: str
    updated_at: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

\n