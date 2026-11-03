from __future__ import annotations

import os
from typing import Any

from agent_video_studio.config import Settings
from agent_video_studio.providers.anthropic import AnthropicProvider
from agent_video_studio.providers.base import ProviderError, TextProvider
from agent_video_studio.providers.openai_compatible import OpenAICompatibleProvider
from agent_video_studio.providers.presets import TEXT_PRESETS


class ProviderRegistry:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def text(self) -> TextProvider:
        provider_id = self.settings.text_provider
        if provider_id == "anthropic":
            return AnthropicProvider(
                api_key=self.settings.anthropic_api_key,
                model=self.settings.text_model,
            )
        preset = TEXT_PRESETS.get(provider_id)
        if preset is None:
            raise ProviderError(
                f"Unknown text provider '{provider_id}'. Choose deepseek, openai, openrouter, "
                "ollama, anthropic, or custom."
            )
        api_key = self._api_key_for(provider_id, preset.env_key)
        base_url = self.settings.text_base_url or preset.base_url
        model = self.settings.text_model or preset.default_model
        if provider_id == "ollama" and not api_key:
            api_key = "ollama-local"
        return OpenAICompatibleProvider(
            provider_id=provider_id,
            api_key=api_key,
            model=model,
            base_url=base_url,
        )

    def list_status(self) -> list[dict[str, Any]]:
        configured = self.settings.text_provider
        statuses: list[dict[str, Any]] = []
        for provider_id, preset in TEXT_PRESETS.items():
            key = self._api_key_for(provider_id, preset.env_key)
            if provider_id == "ollama" and not key:
                configured_key = True
            else:
                configured_key = bool(key)
            model_configured = bool(self.settings.text_model or preset.default_model)
            if provider_id == "anthropic":
                configured_key = bool(self.settings.anthropic_api_key)
                model_configured = bool(self.settings.text_model)
            statuses.append(
                {
                    "id": provider_id,
                    "label": preset.label,
                    "configured": provider_id == configured and configured_key and model_configured,
                    "selected": provider_id == configured,
                    "requires_key": provider_id != "ollama",
                    "base_url": self.settings.text_base_url or preset.base_url,
                }
            )
        return statuses

    def _api_key_for(self, provider_id: str, env_key: str) -> str:
        keys = {
            "deepseek": self.settings.deepseek_api_key,
            "openai": self.settings.openai_api_key,
            "openrouter": os.getenv("OPENROUTER_API_KEY", ""),
            "ollama": os.getenv("OLLAMA_API_KEY", ""),
            "custom": os.getenv("AVS_TEXT_API_KEY", ""),
        }
        return keys.get(provider_id, os.getenv(env_key, ""))
