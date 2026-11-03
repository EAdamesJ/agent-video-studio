from __future__ import annotations

import asyncio
import importlib.util
import json
import shutil
from pathlib import Path

import typer

from agent_video_studio import __version__
from agent_video_studio.application import StudioApplication
from agent_video_studio.config import Settings
from agent_video_studio.core.paths import PathPolicy
from agent_video_studio.publishing.models import PublishRequest

app = typer.Typer(no_args_is_help=True, help="Create and repurpose videos with AI agents.")
project_app = typer.Typer(no_args_is_help=True, help="Create and manage video projects.")
app.add_typer(project_app, name="project")


def _application() -> StudioApplication:
    return StudioApplication(Settings.from_env())


@app.command()
def version() -> None:
    """Show the installed application version."""
    typer.echo(__version__)


@app.command()
def serve(
    host: str | None = typer.Option(None, help="Bind address; defaults to AVS_HOST or 127.0.0.1."),
    port: int | None = typer.Option(None, min=1, max=65535, help="Port; defaults to AVS_PORT or 8787."),
) -> None:
    """Start the browser workspace and REST API."""
    import uvicorn

    settings = Settings.from_env()
    uvicorn.run("agent_video_studio.api.app:app", host=host or settings.host, port=port or settings.port, reload=False)


@app.command()
def mcp(
    transport: str = typer.Option("stdio", help="MCP transport: stdio or streamable-http."),
    host: str | None = typer.Option(None, help="HTTP bind address; local loopback is safest."),
    port: int = typer.Option(8788, min=1, max=65535),
) -> None:
    """Start an MCP server for Claude/Codex-compatible hosts."""
    from agent_video_studio.mcp.server import run_mcp

    if transport not in {"stdio", "streamable-http"}:
        raise typer.BadParameter("Choose 'stdio' or 'streamable-http'.")
    settings = Settings.from_env()
    run_mcp(transport=transport, host=host or settings.host, port=port)


@app.command()
def providers() -> None:
    """List text providers and configuration status without exposing credentials."""
    typer.echo(json.dumps(_application().providers.list_status(), ensure_ascii=False, indent=2))


@app.command()
def doctor() -> None:
    """Check local requirements and optional integrations."""
    settings = Settings.from_env()
    output = {
        "version": __version__,
        "data_directory_exists": settings.data_dir.exists(),
        "ffmpeg": shutil.which("ffmpeg") or "missing",
        "ffprobe": shutil.which("ffprobe") or "missing",
        "text_providers": _application().providers.list_status(),
        "transcription_provider": settings.transcription_provider,
        "tts_provider": settings.tts_provider,
        "tts_configured": (settings.tts_provider == "edge" and importlib.util.find_spec("edge_tts") is not None)
        or (settings.tts_provider == "elevenlabs" and bool(settings.elevenlabs_api_key and settings.elevenlabs_voice_id)),
        "tiktok_configured": bool(settings.tiktok_access_token),
        "youtube_configured": bool(settings.youtube_client_secret_file and Path(settings.youtube_client_secret_file).is_file()),
        "instagram_configured": bool(settings.instagram_graph_token and settings.instagram_account_id
                                      and settings.meta_graph_version and settings.public_media_base_url.startswith("https://")),
    }
    typer.echo(json.dumps(output, ensure_ascii=False, indent=2))


@project_app.command("create")
def create_project(
    title: str = typer.Option(..., prompt=True),
    mode: str = typer.Option("prompt", help="prompt or repurpose"),
    brief: str = typer.Option("", help="Video brief or working notes."),
    language: str = typer.Option("en", help="Script and caption language."),
    aspect_ratio: str = typer.Option("9:16", help="9:16, 16:9, or 1:1."),
) -> None:
    """Create a video project."""
    if aspect_ratio not in {"9:16", "16:9", "1:1"}:
        raise typer.BadParameter("Choose 9:16, 16:9, or 1:1.")
    project = _application().create_project(title, mode, brief, language, [aspect_ratio])
    typer.echo(json.dumps({"id": project.id, "title": project.title, "mode": project.mode}, indent=2))


@project_app.command("list")
def list_projects() -> None:
    """List project IDs, modes, and status."""
    items = _application().projects.list()
    typer.echo(json.dumps([{"id": p.id, "title": p.title, "mode": p.mode, "status": p.status}
                           for p in items], ensure_ascii=False, indent=2))


@project_app.command("show")
def show_project(project_id: str) -> None:
    """Show the editable project document and recent jobs."""
    project = _application().projects.get(project_id)
    bundle = {"id": project.id, "title": project.title, "mode": project.mode, "status": project.status,
              "document": project.document}
    typer.echo(json.dumps(bundle, ensure_ascii=False, indent=2))


@project_app.command("import")
def import_media(project_id: str, path: Path = typer.Argument(..., exists=True, dir_okay=False)) -> None:
    """Copy a local audio/video source into the project's managed media folder."""
    asset = _application().add_media_file(project_id, path)
    asset.pop("path", None)
    typer.echo(json.dumps(asset, ensure_ascii=False, indent=2))


@project_app.command("script")
def generate_script(
    project_id: str,
    language: str = typer.Option("en"),
    target_duration_seconds: int = typer.Option(60, min=10, max=3600),
    platform: str = typer.Option("short-form social video"),
) -> None:
    """Generate an editable script and scene storyboard."""
    result = asyncio.run(
        _application().creation.generate_script(
            project_id,
            {"language": language, "target_duration_seconds": target_duration_seconds, "platform": platform},
        )
    )
    typer.echo(json.dumps(result, ensure_ascii=False, indent=2))


@project_app.command("analyze")
def analyze_media(project_id: str, model: str = typer.Option("small")) -> None:
    """Transcribe imported media and propose clips with exact source times."""
    result = asyncio.run(_application().repurposing.analyze(project_id, model=model))
    result.get("source_asset", {}).pop("path", None)
    typer.echo(json.dumps(result, ensure_ascii=False, indent=2))


@project_app.command("select-highlights")
def select_highlights(project_id: str, ids: str = typer.Argument(..., help="Comma-separated clip IDs.")) -> None:
    """Choose suggested clip IDs for the project timeline."""
    timeline = _application().choose_highlights(project_id, [item.strip() for item in ids.split(",") if item.strip()])
    typer.echo(json.dumps(timeline, ensure_ascii=False, indent=2))


@project_app.command("render")
def render_project(
    project_id: str,
    aspect_ratios: str = typer.Option("9:16", help="Comma-separated: 9:16,16:9,1:1"),
    captions: bool = typer.Option(True, "--captions/--no-captions"),
    tts: bool = typer.Option(True, "--tts/--no-tts"),
) -> None:
    """Render requested layouts and save MP4/caption/project export bundles."""
    ratios = [item.strip() for item in aspect_ratios.split(",") if item.strip()]
    result = asyncio.run(
        _application().rendering.render_project(
            project_id, aspect_ratios=ratios, include_captions=captions, use_tts=tts
        )
    )
    for export in result.get("exports", []):
        for key in ("video_path", "thumbnail_path", "captions_srt", "captions_vtt", "export_dir"):
            if key in export:
                export[key] = str(Path(export[key]).resolve())
    typer.echo(json.dumps(result, ensure_ascii=False, indent=2))


@project_app.command("export")
def export_bundle(project_id: str, render_id: str, aspect_ratio: str, destination: Path) -> None:
    """Copy a completed export bundle to a user-selected directory."""
    if aspect_ratio not in {"9:16", "16:9", "1:1"}:
        raise typer.BadParameter("Choose 9:16, 16:9, or 1:1.")
    if not render_id.isalnum() or len(render_id) > 40:
        raise typer.BadParameter("Invalid render ID.")
    settings = Settings.from_env()
    project = _application().projects.get(project_id)
    ratio = aspect_ratio.replace(":", "x")
    source = PathPolicy(settings.data_dir).managed("exports", project_id, render_id, ratio)
    if not source.is_dir():
        raise typer.BadParameter("The requested export bundle was not found.")
    target = destination.expanduser().resolve()
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        raise typer.BadParameter("Destination already exists; choose a new path to avoid overwriting files.")
    shutil.copytree(source, target)
    typer.echo(json.dumps({"project": project.title, "export_directory": str(target)}, ensure_ascii=False, indent=2))


@project_app.command("preflight-publish")
def preflight_publish(project_id: str, render_id: str, aspect_ratio: str) -> None:
    """Check social publishing requirements without uploading media."""
    if aspect_ratio not in {"9:16", "16:9", "1:1"}:
        raise typer.BadParameter("Choose 9:16, 16:9, or 1:1.")
    app = _application()
    result = asyncio.run(app.publishing.all_preflight(project_id, render_id, aspect_ratio))
    typer.echo(json.dumps(result, ensure_ascii=False, indent=2))


@project_app.command("publish")
def publish_export(
    project_id: str,
    render_id: str,
    aspect_ratio: str,
    platform: str = typer.Option(..., help="youtube, instagram, or tiktok"),
    title: str = typer.Option(..., prompt=True),
    description: str = typer.Option(""),
    privacy_level: str = typer.Option("private"),
    confirm: bool = typer.Option(False, "--confirm/--no-confirm", help="Required to send the post."),
    share_to_feed: bool = typer.Option(True, "--share-to-feed/--no-share-to-feed"),
    ai_generated: bool = typer.Option(True, "--ai-generated/--not-ai-generated"),
) -> None:
    """Publish an existing export after preflight and explicit confirmation."""
    if not confirm:
        raise typer.BadParameter("Review `avs project preflight-publish`, then pass --confirm to publish.")
    if platform == "tiktok" and privacy_level == "private":
        privacy_level = "SELF_ONLY"
    request = PublishRequest(
        project_id=project_id, render_id=render_id, aspect_ratio=aspect_ratio, platform=platform,
        title=title, description=description, privacy_level=privacy_level, confirm=confirm,
        share_to_feed=share_to_feed, ai_generated=ai_generated,
    )
    result = asyncio.run(_application().publish_export(request))
    typer.echo(json.dumps(result, ensure_ascii=False, indent=2))


@project_app.command("jobs")
def list_jobs(project_id: str) -> None:
    """List recent background jobs for a project."""
    jobs = _application().jobs.list_for_project(project_id)
    typer.echo(json.dumps([job.to_dict() for job in jobs], ensure_ascii=False, indent=2))

\n