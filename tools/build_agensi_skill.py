#!/usr/bin/env python3
"""Build a deterministic, text-only Agensi skill archive."""

from __future__ import annotations

import argparse
import os
import zipfile
from pathlib import Path

SKILL_NAME = "business-website-lead-audit"
VERSION = "1.0.0"
MAX_PACKAGE_BYTES = 5 * 1024 * 1024
MAX_SCRIPT_BYTES = 20 * 1024
ALLOWED_SUFFIXES = {".json", ".md", ".py", ".txt", ".yaml", ".yml"}


def collect_files(source: Path) -> list[Path]:
    files: list[Path] = []
    for path in sorted(source.rglob("*")):
        if "__pycache__" in path.parts:
            continue
        if path.is_symlink():
            raise ValueError(f"symbolic links are not allowed: {path}")
        if not path.is_file():
            continue
        if path.suffix.lower() not in ALLOWED_SUFFIXES:
            raise ValueError(f"non-text file type is not allowed: {path}")
        data = path.read_bytes()
        data.decode("utf-8")
        if path.parent.name == "scripts" and len(data) > MAX_SCRIPT_BYTES:
            raise ValueError(f"skill script exceeds 20 KB: {path}")
        files.append(path)
    if source / "SKILL.md" not in files:
        raise ValueError("SKILL.md is required")
    return files


def build(output: Path) -> Path:
    repository = Path(__file__).resolve().parents[1]
    source = repository / "agensi" / SKILL_NAME
    files = collect_files(source)
    output.parent.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in files:
            relative = path.relative_to(source)
            archive_name = Path(SKILL_NAME) / relative
            info = zipfile.ZipInfo(archive_name.as_posix(), date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (0o644 & 0xFFFF) << 16
            archive.writestr(info, path.read_bytes())

    if output.stat().st_size > MAX_PACKAGE_BYTES:
        output.unlink(missing_ok=True)
        raise ValueError("archive exceeds the 5 MB agent-upload limit")
    return output


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    default = Path("dist") / f"{SKILL_NAME}-{VERSION}.zip"
    parser.add_argument("--output", type=Path, default=default)
    return parser.parse_args()


def main() -> int:
    output = build(parse_args().output.resolve())
    print(os.fspath(output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
