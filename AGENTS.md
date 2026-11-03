# Repository guidance

- Read `SPEC.md`, `CAPABILITY_MAP.md`, and the affected module spec before changing product boundaries.
- Keep provider keys and media out of source control. Add new configuration keys to `.env.example` and both provider guides.
- Keep all media inside `AVS_DATA_DIR` and use `PathPolicy` for managed paths.
- Invoke FFmpeg with argument arrays, never shell command strings.
- Preserve source timecodes and editable project data across repurposing, rendering, and export.
- Keep web, CLI, REST, and MCP behavior on shared application services.
- External publishing must show a platform preflight and require an explicit confirmation.
- Do not tag `0.1.0` until the full release checklist in `tasks/todo.md` is complete.
\n