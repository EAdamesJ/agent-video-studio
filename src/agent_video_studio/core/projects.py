from __future__ import annotations

from typing import Any

from agent_video_studio.core.db import Database, decode_json, encode_json
from agent_video_studio.core.models import Project, new_id, utc_now


class ProjectStore:
    def __init__(self, db: Database) -> None:
        self.db = db

    def create(
        self,
        title: str,
        mode: str,
        brief: str = "",
        language: str = "en",
        aspect_ratios: list[str] | None = None,
    ) -> Project:
        title = title.strip()
        if not title:
            raise ValueError("Project title cannot be empty.")
        if mode not in {"prompt", "repurpose"}:
            raise ValueError("Project mode must be 'prompt' or 'repurpose'.")
        now = utc_now()
        project_id = new_id("prj")
        document: dict[str, Any] = {
            "brief": brief.strip(),
            "language": language or "en",
            "aspect_ratios": aspect_ratios or ["9:16"],
            "script": None,
            "transcript": None,
            "highlights": [],
            "timeline": {"version": 1, "scenes": []},
            "exports": [],
            "metadata": {},
        }
        with self.db.connect() as connection:
            connection.execute(
                "INSERT INTO projects(id,title,mode,status,created_at,updated_at,document_json) "
                "VALUES(?,?,?,?,?,?,?)",
                (project_id, title, mode, "draft", now, now, encode_json(document)),
            )
        return Project(project_id, title, mode, "draft", now, now, document)  # type: ignore[arg-type]

    def get(self, project_id: str) -> Project:
        with self.db.connect() as connection:
            row = connection.execute("SELECT * FROM projects WHERE id=?", (project_id,)).fetchone()
        if row is None:
            raise KeyError(f"Project '{project_id}' was not found.")
        return self._from_row(row)

    def list(self, limit: int = 100) -> list[Project]:
        with self.db.connect() as connection:
            rows = connection.execute(
                "SELECT * FROM projects ORDER BY updated_at DESC LIMIT ?", (max(1, min(limit, 500)),)
            ).fetchall()
        return [self._from_row(row) for row in rows]

    def update(
        self,
        project_id: str,
        *,
        title: str | None = None,
        status: str | None = None,
        document_patch: dict[str, Any] | None = None,
    ) -> Project:
        project = self.get(project_id)
        if title is not None:
            if not title.strip():
                raise ValueError("Project title cannot be empty.")
            project.title = title.strip()
        if status is not None:
            if status not in {"draft", "processing", "ready", "failed"}:
                raise ValueError("Invalid project status.")
            project.status = status  # type: ignore[assignment]
        if document_patch:
            project.document.update(document_patch)
        project.updated_at = utc_now()
        with self.db.connect() as connection:
            connection.execute(
                "UPDATE projects SET title=?, status=?, updated_at=?, document_json=? WHERE id=?",
                (project.title, project.status, project.updated_at, encode_json(project.document), project_id),
            )
        return project

    def delete(self, project_id: str) -> None:
        with self.db.connect() as connection:
            cursor = connection.execute("DELETE FROM projects WHERE id=?", (project_id,))
        if cursor.rowcount == 0:
            raise KeyError(f"Project '{project_id}' was not found.")

    @staticmethod
    def _from_row(row: Any) -> Project:
        return Project(
            id=row["id"],
            title=row["title"],
            mode=row["mode"],
            status=row["status"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
            document=decode_json(row["document_json"], {}) or {},  # type: ignore[arg-type]
        )

\n