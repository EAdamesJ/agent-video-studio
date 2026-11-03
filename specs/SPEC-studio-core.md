# Module Spec: `studio-core`

## Objective

Own project, asset, scene, timeline, job, local-storage, and configuration contracts. This module is the system of record for every other capability.

## Commands

```powershell
python -m pip install -e ".[mcp]"
agent-video-studio doctor
agent-video-studio project create --title "Example" --mode prompt
```

## Project structure

`src/agent_video_studio/core/` contains domain models, SQLite repository, job runner, path policy, and configuration. Persistent data lives beneath the configured data root, separate from source code.

## Code style

Use typed domain objects and repository interfaces. Persist UTC timestamps and explicit status values; never store API keys in project rows.

## Testing strategy

Plan unit coverage for project transitions, path validation, job recovery, and SQLite repositories in `tests/core/`; no database or external provider is required.

## Boundaries

- Always: keep project IDs stable, validate media paths, and support interrupted-job recovery.
- Ask first: add multi-user identity or move default storage to a hosted service.
- Never: trust a client-supplied output path or serialize secrets into project exports.

## Success criteria

- Projects persist across restarts with prompt, source, scene/timeline, provider selection, exports, and status.
- Jobs have queued/running/failed/completed states, timestamps, progress, and actionable safe errors.
- Local assets have stable IDs, metadata, MIME type, file size, and managed paths under the data root.
