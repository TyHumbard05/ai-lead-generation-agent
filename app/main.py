from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException

from app.brave_search import BraveSearchConfigurationError, BraveSearchError, search_business
from app.config import Settings, get_settings
from app.models import (
    BatchVerifyItemResult,
    BatchVerifyRequest,
    BatchVerifyResult,
    ConfirmRequest,
    SearchVerifyRequest,
    SearchVerifyResult,
    VerificationResult,
    VerificationStatus,
    VerifyRequest,
)
from app.verifier import confirm_no_website, verify_candidates

app = FastAPI(
    title="Web Lead Agent",
    version="0.3.0",
    description=(
        "Evidence-based business website discovery and deterministic verification. "
        "Uncertain results are always routed to human review."
    ),
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/verify", response_model=VerificationResult)
def verify(request: VerifyRequest) -> VerificationResult:
    return verify_candidates(request.business, request.candidates)


@app.post("/verify/batch", response_model=BatchVerifyResult)
def verify_batch(request: BatchVerifyRequest) -> BatchVerifyResult:
    results = [
        BatchVerifyItemResult(
            id=lead.id,
            verification=verify_candidates(lead.business, lead.candidates),
        )
        for lead in request.leads
    ]
    website_found = sum(
        result.verification.status == VerificationStatus.WEBSITE_FOUND for result in results
    )
    return BatchVerifyResult(
        total=len(results),
        website_found=website_found,
        inconclusive=len(results) - website_found,
        results=results,
    )


@app.post("/search-and-verify", response_model=SearchVerifyResult)
def search_and_verify(
    request: SearchVerifyRequest,
    settings: Annotated[Settings, Depends(get_settings)],
) -> SearchVerifyResult:
    try:
        query, candidates = search_business(
            request.business,
            settings=settings,
            count=request.count,
        )
    except BraveSearchConfigurationError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except BraveSearchError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    return SearchVerifyResult(
        query=query,
        candidates=candidates,
        verification=verify_candidates(request.business, candidates),
    )


@app.post("/confirm-no-website", response_model=VerificationResult)
def confirm(request: ConfirmRequest) -> VerificationResult:
    try:
        return confirm_no_website(request.result, request.reason)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
