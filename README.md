<div align="center">

# Agent Video Studio

**One video engine. Two workflows. Any agent.**

Create short videos from an idea, or turn long-form media into timestamped clips. Operate the same projects from a web workspace, CLI, API, or MCP client.

[English](#english) · [Español](#español) · [Roadmap](tasks/plan.md) · [Contributing](CONTRIBUTING.md)

</div>

> **Status:** Version 0.1.0 is in active development. The full intended release scope is documented in [`SPEC.md`](SPEC.md). No release tag has been published.

## English

Agent Video Studio is an open-source, self-hosted workspace for end-to-end AI-assisted video creation and repurposing. Its project format is provider-neutral, and the web app, CLI, REST API, and MCP server share one engine.

### Two complete content paths

1. **Idea to video:** brief → script → storyboard → voice and visuals → captions and music → editable timeline → rendered formats.
2. **Long-form to clips:** supplied video/audio → transcript → explained highlight candidates with source timestamps → reviewed vertical clips → export package.

### Designed for agents and people

- Connect Claude and Codex through MCP; use DeepSeek, Anthropic Claude, OpenAI-compatible endpoints, or another configured provider for model work.
- Review and edit scripts, clip boundaries, scene assets, captions, audio, and final metadata before export.
- Render with FFmpeg to 9:16, 16:9, and 1:1 layouts.
- Keep a local project history and export MP4, SRT/VTT, thumbnails, metadata, and editable project data.
- Add authorized publishing integrations for YouTube, Instagram, and TikTok. Every external post requires a separate confirmation.

### 0.1.0 scope

The first public release is intended to include the full creation and repurposing workflows, provider adapters, durable jobs, responsive web workspace, CLI, REST API, MCP tools, export bundles, and supported publishing adapters. See the [approved capability map](CAPABILITY_MAP.md) and [module specifications](specs/).

### Development setup

Requirements and exact setup commands will be maintained in [`docs/INSTALLATION.md`](docs/INSTALLATION.md). FFmpeg is required for media rendering; remote model, stock-media, and publishing services are optional and require operator credentials.

## Español

Agent Video Studio es un espacio de trabajo de código abierto y autoalojado para crear videos con IA y reutilizar contenido largo. Su formato de proyecto no depende de un proveedor, y la aplicación web, la CLI, la API REST y el servidor MCP comparten el mismo motor.

### Dos flujos completos

1. **Idea a video:** brief → guion → storyboard → voz e imágenes → subtítulos y música → timeline editable → render en varios formatos.
2. **Video largo a clips:** video/audio suministrado → transcripción → momentos sugeridos con marcas de tiempo → clips verticales revisables → paquete de exportación.

Claude y Codex podrán controlar proyectos mediante MCP. DeepSeek, Claude, OpenAI y endpoints compatibles se conectarán como proveedores de modelos. Antes de exportar, el usuario podrá revisar y modificar cortes, escenas, texto, voz, subtítulos y metadatos.

La versión 0.1.0 cubrirá el flujo completo acordado. El estado actual y los criterios de salida están en [`SPEC.md`](SPEC.md), [`CAPABILITY_MAP.md`](CAPABILITY_MAP.md) y [`tasks/todo.md`](tasks/todo.md).

## Architecture

```text
Web UI ─┐
CLI ────┼── Application services ── Project/Job store (SQLite + local media)
REST ───┤             │
MCP ────┘             ├── Provider hub (LLM, transcription, speech, stock/media)
                      ├── Creation and repurposing workflows
                      ├── FFmpeg timeline renderer
                      └── Export and confirmed publishing adapters
```

## License

MIT. See [`LICENSE`](LICENSE).

## Español: contribuciones

Se aceptan reportes de errores, ideas y contribuciones. Antes de abrir un PR, revisa [`CONTRIBUTING.md`](CONTRIBUTING.md) y el contrato de cada módulo en [`specs/`](specs/).
