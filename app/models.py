from enum import StrEnum
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_validator, model_validator


class ApiModel(BaseModel):
    """Shared API model defaults.

    Rejecting unknown fields catches misspelled input instead of silently running a
    verification with incomplete evidence.
    """

    model_config = ConfigDict(extra="forbid")


class VerificationStatus(StrEnum):
    WEBSITE_FOUND = "WEBSITE_FOUND"
    INCONCLUSIVE = "INCONCLUSIVE"
    VERIFIED_NO_WEBSITE = "VERIFIED_NO_WEBSITE"


class BusinessIdentity(ApiModel):
    name: str = Field(min_length=1, max_length=200)
    phone: str | None = Field(default=None, max_length=50)
    address: str | None = Field(default=None, max_length=300)
    city: str | None = Field(default=None, max_length=100)
    state: str | None = Field(default=None, max_length=100)
    category: str | None = Field(default=None, max_length=150)

    @field_validator("name", mode="before")
    @classmethod
    def strip_name(cls, value: object) -> object:
        return value.strip() if isinstance(value, str) else value

    @field_validator("phone", "address", "city", "state", "category", mode="before")
    @classmethod
    def normalize_optional_text(cls, value: object) -> object:
        if isinstance(value, str):
            return value.strip() or None
        return value


class CandidateSite(ApiModel):
    url: HttpUrl
    title: str | None = None
    snippet: str | None = None
    phone: str | None = None
    address: str | None = None
    city: str | None = None
    state: str | None = None
    category: str | None = None


class ScoredCandidate(ApiModel):
    url: HttpUrl
    score: int = Field(ge=0)
    reasons: list[str] = Field(default_factory=list)


class VerificationResult(ApiModel):
    status: VerificationStatus
    best_candidate: ScoredCandidate | None = None
    candidates: list[ScoredCandidate] = Field(default_factory=list)
    requires_human_review: bool = False
    reason: str | None = None


class VerifyRequest(ApiModel):
    business: BusinessIdentity
    candidates: list[CandidateSite] = Field(default_factory=list, max_length=50)


class BatchVerifyItem(ApiModel):
    id: str = Field(min_length=1, max_length=100)
    business: BusinessIdentity
    candidates: list[CandidateSite] = Field(default_factory=list, max_length=50)

    @field_validator("id", mode="before")
    @classmethod
    def strip_id(cls, value: object) -> object:
        return value.strip() if isinstance(value, str) else value


class BatchVerifyRequest(ApiModel):
    leads: list[BatchVerifyItem] = Field(min_length=1, max_length=100)

    @model_validator(mode="after")
    def require_unique_ids(self) -> Self:
        ids = [lead.id for lead in self.leads]
        if len(ids) != len(set(ids)):
            raise ValueError("Lead IDs must be unique within a batch.")
        return self


class BatchVerifyItemResult(ApiModel):
    id: str
    verification: VerificationResult


class BatchVerifyResult(ApiModel):
    total: int = Field(ge=0)
    website_found: int = Field(ge=0)
    inconclusive: int = Field(ge=0)
    results: list[BatchVerifyItemResult] = Field(default_factory=list)


class ConfirmRequest(ApiModel):
    result: VerificationResult
    reason: str = Field(min_length=1, max_length=1000)

    @field_validator("reason", mode="before")
    @classmethod
    def strip_reason(cls, value: object) -> object:
        return value.strip() if isinstance(value, str) else value


class SearchVerifyRequest(ApiModel):
    business: BusinessIdentity
    count: int = Field(default=10, ge=1, le=20)


class SearchVerifyResult(ApiModel):
    query: str
    candidates: list[CandidateSite] = Field(default_factory=list)
    verification: VerificationResult
