# AI Lead Generation Agent

An AI-assisted workflow for researching businesses that may be good candidates for website redesign or other digital services.

The project focuses on combining automated discovery, deterministic scoring, first-party contact enrichment, and human review so that automation helps with research without presenting uncertain results as facts.

## Current Capabilities

- Business candidate discovery
- Website-presence verification
- Contact enrichment from first-party sources
- Candidate scoring based on multiple identity signals
- Rejection of social networks, map pages, and directory sites as official websites
- Human-review flow for ambiguous or uncertain results

## Website Verification

The verification workflow scores possible website matches using signals such as:

- Phone-number matches
- Address similarity
- Business-name similarity
- Page-title identity
- City and state matches
- Category similarity
- Domain-name similarity

Automated checks are intentionally conservative. The system can identify a likely website or mark a result as inconclusive, while stronger negative conclusions require explicit human confirmation.

## Contact Enrichment

The enrichment workflow is designed to:

- Stay on the same registrable domain
- Inspect a limited number of relevant pages
- Respect `robots.txt`
- Look for first-party contact information
- Avoid treating unrelated third-party listings as authoritative

## Why I Built It

This project is an experiment in building AI and automation systems that do more than generate text. It explores how software can gather evidence, apply structured rules, call external services, and route uncertain decisions to a human.

## Areas Explored

- AI-agent workflows
- API integration
- Search and data enrichment
- Deterministic scoring
- Human-in-the-loop design
- Data validation
- Automation safeguards
- Modular software architecture

## Status

**Active development.**

The system is being developed incrementally, with an emphasis on reliability and clear separation between verified, inferred, and inconclusive information.

## Responsible Use

This project is intended for legitimate business research and outreach. Automated findings should be reviewed before contacting businesses, and outreach should follow applicable platform rules, privacy requirements, and anti-spam laws.
