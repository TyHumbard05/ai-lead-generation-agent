# Agensi listing kit

Use this copy for the initial Agensi listing. The package itself remains
`dist/business-website-lead-audit-1.0.0.zip`.

## Core listing fields

**Title:** Business Website Lead Audit

**Summary:** Find and qualify website-redesign prospects with transparent evidence, deterministic
scoring, and mandatory human review for uncertain or no-website conclusions.

**Recommended pricing:** $5 one-time. This keeps the first release inexpensive while allowing both
card and Agensi-balance checkout. If early adoption matters more than revenue, launch free and revisit
pricing after collecting usage feedback.

**Primary category:** Sales & Lead Gen

**Additional categories:** Research & Analysis; Workflow Automation

**Compatibility note:** Requires an authorized web-search or business-search tool. Browser access is
needed only for site inspection. Python 3.11+ and terminal access are optional for deterministic
scoring. Contact enrichment is optional and off by default.

## Description

Business Website Lead Audit turns a business list or local-market brief into an evidence-backed lead
report for website redesign services. It searches for likely first-party websites, rejects directory,
map, review, and social hosts, scores identity evidence with explainable rules, and inspects confirmed
sites for observable redesign signals.

The skill preserves uncertainty. A missing search result never becomes an automatic no-website claim,
close candidates go to a human review queue, and only a person can confirm `VERIFIED_NO_WEBSITE` with
a written reason. It includes an optional standard-library Python scorer that has no network access,
contains no credentials, and produces reviewable scoring reasons.

The workflow stops at research and qualification. It does not contact prospects, send outreach,
change CRM records, bypass site controls, or collect personal contact data unless the user separately
requests an authorized contact-discovery step. Before any paid tool call, it presents the exact quote
and waits for approval.

## Tags

1. lead generation
2. website audit
3. business research
4. sales prospecting
5. local business
6. website redesign
7. lead qualification
8. sales research
9. digital agency
10. human in the loop

## Keywords

1. website redesign leads
2. business website verification
3. local business research
4. prospect research
5. first-party website
6. lead scoring
7. digital services leads
8. website audit report
9. human review queue
10. business discovery

## Use cases

1. Find local businesses with weak or missing websites.
2. Verify whether a supplied domain is a business's likely first-party website.
3. Audit an existing lead list for false website matches.
4. Prioritize website-redesign prospects using observable evidence.
5. Create a human review queue for ambiguous or possible no-website cases.
6. Gather research evidence before planning outreach.
7. Reject directory, map, review, and social pages as website matches.
8. Produce review-ready Markdown, CSV, or JSON lead reports.

## See it in action

**Request**

> Find up to 10 independent electronics-repair businesses around Rolla, Missouri that may be good
> website-redesign prospects. Verify the likely first-party site for each business, flag only problems
> you can observe, and put uncertain matches in a review queue. Do not find personal emails or contact
> anyone.

**Example result**

The audit reviewed 10 businesses and returned seven likely first-party websites, two inconclusive
records, and one human-confirmed no-website record. Each lead includes a stable ID, location, selected
domain, identity score, scoring reasons, evidence links, observed redesign signals, and confidence.

Northline Repair is marked `WEBSITE_FOUND` with a score of 105 because the phone number, business
name, address, and location agree across the candidate site and search evidence. Its redesign signals
are limited to conditions observed during the browser review: a navigation menu that fails at the
mobile breakpoint, an outdated copyright line, and no service-detail pages. A Yelp result helped
discover the business but was rejected as the selected website because it is a third-party host.

Harbor Device Clinic remains `INCONCLUSIVE` because two candidate domains both clear the 70-point
identity threshold and fall inside the 15-point ambiguity window. The report does not guess. It adds
the record to the review queue with the queries checked, both domains, their evidence, and one next
action: compare the public phone number on each contact page.

Another business has no reliable candidate after multiple query variants, but it is not automatically
labeled as having no website. It stays in the review queue until a person examines the evidence and,
if appropriate, records a reason for `VERIFIED_NO_WEBSITE`. The final summary separates verified
matches, inconclusive records, human-confirmed decisions, and leads with observable redesign signals.

## Limitations

- Search indexes can be incomplete or stale.
- Deterministic scoring verifies likely business identity, not website ownership as a legal fact.
- Website-quality findings depend on the browser and pages available during the run.
- The default matching rules are strongest for US-style phone and address data.
- Contact discovery is optional and should prefer public business channels.
- Outreach, CRM changes, and automatic no-website conclusions are not included.

## FAQ

**Does it need a Brave API key?**

No. The marketplace skill uses an authorized search tool already available to the buyer's agent. The
repository's original FastAPI application can still use Brave independently.

**Does the included script send business data anywhere?**

No. It reads JSON from standard input, scores it locally, writes JSON to standard output, and makes no
network calls.

**Can it find contacts?**

Only when the user explicitly asks and an authorized enrichment tool is available. Public business
channels are preferred and personal data should be minimized.

**Will it say a business has no website?**

Not automatically. That conclusion requires human review and a written reason.

**Can it use paid Agensi tools?**

Yes, if the creator assigns appropriate tools. The skill requires an exact quote and explicit approval
before each paid call or approved batch.

**Does it send outreach or write to a CRM?**

No. Those are separate actions and require a separate user request and authorization.

## Permissions declaration

- **Search or business-data tools:** required for discovery.
- **Browser and network:** used for search and candidate-site inspection.
- **Terminal:** optional, for the bundled deterministic scorer.
- **Standard input/output:** used by the scorer.
- **File reads:** used only for user-supplied lead data or requested report inputs.
- **File writes:** used only when the user requests a saved report.
- **Environment variables:** not required by the skill.
- **Paid tool calls:** always quoted and explicitly approved first.

## Media upload order

1. `logo-512.png` — square marketplace logo.
2. `01-overview.png` — workflow and value proposition.
3. `02-report.png` — fictional example of the review-ready report.
4. `03-safety.png` — explainable scoring and safety guardrails.

Suggested screenshot captions:

1. **From search brief to review queue:** Discover, verify, audit, and review with every conclusion
   tied to evidence.
2. **A report your team can act on:** Stable lead IDs, identity scores, observable redesign signals,
   source counts, and next actions.
3. **Deterministic where possible, human where necessary:** Transparent scoring rejects weak and
   ambiguous matches instead of guessing.

## Final upload checklist

- Upload `business-website-lead-audit-1.0.0.zip` as the skill package.
- Upload `logo-512.png` as the listing logo.
- Upload the three screenshots in the order above.
- Paste the title, summary, description, demo, compatibility note, limitations, and FAQ.
- Select the three categories and add the tags, keywords, and use cases.
- Choose pricing and confirm a payout method if the listing is paid.
- Verify every detected permission and attached service in Agensi's preview.
- Test the skill in the creator's own connected agent before submission.
- Submit for security and human review.
