from __future__ import annotations

from typing import Any

from pydantic import ValidationError

from agent_video_studio.creation.prompts import HIGHLIGHTS_SYSTEM_PROMPT
from agent_video_studio.providers.base import ProviderError, parse_json_object
from agent_video_studio.providers.registry import ProviderRegistry
from agent_video_studio.repurposing.models import Highlight, TranscriptDocument


class HighlightSelector:
    def __init__(self, providers: ProviderRegistry) -> None:
        self.providers = providers

    async def select(self, transcript: TranscriptDocument) -> list[dict[str, Any]]:
        if not transcript.segments:
            raise ValueError("The transcript is empty; there are no clips to select.")
        compact_transcript = [segment.model_dump() for segment in transcript.segments]
        prompt = (
            f"Source duration: {transcript.duration_seconds:.2f} seconds. "
            f"Transcript language: {transcript.language}.\nTranscript segments:\n{compact_transcript}"
        )
        provider = self.providers.text()
        raw = await provider.generate(HIGHLIGHTS_SYSTEM_PROMPT, prompt, max_tokens=5000)
        try:
            raw_items = parse_json_object(raw).get("highlights", [])
            highlights = [Highlight.model_validate(item) for item in raw_items]
        except (ProviderError, ValidationError, TypeError) as exc:
            raise ProviderError(f"Could not validate suggested clip timestamps: {exc}") from exc
        valid: list[dict[str, Any]] = []
        for index, item in enumerate(highlights):
            start = max(0.0, item.start_seconds)
            end = min(transcript.duration_seconds, item.end_seconds)
            if end <= start or end - start < 3:
                continue
            valid.append(
                item.model_copy(
                    update={"id": item.id or f"clip-{index + 1}", "start_seconds": start, "end_seconds": end}
                ).model_dump(mode="json")
            )
        if not valid:
            raise ProviderError("The model did not return valid clip candidates. Try another provider or prompt.")
        return valid
