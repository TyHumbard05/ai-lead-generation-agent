import re
from urllib.parse import urlparse

from app.models import BusinessIdentity, CandidateSite, ScoredCandidate

BLOCKED_HOST_HINTS = {
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


def _norm(value: str | None) -> str:
    return re.sub(r"[^a-z0-9]", "", (value or "").lower())


def _phone_digits(value: str | None) -> str:
    digits = re.sub(r"\D", "", value or "")
    return digits[-10:] if len(digits) >= 10 else digits


def _contains_normalized(container: str | None, value: str | None, *, min_length: int = 4) -> bool:
    normalized_value = _norm(value)
    return len(normalized_value) >= min_length and normalized_value in _norm(container)


def _host(url: str) -> str:
    return urlparse(url).netloc.lower().removeprefix("www.")


def is_blocked_site(url: str) -> bool:
    host = _host(url)
    return any(host == blocked or host.endswith("." + blocked) for blocked in BLOCKED_HOST_HINTS)


def score_candidate(business: BusinessIdentity, candidate: CandidateSite) -> ScoredCandidate:
    if is_blocked_site(str(candidate.url)):
        return ScoredCandidate(
            url=candidate.url, score=0, reasons=["directory/social/map host rejected"]
        )

    score = 0
    reasons: list[str] = []

    business_phone = _phone_digits(business.phone)
    candidate_phone = _phone_digits(candidate.phone)
    if len(business_phone) >= 7 and business_phone == candidate_phone:
        score += 55
        reasons.append("exact phone +55")
    if _contains_normalized(candidate.address, business.address, min_length=6):
        score += 20
        reasons.append("strong address +20")

    name = _norm(business.name)
    title = _norm(candidate.title)
    host = _norm(_host(str(candidate.url)))
    if name and name in title:
        score += 30
        reasons.append("business name in title +30")
    elif name and (name in host or host in name):
        score += 15
        reasons.append("domain/name similarity +15")
    elif name and any(
        part in title for part in re.findall(r"[a-z0-9]+", business.name.lower()) if len(part) >= 4
    ):
        score += 10
        reasons.append("partial name match +10")

    if business.city and candidate.city and _norm(business.city) == _norm(candidate.city):
        score += 10
        reasons.append("city +10")
    if business.state and candidate.state and _norm(business.state) == _norm(candidate.state):
        score += 5
        reasons.append("state +5")
    if (
        business.category
        and candidate.category
        and _norm(business.category) == _norm(candidate.category)
    ):
        score += 5
        reasons.append("category +5")

    return ScoredCandidate(url=candidate.url, score=score, reasons=reasons)
