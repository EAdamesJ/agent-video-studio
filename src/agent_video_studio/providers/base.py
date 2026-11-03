from __future__ import annotations

import json
import re
from typing import Any, Protocol


class ProviderError(RuntimeError):
    """Safe, user-facing provider error without request credentials or bodies."""


class TextProvider(Protocol):
    id: str
    model: str

    async def generate(self, system_prompt: str, user_prompt: str, *, max_tokens: int = 4000) -> str: ...


def parse_json_object(text: str) -> dict[str, Any]:
    candidate = text.strip()
    candidate = re.sub(r"^```(?:json)?\s*|\s*```$", "", candidate, flags=re.IGNORECASE)
    start, end = candidate.find("{"), candidate.rfind("}")
    if start < 0 or end <= start:
        raise ProviderError("The model returned no JSON object. Try again or change providers.")
    try:
        value = json.loads(candidate[start : end + 1])
    except json.JSONDecodeError as exc:
        raise ProviderError("The model returned invalid JSON. Try again or change providers.") from exc
    if not isinstance(value, dict):
        raise ProviderError("The model response must be a JSON object.")
    return value

\n