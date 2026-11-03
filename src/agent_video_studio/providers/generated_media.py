from __future__ import annotations

from typing import Any, Protocol


class GeneratedMediaProvider(Protocol):
    id: str

    async def generate_image(self, prompt: str, **options: Any) -> bytes: ...

    async def generate_video(self, prompt: str, **options: Any) -> bytes: ...


class GeneratedMediaRegistry:
    """Extension point for opt-in image/video generation integrations."""

    def __init__(self) -> None:
        self._providers: dict[str, GeneratedMediaProvider] = {}

    def register(self, provider: GeneratedMediaProvider) -> None:
        self._providers[provider.id] = provider

    def get(self, provider_id: str) -> GeneratedMediaProvider:
        try:
            return self._providers[provider_id]
        except KeyError as exc:
            available = ", ".join(sorted(self._providers)) or "none installed"
            raise KeyError(f"Generated-media provider '{provider_id}' is unavailable. Available: {available}.") from exc

    def list(self) -> list[str]:
        return sorted(self._providers)
