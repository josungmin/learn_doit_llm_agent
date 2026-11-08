"""웹 검색과 스팀 상점 정보 조회 도구."""

import asyncio
import json
import re
from datetime import datetime, timedelta, timezone
from urllib.parse import parse_qs, urljoin, urlsplit

import httpx
from bs4 import BeautifulSoup
from ddgs import DDGS
from langchain_core.tools import tool

STEAM_HOST = "store.steampowered.com"
MAX_BODY = 1_000_000
STEAM_TAG_IDS = {
    "협동": 1685, "생존": 1662, "파티": 7107, "전략": 9, "퍼즐": 1664,
    "액션": 19, "RPG": 122, "시뮬레이션": 599, "어드벤처": 21, "공포": 1667,
}


def steam_app_id(url: str) -> str | None:
    """스팀 상점의 앱 주소를 확인하고 유효한 앱 ID만 반환한다."""
    try:
        parsed = urlsplit(url)
        if (parsed.scheme != "https" or parsed.hostname != STEAM_HOST
                or parsed.username is not None or parsed.password is not None
                or parsed.port not in (None, 443)):
            return None
        match = re.match(r"^/app/([1-9]\d{0,11})(?:/|$)", parsed.path)
        return match.group(1) if match else None
    except (TypeError, ValueError):
        return None


def steam_price(data: dict) -> int | None:
    """한국 원화 가격을 반환하며, 확인할 수 없으면 None을 반환한다."""
    if data.get("is_free") is True:
        return 0
    if data.get("is_free") is not False:
        return None
    price = data.get("price_overview")
    if not isinstance(price, dict) or price.get("currency") != "KRW":
        return None
    text = price.get("final_formatted")
    if not isinstance(text, str):
        return None
    match = re.fullmatch(r"\s*₩\s*(\d+(?:,\d{3})*)\s*", text)
    return int(match.group(1).replace(",", "")) if match else None


def parse_steam_details(app_id: str, payload: dict) -> dict | None:
    """스팀 응답에서 PC 게임 본편을 확인하고 추천에 필요한 정보만 추린다."""
    entry = payload.get(app_id)
    if not isinstance(entry, dict) or entry.get("success") is not True:
        return None
    data = entry.get("data")
    if not isinstance(data, dict) or str(data.get("steam_appid")) != app_id:
        return None
    platforms = data.get("platforms")
    if (data.get("type") != "game" or not isinstance(platforms, dict)
            or not any(platforms.get(p) is True for p in ("windows", "mac", "linux"))):
        return None
    release = data.get("release_date")
    coming_soon = release.get("coming_soon") if isinstance(release, dict) else None
    if coming_soon is True:
        return None
    name = data.get("name")
    if not isinstance(name, str) or not name.strip():
        return None
    categories = data.get("categories")
    categories = categories if isinstance(categories, list) else []
    singleplayer = any(
        item.get("id") == 2 or str(item.get("description", "")).strip().casefold()
        in {"single-player", "single player", "싱글 플레이어", "싱글플레이어"}
        for item in categories if isinstance(item, dict)
    )
    labels = [item["description"] for item in categories
              if isinstance(item, dict) and isinstance(item.get("description"), str)]
    genres = data.get("genres")
    genres = genres if isinstance(genres, list) else []
    labels += [item["description"] for item in genres
               if isinstance(item, dict) and isinstance(item.get("description"), str)]
    description = data.get("detailed_description")
    soup = BeautifulSoup(description if isinstance(description, str) else "", "html.parser")
    for element in soup(["script", "style"]):
        element.decompose()
    source = " | ".join([*labels, soup.get_text(" ", strip=True)])[:6000]
    online = any(re.search(r"(?i)(online|온라인).*(co[ -]?op|multi|pvp|협동|멀티)", label)
                 for label in labels)
    return {
        "app_id": app_id,
        "name": name.strip()[:120],
        "url": f"https://{STEAM_HOST}/app/{app_id}/",
        "source": source,
        "online": True if online else None,
        "singleplayer": True if singleplayer else None,
        "released": True if coming_soon is False else None,
        "price": steam_price(data),
        "checked_at": datetime.now(timezone(timedelta(hours=9))).strftime("%Y-%m-%d %H:%M KST"),
    }


def _safe_redirect(url: str, app_id: str) -> bool:
    try:
        parsed = urlsplit(url)
        return (parsed.scheme == "https" and parsed.hostname == STEAM_HOST
                and parsed.username is None and parsed.password is None
                and parsed.port in (None, 443)
                and parsed.path == "/api/appdetails"
                and parse_qs(parsed.query).get("appids") == [app_id])
    except (TypeError, ValueError):
        return False


@tool
async def web_search(query: str) -> list[str]:
    """Search the web for Steam store pages matching a short game query."""
    query = " ".join(query.split())[:160]
    if not query:
        return []
    def search() -> list[str]:
        results = DDGS(timeout=5).text(
            f"site:{STEAM_HOST} {query}", max_results=10
        )
        return [item["href"] for item in results
                if isinstance(item, dict) and isinstance(item.get("href"), str)]
    try:
        return await asyncio.to_thread(search)
    except Exception as exc:
        if "no results found" in str(exc).lower():
            return []
        raise


@tool
async def search_steam_store(players: int, budget: int, preferences: list[str]) -> list[str]:
    """Search Steam directly when a general web search cannot find game pages."""
    if not 1 <= players <= 10 or budget < 0:
        raise ValueError("Invalid player count or budget")
    params = {
        "category1": 998,
        "category2": 2 if players == 1 else 1,
        "maxprice": "free" if budget == 0 else budget,
        "cc": "kr",
        "l": "koreana",
    }
    for preference in preferences:
        if preference in STEAM_TAG_IDS:
            params["tags"] = STEAM_TAG_IDS[preference]
            break
    async with httpx.AsyncClient(timeout=5, follow_redirects=False) as client:
        async with client.stream("GET", f"https://{STEAM_HOST}/search/results/", params=params) as response:
            response.raise_for_status()
            body = bytearray()
            async for chunk in response.aiter_bytes():
                body.extend(chunk)
                if len(body) > MAX_BODY:
                    raise ValueError("Steam search response is too large")
    soup = BeautifulSoup(bytes(body), "html.parser")
    urls = [row.get("href") for row in soup.select("a.search_result_row[href]")]
    return [url for url in urls if steam_app_id(url)][:10]


@tool
async def fetch_steam_details(app_id: str) -> dict:
    """Read public Steam store details for one numeric application ID."""
    if not re.fullmatch(r"[1-9]\d{0,11}", app_id):
        return {"status": "invalid"}
    url = f"https://{STEAM_HOST}/api/appdetails?appids={app_id}&cc=kr&l=koreana"
    try:
        async with httpx.AsyncClient(timeout=5, follow_redirects=False) as client:
            for attempt in range(2):
                async with client.stream("GET", url) as response:
                    if response.is_redirect:
                        target = urljoin(url, response.headers.get("location", ""))
                        if attempt == 0 and _safe_redirect(target, app_id):
                            url = target
                            continue
                        return {"status": "unavailable"}
                    response.raise_for_status()
                    body = bytearray()
                    async for chunk in response.aiter_bytes():
                        body.extend(chunk)
                        if len(body) > MAX_BODY:
                            return {"status": "unavailable"}
                payload = json.loads(body)
                game = parse_steam_details(app_id, payload) if isinstance(payload, dict) else None
                return {"status": "ok", "game": game} if game else {"status": "invalid"}
    except (httpx.HTTPError, ValueError, UnicodeError):
        return {"status": "unavailable"}
    return {"status": "unavailable"}

