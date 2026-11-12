# Agensi tool routing

Use only the tools attached to this listing by its creator. Call `skill_tools` before research to see
their current names, purposes, parameters, and prices. Do not assume that Hunter, Apollo, ContactOut,
or another provider is attached merely because Agensi offers it.

## Required role

Choose one attached web-search, business-search, or company-discovery tool for candidate discovery.
If none is attached or available, tell the user that discovery cannot start and identify the missing
capability. Do not silently switch to an unrelated paid provider.

## Optional roles

- Use an attached company-enrichment tool only for business attributes needed to verify identity or
  fulfill the requested report.
- Use Hunter, Apollo, ContactOut, or another attached contact tool only when the user explicitly asks
  for contact discovery. Prefer public business channels and minimize personal data.
- Do not call multiple enrichment providers for the same record unless the first result is incomplete
  and the user approves the additional cost.

## Paid calls

1. Use `quote_tool` with the intended tool, parameters, and batch size.
2. Show the exact quoted price, the purpose of the call, and the number of records to the user.
3. Wait for explicit approval of that quote or batch.
4. Use `run_tool` only after approval. A prior approval does not cover a changed price, larger batch,
   different provider, or later call.
5. If the call fails, do not retry a chargeable alternative without a new quote and approval.

Tool charges belong to the user's Agensi balance and are separate from the skill purchase. Never imply
that the creator receives a share of tool-call charges.

## Local scorer

The bundled `scripts/score_candidates.py` is not an Agensi data tool. It is optional, uses only the
Python standard library, reads JSON from standard input, makes no network calls, and requires no API
key. The skill does not require the repository's Brave Search setup or a buyer-owned Brave account.
