from __future__ import annotations

import asyncio
from pathlib import Path
from urllib.parse import quote

import httpx

from agent_video_studio.config import Settings
from agent_video_studio.providers.base import ProviderError


class EdgeTextToSpeech:
    """Optional online TTS adapter using Microsoft's Edge speech service."""

    async def synthesize(self, text: str, destination: Path, language: str = "en") -> Path:
        try:
            import edge_tts
        except ImportError as exc:
            raise ProviderError("Install speech support with `pip install 'agent-video-studio[speech]'`.") from exc
        voice = _edge_voice(language)
        destination.parent.mkdir(parents=True, exist_ok=True)
        try:
            await edge_tts.Communicate(text=text, voice=voice).save(str(destination))
        except Exception as exc:
            raise ProviderError("Speech generation failed. Check network connectivity and the selected voice.") from exc
        if not destination.is_file() or destination.stat().st_size == 0:
            raise ProviderError("Speech provider returned an empty audio file.")
        return destination


class ElevenLabsTextToSpeech:
    """Optional ElevenLabs HTTP adapter for operator-selected narration."""

    def __init__(self, api_key: str, voice_id: str, model_id: str = "eleven_multilingual_v2") -> None:
        if not api_key:
            raise ProviderError("Set ELEVENLABS_API_KEY to use ElevenLabs narration.")
        if not voice_id:
            raise ProviderError("Set ELEVENLABS_VOICE_ID to choose an ElevenLabs voice.")
        self.api_key = api_key
        self.voice_id = voice_id
        self.model_id = model_id or "eleven_multilingual_v2"

    async def synthesize(self, text: str, destination: Path, language: str = "en") -> Path:
        del language  # The chosen ElevenLabs voice/model controls language behavior.
        destination.parent.mkdir(parents=True, exist_ok=True)
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{quote(self.voice_id, safe='')}"
        try:
            async with httpx.AsyncClient(timeout=httpx.Timeout(180, connect=20)) as client:
                response = await client.post(
                    url,
                    params={"output_format": "mp3_44100_128"},
                    headers={"xi-api-key": self.api_key, "Content-Type": "application/json"},
                    json={"text": text, "model_id": self.model_id},
                )
                response.raise_for_status()
                audio = response.content
        except httpx.TimeoutException as exc:
            raise ProviderError("ElevenLabs narration timed out.") from exc
        except httpx.HTTPStatusError as exc:
            raise ProviderError(f"ElevenLabs returned HTTP {exc.response.status_code} for speech generation.") from exc
        except httpx.HTTPError as exc:
            raise ProviderError("Could not reach ElevenLabs for speech generation.") from exc
        if not audio:
            raise ProviderError("ElevenLabs returned an empty audio file.")
        destination.write_bytes(audio)
        return destination


def build_text_to_speech(settings: Settings) -> EdgeTextToSpeech | ElevenLabsTextToSpeech:
    if settings.tts_provider == "edge":
        return EdgeTextToSpeech()
    if settings.tts_provider == "elevenlabs":
        return ElevenLabsTextToSpeech(
            settings.elevenlabs_api_key,
            settings.elevenlabs_voice_id,
            settings.elevenlabs_model_id,
        )
    raise ProviderError("Unknown TTS provider. Choose 'edge' or 'elevenlabs'.")


def _edge_voice(language: str) -> str:
    prefix = language.lower().replace("_", "-")
    voices = {
        "en": "en-US-AvaNeural",
        "es": "es-MX-DaliaNeural",
        "es-419": "es-MX-DaliaNeural",
        "es-es": "es-ES-ElviraNeural",
        "pt": "pt-BR-FranciscaNeural",
        "fr": "fr-FR-DeniseNeural",
        "de": "de-DE-KatjaNeural",
        "ja": "ja-JP-NanamiNeural",
        "zh": "zh-CN-XiaoxiaoNeural",
    }
    return voices.get(prefix, voices.get(prefix.split("-")[0], "en-US-AvaNeural"))

\n