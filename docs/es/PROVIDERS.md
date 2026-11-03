# Proveedores

Las claves permanecen en el equipo del operador. Configura `.env`, reinicia el servidor y comprueba el estado con `avs providers` o `avs doctor`.

## Modelos de texto

DeepSeek, Claude (Anthropic), OpenAI, OpenRouter, Ollama y endpoints compatibles se configuran mediante `AVS_TEXT_PROVIDER`, `AVS_TEXT_MODEL` y la clave del proveedor. Para una URL compatible propia, usa `AVS_TEXT_PROVIDER=custom`, `AVS_TEXT_BASE_URL` y `AVS_TEXT_API_KEY`.

```dotenv
AVS_TEXT_PROVIDER=deepseek
AVS_TEXT_MODEL=deepseek-flash
DEEPSEEK_API_KEY=...
```

Consulta [`PROVIDERS.md`](../PROVIDERS.md) para más ejemplos y los requisitos de Ollama.

## Transcripción

Por defecto se usa Whisper local. Instala `agent-video-studio[transcription]`. También puedes seleccionar la API de OpenAI con `AVS_TRANSCRIPTION_PROVIDER=openai` y `OPENAI_API_KEY`; esto envía el audio elegido a OpenAI.

## Narración

Elige `AVS_TTS_PROVIDER=edge` o `elevenlabs`. Edge requiere `.[speech]`. ElevenLabs requiere `ELEVENLABS_API_KEY`, `ELEVENLABS_VOICE_ID` y, opcionalmente, `ELEVENLABS_MODEL_ID`. La opción **Voz en off** controla si se envía texto para sintetizar voz.

## Stock y medios generados

Define `PEXELS_API_KEY` o `PIXABAY_API_KEY` para habilitar búsqueda de videos de stock. Revisa licencia y atribución en el proveedor antes de uso comercial. Los proveedores concretos de imagen/video generados se añaden mediante la interfaz documentada en `providers/generated_media.py`; no se activa un servicio de pago automáticamente.

## Privacidad y costos

- FFmpeg procesa los archivos localmente.
- El proveedor de texto recibe el brief y el contexto usado para generar el resultado.
- La transcripción, la voz y la búsqueda de stock solo contactan los servicios seleccionados para esa operación.
- No hay cambio silencioso de proveedor. Tarifas, retención y disponibilidad dependen del servicio configurado.
\n