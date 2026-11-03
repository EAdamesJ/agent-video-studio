# Capability Map: Agent Video Studio

## Product intent

An open-source, self-hosted AI video workspace that can create a finished video from a brief or turn owned long-form media into short clips. The same project engine is available in the web app, CLI, REST API, and MCP server so people and agents can run the same workflows.

## Approved modules

| Module id | Responsibility | Depends on |
|---|---|---|
| `studio-core` | Projects, assets, scene/timeline model, durable jobs, local storage, configuration | — |
| `provider-hub` | Model, transcription, speech, stock-media, and generated-media adapters | `studio-core` |
| `video-creation` | Brief-to-script, storyboard, voice, scene assets, and publish-ready video projects | `studio-core`, `provider-hub` |
| `video-repurposing` | Media ingest, transcription, speaker/segment analysis, highlight selection, and clip projects | `studio-core`, `provider-hub` |
| `rendering` | Timeline composition, subtitles, audio mix, aspect-ratio layouts, FFmpeg rendering, thumbnails | `studio-core`, `provider-hub` |
| `agent-surfaces` | Web app, CLI, REST API, and MCP tools using shared application services | `studio-core`, `video-creation`, `video-repurposing`, `rendering` |
| `publishing` | Export bundles, captions/metadata, scheduling data, and authorized social-platform delivery adapters | `studio-core`, `rendering`, `provider-hub` |

## Build order

`studio-core` → `provider-hub` → (`video-creation` and `video-repurposing`) → `rendering` → `agent-surfaces` → `publishing`.

`video-creation` and `video-repurposing` share provider and project contracts; their outputs converge on the same timeline and renderer. Publishing remains downstream of a completed render and always requires an explicit user action.

## Cross-cutting requirements

- Python 3.11+ service, portable local-first operation, SQLite for the single-user installation, and filesystem media storage.
- Provider credentials are supplied by environment/configuration and are never written into project exports or logs.
- Outputs are deterministic project files plus MP4 media and common caption formats.
- MCP follows the official protocol and exposes bounded actions; publishing tools require user confirmation.
- External platform credentials, audits, and app approvals remain controlled by the operator.
