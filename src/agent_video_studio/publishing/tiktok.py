from __future__ import annotations

import math
from pathlib import Path
from typing import Any

import httpx

from agent_video_studio.config import Settings
from agent_video_studio.providers.base import ProviderError
from agent_video_studio.publishing.models import PublishRequest

API_ROOT = "https://open.tiktokapis.com/v2"


class TikTokPublisher:
    id = "tiktok"

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    async def preflight(self, request: PublishRequest, media_path: Path) -> dict[str, Any]:
        if not self.settings.tiktok_access_token:
            return {
                "platform": self.id,
                "ready": False,
                "requirements": [
                    "Set TIKTOK_ACCESS_TOKEN with the video.publish scope.",
                    "Register an app with TikTok Content Posting API and complete its audit for public posting.",
                ],
            }
        info = await self._creator_info()
        options = info.get("data", {}).get("privacy_level_options", [])
        return {
            "platform": self.id,
            "ready": media_path.is_file() and bool(options),
            "privacy_options": options,
            "requirements": ["Unaudited clients may only publish privately."],
        }

    async def publish(self, request: PublishRequest, media_path: Path, public_url: str = "") -> dict[str, Any]:
        if not request.confirm:
            raise ValueError("Publishing requires confirm=true after reviewing the destination and metadata.")
        if not self.settings.tiktok_access_token:
            raise ProviderError("Set TIKTOK_ACCESS_TOKEN with the approved video.publish scope.")
        creator = await self._creator_info()
        options = creator.get("data", {}).get("privacy_level_options", [])
        if request.privacy_level not in options:
            raise ValueError("Select a privacy level returned by TikTok creator_info/query.")
        size = media_path.stat().st_size
        if size <= 0:
            raise ValueError("The rendered video file is empty.")
        chunk_size = min(10 * 1024 * 1024, size)
        chunk_count = max(1, math.ceil(size / chunk_size))
        title = "\n\n".join(part.strip() for part in (request.title, request.description) if part.strip())
        if len(title) > 2200:
            raise ValueError("TikTok title and caption must fit within 2,200 characters.")
        init_body = {
            "post_info": {
                "title": title,
                "privacy_level": request.privacy_level,
                "disable_duet": False,
                "disable_comment": False,
                "disable_stitch": False,
                "brand_content_toggle": False,
                "brand_organic_toggle": False,
                "is_aigc": request.ai_generated,
            },
            "source_info": {"source": "FILE_UPLOAD", "video_size": size,
                            "chunk_size": chunk_size, "total_chunk_count": chunk_count},
        }
        headers = {"Authorization": f"Bearer {self.settings.tiktok_access_token}", "Content-Type": "application/json"}
        try:
            async with httpx.AsyncClient(timeout=httpx.Timeout(120, connect=20)) as client:
                init = await client.post(f"{API_ROOT}/post/publish/video/init/", headers=headers, json=init_body)
                init.raise_for_status()
                init_data = init.json()
                error = init_data.get("error", {})
                if error.get("code") not in {None, "ok"}:
                    raise ProviderError(f"TikTok rejected the request: {error.get('message', error.get('code'))}")
                publish_id = init_data.get("data", {}).get("publish_id")
                upload_url = init_data.get("data", {}).get("upload_url")
                if not publish_id or not upload_url:
                    raise ProviderError("TikTok returned no upload ticket.")
                with media_path.open("rb") as media:
                    for index in range(chunk_count):
                        start = index * chunk_size
                        chunk = media.read(chunk_size)
                        end = start + len(chunk) - 1
                        upload = await client.put(
                            upload_url,
                            headers={"Content-Type": "video/mp4", "Content-Length": str(len(chunk)),
                                     "Content-Range": f"bytes {start}-{end}/{size}"},
                            content=chunk,
                        )
                        upload.raise_for_status()
                status_response = await client.post(
                    f"{API_ROOT}/post/publish/status/fetch/", headers=headers, json={"publish_id": publish_id}
                )
                status_response.raise_for_status()
                status_data = status_response.json().get("data", {})
        except httpx.HTTPStatusError as exc:
            raise ProviderError(f"TikTok API returned HTTP {exc.response.status_code}.") from exc
        except httpx.HTTPError as exc:
            raise ProviderError("Could not complete the TikTok upload. Check network and token scopes.") from exc
        return {"platform": self.id, "external_id": publish_id,
                "status": status_data.get("status", "processing"), "fail_reason": status_data.get("fail_reason"),
                "privacy": request.privacy_level}

    async def _creator_info(self) -> dict[str, Any]:
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.post(
                    f"{API_ROOT}/post/publish/creator_info/query/",
                    headers={"Authorization": f"Bearer {self.settings.tiktok_access_token}",
                             "Content-Type": "application/json"},
                    json={},
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as exc:
            raise ProviderError(f"TikTok creator preflight returned HTTP {exc.response.status_code}.") from exc
        except httpx.HTTPError as exc:
            raise ProviderError("Could not query TikTok creator permissions.") from exc
