from __future__ import annotations

import httpx

from agent_video_studio.providers.base import ProviderError


class OpenAICompatibleProvider:
    def __init__(
        self,
        *,
        provider_id: str,
        api_key: str,
        model: str,
        base_url: str,
        timeout_seconds: float = 90,
    ) -> None:
        if not api_key:
            raise ProviderError(f"Set the API key for '{provider_id}' before using this provider.")
        if not model:
            raise ProviderError(f"Set AVS_TEXT_MODEL for '{provider_id}'.")
        self.id = provider_id
        self.api_key = api_key
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.timeout_seconds = timeout_seconds

    async def generate(self, system_prompt: str, user_prompt: str, *, max_tokens: int = 4000) -> str:
        endpoint = self.base_url
        if endpoint.endswith("/v1"):
            endpoint = endpoint[:-3]
        url = f"{endpoint}/chat/completions"
        body = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "max_tokens": max_tokens,
            "temperature": 0.45,
        }
        try:
            async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
                response = await client.post(
                    url,
                    headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
                    json=body,
                )
                response.raise_for_status()
                data = response.json()
        except httpx.TimeoutException as exc:
            raise ProviderError(f"{self.id} timed out. Check provider status and try again.") from exc
        except httpx.HTTPStatusError as exc:
            raise ProviderError(f"{self.id} returned HTTP {exc.response.status_code}.") from exc
        except (httpx.HTTPError, ValueError) as exc:
            raise ProviderError(f"Could not reach {self.id}. Check the base URL and network.") from exc
        try:
            content = data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise ProviderError(f"{self.id} returned an unexpected chat-completions response.") from exc
        if isinstance(content, list):
            content = "\n".join(str(item.get("text", "")) for item in content if isinstance(item, dict))
        if not isinstance(content, str) or not content.strip():
            raise ProviderError(f"{self.id} returned an empty response.")
        return content.strip()
