# Configuración MCP

El servidor MCP usa los mismos proyectos y servicios que la aplicación. Acepta conexiones por stdio o Streamable HTTP.

Instala las dependencias:

```bash
python -m pip install -e '.[mcp,transcription,speech]'
```

Configura las claves en `.env` en el entorno del proceso MCP. Para medios, importa primero los archivos al directorio de datos de la aplicación.

Para un endpoint HTTP local, inicia `avs mcp --transport streamable-http --host 127.0.0.1 --port 8788` y conecta el cliente a `http://127.0.0.1:8788/mcp`. Mantén loopback a menos que protejas el endpoint detrás de TLS y autenticación.

## Claude Code

```bash
claude mcp add --transport stdio agent-video-studio -- agent-video-studio mcp
claude mcp list
```

## Codex

Añade a `~/.codex/config.toml`:

```toml
[mcp_servers.agent_video_studio]
command = "agent-video-studio"
args = ["mcp"]
```

## Claude Desktop

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

El servidor ofrece herramientas de proyectos, guiones, importación, análisis, selección de clips, edición, render, estado de proveedores y preflight de publicación. `publish_export` solo debe llamarse con `confirm=true` después de revisar el post. El cliente MCP compatible se debe configurar por separado; este proyecto no afirma que DeepSeek aloje servidores MCP.
\n