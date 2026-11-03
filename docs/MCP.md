# MCP setup

The MCP server exposes the same project workflows used by the web app and CLI. It supports local stdio and Streamable HTTP transports through the official Python MCP SDK.

## Install and configure

```bash
python -m pip install -e '.[mcp,transcription,speech]'
```

Set model/provider keys in `.env` in the directory from which the MCP process starts. For media tools, place source files inside `AVS_DATA_DIR` and pass their managed path to `import_media`.

## Claude Code

Add the server with Claude Code's MCP command:

```bash
claude mcp add --transport stdio agent-video-studio -- agent-video-studio mcp
claude mcp list
```

If the executable is not on PATH, use the absolute path to `.venv/bin/agent-video-studio` (macOS/Linux) or `.venv\Scripts\agent-video-studio.exe` (Windows) as the command.

## Codex

Add this entry to `~/.codex/config.toml`:

```toml
[mcp_servers.agent_video_studio]
command = "agent-video-studio"
args = ["mcp"]
```

Restart Codex or reload MCP servers, then inspect available tools. If `avs` was installed into a virtual environment, set `command` to that environment's absolute executable path.

## Claude Desktop JSON configuration

In Claude Desktop's MCP server configuration, add:

```json
{
  "mcpServers": {
    "agent-video-studio": {
      "command": "agent-video-studio",
      "args": ["mcp"]
    }
  }
}
```

Use the path to the installed executable if the desktop process does not inherit the terminal PATH.

## Streamable HTTP

For a local HTTP endpoint, start `avs mcp --transport streamable-http --host 127.0.0.1 --port 8788`. Connect compatible clients to `http://127.0.0.1:8788/mcp`. Keep the loopback host unless an authenticated TLS gateway protects the endpoint; this server does not add user authentication.

## Tools

- `list_projects`, `create_project`, `get_project`
- `generate_script`, `import_media`, `analyze_media`, `select_highlights`, `edit_scene`
- `render_project`, `get_job`, `list_providers`
- `preflight_publish` to inspect platform requirements before the user confirms a post
- `publish_export` for an existing render, with an explicit `confirm=true` argument

The media import tool only reads files inside the configured app data directory. Use the web upload or CLI import command to copy a source into that directory first.

DeepSeek is a configurable model provider. An MCP client/host still needs to be supplied by a compatible application; this project does not claim that every DeepSeek product hosts MCP servers.

\n