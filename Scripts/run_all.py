#!/usr/bin/env python3
"""
run_all.py
===========
Run the full YouTube History Research pipeline in order.

Usage:
    python Scripts/run_all.py

Expected input files in Raw/:
    - master_table_hydrated.csv
    - hydrated_videos.csv

Full output structure:
    YouTube Research/
        Raw/          original source files
        Clean/        cleaned and themed datasets
        Analysis/     summary CSV tables
        Charts/       PNG visualizations
        Reports/      markdown + HTML reports
        Documentation/data dictionary + classification rules
"""

import subprocess
import sys
import time
from pathlib import Path

ROOT    = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "Scripts"

PIPELINE = [
    "01_data_inspection.py",
    "02_clean_and_engineer_features.py",
    "03_classify_themes.py",
    "04_generate_statistics.py",
    "05_create_visualizations.py",
    "06_generate_reports.py",
]

def count_files(directory, ext="*"):
    d = ROOT / directory
    if not d.exists():
        return 0
    if ext == "*":
        return len(list(d.iterdir()))
    return len(list(d.glob(f"*.{ext}")))

def count_rows(csv_path):
    try:
        with open(csv_path, encoding="utf-8-sig") as f:
            return sum(1 for _ in f) - 1  # subtract header
    except:
        return 0

print("=" * 60)
print("  YouTube History Research — Full Pipeline")
print("=" * 60)
print()

total_start = time.time()
failed = []

for script in PIPELINE:
    path = SCRIPTS / script
    print(f"Running: {script}")
    print("-" * 40)
    start = time.time()
    result = subprocess.run([sys.executable, str(path)], capture_output=False)
    elapsed = round(time.time() - start, 1)

    if result.returncode != 0:
        print(f"  [ERROR] {script} failed (return code {result.returncode})")
        failed.append(script)
    else:
        print(f"  [OK] Completed in {elapsed}s")
    print()

total_elapsed = round(time.time() - total_start, 1)

# ── FINAL SUMMARY ─────────────────────────────────────────────────────────────
print("=" * 60)
print("  PIPELINE COMPLETE")
print("=" * 60)
print()

# Files created
print("  FILES CREATED:")
print(f"    Clean/     {count_files('Clean')} files")
print(f"    Analysis/  {count_files('Analysis')} files")
print(f"    Charts/    {count_files('Charts', 'png')} PNG charts")
print(f"    Reports/   {count_files('Reports')} files")
print(f"    Documentation/ {count_files('Documentation')} files")

# Row counts
print()
print("  ROW COUNTS:")
for f in ["youtube_history_clean.csv", "youtube_history_themed.csv"]:
    n = count_rows(ROOT / "Clean" / f)
    print(f"    Clean/{f}: {n:,} rows")

for f in ["top_channels.csv", "theme_summary.csv", "yearly_summary.csv",
          "monthly_summary.csv", "phase_summary.csv"]:
    n = count_rows(ROOT / "Analysis" / f)
    print(f"    Analysis/{f}: {n} rows")

print()
print(f"  Charts created:  {count_files('Charts', 'png')}")
print(f"  Reports created: {count_files('Reports')}")
print(f"  Total runtime:   {total_elapsed}s")

if failed:
    print()
    print("  FAILURES:")
    for f in failed:
        print(f"    [FAILED] {f}")
else:
    print()
    print("  All scripts completed successfully.")

print()
print("  KNOWN LIMITATIONS:")
print("    - 384 videos unavailable (deleted/private). Content unrecoverable.")
print("    - ~30% of videos have no tags. Classification uses title + channel.")
print("    - Archive reflects saves, not confirmed watch events.")
print("    - Watch Later playlist (2,434 entries) is a catch-all — theme signal weaker.")
print("    - Timestamps in UTC. Day-of-week analysis is not timezone-adjusted.")
print()
