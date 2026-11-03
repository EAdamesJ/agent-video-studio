# Privacy and security

Agent Video Studio is designed for a single local operator. Project metadata and media are stored in the configured data directory. The local API binds to loopback by default and has no multi-user authentication in version 0.1.

## Data handling

- Source files are copied into the project data directory; originals are not edited.
- Provider credentials are read from `.env` or the operator environment and are never returned by the provider-status API.
- OAuth credentials and refresh tokens are stored under the local `credentials/` directory.
- Export bundles omit managed absolute file paths and provider credentials.
- A remote service is only called by the provider selected for that operation. No silent fallback is performed.

## Agent access

MCP tools are intentionally bounded to project operations. `import_media` accepts paths only within `AVS_DATA_DIR`. Rendering uses FFmpeg argument arrays; arbitrary shell text is not accepted as an operation.

Publishing calls send video/metadata to a social network and require a separate `confirm=true` request after reviewing the post. Use each host's tool approval controls as an additional review step.

## Network deployment

Keep `AVS_HOST=127.0.0.1` for local use. If remote access is needed, put the server behind a TLS endpoint with authentication and network access controls. Do not expose raw local API routes to the public internet.

Instagram direct publishing requires the rendered MP4 to be reachable from Meta over public HTTPS. The configured public origin exposes that export while Meta fetches it; avoid using it for media that should remain private.
