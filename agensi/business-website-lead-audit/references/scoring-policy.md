# Scoring policy

Score only evidence tied to a first-party website candidate. Directory, social, map, marketplace,
and review hosts receive a score of zero.

## Identity signals

| Signal | Points | Condition |
| --- | ---: | --- |
| Exact phone | 55 | Last 10 digits match; at least 7 digits are present |
| Strong address | 20 | Normalized business address of at least 6 characters appears in candidate evidence |
| Business name in title | 30 | Full normalized name appears in the page title |
| Domain/name similarity | 15 | Normalized name contains the host or the host contains the name |
| Partial name in title | 10 | A business-name token of at least 4 characters appears in the title |
| City | 10 | Normalized values match |
| State or region | 5 | Normalized values match |
| Category | 5 | Normalized values match |

Count only one name signal: full title match, otherwise domain similarity, otherwise partial title
match.

## Decisions

- `WEBSITE_FOUND`: top score is at least 70 and exceeds the next viable candidate by more than 15.
- `INCONCLUSIVE`: no viable candidate, top score below 70, or another viable candidate is within 15
  points of the leader.
- `VERIFIED_NO_WEBSITE`: human-only transition from `INCONCLUSIVE`, with a written reason after
  reviewing the search evidence.

Common blocked hosts include Angi, BBB, Bing, Facebook, Google, Instagram, LinkedIn, MapQuest,
Nextdoor, TripAdvisor, X, Yellow Pages, and Yelp, including their subdomains. Add another host to the
blocked set when it is clearly third-party; record the reason in the report.

Scoring verifies identity, not redesign quality. Audit the selected site separately and report only
observable conditions.
