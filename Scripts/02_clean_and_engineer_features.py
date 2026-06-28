#!/usr/bin/env python3
"""
02_clean_and_engineer_features.py
===================================
Phase 3: Clean data and add derived features.
Produces:
  - Clean/youtube_history_clean.csv
"""

import csv
import math
import re
from datetime import datetime
from pathlib import Path

ROOT  = Path(__file__).resolve().parent.parent
RAW   = ROOT / "Raw"
CLEAN = ROOT / "Clean"
CLEAN.mkdir(exist_ok=True)

MASTER = RAW / "master_table_hydrated.csv"

ISO_DUR = re.compile(r"^PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?$")

def parse_duration_seconds(s):
    if not s:
        return 0
    m = ISO_DUR.match(s.strip())
    if not m:
        return 0
    h = int(m.group(1) or 0)
    mn = int(m.group(2) or 0)
    sc = int(m.group(3) or 0)
    return h * 3600 + mn * 60 + sc

def duration_bucket(sec):
    if sec == 0:         return "Unknown"
    if sec < 60:         return "Under 1 min"
    if sec < 300:        return "1–5 min"
    if sec < 900:        return "5–15 min"
    if sec < 1800:       return "15–30 min"
    if sec < 3600:       return "30–60 min"
    return "Over 60 min"

def view_bucket(n):
    if n == 0:           return "Unknown"
    if n < 1000:         return "Niche (<1K)"
    if n < 10000:        return "Small (1K–10K)"
    if n < 100000:       return "Mid (10K–100K)"
    if n < 1000000:      return "Large (100K–1M)"
    return "Viral (>1M)"

def likely_content_type(dur_sec, category, title):
    title_l = (title or "").lower()
    cat_l   = (category or "").lower()

    if any(k in title_l for k in ["podcast","episode","ep.","#","interview","show"]):
        return "Podcast"
    if any(k in cat_l for k in ["music"]):
        return "Music"
    if any(k in title_l for k in ["news","breaking","report","update","explained"]):
        return "News/Commentary"
    if dur_sec >= 3600:
        return "Long-Form Educational"
    if dur_sec >= 1200:
        return "Educational"
    if dur_sec < 300:
        return "Short Clip"
    return "Tutorial/How-To"

LIFE_PHASES = [
    ("2016-01-01", "2017-12-31", "Phase 1: Foundation (2016–2017)"),
    ("2018-01-01", "2019-12-31", "Phase 2: Expansion (2018–2019)"),
    ("2020-01-01", "2021-12-31", "Phase 3: Deep Study (2020–2021)"),
    ("2022-01-01", "2022-12-31", "Phase 4: Consolidation (2022)"),
    ("2023-01-01", "2023-12-31", "Phase 5: Transition (2023)"),
    ("2024-01-01", "2099-12-31", "Phase 6: Operator/AI (2024–2026)"),
]

def get_phase(ts):
    if not ts:
        return "Unknown"
    try:
        d = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        ds = d.strftime("%Y-%m-%d")
        for start, end, label in LIFE_PHASES:
            if start <= ds <= end:
                return label
    except:
        pass
    return "Unknown"

print("[02] Loading master table...")
with open(MASTER, newline="", encoding="utf-8-sig") as f:
    rows = list(csv.DictReader(f))
print(f"  Rows loaded: {len(rows)}")

enriched = []
for r in rows:
    e = dict(r)

    # — Added Timestamp features —
    ts_str = r.get("Added Timestamp", "").strip()
    ts = None
    try:
        ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
    except:
        pass

    e["added_year"]     = ts.year        if ts else ""
    e["added_month"]    = ts.month       if ts else ""
    e["added_month_str"]= ts.strftime("%Y-%m") if ts else ""
    e["added_quarter"]  = f"{ts.year}-Q{math.ceil(ts.month/3)}" if ts else ""
    e["added_weekday"]  = ts.strftime("%A") if ts else ""
    e["added_hour"]     = ts.hour        if ts else ""

    # — Published At features —
    pub_str = r.get("Published At", "").strip()
    pub = None
    try:
        pub = datetime.fromisoformat(pub_str.replace("Z", "+00:00"))
    except:
        pass

    e["pub_year"]  = pub.year  if pub else ""
    e["pub_month"] = pub.month if pub else ""

    # — Video age at time of save —
    if ts and pub:
        age_days = max(0, (ts - pub).days)
        e["video_age_days"] = age_days
        if age_days < 7:      e["age_bucket"] = "< 1 week"
        elif age_days < 30:   e["age_bucket"] = "< 1 month"
        elif age_days < 365:  e["age_bucket"] = "1–12 months"
        elif age_days < 1095: e["age_bucket"] = "1–3 years"
        else:                  e["age_bucket"] = "> 3 years"
    else:
        e["video_age_days"] = ""
        e["age_bucket"]     = "Unknown"

    # — Duration —
    dur_s = parse_duration_seconds(r.get("Duration", ""))
    # If Duration Seconds column already populated, prefer it
    ds_col = r.get("Duration Seconds", "").strip()
    if ds_col.isdigit():
        dur_s = int(ds_col)
    e["duration_s"]      = dur_s
    e["duration_bucket"] = duration_bucket(dur_s)
    e["format_type"]     = ("Long-Form" if dur_s >= 1800
                            else "Short-Form" if dur_s > 0 and dur_s < 600
                            else "Medium" if dur_s > 0
                            else "Unknown")

    # — View count —
    vc_raw = r.get("View Count", "").strip()
    vc = int(vc_raw) if vc_raw.isdigit() else 0
    e["view_count_int"]  = vc
    e["view_bucket"]     = view_bucket(vc)

    # — Title features —
    title = r.get("Title", "").strip()
    e["title_word_count"] = len(title.split()) if title else 0

    # — Tag count —
    tags = r.get("Tags", "").strip()
    e["tag_count"] = len([t for t in tags.split("|") if t.strip()]) if tags else 0

    # — Availability —
    e["is_available"] = 1 if r.get("Status", "").strip() == "found" else 0

    # — Content type —
    e["content_type"] = likely_content_type(
        dur_s, r.get("Category", ""), title
    )

    # — Life phase (re-derived from timestamp for consistency) —
    e["life_phase_clean"] = get_phase(ts_str)

    enriched.append(e)

# ── OUTPUT COLUMNS ────────────────────────────────────────────────────────────
OUT_COLS = [
    "Video ID","Playlist","Added Timestamp","Status","is_available",
    "added_year","added_month","added_month_str","added_quarter",
    "added_weekday","added_hour",
    "life_phase_clean",
    "Title","Channel Name","Channel ID",
    "Published At","pub_year","pub_month",
    "video_age_days","age_bucket",
    "Category","Duration","duration_s","duration_bucket","format_type",
    "View Count","view_count_int","view_bucket",
    "Like Count","Tags","tag_count","title_word_count",
    "content_type","YouTube URL",
]

with open(CLEAN / "youtube_history_clean.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=OUT_COLS, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(enriched)

found     = sum(1 for r in enriched if r["is_available"])
not_found = len(enriched) - found
print(f"  Active rows:      {found}")
print(f"  Unavailable rows: {not_found}")
print(f"  Output columns:   {len(OUT_COLS)}")
print(f"\n  Saved: Clean/youtube_history_clean.csv")
print("\n[02] DONE")
