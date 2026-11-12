# Deterministic scorer interface

Pass one JSON object to `scripts/score_candidates.py` on standard input:

```json
{
  "leads": [
    {
      "id": "lead-001",
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
          "url": "https://acmerepair.example",
          "title": "Acme Repair",
          "phone": "+1 555 123 4567",
          "address": "123 Main Street",
          "city": "Rolla",
          "state": "MO",
          "category": "Electronics Repair"
        }
      ]
    }
  ]
}
```

Required fields are `leads`, a unique non-empty `id`, `business.name`, `candidates`, and each
candidate `url`. Other identity fields are optional strings. The script accepts 1 to 100 leads and
up to 50 candidates per lead. Candidate URLs must use HTTP or HTTPS.

Example execution:

```text
python score_candidates.py < scorer-input.json
```

The output contains summary counts plus each lead's status, scored candidates, best candidate,
human-review flag, and decision reason. A validation problem returns a non-zero exit code and a
short error on standard error. The script performs no search and makes no network requests.
