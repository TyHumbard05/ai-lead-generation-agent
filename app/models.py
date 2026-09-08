from enum import Enum
from pydantic import BaseModel, Field, HttpUrl


class VerificationStatus(str, Enum):
    WEBSITE_FOUND = "WEBSITE_FOUND"
    INCONCLUSIVE = "INCONCLUSIVE"
    VERIFIED_NO_WEBSITE = "VERIFIED_NO_WEBSITE"


class BusinessIdentity(BaseModel):
    name: str
    phone: str | None = None
    address: str | None = None
    city: str | None = None
    state: str | None = None
    category: str | None = None


class CandidateSite(BaseModel):
    url: HttpUrl
    title: str | None = None
    snippet: str | None = None
    phone: str | None = None
    address: str | None = None
    city: str | None = None
    state: str | None = None
    category: str | None = None


class ScoredCandidate(BaseModel):
    url: HttpUrl
    score: int = Field(ge=0)
    reasons: list[str] = Field(default_factory=list)


class VerificationResult(BaseModel):
    status: VerificationStatus
    best_candidate: ScoredCandidate | None = None
    candidates: list[ScoredCandidate] = Field(default_factory=list)
    requires_human_review: bool = False
    reason: str | None = None


class SearchVerifyRequest(BaseModel):
    business: BusinessIdentity
    count: int = Field(default=10, ge=1, le=20)


class SearchVerifyResult(BaseModel):
    query: str
    candidates: list[CandidateSite] = Field(default_factory=list)
    verification: VerificationResult
