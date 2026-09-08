import httpx
import pytest

from app.brave_search import BraveSearchError, build_business_query, parse_brave_results, search_business
from app.config import Settings
from app.models import BusinessIdentity


def business() -> BusinessIdentity:
    return BusinessIdentity(
        name="Acme Repair",
        phone="555-123-4567",
        address="123 Main St",
        city="Rolla",
        state="MO",
        category="Electronics Repair",
    )


def test_build_query_includes_identity_context():
    query = build_business_query(business())
    assert '"Acme Repair"' in query
    assert "Rolla" in query
    assert "MO" in query
    assert "Electronics Repair" in query


def test_parse_results_extracts_evidence_and_rejects_directory_hosts():
    payload = {
        "web": {
            "results": [
                {
                    "url": "https://acmerepair.com/contact",
                    "title": "Acme Repair | Rolla MO",
                    "description": "Electronics Repair at 123 Main St. Call 555-123-4567.",
                },
                {
                    "url": "https://www.yelp.com/biz/acme-repair",
                    "title": "Acme Repair",
                    "description": "Directory listing",
                },
            ]
        }
    }
    candidates = parse_brave_results(business(), payload)
    assert len(candidates) == 1
    candidate = candidates[0]
    assert candidate.phone == "555-123-4567"
    assert candidate.address == "123 Main St"
    assert candidate.city == "Rolla"
    assert candidate.state == "MO"
    assert candidate.category == "Electronics Repair"


def test_parse_results_deduplicates_same_host():
    payload = {
        "web": {
            "results": [
                {"url": "https://acmerepair.com/", "title": "Acme Repair"},
                {"url": "https://www.acmerepair.com/contact", "title": "Contact Acme Repair"},
            ]
        }
    }
    assert len(parse_brave_results(business(), payload)) == 1


def test_search_business_sends_brave_auth_and_clamps_count():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.headers["X-Subscription-Token"] == "test-key"
        assert request.url.params["count"] == "20"
        assert request.url.params["country"] == "US"
        return httpx.Response(200, json={"web": {"results": []}})

    client = httpx.Client(transport=httpx.MockTransport(handler))
    query, candidates = search_business(
        business(),
        settings=Settings(brave_search_api_key="test-key"),
        count=99,
        client=client,
    )
    assert query.startswith('"Acme Repair"')
    assert candidates == []
    client.close()


def test_search_business_requires_api_key():
    with pytest.raises(BraveSearchError, match="BRAVE_SEARCH_API_KEY"):
        search_business(business(), settings=Settings(brave_search_api_key=None))
