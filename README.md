# AI Lead Generation Agent

A portfolio project for researching businesses that may benefit from website redesign or other digital services. The current MVP focuses on one of the hardest parts of that workflow: deciding whether a candidate URL is likely to be a business's real first-party website without overstating uncertain results.

## Current MVP

Implemented now:

- Deterministic website-candidate scoring
- Exact phone-match weighting
- Address, business-name, title, city, state, category, and domain signals
- Rejection of common social, map, and directory hosts
- `WEBSITE_FOUND` and `INCONCLUSIVE` automated outcomes
- Human-only promotion to `VERIFIED_NO_WEBSITE`
- Ambiguity handling when top candidates are too close
- FastAPI endpoints for verification and human confirmation
- Pytest coverage for core guardrails

## Scoring Model

The scoring approach is intentionally explainable rather than opaque. Important identity signals include:

- Exact phone match: strong evidence
- Strong address match
- Business-name and page-title match
- City/state agreement
- Business category agreement
- Domain/business-name similarity

A candidate must clear the verification threshold to be marked `WEBSITE_FOUND`. If the evidence is weak or competing candidates are too close, the result stays `INCONCLUSIVE` for human review.

The application never automatically concludes that a business has no website. `VERIFIED_NO_WEBSITE` requires an explicit human confirmation and reason.

## Project Structure

```text
app/
  main.py       FastAPI application
  models.py     Request/result models and verification states
  scoring.py    Deterministic identity scoring and blocked-host rules
  verifier.py   Threshold, ambiguity, and human-review logic

tests/
  test_verifier.py
```

## Run Locally

Requires Python 3.11+.

```bash
python -m venv .venv
source .venv/bin/activate       # Linux/macOS
# .venv\Scripts\activate        # Windows PowerShell

pip install -e ".[dev]"
pytest
uvicorn app.main:app --reload
```

Then open `http://127.0.0.1:8000/docs` for the interactive API documentation.

## Example

`POST /verify`

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
  "candidates": [
    {
      "url": "https://acmerepair.com",
      "title": "Acme Repair",
      "phone": "555-123-4567",
      "address": "123 Main St"
    }
  ]
}
```

## Roadmap

Planned next steps from the larger lead-agent design:

- Brave Search API candidate retrieval
- Business discovery adapters
- First-party contact enrichment
- Same-registrable-domain crawling with a strict page cap
- `robots.txt` enforcement
- Persistence and provenance tracking
- Lead review queue and export
- Optional AI-assisted research/orchestration layer

## Why I Built It

This project explores how AI/automation systems can gather evidence, apply structured rules, call external services, and route uncertain decisions to a human instead of hallucinating certainty.

## Responsible Use

This project is intended for legitimate business research. Automated findings should be reviewed before outreach, and any outreach should comply with applicable platform rules, privacy requirements, and anti-spam laws.

## Status

**Active development.** The repository currently contains the runnable website-verification MVP. The broader discovery/enrichment workflow is documented in the roadmap and will be added incrementally.
