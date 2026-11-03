from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Any

from agent_video_studio.config import Settings
from agent_video_studio.providers.base import ProviderError
from agent_video_studio.publishing.models import PublishRequest

YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"


class YouTubePublisher:
    id = "youtube"

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    async def preflight(self, request: PublishRequest, media_path: Path) -> dict[str, Any]:
        configured = bool(self.settings.youtube_client_secret_file and Path(self.settings.youtube_client_secret_file).is_file())
        return {
            "platform": self.id, "ready": configured and media_path.is_file() and media_path.stat().st_size > 0,
            "requirements": [
                "Set YOUTUBE_CLIENT_SECRET_FILE to a Google OAuth desktop-app client JSON file.",
                "The first upload opens the local Google authorization flow.",
                "Review the selected title, description, and privacy before confirming.",
            ] if not configured else [],
            "default_privacy": "private",
        }

    async def publish(self, request: PublishRequest, media_path: Path, public_url: str = "") -> dict[str, Any]:
        if not request.confirm:
            raise ValueError("Publishing requires confirm=true after reviewing the destination and metadata.")
        return await asyncio.to_thread(self._publish_sync, request, media_path)

    def _publish_sync(self, request: PublishRequest, media_path: Path) -> dict[str, Any]:
        if not self.settings.youtube_client_secret_file:
            raise ProviderError("Set YOUTUBE_CLIENT_SECRET_FILE to enable YouTube publishing.")
        try:
            from google.auth.transport.requests import Request as GoogleRequest
            from google.oauth2.credentials import Credentials
            from google_auth_oauthlib.flow import InstalledAppFlow
            from googleapiclient.discovery import build
            from googleapiclient.http import MediaFileUpload
        except ImportError as exc:
            raise ProviderError("Install YouTube publishing support with `pip install 'agent-video-studio[youtube]'`.") from exc
        token_path = self.settings.data_dir / "credentials" / "youtube-token.json"
        token_path.parent.mkdir(parents=True, exist_ok=True)
        credentials = None
        if token_path.is_file():
            try:
                credentials = Credentials.from_authorized_user_file(str(token_path), [YOUTUBE_UPLOAD_SCOPE])
            except (ValueError, OSError):
                credentials = None
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(GoogleRequest())
        if not credentials or not credentials.valid:
            flow = InstalledAppFlow.from_client_secrets_file(
                self.settings.youtube_client_secret_file, [YOUTUBE_UPLOAD_SCOPE]
            )
            credentials = flow.run_local_server(port=0, open_browser=True)
        token_path.write_text(credentials.to_json(), encoding="utf-8")
        try:
            youtube = build("youtube", "v3", credentials=credentials, cache_discovery=False)
            body = {
                "snippet": {
                    "title": request.title[:100],
                    "description": request.description[:5000],
                    "tags": [],
                    "categoryId": "22",
                },
                "status": {"privacyStatus": request.privacy_level, "selfDeclaredMadeForKids": False},
            }
            upload = youtube.videos().insert(
                part="snippet,status",
                body=body,
                media_body=MediaFileUpload(str(media_path), chunksize=8 * 1024 * 1024, resumable=True),
            )
            response = None
            while response is None:
                _status, response = upload.next_chunk()
            video_id = str(response.get("id", ""))
            return {
                "platform": self.id,
                "external_id": video_id,
                "url": f"https://www.youtube.com/watch?v={video_id}" if video_id else "",
                "status": "uploaded",
                "privacy": request.privacy_level,
            }
        except Exception as exc:
            raise ProviderError("YouTube upload failed. Review OAuth permissions, quota, and video metadata.") from exc

\n