# Implementation Tasks

Tasks are ordered by the approved module dependency graph. Each code task is scoped to a small vertical slice; implementation phases do not reduce the agreed 0.1.0 release scope.

## Phase 1 — Foundation

- [ ] Task 1: Package scaffold and CLI entry point.
  - Acceptance: editable Python package installs and exposes a discoverable CLI.
  - Verify: inspect CLI help and package metadata.
  - Files: `pyproject.toml`, `src/agent_video_studio/__init__.py`, `src/agent_video_studio/__main__.py`, `src/agent_video_studio/cli.py`.
- [ ] Task 2: Settings, local data root, logging redaction, and media path policy.
  - Acceptance: defaults are local/loopback; credentials never appear in logs; all managed paths stay under the data root.
  - Verify: inspect settings and diagnostic output with fake credentials.
  - Files: `src/agent_video_studio/config.py`, `src/agent_video_studio/core/paths.py`, `src/agent_video_studio/core/logging.py`, `.env.example`.
- [ ] Task 3: SQLite schema and project/asset repositories.
  - Acceptance: create/list/read/update project and asset records across restarts.
  - Verify: create a project via CLI and inspect persisted project metadata.
  - Dependencies: Tasks 1–2.
  - Files: `src/agent_video_studio/core/models.py`, `src/agent_video_studio/core/db.py`, `src/agent_video_studio/core/projects.py`, `src/agent_video_studio/core/assets.py`.
- [ ] Task 4: Durable job queue and progress state.
  - Acceptance: queued/running/completed/failed/cancelled jobs persist and recover safely.
  - Verify: run a no-op job and inspect state after process restart.
  - Dependencies: Task 3.
  - Files: `src/agent_video_studio/core/jobs.py`, `src/agent_video_studio/core/worker.py`, `src/agent_video_studio/core/events.py`.

## Phase 2 — Providers and content paths

- [ ] Task 5: Provider contracts, registry, and diagnostics.
  - Acceptance: providers declare capabilities, setup requirements, and local/remote processing behavior.
  - Verify: provider listing and doctor output work with missing optional credentials.
  - Dependencies: Task 2.
  - Files: `src/agent_video_studio/providers/base.py`, `src/agent_video_studio/providers/registry.py`, `src/agent_video_studio/providers/health.py`.
- [ ] Task 6: Anthropic and OpenAI-compatible text generation adapters.
  - Acceptance: Claude and DeepSeek/OpenAI-compatible configuration returns normalized structured output.
  - Verify: mocked responses and redacted network errors.
  - Dependencies: Task 5.
  - Files: `src/agent_video_studio/providers/llm.py`, `src/agent_video_studio/providers/anthropic.py`, `src/agent_video_studio/providers/openai_compatible.py`, `src/agent_video_studio/providers/presets.py`.
- [ ] Task 7: Brief-to-script/storyboard workflow and scene editing.
  - Acceptance: editable, ordered scenes preserve approved text during targeted revisions.
  - Verify: create a script from a brief and update one scene without changing others.
  - Dependencies: Tasks 3 and 6.
  - Files: `src/agent_video_studio/creation/models.py`, `src/agent_video_studio/creation/service.py`, `src/agent_video_studio/creation/prompts.py`, `src/agent_video_studio/creation/edits.py`.
- [ ] Task 8: Media upload, probing, and source asset registration.
  - Acceptance: supported local audio/video inputs are validated and registered without modifying originals.
  - Verify: import an owned media fixture and inspect metadata.
  - Dependencies: Tasks 2–3.
  - Files: `src/agent_video_studio/media/ingest.py`, `src/agent_video_studio/media/probe.py`, `src/agent_video_studio/api/uploads.py`.
- [ ] Task 9: Transcription and highlight selection.
  - Acceptance: transcript segments and selected clips retain exact source timestamps and rationale.
  - Verify: exercise local/remote transcription adapters and inspect bounded clip times.
  - Dependencies: Tasks 5–6 and 8.
  - Files: `src/agent_video_studio/providers/transcription.py`, `src/agent_video_studio/repurposing/transcript.py`, `src/agent_video_studio/repurposing/highlights.py`, `src/agent_video_studio/repurposing/service.py`.
- [ ] Task 10: Stock, speech, and generated-media adapters.
  - Acceptance: user can select local media, configured stock search, TTS, or a registered generated-media provider.
  - Verify: provider discovery and one selected asset/TTS flow with configured credentials.
  - Dependencies: Task 5.
  - Files: `src/agent_video_studio/providers/speech.py`, `src/agent_video_studio/providers/stock.py`, `src/agent_video_studio/providers/generated_media.py`, `src/agent_video_studio/providers/assets.py`.

## Checkpoint — Content workflows

- [ ] Brief projects and repurpose projects both produce editable timeline data through the shared core.

## Phase 3 — Rendering and exports

- [ ] Task 11: Timeline model, safe FFmpeg runner, and aspect-ratio layouts.
  - Acceptance: project renders MP4 9:16, 16:9, and 1:1 without shell interpolation.
  - Verify: render a short local fixture and probe output dimensions.
  - Dependencies: Tasks 7 and 9.
  - Files: `src/agent_video_studio/media/timeline.py`, `src/agent_video_studio/media/ffmpeg.py`, `src/agent_video_studio/media/layouts.py`, `src/agent_video_studio/media/render.py`.
- [ ] Task 12: Audio mix, captions, thumbnails, and export bundle.
  - Acceptance: export includes MP4, editable project, SRT/VTT, thumbnail, and social metadata.
  - Verify: inspect a generated local export bundle.
  - Dependencies: Task 11.
  - Files: `src/agent_video_studio/media/audio.py`, `src/agent_video_studio/media/captions.py`, `src/agent_video_studio/media/thumbnails.py`, `src/agent_video_studio/media/export.py`.
- [ ] Task 13: Batch render, cancellation, history, and job recovery.
  - Acceptance: jobs expose progress and can resume/retry/cancel without corrupting sources.
  - Verify: interrupt a local render and resume/retry from saved state.
  - Dependencies: Tasks 4, 11, and 12.
  - Files: `src/agent_video_studio/core/worker.py`, `src/agent_video_studio/media/render.py`, `src/agent_video_studio/core/jobs.py`.

## Phase 4 — Operator and agent surfaces

- [ ] Task 14: REST API for projects, providers, jobs, scripts, highlights, rendering, and export.
  - Acceptance: all core operations use shared application services and validated schemas.
  - Verify: inspect API schema and exercise a complete project flow.
  - Dependencies: Tasks 3–13.
  - Files: `src/agent_video_studio/api/app.py`, `src/agent_video_studio/api/routes.py`, `src/agent_video_studio/api/schemas.py`, `src/agent_video_studio/api/dependencies.py`.
- [ ] Task 15: Browser workspace with project creation, editing, preview, progress, and export.
  - Acceptance: prompt-to-video and repurposing paths are operable from the browser.
  - Verify: browser walkthrough from project start through export download.
  - Dependencies: Task 14.
  - Files: `src/agent_video_studio/web/index.html`, `src/agent_video_studio/web/app.js`, `src/agent_video_studio/web/styles.css`, `src/agent_video_studio/api/app.py`.
- [ ] Task 16: CLI project parity, export/publishing commands, and diagnostics.
  - Acceptance: key project, provider, render, and export operations are scriptable.
  - Verify: run documented command help and a local project flow.
  - Dependencies: Tasks 3–14.
  - Files: `src/agent_video_studio/cli.py`, `src/agent_video_studio/commands/projects.py`, `src/agent_video_studio/commands/providers.py`, `src/agent_video_studio/commands/system.py`.
- [ ] Task 17: MCP tools and Claude/Codex connection examples.
  - Acceptance: bounded MCP tools call shared services over stdio; publishing requires a separate confirmation.
  - Verify: inspect tool schemas and execute a local safe project flow through MCP.
  - Dependencies: Tasks 14–16.
  - Files: `src/agent_video_studio/mcp/server.py`, `src/agent_video_studio/mcp/tools.py`, `docs/AGENTS.md`, `docs/MCP.md`.

## Phase 5 — Publishing and release

- [ ] Task 18: Publishing preflight, metadata, and delivery tracking.
  - Acceptance: every upload displays destination, account, media, caption, and visibility before confirmation.
  - Verify: mock preflight and confirmation-gated state transition.
  - Dependencies: Tasks 3 and 12.
  - Files: `src/agent_video_studio/publishing/base.py`, `src/agent_video_studio/publishing/models.py`, `src/agent_video_studio/publishing/service.py`, `src/agent_video_studio/web/app.js`.
- [ ] Task 19: YouTube upload adapter.
  - Acceptance: configured OAuth client can upload with explicit privacy and metadata options.
  - Verify: mocked upload and documented private/test-account path.
  - Dependencies: Task 18.
  - Files: `src/agent_video_studio/publishing/youtube.py`, `src/agent_video_studio/publishing/oauth.py`, `docs/PUBLISHING.md`.
- [ ] Task 20: TikTok and Instagram adapters.
  - Acceptance: supported direct-post flows validate OAuth, app approval, and public-media prerequisites.
  - Verify: mocked API protocol flows; no live public post during development.
  - Dependencies: Task 18.
  - Files: `src/agent_video_studio/publishing/tiktok.py`, `src/agent_video_studio/publishing/instagram.py`, `src/agent_video_studio/publishing/preflight.py`.
- [ ] Task 21: Bilingual install, provider, privacy, and troubleshooting documentation.
  - Acceptance: clean setup guidance covers Windows/macOS/Linux, local and remote providers, and agent clients.
  - Verify: follow installation guide in a clean environment.
  - Dependencies: Tasks 1–20.
  - Files: `README.md`, `docs/INSTALLATION.md`, `docs/PROVIDERS.md`, `docs/PRIVACY.md`.
- [ ] Task 22: Contribution, license, changelog, and release checklist.
  - Acceptance: contribution standards and version/release notes match implemented capabilities; v0.1.0 remains untagged until complete.
  - Verify: review repository metadata and release checklist.
  - Dependencies: Tasks 1–21.
  - Files: `LICENSE`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `CHANGELOG.md`, `.gitignore`.

## Final checkpoint — 0.1.0

- [ ] All module specs' success criteria are satisfied.
- [ ] No release tag is created until the feature-complete checklist is met.
\n