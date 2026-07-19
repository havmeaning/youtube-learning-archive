#!/usr/bin/env python3
"""Validate publication safety and evidence integrity for the public repository."""

from __future__ import annotations

import re
import struct
import subprocess
import sys
from pathlib import Path, PurePosixPath
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parent.parent

REQUIRED_DOCUMENTS = (
    "README.md",
    "CASE_STUDY.md",
    "PROJECT_MANIFEST.md",
    "PUBLICATION_CHECKLIST.md",
    "dashboard/README.md",
    ".gitignore",
)

EXPECTED_SCREENSHOTS = (
    "knowledge_intelligence_overview.png",
    "operator_evolution_timeline.png",
    "channel_influence_map.png",
    "evidence_validation_dashboard.png",
    "skill_transfer_map.png",
    "system_architecture.png",
)

PROHIBITED_DATASET_NAMES = {
    "master_table.csv",
    "master_table_hydrated.csv",
    "hydrated_videos.csv",
    "youtube_history_clean.csv",
    "youtube_history_themed.csv",
    "top_viewed_videos.csv",
}

PROHIBITED_PARTS = {
    "raw",
    "clean",
    "takeout",
    "backups",
    "private",
    "private_powerbi",
    "local_backup_before_rebase",
}

MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")


class Results:
    def __init__(self) -> None:
        self.failures: list[str] = []
        self.warnings: list[str] = []
        self.notes: list[str] = []

    def fail(self, message: str) -> None:
        self.failures.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)

    def note(self, message: str) -> None:
        self.notes.append(message)


def git_tracked_files(results: Results) -> list[str]:
    try:
        completed = subprocess.run(
            ["git", "ls-files", "-z"],
            cwd=ROOT,
            check=True,
            capture_output=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        results.fail(f"Could not list Git tracked files: {exc}")
        return []

    return [item.decode("utf-8", errors="surrogateescape") for item in completed.stdout.split(b"\0") if item]


def png_dimensions(path: Path) -> tuple[int, int]:
    with path.open("rb") as handle:
        signature = handle.read(24)
    if len(signature) < 24 or signature[:8] != b"\x89PNG\r\n\x1a\n" or signature[12:16] != b"IHDR":
        raise ValueError("not a valid PNG header")
    return struct.unpack(">II", signature[16:24])


def check_required_documents(results: Results) -> None:
    for relative in REQUIRED_DOCUMENTS:
        if not (ROOT / relative).is_file():
            results.fail(f"Required documentation file is missing: {relative}")


def check_tracked_names(tracked: list[str], results: Results) -> None:
    for name in tracked:
        path = PurePosixPath(name.replace("\\", "/"))
        lowered_parts = {part.lower() for part in path.parts[:-1]}
        basename = path.name.lower()

        if lowered_parts & PROHIBITED_PARTS:
            results.fail(f"Tracked path uses a prohibited private-data directory: {name}")
        if basename in PROHIBITED_DATASET_NAMES:
            results.fail(f"Tracked prohibited row-level dataset filename: {name}")
        if basename.endswith(".pbix"):
            results.fail(f"Tracked Power BI source file: {name}")
        if basename == ".env" or basename.startswith(".env."):
            results.fail(f"Tracked environment file: {name}")
        if re.search(r"(?i)(api[_-]?key|row[_-]?level)", basename):
            results.fail(f"Tracked filename matches a prohibited safety pattern: {name}")


def check_screenshots(tracked: list[str], results: Results) -> None:
    screenshot_dir = ROOT / "dashboard" / "screenshots"
    tracked_set = {name.replace("\\", "/") for name in tracked}

    for filename in EXPECTED_SCREENSHOTS:
        relative = f"dashboard/screenshots/{filename}"
        path = ROOT / relative
        if relative not in tracked_set or not path.is_file():
            results.warn(f"Expected dashboard screenshot is missing: {relative}")
            continue

        try:
            width, height = png_dimensions(path)
        except (OSError, ValueError) as exc:
            results.fail(f"Could not inspect {relative}: {exc}")
            continue

        size = path.stat().st_size
        results.note(f"Screenshot {filename}: {width}x{height}, {size} bytes")
        if width <= 16 or height <= 16 or size < 256:
            results.fail(f"Placeholder or invalid dashboard screenshot detected: {relative} ({width}x{height}, {size} bytes)")
        elif width < 800 or height < 450:
            results.warn(f"Suspiciously small dashboard screenshot: {relative} ({width}x{height})")

    expected = set(EXPECTED_SCREENSHOTS)
    if screenshot_dir.is_dir():
        for path in screenshot_dir.iterdir():
            if path.is_file() and path.suffix.lower() == ".png" and path.name not in expected:
                results.warn(f"Non-canonical dashboard screenshot filename: dashboard/screenshots/{path.name}")

    for name in tracked:
        if not name.lower().endswith(".png"):
            continue
        path = ROOT / name
        try:
            width, height = png_dimensions(path)
        except (OSError, ValueError):
            continue
        if width == 1 and height == 1:
            results.fail(f"Tracked 1x1 PNG detected: {name}")


def normalize_link_target(raw_target: str) -> str:
    target = raw_target.strip()
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1]
    return unquote(target.split("#", 1)[0])


def check_markdown_links(tracked: list[str], results: Results) -> None:
    for name in tracked:
        if not name.lower().endswith(".md"):
            continue
        path = ROOT / name
        try:
            content = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            results.fail(f"Could not read Markdown as UTF-8: {name}: {exc}")
            continue

        for match in MARKDOWN_LINK.finditer(content):
            raw_target = match.group(1).strip()
            if not raw_target or raw_target.startswith("#") or re.match(r"^(?:https?://|mailto:)", raw_target, re.I):
                continue
            target = normalize_link_target(raw_target)
            if not target:
                continue
            resolved = (path.parent / target).resolve()
            try:
                resolved.relative_to(ROOT.resolve())
            except ValueError:
                results.fail(f"Relative Markdown link escapes the repository: {name} -> {raw_target}")
                continue
            if not resolved.exists():
                results.fail(f"Broken relative Markdown link: {name} -> {raw_target}")


def print_section(title: str, entries: list[str]) -> None:
    print(f"\n{title} ({len(entries)})")
    if entries:
        for entry in entries:
            print(f"  - {entry}")
    else:
        print("  - none")


def main() -> int:
    results = Results()
    tracked = git_tracked_files(results)

    check_required_documents(results)
    check_tracked_names(tracked, results)
    check_screenshots(tracked, results)
    check_markdown_links(tracked, results)

    results.note(f"Git tracked-file count: {len(tracked)}")
    print("YouTube Learning Archive public-release validation")
    print_section("NOTES", results.notes)
    print_section("WARNINGS", results.warnings)
    print_section("FAILURES", results.failures)

    if results.failures:
        print("\nRESULT: FAIL")
        return 1
    print("\nRESULT: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
