import pytest
from pydantic import ValidationError

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


def test_name_signal_is_not_counted_twice():
    candidate = CandidateSite(url="https://acmerepair.com", title="Acme Repair")

    scored = score_candidate(business(), candidate)

    assert scored.score == 30
    assert scored.reasons == ["business name in title +30"]


def test_phone_matching_ignores_country_code_and_formatting():
    candidate = CandidateSite(url="https://example.com", phone="+1 (555) 123-4567")

    scored = score_candidate(business(), candidate)

    assert "exact phone +55" in scored.reasons


def test_short_address_fragment_is_not_strong_evidence():
    lead = BusinessIdentity(name="Acme", address="12")
    candidate = CandidateSite(url="https://example.com", address="112 Main Street")

    assert "strong address +20" not in score_candidate(lead, candidate).reasons


def test_directory_hosts_are_rejected():
    assert is_blocked_site("https://www.yelp.com/biz/acme-repair")
    candidate = CandidateSite(url="https://www.yelp.com/biz/acme-repair", title="Acme Repair")
    assert score_candidate(business(), candidate).score == 0


def test_blocking_uses_domain_boundaries():
    assert not is_blocked_site("https://notyelp.com/acme")


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


def test_qualifying_candidates_inside_ambiguity_window_require_review():
    candidates = [
        CandidateSite(
            url="https://acmerepair.com",
            title="Acme Repair",
            phone="555-123-4567",
        ),
        CandidateSite(
            url="https://acme-repair.com",
            title="Acme Repair in Rolla",
            phone="555-123-4567",
        ),
    ]

    result = verify_candidates(business(), candidates)

    assert result.status == VerificationStatus.INCONCLUSIVE
    assert result.reason == "Top website candidates are too close to resolve automatically."


def test_viable_candidate_below_threshold_requires_review():
    candidate = CandidateSite(url="https://acmerepair.com", title="Unrelated Company")

    result = verify_candidates(business(), [candidate])

    assert result.status == VerificationStatus.INCONCLUSIVE
    assert result.reason == "Best candidate scored below 70."


def test_verified_no_website_requires_human_reason():
    result = verify_candidates(business(), [])
    with pytest.raises(ValueError):
        confirm_no_website(result, "")

    confirmed = confirm_no_website(
        result, "Reviewed search results manually; no first-party site found."
    )
    assert confirmed.status == VerificationStatus.VERIFIED_NO_WEBSITE


def test_business_identity_rejects_blank_name_and_unknown_fields():
    with pytest.raises(ValidationError):
        BusinessIdentity(name="   ")

    with pytest.raises(ValidationError):
        BusinessIdentity(name="Acme", website="https://example.com")


def test_business_identity_normalizes_optional_blank_text():
    lead = BusinessIdentity(name="  Acme  ", city="  ", state=" MO ")

    assert lead.name == "Acme"
    assert lead.city is None
    assert lead.state == "MO"
