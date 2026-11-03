# Module Spec: `provider-hub`

## Objective

Offer explicit, replaceable interfaces for text generation, transcription, speech, stock media, and generated media. Provider selection and cost/privacy implications are visible to the operator.

## Commands

```powershell
agent-video-studio providers
agent-video-studio doctor
```

## Project structure

`src/agent_video_studio/providers/` contains provider protocols, registry, configuration, and vendor implementations. Credentials are read from environment variables or the local settings store.

## Code style

Every adapter implements a narrow async interface and normalizes vendor output into internal models. Network timeouts, retry policy, and redacted errors are centralized.

## Testing strategy

Plan contract tests with mocked HTTP responses. Live provider checks are opt-in and must never publish or incur charges without a user action.

## Boundaries

- Always: expose whether processing is local or remote; redact secrets; allow a custom OpenAI-compatible URL.
- Ask first: add paid providers that require a new account or data retention change.
- Never: silently upload media or fall back to a different vendor.

## Success criteria

- Anthropic and OpenAI-compatible text adapters work from configuration; DeepSeek is a documented preset.
- Transcription, speech, stock, and generated-media interfaces can be installed or enabled independently.
- A missing credential/provider produces setup guidance instead of a silent mock response.
