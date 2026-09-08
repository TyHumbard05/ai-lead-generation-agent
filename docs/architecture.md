# Architecture

The service uses a deliberately small pipeline so every automated conclusion is traceable to supplied evidence.

```text
Business identity
       |
       +---------------------------+
       |                           |
       v                           v
Brave Search adapter       Supplied candidates
       |                           |
       +------------+--------------+
                    v
          Candidate normalization
                    |
                    v
          Deterministic scoring
                    |
                    v
       Threshold + ambiguity policy
             /              \
            v                v
    WEBSITE_FOUND       INCONCLUSIVE
                             |
                             v
                    Optional human review
                             |
                             v
                  VERIFIED_NO_WEBSITE
```

## Components

- `app/models.py` owns the API contract, validation limits, and result states.
- `app/brave_search.py` is the only module that communicates with Brave Search. It builds queries, validates upstream response shapes, extracts identity evidence, filters third-party hosts, and deduplicates domains.
- `app/scoring.py` contains pure functions for candidate scoring. Each reason includes its weight so callers can audit the result.
- `app/verifier.py` applies the acceptance threshold and ambiguity window. It is also the only place that permits the human-only `VERIFIED_NO_WEBSITE` transition.
- `app/main.py` maps HTTP requests and errors onto those domain functions. Configuration is injected through FastAPI dependencies so endpoint tests do not need real credentials.

## Decision Invariants

1. A blocked directory, map, or social host cannot be selected as a first-party site.
2. A candidate must score at least 70 to become `WEBSITE_FOUND`.
3. A qualifying candidate remains `INCONCLUSIVE` when another viable candidate is within 15 points.
4. Empty, weak, malformed, or contradictory evidence fails toward human review.
5. Only an explicit human action with a non-empty reason can produce `VERIFIED_NO_WEBSITE`.
6. A result already marked `WEBSITE_FOUND` cannot be overwritten as no-website through the confirmation endpoint.
7. IDs in a batch must be unique so callers can correlate every result unambiguously.

## Why Deterministic Scoring?

An LLM-based classifier could be added later, but it would make the current identity decision harder to reproduce and test. The current rules provide a stable baseline that can be evaluated against a labeled dataset before any probabilistic layer is introduced.

## Production Gaps

This is a portfolio MVP, not a production outreach system. A production deployment would need authentication, rate limiting, durable provenance, encrypted secret management, retry/backoff policy, observability, and a labeled evaluation dataset. Website crawling would also require strict same-domain limits and `robots.txt` enforcement.
