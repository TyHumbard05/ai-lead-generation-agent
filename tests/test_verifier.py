import pytest

from app.models import BusinessIdentity, CandidateSite, VerificationStatus
from app.scoring import is_blocked_site, score_candidate
from app.verifier import confirm_no_website, verify_candidates


def business() -> BusinessIdentity:
    return BusinessIdentity(
        name="Acme Repair",
        phone="555-123-4567",
        address="123 Main St",
        city="Rolla",
        state="MO",
        category="Electronics Repair",
    )


def test_exact_identity_signals_clear_threshold():
    candidate = CandidateSite(
        url="https://acmerepair.com",
        title="Acme Repair",
        phone="5551234567",
        address="123 Main St",
        city="Rolla",
        state="MO",
        category="Electronics Repair",
    )
    scored = score_candidate(business(), candidate)
    assert scored.score >= 70


def test_directory_hosts_are_rejected():
    assert is_blocked_site("https://www.yelp.com/biz/acme-repair")
    candidate = CandidateSite(url="https://www.yelp.com/biz/acme-repair", title="Acme Repair")
    assert score_candidate(business(), candidate).score == 0


def test_strong_candidate_becomes_website_found():
    candidate = CandidateSite(
        url="https://acmerepair.com",
        title="Acme Repair",
        phone="555-123-4567",
        address="123 Main St",
    )
    result = verify_candidates(business(), [candidate])
    assert result.status == VerificationStatus.WEBSITE_FOUND


def test_low_confidence_result_requires_human_review():
    candidate = CandidateSite(url="https://example.com", title="Something Else")
    result = verify_candidates(business(), [candidate])
    assert result.status == VerificationStatus.INCONCLUSIVE
    assert result.requires_human_review is True


def test_verified_no_website_requires_human_reason():
    result = verify_candidates(business(), [])
    with pytest.raises(ValueError):
        confirm_no_website(result, "")

    confirmed = confirm_no_website(result, "Reviewed search results manually; no first-party site found.")
    assert confirmed.status == VerificationStatus.VERIFIED_NO_WEBSITE
