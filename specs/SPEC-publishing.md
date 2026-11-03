# Module Spec: `publishing`

## Objective

Prepare complete distribution packages and provide authorized upload adapters for supported platforms.

## Commands

```powershell
agent-video-studio project preflight-publish <project-id> <render-id> 9:16
agent-video-studio project publish <project-id> <render-id> 9:16 --platform youtube --title "Launch" --confirm
```

## Project structure

`src/agent_video_studio/publishing/` contains export presets, platform metadata, OAuth token abstractions, upload clients, and delivery status tracking.

## Code style

Platform adapters expose capability discovery and preflight validation. Publishing requests are explicit, idempotently tracked, and never inferred from rendering.

## Testing strategy

Plan mocked OAuth/upload tests and metadata validation. Live publication is manual, opt-in, and must target a private/test account unless the operator deliberately changes privacy settings.

## Boundaries

- Always: show target account, caption, visibility, and final media before sending; retain delivery IDs and status.
- Ask first: add access scopes, change privacy defaults, or enable scheduled automated posting.
- Never: publish without a separate confirmation action or claim approval for an unaudited social app.

## Success criteria

- Export produces a platform-ready folder even when OAuth is not configured.
- YouTube, Instagram, and TikTok adapters report setup/audit requirements and support the platform's permitted upload flow when configured.
- Post metadata and user-selected visibility are validated before upload; failures do not lose the rendered project.
