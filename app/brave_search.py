import re
from urllib.parse import urlparse

import httpx

from app.config import Settings
from app.models import BusinessIdentity, CandidateSite
from app.scoring import is_blocked_site


class BraveSearchError(RuntimeError):
    pass


def _norm(value: str | None) -> str:
    return re.sub(r"[^a-z0-9]", "", (value or "").lower())


def _contains_phrase(text: str, phrase: str | None) -> bool:
    if not phrase:
        return False
    return _norm(phrase) in _norm(text)


def _contains_state(text: str, state: str | None) -> bool:
    if not state:
        return False
    return re.search(rf"\b{re.escape(state)}\b", text, flags=re.IGNORECASE) is not None


def build_business_query(business: BusinessIdentity) -> str:
    parts = [f'"{business.name.strip()}"']
    if business.city:
        parts.append(business.city.strip())
    if business.state:
        parts.append(business.state.strip())
    if business.category:
        parts.append(business.category.strip())
    return " ".join(part for part in parts if part)[:600]


def _host(url: str) -> str:
    return urlparse(url).netloc.lower().removeprefix("www.")


def _candidate_from_result(business: BusinessIdentity, result: dict) -> CandidateSite | None:
    url = result.get("url")
    if not url or is_blocked_site(url):
        return None

    title = result.get("title") or None
    snippet = result.get("description") or None
    evidence = " ".join(value for value in [title, snippet] if value)

    return CandidateSite(
        url=url,
        title=title,
        snippet=snippet,
        phone=business.phone if _contains_phrase(evidence, business.phone) else None,
        address=business.address if _contains_phrase(evidence, business.address) else None,
        city=business.city if _contains_phrase(evidence, business.city) else None,
        state=business.state if _contains_state(evidence, business.state) else None,
        category=business.category if _contains_phrase(evidence, business.category) else None,
    )


def parse_brave_results(business: BusinessIdentity, payload: dict) -> list[CandidateSite]:
    raw_results = (payload.get("web") or {}).get("results") or []
    candidates: list[CandidateSite] = []
    seen_hosts: set[str] = set()

    for result in raw_results:
        candidate = _candidate_from_result(business, result)
        if candidate is None:
            continue
        host = _host(str(candidate.url))
        if not host or host in seen_hosts:
            continue
        seen_hosts.add(host)
        candidates.append(candidate)

    return candidates


def search_business(
    business: BusinessIdentity,
    settings: Settings,
    count: int = 10,
    client: httpx.Client | None = None,
) -> tuple[str, list[CandidateSite]]:
    if not settings.brave_search_api_key:
        raise BraveSearchError("BRAVE_SEARCH_API_KEY is not configured.")

    query = build_business_query(business)
    owns_client = client is None
    http = client or httpx.Client(timeout=settings.http_timeout_seconds)

    try:
        response = http.get(
            settings.brave_search_url,
            params={
                "q": query,
                "count": max(1, min(count, 20)),
                "country": settings.brave_country,
                "search_lang": settings.brave_search_lang,
            },
            headers={
                "Accept": "application/json",
                "X-Subscription-Token": settings.brave_search_api_key,
            },
        )
        response.raise_for_status()
    except httpx.HTTPError as exc:
        raise BraveSearchError(f"Brave Search request failed: {exc}") from exc
    finally:
        if owns_client:
            http.close()

    return query, parse_brave_results(business, response.json())
