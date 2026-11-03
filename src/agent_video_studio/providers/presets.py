from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ProviderPreset:
    id: str
    label: str
    base_url: str
    env_key: str
    default_model: str = ""


TEXT_PRESETS = {
    "deepseek": ProviderPreset(
        "deepseek", "DeepSeek", "https://api.deepseek.com", "DEEPSEEK_API_KEY", "deepseek-flash"
    ),
    "openai": ProviderPreset(
        "openai", "OpenAI", "https://api.openai.com/v1", "OPENAI_API_KEY", ""
    ),
    "openrouter": ProviderPreset(
        "openrouter", "OpenRouter", "https://openrouter.ai/api/v1", "OPENROUTER_API_KEY", ""
    ),
    "ollama": ProviderPreset(
        "ollama", "Ollama", "http://127.0.0.1:11434/v1", "OLLAMA_API_KEY", ""
    ),
    "anthropic": ProviderPreset(
        "anthropic", "Anthropic Claude", "https://api.anthropic.com", "ANTHROPIC_API_KEY", ""
    ),
    "custom": ProviderPreset("custom", "OpenAI-compatible custom endpoint", "", "AVS_TEXT_API_KEY", ""),
}
