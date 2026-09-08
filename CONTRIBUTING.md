# Contributing

## Setup

Use Python 3.11 or newer:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

On Windows PowerShell, activate with `.venv\Scripts\Activate.ps1`.

## Quality Checks

Run the same checks enforced by CI before opening a pull request:

```bash
ruff check .
ruff format --check .
pytest --cov=app --cov-report=term-missing --cov-fail-under=90
```

Tests that exercise Brave Search must use `httpx.MockTransport`; never place a real API key in source code, fixtures, logs, or recorded responses.

## Pull Requests

- Keep search-provider I/O separate from deterministic scoring and verification logic.
- Add tests for both the successful path and the safe-failure path.
- Update the README when an endpoint or user-visible behavior changes.
- Describe implemented behavior precisely; keep proposed functionality in the roadmap.
