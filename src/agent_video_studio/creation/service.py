from __future__ import annotations

from typing import Any

from pydantic import ValidationError

from agent_video_studio.core.projects import ProjectStore
from agent_video_studio.creation.models import SceneEdit, ScriptDocument
from agent_video_studio.creation.prompts import SCRIPT_SYSTEM_PROMPT
from agent_video_studio.providers.base import ProviderError, parse_json_object
from agent_video_studio.providers.registry import ProviderRegistry


class CreationService:
    def __init__(self, projects: ProjectStore, providers: ProviderRegistry) -> None:
        self.projects = projects
        self.providers = providers

    async def generate_script(self, project_id: str, options: dict[str, Any] | None = None) -> dict[str, Any]:
        project = self.projects.get(project_id)
        brief = str(project.document.get("brief", "")).strip()
        if not brief:
            raise ValueError("Add a brief or script prompt to this project first.")
        options = options or {}
        language = str(options.get("language") or project.document.get("language") or "en")
        duration = int(options.get("target_duration_seconds") or 60)
        platform = str(options.get("platform") or "short-form social video")
        prompt = (
            f"Project brief:\n{brief}\n\nLanguage: {language}\n"
            f"Target duration: {duration} seconds\nPlatform: {platform}\n"
            "Generate the script and storyboard as the requested JSON object."
        )
        provider = self.providers.text()
        raw = await provider.generate(SCRIPT_SYSTEM_PROMPT, prompt, max_tokens=6000)
        try:
            data = parse_json_object(raw)
            data.setdefault("language", language)
            script = ScriptDocument.model_validate(data)
        except (ProviderError, ValidationError) as exc:
            raise ProviderError(f"Could not validate the generated script: {exc}") from exc
        script.scenes = [
            scene.model_copy(update={"id": scene.id or f"scene-{index + 1}"})
            for index, scene in enumerate(script.scenes)
        ]
        script_data = script.model_dump(mode="json")
        timeline = {
            "version": 1,
            "scenes": [
                {
                    "id": scene.id,
                    "title": scene.title,
                    "start_seconds": sum(s.duration_seconds for s in script.scenes[:index]),
                    "duration_seconds": scene.duration_seconds,
                    "narration": scene.narration,
                    "visual_direction": scene.visual_direction,
                    "asset_search_query": scene.asset_search_query,
                    "caption_text": scene.caption_text or scene.narration,
                    "asset_ids": [],
                }
                for index, scene in enumerate(script.scenes)
            ],
        }
        self.projects.update(
            project_id,
            status="draft",
            document_patch={
                "script": script_data,
                "timeline": timeline,
                "generation": {"provider": provider.id, "model": provider.model},
            },
        )
        return script_data

    def edit_scene(self, project_id: str, scene_id: str, edit: SceneEdit) -> dict[str, Any]:
        project = self.projects.get(project_id)
        timeline = project.document.get("timeline") or {"version": 1, "scenes": []}
        scenes = timeline.get("scenes", [])
        for scene in scenes:
            if scene.get("id") == scene_id:
                changes = edit.model_dump(exclude_unset=True, exclude_none=True)
                scene.update(changes)
                cursor = 0.0
                for item in scenes:
                    item["start_seconds"] = cursor
                    cursor += float(item.get("duration_seconds", 6))
                self.projects.update(project_id, document_patch={"timeline": timeline})
                return scene
        raise KeyError(f"Scene '{scene_id}' was not found in project '{project_id}'.")
