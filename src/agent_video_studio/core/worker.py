from __future__ import annotations

import asyncio
import logging
from collections.abc import Awaitable, Callable
from typing import Any

from agent_video_studio.core.jobs import JobStore
from agent_video_studio.core.models import Job
from agent_video_studio.core.projects import ProjectStore

logger = logging.getLogger(__name__)
JobHandler = Callable[[Job, Callable[[float, str], Awaitable[None]]], Awaitable[dict[str, Any]]]


class JobRunner:
    """Single-process durable worker suitable for a self-hosted workspace."""

    def __init__(self, jobs: JobStore, projects: ProjectStore | None = None) -> None:
        self.jobs = jobs
        self.projects = projects
        self.handlers: dict[str, JobHandler] = {}
        self.queue: asyncio.Queue[str | None] = asyncio.Queue()
        self.worker_task: asyncio.Task[None] | None = None
        self._cancelled: set[str] = set()

    def register(self, kind: str, handler: JobHandler) -> None:
        self.handlers[kind] = handler

    async def start(self) -> None:
        if self.worker_task is not None:
            return
        recovered = self.jobs.recover_interrupted()
        for job in recovered:
            await self.queue.put(job.id)
        self.worker_task = asyncio.create_task(self._run(), name="avs-job-worker")

    async def stop(self) -> None:
        if self.worker_task is None:
            return
        await self.queue.put(None)
        await self.worker_task
        self.worker_task = None

    async def submit(self, project_id: str, kind: str, payload: dict[str, Any]) -> Job:
        if kind not in self.handlers:
            raise ValueError(f"No job handler is registered for '{kind}'.")
        job = self.jobs.create(project_id, kind, payload)
        await self.queue.put(job.id)
        return job

    def cancel(self, job_id: str) -> Job:
        job = self.jobs.get(job_id)
        if job.status in {"completed", "failed", "cancelled"}:
            return job
        self._cancelled.add(job_id)
        if job.status == "queued":
            if self.projects:
                self.projects.update(job.project_id, status="draft")
            return self.jobs.update(job_id, status="cancelled", message="Cancelled by user.")
        return self.jobs.update(job_id, message="Cancellation requested.")

    def is_cancelled(self, job_id: str) -> bool:
        return job_id in self._cancelled

    async def _run(self) -> None:
        while True:
            job_id = await self.queue.get()
            if job_id is None:
                self.queue.task_done()
                break
            try:
                job = self.jobs.get(job_id)
                if job.status == "cancelled":
                    continue
                handler = self.handlers.get(job.kind)
                if handler is None:
                    self.jobs.update(job_id, status="failed", error="Job handler is unavailable.")
                    continue
                self.jobs.update(job_id, status="running", progress=1, message="Starting")
                if self.projects:
                    self.projects.update(job.project_id, status="processing")

                async def report(progress: float, message: str) -> None:
                    if self.is_cancelled(job_id):
                        raise asyncio.CancelledError
                    self.jobs.update(job_id, progress=progress, message=message)

                try:
                    result = await handler(job, report)
                    if self.is_cancelled(job_id):
                        self.jobs.update(job_id, status="cancelled", message="Cancelled by user.")
                        if self.projects:
                            self.projects.update(job.project_id, status="draft")
                    else:
                        self.jobs.update(
                            job_id, status="completed", progress=100, message="Complete", result=result
                        )
                        if self.projects:
                            self.projects.update(job.project_id, status="ready")
                except asyncio.CancelledError:
                    self.jobs.update(job_id, status="cancelled", message="Cancelled by user.")
                    if self.projects:
                        self.projects.update(job.project_id, status="draft")
                except Exception as exc:
                    logger.exception("Job %s failed (%s)", job_id, job.kind)
                    self.jobs.update(job_id, status="failed", message="Failed", error=str(exc))
                    if self.projects:
                        self.projects.update(job.project_id, status="failed")
            finally:
                self._cancelled.discard(job_id)
                self.queue.task_done()
