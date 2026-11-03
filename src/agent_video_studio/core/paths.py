from __future__ import annotations

import re
from pathlib import Path


class PathPolicy:
    def __init__(self, data_root: Path) -> None:
        self.root = data_root.expanduser().resolve()
        self.root.mkdir(parents=True, exist_ok=True)

    def managed(self, *parts: str) -> Path:
        candidate = self.root.joinpath(*parts).resolve()
        if not candidate.is_relative_to(self.root):
            raise ValueError("Requested path escapes the configured data directory.")
        return candidate

    def require_managed(self, path: str | Path) -> Path:
        candidate = Path(path).expanduser().resolve()
        if not candidate.is_relative_to(self.root):
            raise ValueError("File must be inside the configured data directory.")
        return candidate


def safe_filename(value: str, fallback: str = "media") -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "_", Path(value).name).strip("._")
    return cleaned[:120] or fallback
