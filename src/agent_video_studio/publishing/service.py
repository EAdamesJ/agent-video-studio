from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from agent_video_studio.config import Settings
from agent_video_studio.core.paths import PathPolicy
from agent_video_studio.core.projects import ProjectStore
from agent_video_studio.publishing.instagram import InstagramPublisher
from agent_video_studio.publishing.models import PublishRequest
from agent_video_studio.publishing.tiktok import TikTokPublisher
from agent_video_studio.publishing.youtube import YouTubePublisher


class PublishingService:
    def __init__(self, settings: Settings, projects: ProjectStore) -> None:
        self.settings = settings
        self.projects = projects
        self.paths = PathPolicy(settings.data_dir)
        self.publishers = {"youtube": YouTubePublisher(settings), "instagram": InstagramPublisher(settings),
                           "tiktok": TikTokPublisher(settings)}

    def media_path(self, request: PublishRequest) -> Path:
        aspect = request.aspect_ratio.replace(":", "x")
        path = self.paths.managed("exports", request.project_id, request.render_id, aspect, "video.mp4")
        if not path.is_file():
            raise FileNotFoundError("Rendered export was not found. Render the project first.")
        return path

    def public_url(self, request: PublishRequest) -> str:
        aspect = request.aspect_ratio.replace(":", "x")
        return (f"{self.settings.public_media_base_url}/api/projects/{request.project_id}/exports/"
                f"{request.render_id}/{aspect}/video.mp4")

    async def preflight(self, request: PublishRequest) -> dict[str, Any]:
        publisher = self._publisher(request.platform)
        media = self.media_path(request)
        result = await publisher.preflight(request, media)
        result["project_id"] = request.project_id
        result["aspect_ratio"] = request.aspect_ratio
        if request.platform == "instagram":
            result["media_url_configured"] = self.public_url(request).startswith("https://")
        return result

    async def publish(self, request: PublishRequest) -> dict[str, Any]:
        if request.confirm is not True:
            raise ValueError("Publishing is an external action. Set confirm=true only after reviewing the post.")
        self._validate_metadata(request)
        publisher = self._publisher(request.platform)
        media = self.media_path(request)
        url = self.public_url(request) if request.platform == "instagram" else ""
        preflight = await publisher.preflight(request, media)
        if not preflight.get("ready"):
            raise ValueError("Publishing is not ready: " + " ".join(preflight.get("requirements", [])))
        result = await publisher.publish(request, media, public_url=url)
        project = self.projects.get(request.project_id)
        deliveries = list(project.document.get("deliveries") or [])
        delivery = {**result, "render_id": request.render_id, "aspect_ratio": request.aspect_ratio,
                    "title": request.title, "published_at": datetime.now(UTC).isoformat(timespec="seconds")}
        deliveries.append(delivery)
        self.projects.update(request.project_id, document_patch={"deliveries": deliveries})
        return delivery

    @staticmethod
    def _validate_metadata(request: PublishRequest) -> None:
        if request.platform == "youtube":
            if len(request.title) > 100:
                raise ValueError("YouTube titles must be 100 characters or fewer.")
            if request.privacy_level not in {"private", "unlisted", "public"}:
                raise ValueError("YouTube visibility must be private, unlisted, or public.")
        elif request.platform in {"instagram", "tiktok"}:
            caption = "\n\n".join(part.strip() for part in (request.title, request.description) if part.strip())
            if len(caption) > 2200:
                raise ValueError(f"{request.platform.title()} title and caption must fit within 2,200 characters.")

    async def all_preflight(self, project_id: str, render_id: str, aspect_ratio: str) -> list[dict[str, Any]]:
        results = []
        for platform in self.publishers:
            request = PublishRequest(project_id=project_id, render_id=render_id, aspect_ratio=aspect_ratio,
                                     platform=platform, title="Preflight", confirm=False)
            try:
                results.append(await self.preflight(request))
            except Exception as exc:
                results.append({"platform": platform, "ready": False, "requirements": [str(exc)]})
        return results

    def _publisher(self, platform: str):
        try:
            return self.publishers[platform]
        except KeyError as exc:
            raise ValueError(f"Unsupported publishing platform '{platform}'.") from exc
