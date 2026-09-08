from fastapi import FastAPI
from pydantic import BaseModel

from app.models import BusinessIdentity, CandidateSite, VerificationResult
from app.verifier import confirm_no_website, verify_candidates

app = FastAPI(title="Web Lead Agent", version="0.1.0")


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


@app.post("/confirm-no-website", response_model=VerificationResult)
def confirm(request: ConfirmRequest) -> VerificationResult:
    return confirm_no_website(request.result, request.reason)
