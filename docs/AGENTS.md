# Agent developer notes

- Read `SPEC.md` and `CAPABILITY_MAP.md` before changing module boundaries.
- Keep text, transcription, speech, stock, generated media, and publishing behind their module contracts in `specs/`.
- Do not add automatic provider fallbacks or upload user media without selection and consent.
- MCP tools must use shared application services and should not expose arbitrary filesystem, shell, or network controls.
- Preserve source timestamps and editable timeline data through rendering/export.
- Use FFmpeg argument arrays and keep managed files under the configured data directory.
- Publishing must retain the explicit confirmation gate and preflight checks.
