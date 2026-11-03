# Providers

Provider credentials stay on the operator's machine. Configure `.env`, restart the server, then check **Model provider** in the project workspace or run `avs providers`.

## Text models

### DeepSeek

```dotenv
AVS_TEXT_PROVIDER=deepseek
AVS_TEXT_MODEL=deepseek-flash
DEEPSEEK_API_KEY=...
```

DeepSeek documents an OpenAI-compatible API at `https://api.deepseek.com`; the adapter uses that compatibility surface. Model identifiers may change, so use the current value from [DeepSeek API docs](https://api-docs.deepseek.com/guides/codex).

### Anthropic Claude

```dotenv
AVS_TEXT_PROVIDER=anthropic
AVS_TEXT_MODEL=<current Anthropic model id>
ANTHROPIC_API_KEY=...
```

### OpenAI

```dotenv
AVS_TEXT_PROVIDER=openai
AVS_TEXT_MODEL=<current OpenAI model id>
OPENAI_API_KEY=...
```

### Other OpenAI-compatible endpoints

DeepSeek, OpenRouter, Ollama, and compatible gateways use the same adapter. Choose one of `deepseek`, `openrouter`, `ollama`, `openai`, or `custom` for `AVS_TEXT_PROVIDER`. Set `AVS_TEXT_BASE_URL` to override the default endpoint and set the matching key variable. Ollama can run without a key on loopback.

```dotenv
AVS_TEXT_PROVIDER=custom
AVS_TEXT_BASE_URL=https://your-compatible-endpoint.example/v1
AVS_TEXT_MODEL=your-model-id
AVS_TEXT_API_KEY=...
```

The adapter targets chat completions and normalizes model output into the project schema. Provider-specific tool calling is not required for script generation.

## Transcription

Local transcription is selected by default:

```dotenv
AVS_TRANSCRIPTION_PROVIDER=local
```

Install `agent-video-studio[transcription]`. The model runs on the operator's machine after its weights are downloaded. For remote OpenAI transcription:

```dotenv
AVS_TRANSCRIPTION_PROVIDER=openai
OPENAI_API_KEY=...
```

Remote transcription sends the selected source audio to OpenAI. The app does not switch providers silently.

## Narration

The app supports Edge TTS and ElevenLabs. Select the adapter in `.env`; the **Voiceover** option controls whether narration text is sent for synthesis. Repurposed clips preserve source audio when available.

Edge TTS requires `agent-video-studio[speech]` and uses the selected output language:

```dotenv
AVS_TTS_PROVIDER=edge
```

ElevenLabs uses the direct [text-to-speech API](https://elevenlabs.io/docs/api-reference/text-to-speech/convert):

```dotenv
AVS_TTS_PROVIDER=elevenlabs
ELEVENLABS_API_KEY=...
ELEVENLABS_VOICE_ID=...
ELEVENLABS_MODEL_ID=eleven_multilingual_v2
```

This is an online, usage-billed provider. Check your account's current rate limits, model language support, and voice rights before rendering.

## Stock media

Set one or both keys to enable stock footage search:

```dotenv
PEXELS_API_KEY=...
PIXABAY_API_KEY=...
```

Each selected asset retains its provider, creator, source page, and search phrase when available. Review the source provider's current license and attribution requirements before using media commercially.

## Generated media

Image and video generation providers implement the `GeneratedMediaProvider` interface in `providers/generated_media.py`. The base package does not silently select a paid generation service; each concrete integration must be configured and selected explicitly.

## Privacy and costs

- Local FFmpeg composition does not upload video files.
- Remote text generation sends the brief and the exact context used in the prompt.
- Remote transcription/speech/stock services receive the media or text needed for that operation.
- Provider errors are redacted and no automatic fallback sends the same content to another service.
- Prices, retention, and model availability depend on the provider; review their current terms before enabling them.

\n