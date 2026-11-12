# Agensi publishing guide

This repository keeps the Agensi marketplace artifact separate from the FastAPI application. The
source package is `agensi/business-website-lead-audit`; the generated ZIP is not committed.

The final listing copy, tags, use cases, FAQ, permissions declaration, pricing recommendation, and
media upload order are in [`agensi-listing-kit.md`](agensi-listing-kit.md). The logo and screenshots
are in [`agensi-media/`](agensi-media/).

Requirements below were checked against Agensi's current documentation on November 10, 2026:

- [Package your skill](https://www.agensi.io/docs/packaging)
- [Submit on the website](https://www.agensi.io/docs/submit-on-the-website)
- [Review and approval](https://www.agensi.io/docs/review-and-approval)
- [Creator quickstart](https://www.agensi.io/docs/creator-quickstart)

## Build and validate

Requires Python 3.11 or newer.

```bash
python tools/build_agensi_skill.py
pytest tests/test_agensi_skill.py -q
ruff check .
ruff format --check .
```

The builder creates `dist/business-website-lead-audit-1.0.0.zip`. It rejects non-text files,
symlinks, scripts over 20 KB, missing `SKILL.md`, and archives over Agensi's 5 MB agent-upload
limit. `SKILL.md`, `scripts/`, `references/`, and `templates/` sit directly at the ZIP root.

## Listing draft

**Name:** Business Website Lead Audit

**Summary:** Find and qualify website-redesign prospects with transparent evidence, deterministic
scoring, and mandatory human review for uncertain or no-website conclusions.

**Primary category:** Sales & Lead Gen

**Additional categories:** Research & Analysis; Workflow Automation

**Compatibility note:** Requires one web-search, business-search, or company-discovery tool attached
to the listing in Agensi. Browser access is needed only for site inspection. Python 3.11+ and
terminal access are optional for deterministic scoring. Contact enrichment is optional and off by
default. No buyer-owned Brave API account is required.

**Suggested price:** $5 one-time. This keeps the first release inexpensive while allowing card and
Agensi-balance checkout. A paid listing requires a configured payout method.

### Description

Business Website Lead Audit turns a business list or local-market brief into an evidence-backed lead
report for website redesign services. It searches for likely first-party websites, rejects directory
and social hosts, scores identity evidence with explainable rules, and inspects confirmed sites for
observable redesign signals.

The skill preserves uncertainty. A missing result never becomes an automatic no-website claim, close
candidates go to a human review queue, and only a person can confirm `VERIFIED_NO_WEBSITE` with a
written reason. It can use an optional standard-library Python scorer that has no network access and
contains no credentials.

It stops at research and qualification. It does not contact prospects, send outreach, change CRM
records, bypass site controls, or collect personal contact data unless the user separately requests
an authorized contact-discovery step.

### See it in action

**Request:** Find up to 10 independent electronics-repair businesses around Rolla, Missouri that may
be good website-redesign prospects. Verify the likely first-party site for each business, flag only
problems you can observe, and put uncertain matches in a review queue. Do not find personal emails or
contact anyone.

**Example result:** The report lists each business with a stable lead ID, location, selected domain,
identity score, evidence links, observed redesign signals, and confidence. One business is marked
`WEBSITE_FOUND` because the phone number, business name, and location agree across the first-party
site and public search evidence. A Yelp page is retained only as a discovery clue and is rejected as
the business website. Another record remains `INCONCLUSIVE` because two domains score within the
15-point ambiguity window; the next action is to compare the phone number on each contact page. A
third business has no reliable candidate after multiple query variants, but it is not labeled as
having no website. It remains in the human review queue with the queries and sources checked. The
summary counts verified websites, inconclusive records, and leads with observed redesign signals,
then states the search and freshness limitations.

### Limitations

- Search indexes can be incomplete or stale.
- Deterministic scoring verifies likely business identity, not website ownership as a legal fact.
- Website-quality findings depend on the browser and pages available during the run.
- The default matching rules are strongest for US-style phone and address data.
- No outreach, CRM mutation, or automatic no-website conclusion is included.

### FAQ

**Does it need a Brave API key?** No. The skill uses an authorized search tool already available to
the buyer's agent. The original application can still use Brave independently.

**Does the script send business data anywhere?** No. It reads JSON from standard input, scores it
locally, writes JSON to standard output, and makes no network calls.

**Can it find contacts?** Only when the user explicitly asks and an authorized enrichment tool is
available. Public business channels are preferred; personal data should be minimized.

**Will it say a business has no website?** Not automatically. That conclusion requires human review
and a written reason.

## Permissions to verify in the preview

- Search or business-data tool access: required for discovery.
- Browser and network access: required only for search and candidate-site inspection.
- Terminal: optional, for the bundled scorer.
- Standard input/output: used by the scorer.
- File writes: not required by the skill unless the user requests a saved report.
- Environment variables: not required by the skill.

## Submission checklist

1. Create or sign in to Agensi, enable Creator Mode, and complete the creator profile.
2. Configure Stripe Connect or Zoneless before choosing paid pricing. Free listings do not require a
   payout method.
3. Confirm that `Business Website Lead Audit` is still unique; Agensi names are unique.
4. Run the repository checks and build the ZIP from the commit being submitted.
5. Upload the ZIP at <https://www.agensi.io/dashboard/submit>.
6. Paste the listing draft, choose categories and pricing, and add a 512 x 512 square logo if desired.
7. In the preview, verify detected permissions and declare every service the skill needs.
8. Attach at least one search or company-discovery tool. Optionally attach one company-enrichment tool
   and one contact provider such as Hunter, Apollo, or ContactOut. Choose only tools the workflow
   actually uses; Agensi allows at most 10 tools per skill.
9. Test the preview in the creator's own agent. Confirm that paid calls are quoted and approved before
   execution and that ambiguous evidence stays inconclusive.
10. Submit for security and human review. Allow up to 48 hours and address any reported finding before
    resubmitting a changed ZIP.

## Outstanding creator decisions

- Free, one-time, or subscription pricing.
- Whether to attach Agensi-hosted search or enrichment tools, and which specific tools to use.
- Logo and optional screenshots/video.
- Final creator profile and payout setup.
