import json
import subprocess
import sys
import zipfile
from pathlib import Path

from tools.build_agensi_skill import MAX_SCRIPT_BYTES, SKILL_NAME, build, collect_files

REPOSITORY = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPOSITORY / "agensi" / SKILL_NAME
SCORER = SKILL_ROOT / "scripts" / "score_candidates.py"


def run_scorer(payload: dict) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCORER)],
        input=json.dumps(payload),
        capture_output=True,
        check=False,
        text=True,
    )


def strong_lead(lead_id: str = "lead-1") -> dict:
    return {
        "id": lead_id,
        "business": {
            "name": "Acme Repair",
            "phone": "555-123-4567",
            "address": "123 Main St",
        },
        "candidates": [
            {
                "url": "https://acmerepair.example",
                "title": "Acme Repair",
                "phone": "+1 (555) 123-4567",
                "address": "123 Main Street",
            }
        ],
    }


def test_skill_frontmatter_and_package_files_are_valid():
    skill_text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
    assert skill_text.startswith("---\n")
    assert f"name: {SKILL_NAME}\n" in skill_text
    assert "description:" in skill_text
    assert len(collect_files(SKILL_ROOT)) <= 100
    assert SCORER.stat().st_size < MAX_SCRIPT_BYTES


def test_scorer_accepts_strong_candidate_and_rejects_third_party_host():
    blocked = strong_lead("lead-2")
    blocked["candidates"][0]["url"] = "https://www.yelp.com/biz/acme-repair"
    completed = run_scorer({"leads": [strong_lead(), blocked]})

    assert completed.returncode == 0, completed.stderr
    result = json.loads(completed.stdout)
    assert result["summary"] == {"total": 2, "website_found": 1, "inconclusive": 1}
    assert result["results"][0]["status"] == "WEBSITE_FOUND"
    assert result["results"][1]["candidates"][0]["score"] == 0
    assert result["results"][1]["requires_human_review"] is True


def test_scorer_routes_close_candidates_to_human_review():
    lead = strong_lead()
    lead["candidates"].append(
        {
            "url": "https://acme-repair.example",
            "title": "Acme Repair in Rolla",
            "phone": "555-123-4567",
            "address": "123 Main St",
        }
    )
    completed = run_scorer({"leads": [lead]})

    assert completed.returncode == 0, completed.stderr
    result = json.loads(completed.stdout)["results"][0]
    assert result["status"] == "INCONCLUSIVE"
    assert "too close" in result["reason"]


def test_scorer_rejects_duplicate_ids_and_unbounded_candidates():
    duplicate = run_scorer({"leads": [strong_lead(), strong_lead()]})
    assert duplicate.returncode == 2
    assert "ids must be unique" in duplicate.stderr

    lead = strong_lead()
    lead["candidates"] = lead["candidates"] * 51
    unbounded = run_scorer({"leads": [lead]})
    assert unbounded.returncode == 2
    assert "at most 50" in unbounded.stderr


def test_builder_creates_expected_text_only_archive(tmp_path):
    output = build(tmp_path / "skill.zip")

    with zipfile.ZipFile(output) as archive:
        names = archive.namelist()
        assert "SKILL.md" in names
        assert "scripts/score_candidates.py" in names
        assert all(not name.startswith(f"{SKILL_NAME}/") for name in names)
        assert all(Path(name).suffix in {".md", ".py"} for name in names)
        assert len(names) <= 100
