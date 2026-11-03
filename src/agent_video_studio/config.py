from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path


@dataclass(frozen=True, slots=True)
class Settings:
    data_dir: Path
    host: str
    port: int
    log_level: str
    text_provider: str
    text_model: str
    text_base_url: str
    deepseek_api_key: str
    anthropic_api_key: str
    openai_api_key: str
    pexels_api_key: str
    pixabay_api_key: str
    elevenlabs_api_key: str
    elevenlabs_voice_id: str
    elevenlabs_model_id: str
    tts_provider: str
    transcription_provider: str
    youtube_client_secret_file: str
    tiktok_client_key: str
    tiktok_client_secret: str
    tiktok_access_token: str
    instagram_graph_token: str
    instagram_account_id: str
    instagram_graph_host: str
    meta_graph_version: str
    public_media_base_url: str

    @classmethod
    def from_env(cls) -> "Settings":
        try:
            from dotenv import load_dotenv

            load_dotenv(override=False)
        except ImportError:
            pass
        default_data_dir = Path.home() / ".agent-video-studio"
        return cls(
            data_dir=Path(os.getenv("AVS_DATA_DIR", str(default_data_dir))).expanduser().resolve(),
            host=os.getenv("AVS_HOST", "127.0.0.1"),
            port=int(os.getenv("AVS_PORT", "8787")),
            log_level=os.getenv("AVS_LOG_LEVEL", "INFO").upper(),
            text_provider=os.getenv("AVS_TEXT_PROVIDER", "deepseek").strip().lower(),
            text_model=os.getenv("AVS_TEXT_MODEL", "").strip(),
            text_base_url=os.getenv("AVS_TEXT_BASE_URL", "").strip(),
            deepseek_api_key=os.getenv("DEEPSEEK_API_KEY", ""),
            anthropic_api_key=os.getenv("ANTHROPIC_API_KEY", ""),
            openai_api_key=os.getenv("OPENAI_API_KEY", ""),
            pexels_api_key=os.getenv("PEXELS_API_KEY", ""),
            pixabay_api_key=os.getenv("PIXABAY_API_KEY", ""),
            elevenlabs_api_key=os.getenv("ELEVENLABS_API_KEY", ""),
            elevenlabs_voice_id=os.getenv("ELEVENLABS_VOICE_ID", "").strip(),
            elevenlabs_model_id=os.getenv("ELEVENLABS_MODEL_ID", "eleven_multilingual_v2").strip(),
            tts_provider=os.getenv("AVS_TTS_PROVIDER", "edge").strip().lower(),
            transcription_provider=os.getenv("AVS_TRANSCRIPTION_PROVIDER", "local").strip().lower(),
            youtube_client_secret_file=os.getenv("YOUTUBE_CLIENT_SECRET_FILE", "").strip(),
            tiktok_client_key=os.getenv("TIKTOK_CLIENT_KEY", "").strip(),
            tiktok_client_secret=os.getenv("TIKTOK_CLIENT_SECRET", ""),
            tiktok_access_token=os.getenv("TIKTOK_ACCESS_TOKEN", "").strip(),
            instagram_graph_token=os.getenv("INSTAGRAM_GRAPH_TOKEN", ""),
            instagram_account_id=os.getenv("INSTAGRAM_ACCOUNT_ID", ""),
            instagram_graph_host=os.getenv("INSTAGRAM_GRAPH_HOST", "graph.instagram.com").strip(),
            meta_graph_version=os.getenv("AVS_META_GRAPH_VERSION", "").strip(),
            public_media_base_url=os.getenv("AVS_PUBLIC_MEDIA_BASE_URL", "").rstrip("/"),
        )

    def ensure_data_dirs(self) -> None:
        for child in ("projects", "assets", "renders", "exports", "tmp", "credentials"):
            (self.data_dir / child).mkdir(parents=True, exist_ok=True)

    @property
    def database_path(self) -> Path:
        return self.data_dir / "studio.sqlite3"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings.from_env()

\n