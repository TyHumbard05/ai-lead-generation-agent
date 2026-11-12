#!/usr/bin/env python3
"""Score first-party website candidates from bounded JSON supplied on standard input."""

from __future__ import annotations

import json
import re
import sys
from typing import Any
from urllib.parse import urlparse

WEBSITE_THRESHOLD = 70
AMBIGUITY_WINDOW = 15
MAX_LEADS = 100
MAX_CANDIDATES = 50

BLOCKED_HOSTS = {
    "angi.com",
    "bbb.org",
    "bing.com",
    "facebook.com",
    "google.com",
    "instagram.com",
    "linkedin.com",
    "mapquest.com",
    "nextdoor.com",
    "tripadvisor.com",
    "x.com",
    "yellowpages.com",
    "yelp.com",
}


class InputError(ValueError):
    """Raised when scorer input is malformed or outside safety bounds."""


def normalize(value: str | None) -> str:
    return re.sub(r"[^a-z0-9]", "", (value or "").lower())


def phone_digits(value: str | None) -> str:
    digits = re.sub(r"\D", "", value or "")
    return digits[-10:] if len(digits) >= 10 else digits


def optional_text(record: dict[str, Any], key: str, context: str) -> str | None:
    value = record.get(key)
    if value is None:
        return None
    if not isinstance(value, str):
        raise InputError(f"{context}.{key} must be a string or null")
    stripped = value.strip()
    return stripped or None


def require_text(record: dict[str, Any], key: str, context: str, limit: int) -> str:
    value = optional_text(record, key, context)
    if value is None:
        raise InputError(f"{context}.{key} is required")
    if len(value) > limit:
        raise InputError(f"{context}.{key} must be at most {limit} characters")
    return value


def host(url: str) -> str:
    return (urlparse(url).hostname or "").lower().removeprefix("www.")


def require_url(record: dict[str, Any], context: str) -> str:
    url = require_text(record, "url", context, 2048)
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise InputError(f"{context}.url must be an HTTP or HTTPS URL")
    return url


def is_blocked(url: str) -> bool:
    candidate_host = host(url)
    return any(
        candidate_host == blocked or candidate_host.endswith(f".{blocked}")
        for blocked in BLOCKED_HOSTS
    )


def contains_normalized(container: str | None, value: str | None, minimum: int) -> bool:
    normalized_value = normalize(value)
    return len(normalized_value) >= minimum and normalized_value in normalize(container)


def score_candidate(business: dict[str, str | None], candidate: dict[str, Any]) -> dict[str, Any]:
    url = candidate["url"]
    if is_blocked(url):
        return {"url": url, "score": 0, "reasons": ["third-party host rejected"]}

    score = 0
    reasons: list[str] = []
    business_phone = phone_digits(business.get("phone"))
    candidate_phone = phone_digits(candidate.get("phone"))
    if len(business_phone) >= 7 and business_phone == candidate_phone:
        score += 55
        reasons.append("exact phone +55")
    if contains_normalized(candidate.get("address"), business.get("address"), 6):
        score += 20
        reasons.append("strong address +20")

    business_name = normalize(business["name"])
    candidate_title = normalize(candidate.get("title"))
    candidate_host = normalize(host(url))
    if business_name and business_name in candidate_title:
        score += 30
        reasons.append("business name in title +30")
    elif business_name and (business_name in candidate_host or candidate_host in business_name):
        score += 15
        reasons.append("domain/name similarity +15")
    elif business_name and any(
        token in candidate_title
        for token in re.findall(r"[a-z0-9]+", business["name"].lower())
        if len(token) >= 4
    ):
        score += 10
        reasons.append("partial name match +10")

    for field, points in (("city", 10), ("state", 5), ("category", 5)):
        business_value = business.get(field)
        candidate_value = candidate.get(field)
        if (
            business_value
            and candidate_value
            and normalize(business_value) == normalize(candidate_value)
        ):
            score += points
            reasons.append(f"{field} +{points}")

    return {"url": url, "score": score, "reasons": reasons}


def parse_business(value: Any, context: str) -> dict[str, str | None]:
    if not isinstance(value, dict):
        raise InputError(f"{context} must be an object")
    business: dict[str, str | None] = {"name": require_text(value, "name", context, 200)}
    for key, limit in (
        ("phone", 50),
        ("address", 300),
        ("city", 100),
        ("state", 100),
        ("category", 150),
    ):
        item = optional_text(value, key, context)
        if item is not None and len(item) > limit:
            raise InputError(f"{context}.{key} must be at most {limit} characters")
        business[key] = item
    return business


def parse_candidates(value: Any, context: str) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        raise InputError(f"{context} must be an array")
    if len(value) > MAX_CANDIDATES:
        raise InputError(f"{context} must contain at most {MAX_CANDIDATES} candidates")
    candidates: list[dict[str, Any]] = []
    for index, raw in enumerate(value):
        item_context = f"{context}[{index}]"
        if not isinstance(raw, dict):
            raise InputError(f"{item_context} must be an object")
        candidate: dict[str, Any] = {"url": require_url(raw, item_context)}
        for key in ("title", "phone", "address", "city", "state", "category"):
            candidate[key] = optional_text(raw, key, item_context)
        candidates.append(candidate)
    return candidates


def evaluate_lead(raw: Any, index: int) -> dict[str, Any]:
    context = f"leads[{index}]"
    if not isinstance(raw, dict):
        raise InputError(f"{context} must be an object")
    lead_id = require_text(raw, "id", context, 100)
    business = parse_business(raw.get("business"), f"{context}.business")
    candidates = parse_candidates(raw.get("candidates"), f"{context}.candidates")
    scored = sorted(
        (score_candidate(business, candidate) for candidate in candidates),
        key=lambda item: item["score"],
        reverse=True,
    )
    viable = [candidate for candidate in scored if candidate["score"] > 0]

    status = "INCONCLUSIVE"
    requires_review = True
    best = viable[0] if viable else None
    if not viable:
        reason = "No trustworthy first-party website candidate was found."
    elif best["score"] < WEBSITE_THRESHOLD:
        reason = f"Best candidate scored below {WEBSITE_THRESHOLD}."
    elif len(viable) > 1 and best["score"] - viable[1]["score"] <= AMBIGUITY_WINDOW:
        reason = "Top website candidates are too close to resolve automatically."
    else:
        status = "WEBSITE_FOUND"
        requires_review = False
        reason = "Top candidate cleared the identity and ambiguity thresholds."

    return {
        "id": lead_id,
        "status": status,
        "best_candidate": best,
        "candidates": scored,
        "requires_human_review": requires_review,
        "reason": reason,
    }


def evaluate(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise InputError("input must be a JSON object")
    leads = payload.get("leads")
    if not isinstance(leads, list):
        raise InputError("leads must be an array")
    if not 1 <= len(leads) <= MAX_LEADS:
        raise InputError(f"leads must contain between 1 and {MAX_LEADS} items")

    results = [evaluate_lead(lead, index) for index, lead in enumerate(leads)]
    ids = [result["id"] for result in results]
    if len(ids) != len(set(ids)):
        raise InputError("lead ids must be unique")
    found = sum(result["status"] == "WEBSITE_FOUND" for result in results)
    return {
        "summary": {
            "total": len(results),
            "website_found": found,
            "inconclusive": len(results) - found,
        },
        "results": results,
    }


def main() -> int:
    try:
        payload = json.load(sys.stdin)
        result = evaluate(payload)
    except (json.JSONDecodeError, InputError) as exc:
        print(f"input error: {exc}", file=sys.stderr)
        return 2
    json.dump(result, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
