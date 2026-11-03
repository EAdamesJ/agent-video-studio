from __future__ import annotations

from typing import Any
from urllib.parse import quote, urlparse

import httpx

from agent_video_studio.config import Settings
from agent_video_studio.providers.base import ProviderError


class PexelsStockProvider:
    id = "pexels"

    def __init__(self, api_key: str) -> None:
        if not api_key:
            raise ProviderError("Set PEXELS_API_KEY to search Pexels stock footage.")
        self.api_key = api_key

    async def search_videos(self, query: str, *, orientation: str = "portrait", limit: int = 8) -> list[dict[str, Any]]:
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.get(
                    "https://api.pexels.com/videos/search",
                    headers={"Authorization": self.api_key},
                    params={"query": query, "orientation": orientation, "per_page": min(max(limit, 1), 20)},
                )
                response.raise_for_status()
                data = response.json()
        except httpx.HTTPStatusError as exc:
            raise ProviderError(f"Pexels returned HTTP {exc.response.status_code}.") from exc
        except (httpx.HTTPError, ValueError) as exc:
            raise ProviderError("Could not search Pexels. Check the API key and network.") from exc
        results = []
        for video in data.get("videos", []):
            files = [item for item in video.get("video_files", []) if item.get("link")]
            best = max(files, key=lambda item: int(item.get("width", 0)) * int(item.get("height", 0)), default=None)
            if best:
                results.append(
                    {
                        "id": str(video.get("id")),
                        "provider": self.id,
                        "duration_seconds": video.get("duration"),
                        "width": best.get("width"),
                        "height": best.get("height"),
                        "download_url": best["link"],
                        "page_url": video.get("url"),
                        "creator": video.get("user", {}).get("name"),
                        "query": query,
                    }
                )
        return results

    async def download(self, asset: dict[str, Any], destination: str) -> str:
        url = str(asset.get("download_url", ""))
        parsed = urlparse(url)
        if parsed.scheme != "https" or not (parsed.hostname or "").endswith(".pexels.com"):
            raise ProviderError("Stock media URL must use HTTPS.")
        try:
            async with httpx.AsyncClient(timeout=httpx.Timeout(180, connect=20), follow_redirects=True) as client:
                async with client.stream("GET", url) as response:
                    response.raise_for_status()
                    length = int(response.headers.get("content-length", "0") or 0)
                    if length > 500 * 1024 * 1024:
                        raise ProviderError("Selected stock footage exceeds the 500 MiB download limit.")
                    total = 0
                    with open(destination, "wb") as output:
                        async for chunk in response.aiter_bytes(1024 * 1024):
                            total += len(chunk)
                            if total > 500 * 1024 * 1024:
                                raise ProviderError("Selected stock footage exceeds the 500 MiB download limit.")
                            output.write(chunk)
        except httpx.HTTPError as exc:
            raise ProviderError("Could not download the selected Pexels media.") from exc
        return destination


class PixabayStockProvider:
    id = "pixabay"

    def __init__(self, api_key: str) -> None:
        if not api_key:
            raise ProviderError("Set PIXABAY_API_KEY to search Pixabay stock footage.")
        self.api_key = api_key

    async def search_videos(self, query: str, *, orientation: str = "vertical", limit: int = 8) -> list[dict[str, Any]]:
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.get(
                    "https://pixabay.com/api/videos/",
                    params={"key": self.api_key, "q": quote(query), "per_page": min(max(limit, 1), 20)},
                )
                response.raise_for_status()
                data = response.json()
        except httpx.HTTPStatusError as exc:
            raise ProviderError(f"Pixabay returned HTTP {exc.response.status_code}.") from exc
        except (httpx.HTTPError, ValueError) as exc:
            raise ProviderError("Could not search Pixabay. Check the API key and network.") from exc
        results = []
        for video in data.get("hits", []):
            variants = video.get("videos", {})
            best = variants.get("medium") or variants.get("small") or variants.get("tiny")
            if best and best.get("url"):
                results.append(
                    {
                        "id": str(video.get("id")),
                        "provider": self.id,
                        "duration_seconds": video.get("duration"),
                        "width": best.get("width"),
                        "height": best.get("height"),
                        "download_url": best["url"],
                        "page_url": video.get("pageURL"),
                        "creator": video.get("user"),
                        "query": query,
                    }
                )
        return results


def build_stock_providers(settings: Settings) -> dict[str, Any]:
    providers: dict[str, Any] = {}
    if settings.pexels_api_key:
        providers["pexels"] = PexelsStockProvider(settings.pexels_api_key)
    if settings.pixabay_api_key:
        providers["pixabay"] = PixabayStockProvider(settings.pixabay_api_key)
    return providers
