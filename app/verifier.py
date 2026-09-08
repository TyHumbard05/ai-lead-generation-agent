from app.models import BusinessIdentity, CandidateSite, VerificationResult, VerificationStatus
from app.scoring import score_candidate

WEBSITE_THRESHOLD = 70
AMBIGUITY_WINDOW = 15


def verify_candidates(
    business: BusinessIdentity, candidates: list[CandidateSite]
) -> VerificationResult:
    scored = sorted(
        (score_candidate(business, candidate) for candidate in candidates),
        key=lambda item: item.score,
        reverse=True,
    )

    viable = [candidate for candidate in scored if candidate.score > 0]
    if not viable:
        return VerificationResult(
            status=VerificationStatus.INCONCLUSIVE,
            candidates=scored,
            requires_human_review=True,
            reason="No trustworthy first-party website candidate was found.",
        )

    best = viable[0]
    if best.score < WEBSITE_THRESHOLD:
        return VerificationResult(
            status=VerificationStatus.INCONCLUSIVE,
            best_candidate=best,
            candidates=scored,
            requires_human_review=True,
            reason=f"Best candidate scored below {WEBSITE_THRESHOLD}.",
        )

    if len(viable) > 1 and best.score - viable[1].score <= AMBIGUITY_WINDOW:
        return VerificationResult(
            status=VerificationStatus.INCONCLUSIVE,
            best_candidate=best,
            candidates=scored,
            requires_human_review=True,
            reason="Top website candidates are too close to resolve automatically.",
        )

    return VerificationResult(
        status=VerificationStatus.WEBSITE_FOUND,
        best_candidate=best,
        candidates=scored,
    )


def confirm_no_website(result: VerificationResult, reason: str) -> VerificationResult:
    if not reason.strip():
        raise ValueError("Human confirmation requires a reason.")
    if result.status == VerificationStatus.WEBSITE_FOUND:
        raise ValueError("Cannot mark a verified website match as no-website.")
    return result.model_copy(
        update={
            "status": VerificationStatus.VERIFIED_NO_WEBSITE,
            "requires_human_review": False,
            "reason": reason.strip(),
        }
    )
