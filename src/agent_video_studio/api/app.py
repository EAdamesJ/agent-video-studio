from __future__ import annotations

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from agent_video_studio import __version__
from agent_video_studio.api.routes import router
from agent_video_studio.application import StudioApplication
from agent_video_studio.config import Settings
from agent_video_studio.core.logging import configure_logging


def create_app(settings: Settings | None = None) -> FastAPI:
    active_settings = settings or Settings.from_env()
    configure_logging(active_settings.log_level)
    application = StudioApplication(active_settings)

    @asynccontextmanager
    async def lifespan(_app: FastAPI):
        await application.start()
        yield
        await application.stop()

    app = FastAPI(
        title="Agent Video Studio API",
        version=__version__,
        description="Local-first AI video creation and repurposing API.",
        lifespan=lifespan,
    )
    app.state.studio = application
    app.include_router(router)
    static_dir = Path(__file__).resolve().parent.parent / "web"
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

    @app.get("/", include_in_schema=False)
    def index() -> FileResponse:
        return FileResponse(static_dir / "index.html")

    return app


app = create_app()

\n