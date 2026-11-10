# Configuration

Use these defaults unless the user provides different constraints. State any material deviation in
the final report.

| Setting | Default | Limit | Purpose |
| --- | ---: | ---: | --- |
| Businesses per run | 25 | 100 | Keeps research bounded and reviewable |
| Search results per query | 10 | 20 | Limits noise and tool cost |
| Candidate sites per business | 10 | 50 | Bounds deterministic scoring |
| Query variants | 2 | 4 | Reduces false no-website conclusions |
| Contact discovery | Off | User-controlled | Avoids collecting unnecessary personal data |
| Output | Markdown | Markdown, CSV, or JSON | Matches the user's downstream workflow |

## Required access

- A web-search or business-search tool for discovery.
- Browser access only when inspecting a candidate website.

## Optional access

- Company enrichment for business attributes the user requested.
- Contact discovery for public business channels when the user explicitly requested outreach-ready
  results.
- Python 3.11 or newer plus terminal access for the deterministic scorer. The scorer uses only the
  Python standard library, reads JSON from standard input, writes JSON to standard output, and makes
  no network calls.

Use connected services for authentication. Never request that an API key, password, or token be
written into the skill, report, repository, or command history.

If a tool charges per call, quote the exact proposed cost and wait for explicit approval before the
call. Approval for one quoted call or batch does not authorize later charges.
