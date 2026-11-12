---
name: business-website-lead-audit
description: Researches businesses, identifies likely first-party websites, and produces evidence-backed website-redesign lead reports without treating missing search results as proof. Use when the user asks to find businesses that may need a website, verify business websites, qualify redesign prospects, or audit a lead list.
---

# Business website lead audit

Research businesses and qualify possible website-redesign leads. Keep discovery evidence separate
from conclusions, use deterministic checks where possible, and route uncertainty to a person.

## Boundaries

- Do not conclude that a business has no website from one query or from missing results.
- Do not treat directory, social, map, marketplace, or review pages as first-party websites.
- Do not invent business facts, contact details, page findings, or tool results.
- Do not contact prospects, send messages, or add records to a CRM unless the user separately asks.
- Do not bypass access controls, robots rules, rate limits, or a site's terms.
- Before any paid tool call, show the quoted price and obtain the user's explicit approval.
- Minimize personal data. Prefer public business contact channels and honor the requested geography.

## Workflow

1. Establish scope. Ask only for missing details that materially affect the result: business list or
   search area, business category, maximum leads, desired output, and whether contact discovery is
   included. Use the conservative defaults in [references/configuration.md](references/configuration.md)
   when the user has no preference.
2. Inspect the tools attached to this Agensi listing with `skill_tools`. A web or business search
   tool is required for discovery. Company enrichment and contact discovery are optional and should
   be used only when the user's request needs them. Follow the routing rules in
   [references/tool-routing.md](references/tool-routing.md). Never ask the user to put credentials in
   a report or project file.
3. Discover candidates with at least two materially different queries per business when the first
   query is inconclusive. Include name plus location, then add phone, street, or category when known.
4. Separate first-party candidates from third-party evidence. Preserve the result URL, title,
   snippet, query, and matching identity fields. A directory may supply a clue but cannot be the
   selected website.
5. Score candidates. When Python 3.11+ and terminal access are available, run
   `scripts/score_candidates.py` exactly as shipped with JSON on standard input. Otherwise apply
   [references/scoring-policy.md](references/scoring-policy.md) directly. The input and output
   shapes are in [references/input-schema.md](references/input-schema.md).
6. Inspect the likely first-party site only when browser access is authorized. Record observable
   redesign signals such as broken navigation, missing HTTPS, poor mobile behavior, stale content,
   inaccessible forms, or missing contact information. Do not infer a problem that was not observed.
7. Classify each business as `WEBSITE_FOUND` or `INCONCLUSIVE`. Only a person may change an
   inconclusive result to `VERIFIED_NO_WEBSITE`, and the confirmation must include a reason.
8. Deliver the result using [templates/lead-report.md](templates/lead-report.md). Cite source links,
   distinguish facts from recommendations, and place uncertain records in a review queue.

## Quality gate

Before delivery, confirm that every lead has a stable ID, source links, a decision reason, and no
unsupported claim. Deduplicate by normalized business identity and first-party domain. If the user
asked for outreach-ready data, remind them that a human should review it and that outreach must
follow applicable privacy, platform, and anti-spam rules.
