from fastapi.testclient import TestClient

from app.config import Settings, get_settings
from app.main import app

client = TestClient(app)


def candidate_payload() -> dict:
    return {
        "url": "https://acmerepair.com",
        "title": "Acme Repair",
        "phone": "555-123-4567",
    }


def business_payload() -> dict:
    return {"name": "Acme Repair", "phone": "555-123-4567"}


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_verify_endpoint():
    response = client.post(
        "/verify",
        json={"business": business_payload(), "candidates": [candidate_payload()]},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "WEBSITE_FOUND"


def test_batch_verify_preserves_ids_and_returns_summary():
    response = client.post(
        "/verify/batch",
        json={
            "leads": [
                {
                    "id": "lead-1",
                    "business": business_payload(),
                    "candidates": [candidate_payload()],
                },
                {
                    "id": "lead-2",
                    "business": {"name": "Unknown Shop"},
                    "candidates": [],
                },
            ]
        },
    )

    assert response.status_code == 200
    assert response.json()["total"] == 2
    assert response.json()["website_found"] == 1
    assert response.json()["inconclusive"] == 1
    assert [item["id"] for item in response.json()["results"]] == ["lead-1", "lead-2"]


def test_batch_verify_enforces_non_empty_bounded_input():
    response = client.post("/verify/batch", json={"leads": []})

    assert response.status_code == 422


def test_batch_verify_rejects_duplicate_ids():
    lead = {"id": "lead-1", "business": business_payload(), "candidates": []}

    response = client.post("/verify/batch", json={"leads": [lead, lead]})

    assert response.status_code == 422
    assert "Lead IDs must be unique" in response.text


def test_confirm_endpoint_rejects_contradicting_human_decision():
    verified = client.post(
        "/verify",
        json={"business": business_payload(), "candidates": [candidate_payload()]},
    ).json()

    response = client.post(
        "/confirm-no-website",
        json={"result": verified, "reason": "Manual review"},
    )

    assert response.status_code == 409
    assert "Cannot mark" in response.json()["detail"]


def test_search_endpoint_reports_missing_configuration():
    app.dependency_overrides[get_settings] = lambda: Settings(brave_search_api_key=None)
    try:
        response = client.post(
            "/search-and-verify",
            json={"business": business_payload(), "count": 5},
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 503
    assert response.json()["detail"] == "BRAVE_SEARCH_API_KEY is not configured."


def test_search_endpoint_maps_upstream_failures_to_bad_gateway(monkeypatch):
    from app import main
    from app.brave_search import BraveSearchError

    def fail_search(*args, **kwargs):
        raise BraveSearchError("upstream unavailable")

    monkeypatch.setattr(main, "search_business", fail_search)
    app.dependency_overrides[get_settings] = lambda: Settings(brave_search_api_key="test-key")
    try:
        response = client.post(
            "/search-and-verify",
            json={"business": business_payload(), "count": 5},
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 502
    assert response.json()["detail"] == "upstream unavailable"


def test_api_rejects_unknown_input_fields():
    response = client.post(
        "/verify",
        json={"business": {"name": "Acme", "nmae": "typo"}, "candidates": []},
    )

    assert response.status_code == 422
