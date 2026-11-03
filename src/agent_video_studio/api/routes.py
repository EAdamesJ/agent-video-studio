from __future__ import annotations

from pathlib import Path
from typing import Any

from fastapi import APIRouter, File, HTTPException, Request, UploadFile
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import FileResponse

from agent_video_studio.api.schemas import (
    AnalyzeRequest,
    HighlightSelectionRequest,
    ProjectCreateRequest,
    ProjectDocumentUpdate,
    ProjectUpdateRequest,
    PublishExportRequest,
    RenderRequest,
    SceneEditRequest,
    ScriptRequest,
)
from agent_video_studio.api.serialization import public_asset, public_job, public_project
from agent_video_studio.core.paths import PathPolicy
from agent_video_studio.providers.base import ProviderError

router = APIRouter(prefix="/api")


def studio(request: Request):
    return request.app.state.studio


@router.get("/health")
def health(request: Request) -> dict[str, Any]:
    app = studio(request)
    from agent_video_studio import __version__

    return {"status": "ok", "version": __version__, "providers": app.providers.list_status()}


@router.get("/providers")
def providers(request: Request) -> dict[str, Any]:
    app = studio(request)
    return {"text": app.providers.list_status(), "transcription": app.settings.transcription_provider,
            "stock": ["pexels" if app.settings.pexels_api_key else None,
                      "pixabay" if app.settings.pixabay_api_key else None]}


@router.get("/projects")
def list_projects(request: Request) -> list[dict[str, Any]]:
    return [public_project(item) for item in studio(request).projects.list()]


@router.post("/projects", status_code=201)
def create_project(body: ProjectCreateRequest, request: Request) -> dict[str, Any]:
    try:
        project = studio(request).create_project(
            body.title, body.mode, body.brief, body.language, body.aspect_ratios
        )
        return public_project(project)
    except ValueError as exc:
        raise HTTPException(400, str(exc)) from exc


@router.get("/projects/{project_id}")
def get_project(project_id: str, request: Request) -> dict[str, Any]:
    try:
        bundle = studio(request).project_bundle(project_id)
        return {
            "project": public_project(bundle["project"]),
            "assets": [public_asset(item) for item in bundle["assets"]],
            "jobs": [public_job(item) for item in bundle["jobs"]],
            "providers": bundle["providers"],
        }
    except KeyError as exc:
        raise HTTPException(404, str(exc)) from exc


@router.patch("/projects/{project_id}")
def update_project(project_id: str, body: ProjectUpdateRequest, request: Request) -> dict[str, Any]:
    app = studio(request)
    try:
        project = app.projects.get(project_id)
        changes = body.model_dump(exclude_unset=True, exclude_none=True)
        document_patch = {key: changes.pop(key) for key in list(changes) if key != "title"}
        return public_project(app.projects.update(project_id, title=changes.get("title"), document_patch=document_patch))
    except KeyError as exc:
        raise HTTPException(404, str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(400, str(exc)) from exc


@router.post("/projects/{project_id}/upload", status_code=201)
async def upload_media(project_id: str, request: Request, file: UploadFile = File(...)) -> dict[str, Any]:
    app = studio(request)
    try:
        app.projects.get(project_id)
        chunks = iter(lambda: file.file.read(1024 * 1024), b"")
        asset = await run_in_threadpool(app.add_media_upload, project_id, file.filename or "media", chunks)
        asset.pop("path", None)
        return {"asset": asset}
    except KeyError as exc:
        raise HTTPException(404, str(exc)) from exc
    except (ValueError, FileNotFoundError) as exc:
        raise HTTPException(400, str(exc)) from exc
    finally:
        await file.close()


@router.post("/projects/{project_id}/script", status_code=202)
async def generate_script(project_id: str, body: ScriptRequest, request: Request) -> dict[str, Any]:
    try:
        app = studio(request)
        job = await app.schedule_script(project_id, body.model_dump(exclude_none=True))
        return {"job": public_job(job)}
    except KeyError as exc:
        raise HTTPException(404, str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(400, str(exc)) from exc
    except ProviderError as exc:
        raise HTTPException(503, str(exc)) from exc


@router.post("/projects/{project_id}/analyze", status_code=202)
async def analyze_media(project_id: str, body: AnalyzeRequest, request: Request) -> dict[str, Any]:
    try:
        app = studio(request)
        job = await app.schedule_analysis(project_id, body.model_dump())
        return {"job": public_job(job)}
    except KeyError as exc:
        raise HTTPException(404, str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(400, str(exc)) from exc


@router.post("/projects/{project_id}/highlights")
def choose_highlights(project_id: str, body: HighlightSelectionRequest, request: Request) -> dict[str, Any]:
    try:
        return studio(request).choose_highlights(project_id, body.selected_ids)
    except KeyError as exc:
        raise HTTPException(404, str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(400, str(exc)) from exc


@router.patch("/projects/{project_id}/scenes/{scene_id}")
def edit_scene(project_id: str, scene_id: str, body: SceneEditRequest, request: Request) -> dict[str, Any]:
    try:
        return studio(request).edit_scene(project_id, scene_id, body)
    except KeyError as exc:
        raise HTTPException(404, str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(400, str(exc)) from exc


@router.patch("/projects/{project_id}/document")
def update_project_document(
    project_id: str, body: ProjectDocumentUpdate, request: Request
) -> dict[str, Any]:
    app = studio(request)
    try:
        patch = body.model_dump(exclude_unset=True, exclude_none=True)
        project = app.projects.update(project_id, document_patch=patch)
        return public_project(project)
    except KeyError as exc:
        raise HTTPException(404, str(exc)) from exc


@router.post("/projects/{project_id}/render", status_code=202)
async def render_project(project_id: str, body: RenderRequest, request: Request) -> dict[str, Any]:
    try:
        app = studio(request)
        job = await app.schedule_render(project_id, body.model_dump(exclude_none=True))
        return {"job": public_job(job)}
    except KeyError as exc:
        raise HTTPException(404, str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(400, str(exc)) from exc


@router.get("/projects/{project_id}/exports/{render_id}/{aspect}/publishers")
async def publisher_preflight(project_id: str, render_id: str, aspect: str, request: Request) -> list[dict[str, Any]]:
    ratio = aspect.replace("x", ":")
    try:
        return await studio(request).publishing.all_preflight(project_id, render_id, ratio)
    except (KeyError, ValueError, FileNotFoundError) as exc:
        raise HTTPException(400, str(exc)) from exc


@router.post("/projects/{project_id}/publish", status_code=201)
async def publish_export(project_id: str, body: PublishExportRequest, request: Request) -> dict[str, Any]:
    try:
        app = studio(request)
        app.projects.get(project_id)
        result = await app.publish_export(body.to_publish_request(project_id))
        return result
    except KeyError as exc:
        raise HTTPException(404, str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(400, str(exc)) from exc
    except ProviderError as exc:
        raise HTTPException(502, str(exc)) from exc


@router.get("/jobs/{job_id}")
def get_job(job_id: str, request: Request) -> dict[str, Any]:
    try:
        return public_job(studio(request).jobs.get(job_id))
    except KeyError as exc:
        raise HTTPException(404, str(exc)) from exc


@router.post("/jobs/{job_id}/cancel")
def cancel_job(job_id: str, request: Request) -> dict[str, Any]:
    try:
        return public_job(studio(request).runner.cancel(job_id))
    except KeyError as exc:
        raise HTTPException(404, str(exc)) from exc


@router.get("/projects/{project_id}/exports/{render_id}/{aspect}/{filename}")
def download_export(
    project_id: str, render_id: str, aspect: str, filename: str, request: Request
) -> FileResponse:
    allowed_files = {"video.mp4", "captions.srt", "captions.vtt", "thumbnail.jpg", "project.json", "social-metadata.json"}
    if filename not in allowed_files:
        raise HTTPException(404, "Export file not found.")
    if aspect not in {"9x16", "16x9", "1x1"} or not render_id.isalnum():
        raise HTTPException(400, "Invalid export reference.")
    app = studio(request)
    path = PathPolicy(app.settings.data_dir).managed("exports", project_id, render_id, aspect, filename)
    if not path.is_file():
        raise HTTPException(404, "Export file not found.")
    return FileResponse(path, filename=filename)
