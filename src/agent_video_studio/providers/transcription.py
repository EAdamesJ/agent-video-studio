from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Any

import httpx

from agent_video_studio.config import Settings
from agent_video_studio.providers.base import ProviderError
from agent_video_studio.repurposing.models import TranscriptDocument, TranscriptSegment


class FasterWhisperTranscriber:
    def __init__(self, model_name: str = "small", device: str = "cpu") -> None:
        self.model_name = model_name
        self.device = device

    async def transcribe(self, path: Path) -> TranscriptDocument:
        def run() -> TranscriptDocument:
            try:
                from faster_whisper import WhisperModel
            except ImportError as exc:
                raise ProviderError(
                    "Local transcription is optional. Install it with `pip install 'agent-video-studio[transcription]'`."
                ) from exc
            model = WhisperModel(self.model_name, device=self.device, compute_type="int8")
            segments, info = model.transcribe(str(path), vad_filter=True, word_timestamps=False)
            normalized = [
                TranscriptSegment(
                    start_seconds=max(0.0, float(segment.start)),
                    end_seconds=max(float(segment.start) + 0.01, float(segment.end)),
                    text=str(segment.text).strip(),
                )
                for segment in segments
                if str(segment.text).strip()
            ]
            duration = max((item.end_seconds for item in normalized), default=0.0)
            return TranscriptDocument(
                language=getattr(info, "language", "und") or "und",
                duration_seconds=duration,
                segments=normalized,
            )

        return await asyncio.to_thread(run)


class OpenAITranscriber:
    def __init__(self, api_key: str, model: str = "gpt-4o-mini-transcribe") -> None:
        if not api_key:
            raise ProviderError("Set OPENAI_API_KEY to use remote transcription.")
        self.api_key = api_key
        self.model = model

    async def transcribe(self, path: Path) -> TranscriptDocument:
        try:
            async with httpx.AsyncClient(timeout=httpx.Timeout(300, connect=20)) as client:
                with path.open("rb") as media:
                    response = await client.post(
                        "https://api.openai.com/v1/audio/transcriptions",
                        headers={"Authorization": f"Bearer {self.api_key}"},
                        data={"model": self.model, "response_format": "verbose_json"},
                        files={"file": (path.name, media, "application/octet-stream")},
                    )
                response.raise_for_status()
                data = response.json()
        except httpx.TimeoutException as exc:
            raise ProviderError("Remote transcription timed out.") from exc
        except httpx.HTTPStatusError as exc:
            raise ProviderError(f"Remote transcription returned HTTP {exc.response.status_code}.") from exc
        except (httpx.HTTPError, ValueError) as exc:
            raise ProviderError("Could not reach the transcription provider.") from exc
        segments = [
            TranscriptSegment(
                start_seconds=max(0.0, float(item.get("start", 0))),
                end_seconds=max(float(item.get("start", 0)) + 0.01, float(item.get("end", 0))),
                text=str(item.get("text", "")).strip(),
            )
            for item in data.get("segments", [])
            if str(item.get("text", "")).strip()
        ]
        duration = float(data.get("duration") or max((item.end_seconds for item in segments), default=0))
        return TranscriptDocument(
            language=str(data.get("language") or "und"), duration_seconds=duration, segments=segments
        )


def build_transcriber(settings: Settings, model: str = "small") -> Any:
    provider = settings.transcription_provider
    if provider == "local":
        return FasterWhisperTranscriber(model_name=model)
    if provider == "openai":
        return OpenAITranscriber(settings.openai_api_key)
    raise ProviderError("Unknown transcription provider. Choose 'local' or 'openai'.")

\n