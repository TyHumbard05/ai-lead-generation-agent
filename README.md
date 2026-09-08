# AI Lead Generation Agent

A portfolio project for researching businesses that may benefit from website redesign or other digital services. The current MVP combines **Brave Search API candidate retrieval**, deterministic website verification, and human-review safeguards so uncertain results are not presented as facts.

## Current MVP

Implemented now:

- Brave Search API integration for business website candidate discovery
- Automatic search query construction from business identity data
- Extraction of phone/address/location/category evidence from search results
- Deterministic website-candidate scoring
- Exact phone-match weighting
- Address, business-name, title, city, state, category, and domain signals
- Rejection of common social, map, and directory hosts
- Duplicate-domain filtering
- `WEBSITE_FOUND` and `INCONCLUSIVE` automated outcomes
- Human-only promotion to `VERIFIED_NO_WEBSITE`
- Ambiguity handling when top candidates are too close
- FastAPI endpoints for direct verification and search + verification
- Pytest coverage and GitHub Actions CI

## How It Works

1. A business identity is submitted with information such as name, phone, address, city, state, and category.
2. The application builds a targeted Brave Search query.
3. Brave returns candidate web results.
4. Known directory, social-network, map, and other third-party hosts are rejected.
5. Search-result evidence is converted into structured candidate signals.
6. Candidates are scored using deterministic identity rules.
7. A strong, unambiguous candidate can become `WEBSITE_FOUND`.
8. Weak or competing matches remain `INCONCLUSIVE` for human review.

The application **never automatically concludes that a business has no website**. `VERIFIED_NO_WEBSITE` requires explicit human confirmation and a reason.

## Scoring Model

The scoring approach is intentionally explainable rather than opaque. Identity signals include:

- Exact phone match: strong evidence
- Strong address match
- Business-name and page-title match
- City/state agreement
- Business category agreement
- Domain/business-name similarity

A candidate must clear the verification threshold to be marked `WEBSITE_FOUND`. If the evidence is weak or competing candidates are too close, the result stays `INCONCLUSIVE`.

## Project Structure

```text
app/
  brave_search.py  Brave Search client, parsing, filtering, and deduplication
  config.py        Environment-based settings
  main.py          FastAPI application and endpoints
  models.py        Request/result models and verification states
  scoring.py       Deterministic identity scoring and blocked-host rules
  verifier.py      Threshold, ambiguity, and human-review logic

tests/
  test_brave_search.py
  test_verifier.py

.github/workflows/
  tests.yml        Pytest CI on pushes and pull requests
```

## Run Locally

Requires Python 3.11+.

```bash
python -m venv .venv
source .venv/bin/activate       # Linux/macOS
# .venv\Scripts\activate        # Windows PowerShell

pip install -e ".[dev]"
cp .env.example .env
```

Add your Brave Search API key to `.env`:

```env
BRAVE_SEARCH_API_KEY=your_key_here
```

Then run:

```bash
pytest
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` for the interactive API documentation.

## Search and Verify Example

`POST /search-and-verify`

```json
{
  "business": {
    "name": "Acme Repair",
    "phone": "555-123-4567",
    "address": "123 Main St",
    "city": "Rolla",
    "state": "MO",
    "category": "Electronics Repair"
  },
  "count": 10
}
```

The response contains the generated search query, first-party candidate sites, and the verification result.

## Direct Verification

The original `POST /verify` endpoint is still available when candidate sites are already known and you want to run only the deterministic verifier.

## Roadmap

Planned next steps from the larger lead-agent design:

- Multi-query Brave verification for stronger phone/address evidence
- Business discovery adapters
- First-party contact enrichment
- Same-domain crawling with a strict page cap
- `robots.txt` enforcement
- Persistence and provenance tracking
- Lead review queue and export
- Optional AI-assisted research/orchestration layer

## Why I Built It

This project explores how AI and automation systems can gather evidence, call external services, apply transparent rules, and route uncertain decisions to a human instead of hallucinating certainty.

## Responsible Use

This project is intended for legitimate business research. Automated findings should be reviewed before outreach, and any outreach should comply with applicable platform rules, privacy requirements, and anti-spam laws.

## Status

**Active development.** The repository contains a runnable Brave-powered website-discovery and verification MVP, with additional enrichment and workflow components planned incrementally.
