# Installation

Agent Video Studio is a self-hosted Python application. The browser workspace, REST API, CLI, and MCP server run locally and share one SQLite project store.

## Requirements

- Python 3.11 or newer.
- FFmpeg and ffprobe available on `PATH`.
- A provider API key only for the remote services you choose. Local transcription and FFmpeg rendering do not require a model API key.

## Windows PowerShell

```powershell
git clone https://github.com/EAdamesJ/agent-video-studio.git
Set-Location agent-video-studio
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[all]"
Copy-Item .env.example .env
```

Edit `.env` with the provider settings you want, then start the app:

```powershell
avs doctor
avs serve
```

Open <http://127.0.0.1:8787>.

## macOS / Linux

Install Python 3.11+ and FFmpeg with the package manager for your system, then:

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

## Optional install profiles

```bash
python -m pip install -e .                  # Web/API/CLI, no local ML or MCP extras
python -m pip install -e '.[mcp]'            # Add the MCP server
python -m pip install -e '.[transcription]'  # Add local faster-whisper transcription
python -m pip install -e '.[speech]'         # Add Edge TTS narration
python -m pip install -e '.[youtube]'        # Add YouTube OAuth/upload support
python -m pip install -e '.[all]'            # Add all packaged optional integrations
```

`faster-whisper` downloads its selected model the first time it runs. The `small` model is the default; select a different model in the analysis operation if your machine needs another quality/speed tradeoff.

## Data location

By default the app stores SQLite data, projects, uploaded files, renders, exports, and OAuth credentials in `~/.agent-video-studio/` (`%USERPROFILE%\.agent-video-studio` on Windows). Set `AVS_DATA_DIR` to choose another directory. Source files are copied into the managed project directory; originals are left untouched.

## Network access

The web/API server binds to `127.0.0.1` by default. The local API does not include multi-user authentication in 0.1. Do not bind it to a public or shared network without placing it behind an authenticated reverse proxy. MCP stdio is the recommended local agent connection.

## Troubleshooting

- `avs doctor` reports `ffmpeg` or `ffprobe` missing: install FFmpeg and restart the terminal so PATH updates are visible.
- No text provider configured: set `AVS_TEXT_PROVIDER`, its API key, and `AVS_TEXT_MODEL` in `.env`.
- Local transcription asks for an optional package: install `.[transcription]` or set `AVS_TRANSCRIPTION_PROVIDER=openai` and configure `OPENAI_API_KEY`.
- The app cannot see a newly edited `.env`: restart `avs serve`; `.env` is loaded when the process starts.
- MCP startup fails: install `.[mcp]` into the same Python environment used by the configured command.

\n