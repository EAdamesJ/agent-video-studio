from __future__ import annotations

from typing import Any

from agent_video_studio.config import Settings
from agent_video_studio.core.assets import AssetStore
from agent_video_studio.core.paths import PathPolicy
from agent_video_studio.core.projects import ProjectStore
from agent_video_studio.providers.base import ProviderError
from agent_video_studio.providers.registry import ProviderRegistry
from agent_video_studio.providers.transcription import build_transcriber
from agent_video_studio.repurposing.highlights import HighlightSelector
from agent_video_studio.repurposing.models import TranscriptDocument


class RepurposingService:
    def __init__(
        self,
        settings: Settings,
        projects: ProjectStore,
        assets: AssetStore,
        providers: ProviderRegistry,
    ) -> None:
        self.settings = settings
        self.projects = projects
        self.assets = assets
        self.providers = providers
        self.paths = PathPolicy(settings.data_dir)

    async def analyze(self, project_id: str, *, model: str = "small") -> dict[str, Any]:
        project = self.projects.get(project_id)
        source_id = project.document.get("source_asset_id")
        if source_id:
            asset = self.assets.get(str(source_id))
        else:
            available = self.assets.list_for_project(project_id)
            asset = next((item for item in available if item.kind in {"video", "audio"}), None)
        if asset is None:
            raise ValueError("Import a video or audio file before analyzing this project.")
        if asset.kind not in {"video", "audio"}:
            raise ValueError("The selected asset does not contain audio or video.")
        media_path = self.paths.require_managed(asset.path)
        transcription = build_transcriber(self.settings, model=model)
        transcript = await transcription.transcribe(media_path)
        if not transcript.duration_seconds:
            duration = float((asset.metadata.get("probe") or {}).get("duration_seconds", 0))
            transcript = transcript.model_copy(update={"duration_seconds": duration})
        highlights = await HighlightSelector(self.providers).select(transcript)
        timeline = self._timeline_from_highlights(highlights, asset.id, transcript)
        transcript_data = transcript.model_dump(mode="json")
        self.projects.update(
            project_id,
            status="draft",
            document_patch={
                "source_asset_id": asset.id,
                "transcript": transcript_data,
                "highlights": highlights,
                "timeline": timeline,
                "analysis": {"transcription_provider": self.settings.transcription_provider},
            },
        )
        return {"transcript": transcript_data, "highlights": highlights, "source_asset": asset.to_dict()}

    def choose_highlights(self, project_id: str, selected_ids: list[str]) -> dict[str, Any]:
        project = self.projects.get(project_id)
        highlights = project.document.get("highlights") or []
        selected = [item for item in highlights if item.get("id") in set(selected_ids)]
        if not selected:
            raise ValueError("Select at least one suggested clip.")
        source_id = project.document.get("source_asset_id")
        if not source_id:
            raise ProviderError("The source asset for these highlights is unavailable.")
        transcript = TranscriptDocument.model_validate(project.document.get("transcript") or {})
        timeline = self._timeline_from_highlights(selected, str(source_id), transcript)
        self.projects.update(project_id, document_patch={"timeline": timeline})
        return timeline

    @staticmethod
    def _timeline_from_highlights(
        highlights: list[dict[str, Any]], asset_id: str, transcript: TranscriptDocument
    ) -> dict[str, Any]:
        scenes = []
        cursor = 0.0
        for item in highlights:
            source_start = float(item["start_seconds"])
            source_end = float(item["end_seconds"])
            duration = source_end - source_start
            caption_segments = [
                {
                    "start_seconds": max(0.0, float(segment.start_seconds) - source_start),
                    "end_seconds": min(duration, float(segment.end_seconds) - source_start),
                    "text": segment.text,
                }
                for segment in transcript.segments
                if float(segment.end_seconds) > source_start and float(segment.start_seconds) < source_end
            ]
            scenes.append(
                {
                    "id": item["id"],
                    "title": item["title"],
                    "start_seconds": cursor,
                    "duration_seconds": duration,
                    "source_asset_id": asset_id,
                    "source_start_seconds": source_start,
                    "source_end_seconds": source_end,
                    "narration": "",
                    "visual_direction": "Reframe the source speaker for the selected aspect ratio.",
                    "caption_text": item["transcript_excerpt"],
                    "caption_segments": caption_segments,
                    "asset_ids": [asset_id],
                    "highlight_reason": item["reason"],
                    "hook": item["hook"],
                }
            )
            cursor += duration
        return {"version": 1, "scenes": scenes}

\n