from __future__ import annotations

from pathlib import Path
from typing import Any

from agent_video_studio.core.db import Database, decode_json, encode_json
from agent_video_studio.core.models import Asset, new_id, utc_now


class AssetStore:
    def __init__(self, db: Database) -> None:
        self.db = db

    def create(
        self,
        project_id: str,
        path: Path,
        kind: str,
        mime_type: str,
        duration_seconds: float | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> Asset:
        if not path.is_file():
            raise FileNotFoundError(f"Asset file does not exist: {path.name}")
        asset = Asset(
            id=new_id("ast"),
            project_id=project_id,
            path=str(path.resolve()),
            kind=kind,
            name=path.name,
            mime_type=mime_type,
            size_bytes=path.stat().st_size,
            duration_seconds=duration_seconds,
            metadata=metadata or {},
        )
        with self.db.connect() as connection:
            exists = connection.execute("SELECT 1 FROM projects WHERE id=?", (project_id,)).fetchone()
            if exists is None:
                raise KeyError(f"Project '{project_id}' was not found.")
            connection.execute(
                "INSERT INTO assets(id,project_id,path,kind,name,mime_type,size_bytes,duration_seconds,"
                "metadata_json,created_at) VALUES(?,?,?,?,?,?,?,?,?,?)",
                (
                    asset.id,
                    asset.project_id,
                    asset.path,
                    asset.kind,
                    asset.name,
                    asset.mime_type,
                    asset.size_bytes,
                    asset.duration_seconds,
                    encode_json(asset.metadata),
                    asset.created_at,
                ),
            )
        return asset

    def get(self, asset_id: str) -> Asset:
        with self.db.connect() as connection:
            row = connection.execute("SELECT * FROM assets WHERE id=?", (asset_id,)).fetchone()
        if row is None:
            raise KeyError(f"Asset '{asset_id}' was not found.")
        return self._from_row(row)

    def list_for_project(self, project_id: str) -> list[Asset]:
        with self.db.connect() as connection:
            rows = connection.execute(
                "SELECT * FROM assets WHERE project_id=? ORDER BY created_at", (project_id,)
            ).fetchall()
        return [self._from_row(row) for row in rows]

    @staticmethod
    def _from_row(row: Any) -> Asset:
        return Asset(
            id=row["id"],
            project_id=row["project_id"],
            path=row["path"],
            kind=row["kind"],
            name=row["name"],
            mime_type=row["mime_type"],
            size_bytes=row["size_bytes"],
            duration_seconds=row["duration_seconds"],
            metadata=decode_json(row["metadata_json"], {}) or {},  # type: ignore[arg-type]
            created_at=row["created_at"],
        )
