from __future__ import annotations

import httpx

from agent_video_studio.providers.base import ProviderError


class AnthropicProvider:
    def __init__(
        self,
        *,
        api_key: str,
        model: str,
        base_url: str = "https://api.anthropic.com",
        timeout_seconds: float = 90,
    ) -> None:
        if not api_key:
            raise ProviderError("Set ANTHROPIC_API_KEY before using Claude as the text provider.")
        if not model:
            raise ProviderError("Set AVS_TEXT_MODEL to an Anthropic model name.")
        self.id = "anthropic"
        self.api_key = api_key
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.timeout_seconds = timeout_seconds

    async def generate(self, system_prompt: str, user_prompt: str, *, max_tokens: int = 4000) -> str:
        try:
            async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
                response = await client.post(
                    f"{self.base_url}/v1/messages",
                    headers={
                        "x-api-key": self.api_key,
                        "anthropic-version": "2023-06-01",
                        "content-type": "application/json",
                    },
                    json={
                        "model": self.model,
                        "max_tokens": max_tokens,
                        "system": system_prompt,
                        "messages": [{"role": "user", "content": user_prompt}],
                    },
                )
                response.raise_for_status()
                data = response.json()
        except httpx.TimeoutException as exc:
            raise ProviderError("Anthropic timed out. Check provider status and try again.") from exc
        except httpx.HTTPStatusError as exc:
            raise ProviderError(f"Anthropic returned HTTP {exc.response.status_code}.") from exc
        except (httpx.HTTPError, ValueError) as exc:
            raise ProviderError("Could not reach Anthropic. Check network and model configuration.") from exc
        try:
            parts = data["content"]
            result = "\n".join(part["text"] for part in parts if part.get("type") == "text")
        except (KeyError, TypeError) as exc:
            raise ProviderError("Anthropic returned an unexpected Messages API response.") from exc
        if not result.strip():
            raise ProviderError("Anthropic returned an empty response.")
        return result.strip()

\n