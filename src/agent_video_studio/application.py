from __future__ import annotations

from pathlib import Path
from typing import Any

from agent_video_studio.config import Settings
from agent_video_studio.core.assets import AssetStore
from agent_video_studio.core.db import Database
from agent_video_studio.core.jobs import JobStore
from agent_video_studio.core.models import Job, Project
from agent_video_studio.core.projects import ProjectStore
from agent_video_studio.core.worker import JobRunner
from agent_video_studio.creation.models import SceneEdit
from agent_video_studio.creation.service import CreationService
from agent_video_studio.media.ingest import MediaIngestService
from agent_video_studio.media.render import RenderService
from agent_video_studio.providers.registry import ProviderRegistry
from agent_video_studio.publishing.models import PublishRequest
from agent_video_studio.publishing.service import PublishingService
from agent_video_studio.repurposing.service import RepurposingService


class StudioApplication:
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or Settings.from_env()
        self.settings.ensure_data_dirs()
        self.db = Database(self.settings.database_path)
        self.projects = ProjectStore(self.db)
        self.assets = AssetStore(self.db)
        self.jobs = JobStore(self.db)
        self.providers = ProviderRegistry(self.settings)
        self.ingest = MediaIngestService(self.settings, self.assets)
        self.creation = CreationService(self.projects, self.providers)
        self.repurposing = RepurposingService(self.settings, self.projects, self.assets, self.providers)
        self.rendering = RenderService(self.settings, self.projects, self.assets, self.providers)
        self.publishing = PublishingService(self.settings, self.projects)
        self.runner = JobRunner(self.jobs, self.projects)
        self.runner.register("generate_script", self._generate_script)
        self.runner.register("analyze_media", self._analyze_media)
        self.runner.register("render_project", self._render_project)

    async def start(self) -> None:
        await self.runner.start()

    async def stop(self) -> None:
        await self.runner.stop()

    def create_project(
        self,
        title: str,
        mode: str,
        brief: str = "",
        language: str = "en",
        aspect_ratios: list[str] | None = None,
    ) -> Project:
        return self.projects.create(title, mode, brief, language, aspect_ratios)

    async def schedule_script(self, project_id: str, options: dict[str, Any]) -> Job:
        return await self._schedule(project_id, "generate_script", options)

    async def schedule_analysis(self, project_id: str, options: dict[str, Any]) -> Job:
        return await self._schedule(project_id, "analyze_media", options)

    async def schedule_render(self, project_id: str, options: dict[str, Any]) -> Job:
        return await self._schedule(project_id, "render_project", options)

    async def _schedule(self, project_id: str, kind: str, payload: dict[str, Any]) -> Job:
        self.projects.get(project_id)
        job = await self.runner.submit(project_id, kind, payload)
        self.projects.update(project_id, status="processing")
        return job

    async def _generate_script(self, job: Job, report: Any) -> dict[str, Any]:
        await report(8, "Generating an editable script and storyboard")
        script = await self.creation.generate_script(job.project_id, job.payload)
        await report(95, "Saving scenes to the project timeline")
        return {"script": script}

    async def _analyze_media(self, job: Job, report: Any) -> dict[str, Any]:
        await report(5, "Preparing transcription")
        result = await self.repurposing.analyze(job.project_id, model=str(job.payload.get("model", "small")))
        await report(95, "Highlights and source timestamps are ready")
        return result

    async def _render_project(self, job: Job, report: Any) -> dict[str, Any]:
        options = job.payload
        return await self.rendering.render_project(
            job.project_id,
            aspect_ratios=options.get("aspect_ratios"),
            include_captions=bool(options.get("include_captions", True)),
            use_tts=bool(options.get("use_tts", True)),
            progress=report,
        )

    def add_media_file(self, project_id: str, source: Path) -> dict[str, Any]:
        project = self.projects.get(project_id)
        asset, _ = self.ingest.copy_into_project(project_id, source)
        patch: dict[str, Any] = {"last_imported_asset_id": asset["id"]}
        if project.mode == "repurpose":
            patch["source_asset_id"] = asset["id"]
        self.projects.update(project_id, document_patch=patch)
        return asset

    def add_media_upload(self, project_id: str, filename: str, chunks: Any) -> dict[str, Any]:
        project = self.projects.get(project_id)
        asset, _ = self.ingest.save_upload(project_id, filename, chunks)
        patch: dict[str, Any] = {"last_imported_asset_id": asset["id"]}
        if project.mode == "repurpose":
            patch["source_asset_id"] = asset["id"]
        self.projects.update(project_id, document_patch=patch)
        return asset

    def choose_highlights(self, project_id: str, selected_ids: list[str]) -> dict[str, Any]:
        return self.repurposing.choose_highlights(project_id, selected_ids)

    def edit_scene(self, project_id: str, scene_id: str, edit: SceneEdit) -> dict[str, Any]:
        return self.creation.edit_scene(project_id, scene_id, edit)

    async def publish_export(self, request: PublishRequest) -> dict[str, Any]:
        return await self.publishing.publish(request)

    def project_bundle(self, project_id: str) -> dict[str, Any]:
        project = self.projects.get(project_id)
        assets = self.assets.list_for_project(project_id)
        jobs = self.jobs.list_for_project(project_id)
        return {
            "project": project,
            "assets": assets,
            "jobs": jobs,
            "providers": self.providers.list_status(),
        }

\n