# Module Spec: `agent-surfaces`

## Objective

Expose the same project and rendering workflows through a browser workspace, CLI, REST API, and MCP server.

## Commands

```powershell
agent-video-studio serve --host 127.0.0.1 --port 8787
agent-video-studio mcp --transport stdio
agent-video-studio mcp --transport streamable-http --host 127.0.0.1 --port 8788
agent-video-studio providers
```

## Project structure

`src/agent_video_studio/api/` contains REST routes and request schemas; `src/agent_video_studio/cli.py` the CLI; `src/agent_video_studio/mcp/` the MCP server; `src/agent_video_studio/web/` the browser application.

## Code style

All surfaces call shared application services. API/MCP errors are bounded and actionable. Tool names describe one operation, with read-only tools separated from render/publish operations.

## Testing strategy

Plan API schema and MCP tool contract checks, CLI command checks, and a browser smoke path for project creation through export.

## Boundaries

- Always: bind to loopback by default, document exposure/authentication before remote use, and limit tool file access to the configured data root.
- Ask first: enable LAN/public access or add account-level authentication.
- Never: expose admin filesystem/process tools to connected agents.

## Success criteria

- Web, CLI, REST, and MCP can list/create/edit projects, generate scripts, import media, select highlights, render, and export.
- MCP works over stdio and Streamable HTTP.
- Claude Code/Claude Desktop and Codex setup examples are provided; DeepSeek is configured as a model provider rather than incorrectly assumed to be an MCP host.
