from __future__ import annotations

from typing import Any

from agent_video_studio.core.models import Asset, Job, Project


def public_project(project: Project) -> dict[str, Any]:
    document = dict(project.document)
    document["exports"] = [
        {key: item.get(key) for key in ("render_id", "aspect_ratio", "duration_seconds", "width", "height")}
        for item in project.document.get("exports", [])
    ]
    return {
        "id": project.id,
        "title": project.title,
        "mode": project.mode,
        "status": project.status,
        "created_at": project.created_at,
        "updated_at": project.updated_at,
        "document": document,
    }


def public_asset(asset: Asset) -> dict[str, Any]:
    return {
        "id": asset.id,
        "project_id": asset.project_id,
        "kind": asset.kind,
        "name": asset.name,
        "mime_type": asset.mime_type,
        "size_bytes": asset.size_bytes,
        "duration_seconds": asset.duration_seconds,
        "metadata": asset.metadata,
        "created_at": asset.created_at,
    }


def public_job(job: Job) -> dict[str, Any]:
    result = job.result
    if isinstance(result, dict) and "exports" in result:
        result = {
            "render_id": result.get("render_id"),
            "exports": [
                {
                    key: value
                    for key, value in item.items()
                    if key not in {"video_path", "thumbnail_path", "captions_srt", "captions_vtt", "export_dir"}
                }
                | {"download_url": f"/api/projects/{job.project_id}/exports/{result.get('render_id')}/"
                   f"{str(item.get('aspect_ratio', '9:16')).replace(':', 'x')}/video.mp4"}
                for item in result["exports"]
            ],
        }
    return {
        "id": job.id,
        "project_id": job.project_id,
        "kind": job.kind,
        "status": job.status,
        "progress": job.progress,
        "message": job.message,
        "payload": job.payload,
        "result": result,
        "error": job.error,
        "created_at": job.created_at,
        "updated_at": job.updated_at,
    }

\n