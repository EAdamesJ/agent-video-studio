from __future__ import annotations

from pathlib import Path
from typing import Any, Protocol

from agent_video_studio.publishing.models import PublishRequest


class Publisher(Protocol):
    id: str

    async def preflight(self, request: PublishRequest, media_path: Path) -> dict[str, Any]: ...

    async def publish(self, request: PublishRequest, media_path: Path, public_url: str = "") -> dict[str, Any]: ...

\n