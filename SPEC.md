# Spec: Agent Video Studio 0.1.0

## Objective

Build a complete, self-hosted AI video studio for creators and developers. It supports two complete content paths: create a video from a brief/script, and repurpose owned long-form audio/video into short clips. A shared engine powers the web workspace, CLI, REST API, and MCP tools so Claude, Codex, DeepSeek-powered agents, and other compatible clients can operate the same projects.

Success means an operator can install the app, configure providers, create or import a project, review and edit its script/timeline, render the requested formats, and export or publish the result without switching to a separate editing pipeline.

## Assumptions

1. Version 0.1.0 is a self-hosted, local-first product for one operator/workspace; multi-tenant SaaS accounts are outside this release.
2. The operator supplies credentials and media rights. No API keys or sample user media are committed.
3. English and Spanish are first-class UI/content languages; the architecture supports additional languages.
4. Platform publishing depends on each platform's OAuth, API access, account type, and review status. Export must remain useful when those are unavailable.
5. Models and media services are replaceable adapters; the project format must not depend on one vendor.

## Capability map

See [`CAPABILITY_MAP.md`](CAPABILITY_MAP.md). Its seven modules define the approved boundaries and build order.

## Tech stack

- Python 3.11+; FastAPI, Pydantic, SQLite, Typer, `httpx`, and the official MCP Python SDK.
- FFmpeg/ffprobe as external media executables.
- Browser UI served by FastAPI from static HTML, CSS, and JavaScript; no separate frontend build is required for self-hosting.
- Local filesystem storage with a configurable data root; SQLite stores projects, assets, providers, and job state.
- Model adapters: Anthropic Messages and OpenAI-compatible chat APIs (including DeepSeek's documented compatible endpoint); generic custom base URLs.
- Optional media adapters: local Whisper-compatible transcription, Edge/OpenAI/ElevenLabs TTS, Pexels/Pixabay stock media, and generated-image/video providers through explicit adapters.

Dependencies use bounded compatible ranges in `pyproject.toml`; external services stay optional and are configured by environment variables or the local settings UI.

## Commands

```powershell
# Install
python -m pip install -e ".[mcp]"

# Start the web application and REST API
agent-video-studio serve --host 127.0.0.1 --port 8787

# Start the MCP server over stdio for Claude/Codex-compatible clients
agent-video-studio mcp

# Inspect providers and system prerequisites
agent-video-studio doctor
agent-video-studio providers

# Create and operate projects
agent-video-studio project create --title "Launch video" --mode prompt
agent-video-studio project list

# Development entry point
python -m agent_video_studio
```

FFmpeg must be available on `PATH` for rendering. Optional provider setup and container installation are documented in `docs/INSTALLATION.md`.

## Project structure

```text
src/agent_video_studio/       Application package
  api/                        REST routes and request models
  providers/                  LLM, speech, transcription, and media adapters
  media/                      Ingest, timeline, FFmpeg render, captions, export
  mcp/                        MCP tools and host examples
  core/                       Projects, persistence, config, jobs, storage
web/                          Browser application assets
specs/                        Product and capability specifications
tasks/                        Implementation plan and task state
docs/                         Installation, providers, agents, publishing, security
```

## Code style

- Use typed Python 3.11+ APIs, small modules, explicit provider interfaces, and Pydantic models at boundaries.
- Use `snake_case` for Python modules/functions, `PascalCase` for types, and stable kebab-case module IDs.
- Raise actionable domain errors; do not leak provider responses, secrets, or local absolute paths into agent-facing errors.
- Avoid shell interpolation for media commands: pass FFmpeg arguments as an argument list and validate paths, durations, and output formats.

```python
async def create_script(project_id: str, request: ScriptRequest) -> ScriptDocument:
    project = await projects.require(project_id)
    provider = providers.require_text_provider(request.provider_id)
    script = await provider.create_script(project.brief, request.options)
    return await projects.save_script(project_id, script)
```

## Testing strategy

The repository's planned test layout is `tests/`: unit tests for project/timeline logic and provider contracts, integration tests for SQLite and FFmpeg workflows using tiny generated fixtures, and MCP/API contract tests. Provider-network tests must be opt-in and use test credentials. No test should require a paid provider or publish externally.

## Boundaries

- **Always:** validate uploaded paths and media metadata; keep secrets outside commits and project exports; require confirmation before external publishing; make provider/network use visible; preserve the project timeline and source timestamps.
- **Ask first:** introduce hosted multi-tenant accounts, change license, store media remotely by default, or add a paid provider as a hard dependency.
- **Never:** publish without user consent; execute user-provided shell text; upload source media to a provider without selecting that provider; commit credentials, private media, or generated render artifacts.

## Success criteria

1. A clean install starts the web app, REST API, CLI, and stdio MCP server from documented commands.
2. A project can be created from a brief, scripted into scenes, reviewed, assigned media/voice/captions, rendered by FFmpeg, and exported as MP4 plus project metadata.
3. An uploaded source video/audio file can be transcribed, segmented into candidate highlights with source timestamps, edited as clips, and rendered in 9:16, 16:9, and 1:1.
4. Text, transcription, speech, and stock-media providers are selectable through adapters; DeepSeek and Anthropic have documented configuration paths.
5. Web, CLI, REST, and MCP surfaces call the same application services and share project/job state.
6. Export packages include video, captions, thumbnail, title/description/hashtags, and editable project data. Platform connectors expose prerequisites and only publish after explicit confirmation.
7. English and Spanish setup/product documentation describes requirements, provider setup, privacy, troubleshooting, and contribution workflow.

## External references

- MCP Python SDK (official): <https://py.sdk.modelcontextprotocol.io/>
- Codex MCP connections (official): <https://developers.openai.com/api/docs/guides/agents-api/tools/mcp>
- Anthropic MCP documentation (official): <https://docs.anthropic.com/en/docs/mcp>
- DeepSeek API compatibility (official): <https://api-docs.deepseek.com/guides/codex>
- YouTube video upload API (official): <https://developers.google.com/youtube/v3/docs/videos/insert>
- TikTok Content Posting API (official): <https://developers.tiktok.com/docs/en/content-posting-api-reference-direct-post>

## Open questions

- The repository owner has not supplied product branding, so `agent-video-studio` is the working product/repository name.
- OAuth client registrations and review approvals for social networks must be supplied by operators; code cannot grant platform permissions.
