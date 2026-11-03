from __future__ import annotations

from typing import Any

from agent_video_studio.core.db import Database, decode_json, encode_json
from agent_video_studio.core.models import Job, new_id, utc_now


class JobStore:
    def __init__(self, db: Database) -> None:
        self.db = db

    def create(self, project_id: str, kind: str, payload: dict[str, Any]) -> Job:
        now = utc_now()
        job = Job(new_id("job"), project_id, kind, "queued", 0, "Queued", payload, None, None, now, now)
        with self.db.connect() as connection:
            exists = connection.execute("SELECT 1 FROM projects WHERE id=?", (project_id,)).fetchone()
            if exists is None:
                raise KeyError(f"Project '{project_id}' was not found.")
            connection.execute(
                "INSERT INTO jobs(id,project_id,kind,status,progress,message,payload_json,result_json,error,"
                "created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?,?)",
                (
                    job.id, job.project_id, job.kind, job.status, job.progress, job.message,
                    encode_json(job.payload), None, None, job.created_at, job.updated_at,
                ),
            )
        return job

    def get(self, job_id: str) -> Job:
        with self.db.connect() as connection:
            row = connection.execute("SELECT * FROM jobs WHERE id=?", (job_id,)).fetchone()
        if row is None:
            raise KeyError(f"Job '{job_id}' was not found.")
        return self._from_row(row)

    def list_for_project(self, project_id: str, limit: int = 100) -> list[Job]:
        with self.db.connect() as connection:
            rows = connection.execute(
                "SELECT * FROM jobs WHERE project_id=? ORDER BY created_at DESC LIMIT ?",
                (project_id, max(1, min(limit, 500))),
            ).fetchall()
        return [self._from_row(row) for row in rows]

    def update(
        self,
        job_id: str,
        *,
        status: str | None = None,
        progress: float | None = None,
        message: str | None = None,
        result: dict[str, Any] | None = None,
        error: str | None = None,
    ) -> Job:
        job = self.get(job_id)
        if status is not None:
            if status not in {"queued", "running", "completed", "failed", "cancelled"}:
                raise ValueError("Invalid job status.")
            job.status = status  # type: ignore[assignment]
        if progress is not None:
            job.progress = max(0.0, min(100.0, float(progress)))
        if message is not None:
            job.message = message[:500]
        if result is not None:
            job.result = result
        if error is not None:
            job.error = error[:2000]
        job.updated_at = utc_now()
        with self.db.connect() as connection:
            connection.execute(
                "UPDATE jobs SET status=?,progress=?,message=?,result_json=?,error=?,updated_at=? WHERE id=?",
                (job.status, job.progress, job.message, encode_json(job.result) if job.result else None,
                 job.error, job.updated_at, job_id),
            )
        return job

    def recover_interrupted(self) -> list[Job]:
        with self.db.connect() as connection:
            rows = connection.execute("SELECT * FROM jobs WHERE status IN ('queued','running')").fetchall()
            connection.execute(
                "UPDATE jobs SET status='queued', message='Recovered after restart', updated_at=? "
                "WHERE status IN ('queued','running')",
                (utc_now(),),
            )
        return [self._from_row(row) for row in rows]

    @staticmethod
    def _from_row(row: Any) -> Job:
        return Job(
            id=row["id"],
            project_id=row["project_id"],
            kind=row["kind"],
            status=row["status"],
            progress=row["progress"],
            message=row["message"],
            payload=decode_json(row["payload_json"], {}) or {},  # type: ignore[arg-type]
            result=decode_json(row["result_json"], None),  # type: ignore[arg-type]
            error=row["error"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

\n