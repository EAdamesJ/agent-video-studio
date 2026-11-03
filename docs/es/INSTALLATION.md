# Instalación

Agent Video Studio es una aplicación autoalojada de Python. La interfaz web, la API REST, la CLI y el servidor MCP comparten SQLite y los archivos locales del proyecto.

## Requisitos

- Python 3.11 o posterior.
- FFmpeg y ffprobe disponibles en `PATH`.
- Claves de API solo para los servicios remotos que decidas usar.

## Windows PowerShell

```powershell
git clone https://github.com/EAdamesJ/agent-video-studio.git
Set-Location agent-video-studio
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[all]"
Copy-Item .env.example .env
avs doctor
avs serve
```

Abre <http://127.0.0.1:8787>.

## macOS y Linux

Instala Python 3.11+ y FFmpeg con el gestor de paquetes de tu sistema. Después:

```bash
git clone https://github.com/EAdamesJ/agent-video-studio.git
cd agent-video-studio
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e '.[all]'
cp .env.example .env
avs doctor
avs serve
```

## Perfiles opcionales

```bash
python -m pip install -e .                   # Web, API y CLI
python -m pip install -e '.[mcp]'            # Integración MCP
python -m pip install -e '.[transcription]'  # Whisper local
python -m pip install -e '.[speech]'         # Edge TTS
python -m pip install -e '.[youtube]'        # OAuth y carga a YouTube
python -m pip install -e '.[all]'            # Integraciones empaquetadas
```

Edita `.env` antes de reiniciar el servidor. La guía de [proveedores](PROVIDERS.md) explica modelos, voz y transcripción.

## Datos y red

Los datos se guardan por defecto en `~/.agent-video-studio/` (en Windows, `%USERPROFILE%\.agent-video-studio`). Usa `AVS_DATA_DIR` para cambiar la ubicación. El proceso escucha en `127.0.0.1`; no lo expongas a una red pública sin autenticación, TLS y controles de acceso delante de la aplicación.

## Solución de problemas

- Si falta FFmpeg o ffprobe, instala FFmpeg y reinicia la terminal para actualizar `PATH`.
- Si no hay proveedor de texto, configura `AVS_TEXT_PROVIDER`, su clave y `AVS_TEXT_MODEL`.
- Para transcripción local, instala `.[transcription]`; la primera ejecución descarga el modelo.
- Si MCP no inicia, instala `.[mcp]` en el mismo entorno Python usado por el agente.
\n