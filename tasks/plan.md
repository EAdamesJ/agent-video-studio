# Implementation Plan: Agent Video Studio 0.1.0

## Overview

Implement the approved seven-module capability map as a complete local-first application: shared project engine, provider adapters, prompt-to-video and long-form repurposing flows, FFmpeg renderer, web/CLI/API/MCP surfaces, and export/publishing adapters.

## Architecture decisions

- One Python service plus static browser assets and a durable SQLite job queue keeps local installation practical while preserving stable API/MCP contracts.
- SQLite/filesystem are the default; provider and platform clients are optional adapters.
- Rendering uses FFmpeg through argument arrays and an intermediate timeline model.
- MCP uses the official Python SDK; stdio is the first-run connection for local Claude/Codex, with Streamable HTTP available for remote hosts.
- Social publishing is a separate, explicitly confirmed action; platform audits/OAuth remain operator prerequisites.
- 0.1.0 is feature-complete across the agreed workflow. Development is sliced vertically; this does not reduce release scope.

## Ordered task list

The ordered implementation checklist is [`todo.md`](todo.md), tasks 1–22. Tasks follow module dependencies and stay scoped to small vertical slices. This plan is the architecture/risk companion; the task file is the execution tracker.

## Checkpoints

- **Foundation:** project/job data persists; CLI and API share the domain service.
- **Content workflows:** prompt and source-media projects both produce editable, timestamped timelines.
- **Production:** timeline renders and export includes all expected files.
- **Agent surfaces:** same operations are available through web, CLI, REST, and MCP with tool boundaries.
- **Release:** setup docs, provider matrix, publishing prerequisites, and clean repository metadata agree.

## Risks and mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Social APIs require OAuth scopes, app review, or domain ownership | Direct publishing may not be available to every installer | Keep export complete, expose preflight requirements, isolate platform adapters |
| Remote provider APIs differ and change | Provider failures or migration cost | Narrow contracts, explicit presets, custom compatible endpoint, no silent fallbacks |
| FFmpeg/media files are large and platform-specific | Slow jobs and storage pressure | Durable job state, cancellation, managed work dirs, clear disk estimates |
| AI output can be inaccurate or mismatched | Poor-quality clips/videos | Editable scripts/timelines, source timestamps, review gates, user-selected providers |
| Full suite is large | Incomplete public release | Track capabilities against module specs and do not tag 0.1.0 until each success criterion is met |

## Task list

Detailed checkboxes live in [`todo.md`](todo.md) and map to these phases and module specs.

## Open questions

- Repository/product name is provisionally `agent-video-studio`; revise before a 1.0 brand commitment if needed.
- Social OAuth registrations and platform reviews require the repository owner/operator.
