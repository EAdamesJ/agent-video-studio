from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

import httpx

from agent_video_studio.config import Settings
from agent_video_studio.providers.base import ProviderError
from agent_video_studio.publishing.models import PublishRequest


class InstagramPublisher:
    id = "instagram"

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def _base_url(self) -> str:
        version = self.settings.meta_graph_version
        host = self.settings.instagram_graph_host
        if not version or not host or "/" in host:
            raise ProviderError("Set AVS_META_GRAPH_VERSION and a valid INSTAGRAM_GRAPH_HOST.")
        return f"https://{host}/{version}"

    async def preflight(self, request: PublishRequest, media_path: Path) -> dict[str, Any]:
        media_origin = urlsplit(self.settings.public_media_base_url)
        public_media_ready = media_origin.scheme == "https" and bool(media_origin.netloc)
        configured = bool(self.settings.instagram_graph_token and self.settings.instagram_account_id
                          and public_media_ready and self.settings.meta_graph_version)
        requirements = []
        if not self.settings.instagram_graph_token or not self.settings.instagram_account_id:
            requirements.append("Set INSTAGRAM_GRAPH_TOKEN and INSTAGRAM_ACCOUNT_ID for an eligible professional account.")
        if not self.settings.meta_graph_version:
            requirements.append("Set AVS_META_GRAPH_VERSION to the Graph API version enabled for your app.")
        if not public_media_ready:
            requirements.append("Set AVS_PUBLIC_MEDIA_BASE_URL to a reachable HTTPS origin that serves the rendered MP4.")
        if not media_path.is_file() or media_path.stat().st_size == 0:
            requirements.append("Render a non-empty MP4 export first.")
        return {
            "platform": self.id, "ready": configured and media_path.is_file() and media_path.stat().st_size > 0,
            "requirements": requirements + [
                "Use an eligible Instagram professional account and an app with content-publishing permission."
            ],
        }

    async def publish(self, request: PublishRequest, media_path: Path, public_url: str = "") -> dict[str, Any]:
        if not request.confirm:
            raise ValueError("Publishing requires confirm=true after reviewing the destination and metadata.")
        if not self.settings.instagram_graph_token or not self.settings.instagram_account_id:
            raise ProviderError("Configure an eligible Instagram account and access token first.")
        if not public_url.startswith("https://"):
            raise ProviderError("Instagram requires a publicly reachable HTTPS video URL.")
        base = self._base_url()
        token = self.settings.instagram_graph_token
        try:
            async with httpx.AsyncClient(timeout=httpx.Timeout(600, connect=20)) as client:
                create = await client.post(
                    f"{base}/{self.settings.instagram_account_id}/media",
                    data={"media_type": "REELS", "video_url": public_url, "caption": _caption(request.title, request.description),
                          "share_to_feed": str(request.share_to_feed).lower(), "access_token": token},
                )
                create.raise_for_status()
                container_id = create.json().get("id")
                if not container_id:
                    raise ProviderError("Instagram returned no media container ID.")
                status = "IN_PROGRESS"
                for _ in range(30):
                    await asyncio.sleep(10)
                    check = await client.get(
                        f"{base}/{container_id}", params={"fields": "status_code,status", "access_token": token}
                    )
                    check.raise_for_status()
                    status_data = check.json()
                    status = status_data.get("status_code", "")
                    if status == "FINISHED":
                        break
                    if status in {"ERROR", "EXPIRED"}:
                        raise ProviderError(f"Instagram media container status: {status_data.get('status', status)}")
                if status != "FINISHED":
                    raise ProviderError("Instagram is still processing the Reel. Check status and retry later.")
                publish = await client.post(
                    f"{base}/{self.settings.instagram_account_id}/media_publish",
                    data={"creation_id": container_id, "access_token": token},
                )
                publish.raise_for_status()
                media_id = publish.json().get("id")
        except httpx.HTTPStatusError as exc:
            raise ProviderError(f"Instagram Graph API returned HTTP {exc.response.status_code}.") from exc
        except httpx.HTTPError as exc:
            raise ProviderError("Could not complete the Instagram Reel publish flow.") from exc
        return {"platform": self.id, "external_id": media_id or container_id, "status": "published"}


def _caption(title: str, description: str) -> str:
    text = "\n\n".join(part.strip() for part in (title, description) if part.strip())
    if len(text) > 2200:
        raise ValueError("Instagram Reel title and caption must fit within 2,200 characters.")
    return text
