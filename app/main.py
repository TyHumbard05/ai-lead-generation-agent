from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.brave_search import BraveSearchError, search_business
from app.config import get_settings
from app.models import (
    BusinessIdentity,
    CandidateSite,
    SearchVerifyRequest,
    SearchVerifyResult,
    VerificationResult,
)
from app.verifier import confirm_no_website, verify_candidates

app = FastAPI(title="Web Lead Agent", version="0.2.0")


class VerifyRequest(BaseModel):
    business: BusinessIdentity
    candidates: list[CandidateSite]


class ConfirmRequest(BaseModel):
    result: VerificationResult
    reason: str


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/verify", response_model=VerificationResult)
def verify(request: VerifyRequest) -> VerificationResult:
    return verify_candidates(request.business, request.candidates)


@app.post("/search-and-verify", response_model=SearchVerifyResult)
def search_and_verify(request: SearchVerifyRequest) -> SearchVerifyResult:
    try:
        query, candidates = search_business(
            request.business,
            settings=get_settings(),
            count=request.count,
        )
    except BraveSearchError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    return SearchVerifyResult(
        query=query,
        candidates=candidates,
        verification=verify_candidates(request.business, candidates),
    )


@app.post("/confirm-no-website", response_model=VerificationResult)
def confirm(request: ConfirmRequest) -> VerificationResult:
    return confirm_no_website(request.result, request.reason)
