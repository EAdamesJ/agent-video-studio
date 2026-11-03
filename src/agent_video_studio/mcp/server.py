from __future__ import annotations

from pathlib import Path
from typing import Any

from agent_video_studio.application import StudioApplication
from agent_video_studio.config import Settings
from agent_video_studio.core.paths import PathPolicy
from agent_video_studio.providers.base import ProviderError


def build_server(settings: Settings | None = None):
    try:
        from mcp.server.fastmcp import FastMCP
    except ImportError as exc:
        raise RuntimeError("Install MCP support with `pip install 'agent-video-studio[mcp]'`.") from exc

    application = StudioApplication(settings or Settings.from_env())
    server = FastMCP("Agent Video Studio")

    @server.tool()
    def list_projects(limit: int = 50) -> list[dict[str, Any]]:
        """List local video projects and their current workflow status."""
        return [
            {"id": item.id, "title": item.title, "mode": item.mode, "status": item.status,
             "updated_at": item.updated_at}
            for item in application.projects.list(limit)
        ]

    @server.tool()
    def create_project(
        title: str,
        mode: str = "prompt",
        brief: str = "",
        language: str = "en",
        aspect_ratio: str = "9:16",
    ) -> dict[str, Any]:
        """Create a prompt-to-video or media-repurposing project."""
        if aspect_ratio not in {"9:16", "16:9", "1:1"}:
            raise ValueError("aspect_ratio must be 9:16, 16:9, or 1:1.")
        return _public_project(
            application.create_project(title, mode, brief, language, [aspect_ratio])
        )

    @server.tool()
    def get_project(project_id: str) -> dict[str, Any]:
        """Read a project's editable script, timeline, highlights, and asset summaries."""
        project = application.projects.get(project_id)
        return {
            "project": _public_project(project),
            "assets": [
                {"id": item.id, "kind": item.kind, "name": item.name, "duration_seconds": item.duration_seconds,
                 "size_bytes": item.size_bytes}
                for item in application.assets.list_for_project(project_id)
            ],
            "jobs": [
                {"id": item.id, "kind": item.kind, "status": item.status,
                 "progress": item.progress, "message": item.message}
                for item in application.jobs.list_for_project(project_id, 20)
            ],
        }

    @server.tool()
    async def generate_script(
        project_id: str,
        language: str = "en",
        target_duration_seconds: int = 60,
        platform: str = "short-form social video",
    ) -> dict[str, Any]:
        """Generate an editable script and storyboard from the project's brief."""
        return await application.creation.generate_script(
            project_id,
            {"language": language, "target_duration_seconds": target_duration_seconds, "platform": platform},
        )

    @server.tool()
    def import_media(project_id: str, source_path: str) -> dict[str, Any]:
        """Import an audio/video file already placed inside the configured Agent Video Studio data folder."""
        source = PathPolicy(application.settings.data_dir).require_managed(Path(source_path))
        asset = application.add_media_file(project_id, source)
        asset.pop("path", None)
        return asset

    @server.tool()
    async def analyze_media(project_id: str, transcription_model: str = "small") -> dict[str, Any]:
        """Transcribe the project's imported source and suggest clips with source timestamps."""
        result = await application.repurposing.analyze(project_id, model=transcription_model)
        result.get("source_asset", {}).pop("path", None)
        return result

    @server.tool()
    def select_highlights(project_id: str, selected_ids: list[str]) -> dict[str, Any]:
        """Choose suggested clip IDs and make them the project's editable timeline."""
        return application.choose_highlights(project_id, selected_ids)

    @server.tool()
    def edit_scene(project_id: str, scene_id: str, changes: dict[str, Any]) -> dict[str, Any]:
        """Edit the title, narration, visual direction, caption, or duration of a project scene."""
        from agent_video_studio.creation.models import SceneEdit

        edit = SceneEdit.model_validate(changes)
        return application.edit_scene(project_id, scene_id, edit)

    @server.tool()
    async def render_project(
        project_id: str,
        aspect_ratios: list[str] | None = None,
        include_captions: bool = True,
        use_tts: bool = True,
    ) -> dict[str, Any]:
        """Render the project and return safe download paths for each requested format."""
        result = await application.rendering.render_project(
            project_id,
            aspect_ratios=aspect_ratios,
            include_captions=include_captions,
            use_tts=use_tts,
        )
        return {
            "render_id": result["render_id"],
            "exports": [
                {key: item[key] for key in ("aspect_ratio", "duration_seconds", "width", "height")}
                | {"export_dir": str(Path(item["export_dir"]).relative_to(application.settings.data_dir))}
                for item in result["exports"]
            ],
        }

    @server.tool()
    async def preflight_publish(
        project_id: str, render_id: str, aspect_ratio: str
    ) -> list[dict[str, Any]]:
        """Check destination credentials, account permissions, and media requirements before publishing."""
        return await application.publishing.all_preflight(project_id, render_id, aspect_ratio)

    @server.tool()
    async def publish_export(
        project_id: str,
        render_id: str,
        aspect_ratio: str,
        platform: str,
        title: str,
        description: str = "",
        privacy_level: str = "private",
        confirm: bool = False,
    ) -> dict[str, Any]:
        """Publish an already rendered export. Set confirm=true only after the user reviews the destination and post details."""
        from agent_video_studio.publishing.models import PublishRequest

        if not confirm:
            raise ValueError("Publishing requires explicit user confirmation. Review the post, then set confirm=true.")
        if platform == "tiktok" and privacy_level == "private":
            privacy_level = "SELF_ONLY"
        request = PublishRequest(
            project_id=project_id,
            render_id=render_id,
            aspect_ratio=aspect_ratio,
            platform=platform,
            title=title,
            description=description,
            privacy_level=privacy_level,
            confirm=confirm,
        )
        return await application.publish_export(request)

    @server.tool()
    def get_job(job_id: str) -> dict[str, Any]:
        """Read the status and progress of an API/CLI background job."""
        job = application.jobs.get(job_id)
        return {"id": job.id, "project_id": job.project_id, "kind": job.kind, "status": job.status,
                "progress": job.progress, "message": job.message, "error": job.error}

    @server.tool()
    def list_providers() -> list[dict[str, Any]]:
        """Show configured text providers without returning API keys."""
        return application.providers.list_status()

    return server


def run_mcp(*, transport: str = "stdio", host: str = "127.0.0.1", port: int = 8788) -> None:
    server = build_server()
    if transport == "stdio":
        server.run(transport="stdio")
    elif transport == "streamable-http":
        server.run(transport="streamable-http", host=host, port=port)
    else:
        raise ValueError("MCP transport must be 'stdio' or 'streamable-http'.")


def _public_project(project: Any) -> dict[str, Any]:
    document = dict(project.document)
    document["exports"] = [
        {key: item.get(key) for key in ("render_id", "aspect_ratio", "duration_seconds", "width", "height")}
        for item in document.get("exports", [])
    ]
    return {"id": project.id, "title": project.title, "mode": project.mode, "status": project.status,
            "document": document}
