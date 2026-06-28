#!/usr/bin/env python3
"""
04_generate_statistics.py
==========================
Phase 5 & 6: Descriptive statistics and timeline analysis.
Produces all Analysis/ CSV files.
"""

import csv
from collections import Counter, defaultdict
from pathlib import Path

ROOT     = Path(__file__).resolve().parent.parent
CLEAN    = ROOT / "Clean"
ANALYSIS = ROOT / "Analysis"
ANALYSIS.mkdir(exist_ok=True)

SOURCE = CLEAN / "youtube_history_themed.csv"

print("[04] Loading themed data...")
with open(SOURCE, newline="", encoding="utf-8-sig") as f:
    rows = list(csv.DictReader(f))

active = [r for r in rows if r.get("is_available","") == "1"]
total  = len(rows)
n_act  = len(active)
print(f"  Total rows:  {total}")
print(f"  Active rows: {n_act}")
print(f"  Unavailable: {total - n_act}")

def write_csv(path, data, fields):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(data)

# ── TOP CHANNELS ──────────────────────────────────────────────────────────────
ch_ctr = Counter(r["Channel Name"] for r in active if r.get("Channel Name","").strip())
ch_rows = []
for ch, cnt in ch_ctr.most_common(50):
    ch_r = [r for r in active if r.get("Channel Name","") == ch]
    years = sorted(set(str(r.get("added_year","")) for r in ch_r if r.get("added_year","")))
    themes = Counter(r["theme"] for r in ch_r)
    ch_rows.append({
        "rank": len(ch_rows)+1,
        "channel_name": ch,
        "video_count": cnt,
        "pct_of_active": round(cnt/n_act*100, 2),
        "primary_theme": themes.most_common(1)[0][0],
        "year_first": years[0] if years else "",
        "year_last":  years[-1] if years else "",
        "span_years": len(set(years)),
    })
write_csv(ANALYSIS / "top_channels.csv", ch_rows,
    ["rank","channel_name","video_count","pct_of_active","primary_theme",
     "year_first","year_last","span_years"])
print("  Saved: Analysis/top_channels.csv")

# ── TOP YOUTUBE CATEGORIES ────────────────────────────────────────────────────
cat_ctr = Counter(r.get("Category","").strip() for r in active if r.get("Category","").strip())
write_csv(ANALYSIS / "category_summary.csv",
    [{"category": k, "count": v, "pct": round(v/n_act*100,2)} for k,v in cat_ctr.most_common()],
    ["category","count","pct"])
print("  Saved: Analysis/category_summary.csv")

# ── DURATION BUCKETS ──────────────────────────────────────────────────────────
dur_order = ["Under 1 min","1–5 min","5–15 min","15–30 min","30–60 min","Over 60 min","Unknown"]
dur_ctr   = Counter(r.get("duration_bucket","Unknown") for r in active)
write_csv(ANALYSIS / "duration_summary.csv",
    [{"duration_bucket": d, "count": dur_ctr.get(d,0),
      "pct": round(dur_ctr.get(d,0)/n_act*100, 2)} for d in dur_order],
    ["duration_bucket","count","pct"])
print("  Saved: Analysis/duration_summary.csv")

# Long-form vs short-form
lf = sum(1 for r in active if r.get("format_type","") == "Long-Form")
sf = sum(1 for r in active if r.get("format_type","") == "Short-Form")
md = sum(1 for r in active if r.get("format_type","") == "Medium")
print(f"\n  Format split:")
print(f"    Long-form (30+ min): {lf}  ({lf/n_act*100:.1f}%)")
print(f"    Short-form (<10min): {sf}  ({sf/n_act*100:.1f}%)")
print(f"    Medium:              {md}  ({md/n_act*100:.1f}%)")

# ── AVAILABILITY ──────────────────────────────────────────────────────────────
write_csv(ANALYSIS / "availability_summary.csv",
    [{"status": "Active/Found", "count": n_act, "pct": round(n_act/total*100,2)},
     {"status": "Unavailable",  "count": total-n_act, "pct": round((total-n_act)/total*100,2)}],
    ["status","count","pct"])
print("  Saved: Analysis/availability_summary.csv")

# ── VIEW COUNT SUMMARY ────────────────────────────────────────────────────────
vc_ctr = Counter(r.get("view_bucket","Unknown") for r in active)
vc_order = ["Viral (>1M)","Large (100K–1M)","Mid (10K–100K)","Small (1K–10K)","Niche (<1K)","Unknown"]
write_csv(ANALYSIS / "view_count_summary.csv",
    [{"view_bucket": b, "count": vc_ctr.get(b,0),
      "pct": round(vc_ctr.get(b,0)/n_act*100,2)} for b in vc_order],
    ["view_bucket","count","pct"])
print("  Saved: Analysis/view_count_summary.csv")

# ── MOST VIEWED VIDEOS ────────────────────────────────────────────────────────
top_viewed = sorted(
    [r for r in active if r.get("view_count_int","0").isdigit() and int(r["view_count_int"]) > 0],
    key=lambda r: int(r["view_count_int"]), reverse=True
)[:25]
write_csv(ANALYSIS / "top_viewed_videos.csv",
    [{"rank": i+1, "title": r.get("Title",""), "channel": r.get("Channel Name",""),
      "view_count": r.get("view_count_int",""), "theme": r.get("theme",""),
      "url": r.get("YouTube URL","")}
     for i,r in enumerate(top_viewed)],
    ["rank","title","channel","view_count","theme","url"])
print("  Saved: Analysis/top_viewed_videos.csv")

# ── MOST COMMON TAGS ──────────────────────────────────────────────────────────
all_tags = []
for r in active:
    raw = r.get("Tags","").strip()
    if raw:
        all_tags.extend([t.strip().lower() for t in raw.split("|") if t.strip()])
tag_ctr = Counter(all_tags)
write_csv(ANALYSIS / "top_tags.csv",
    [{"tag": t, "count": c} for t,c in tag_ctr.most_common(50)],
    ["tag","count"])
print("  Saved: Analysis/top_tags.csv")

# ── YEARLY SUMMARY ────────────────────────────────────────────────────────────
year_data = defaultdict(list)
for r in rows:
    yr = str(r.get("added_year","")).strip()
    if yr.isdigit():
        year_data[yr].append(r)

yr_rows = []
for yr in sorted(year_data.keys()):
    yr_list = year_data[yr]
    yr_active = [r for r in yr_list if r.get("is_available","") == "1"]
    theme_ctr  = Counter(r["theme"] for r in yr_active)
    ch_ctr_yr  = Counter(r.get("Channel Name","") for r in yr_active if r.get("Channel Name",""))
    top_theme  = theme_ctr.most_common(1)[0] if theme_ctr else ("","")
    top_ch     = ch_ctr_yr.most_common(1)[0] if ch_ctr_yr else ("","")
    yr_rows.append({
        "year": yr,
        "total_added": len(yr_list),
        "active": len(yr_active),
        "unavailable": len(yr_list) - len(yr_active),
        "dominant_theme": top_theme[0],
        "dominant_theme_count": top_theme[1],
        "top_channel": top_ch[0],
        "top_channel_count": top_ch[1],
        "unique_channels": len(set(r.get("Channel Name","") for r in yr_active if r.get("Channel Name","")))
    })
write_csv(ANALYSIS / "yearly_summary.csv", yr_rows,
    ["year","total_added","active","unavailable","dominant_theme",
     "dominant_theme_count","top_channel","top_channel_count","unique_channels"])
print("  Saved: Analysis/yearly_summary.csv")

# ── MONTHLY SUMMARY ───────────────────────────────────────────────────────────
month_data = defaultdict(int)
for r in rows:
    ms = r.get("added_month_str","").strip()
    if ms:
        month_data[ms] += 1
write_csv(ANALYSIS / "monthly_summary.csv",
    [{"year_month": k, "videos_added": v} for k,v in sorted(month_data.items())],
    ["year_month","videos_added"])
print("  Saved: Analysis/monthly_summary.csv")

# ── THEME BY YEAR ─────────────────────────────────────────────────────────────
tby = defaultdict(Counter)
for r in active:
    yr = str(r.get("added_year","")).strip()
    if yr.isdigit():
        tby[yr][r["theme"]] += 1

all_themes = sorted(set(r["theme"] for r in active))
years_sorted = sorted(tby.keys())

tby_rows = []
for yr in years_sorted:
    row = {"year": yr}
    for th in all_themes:
        row[th] = tby[yr].get(th, 0)
    tby_rows.append(row)

write_csv(ANALYSIS / "theme_by_year.csv", tby_rows, ["year"] + all_themes)
print("  Saved: Analysis/theme_by_year.csv")

# ── CHANNEL BY YEAR ───────────────────────────────────────────────────────────
top20_channels = [c[0] for c in ch_ctr.most_common(20)]
cby = defaultdict(Counter)
for r in active:
    yr = str(r.get("added_year","")).strip()
    ch = r.get("Channel Name","").strip()
    if yr.isdigit() and ch in top20_channels:
        cby[yr][ch] += 1

cby_rows = []
for yr in sorted(cby.keys()):
    row = {"year": yr}
    for ch in top20_channels:
        row[ch] = cby[yr].get(ch, 0)
    cby_rows.append(row)

write_csv(ANALYSIS / "channel_by_year.csv", cby_rows, ["year"] + top20_channels)
print("  Saved: Analysis/channel_by_year.csv")

# ── PHASE SUMMARY ─────────────────────────────────────────────────────────────
phase_data = defaultdict(list)
for r in active:
    ph = r.get("life_phase_clean","").strip()
    if ph:
        phase_data[ph].append(r)

PHASE_ORDER = [
    "Phase 1: Foundation (2016–2017)",
    "Phase 2: Expansion (2018–2019)",
    "Phase 3: Deep Study (2020–2021)",
    "Phase 4: Consolidation (2022)",
    "Phase 5: Transition (2023)",
    "Phase 6: Operator/AI (2024–2026)",
]

ph_rows = []
for ph in PHASE_ORDER:
    ph_list = phase_data.get(ph, [])
    tc = Counter(r["theme"] for r in ph_list)
    cc = Counter(r.get("Channel Name","") for r in ph_list if r.get("Channel Name",""))
    top3_themes = "; ".join(f"{t}:{c}" for t,c in tc.most_common(3))
    top3_ch     = "; ".join(f"{c}:{n}" for c,n in cc.most_common(3))
    ph_rows.append({
        "phase": ph,
        "video_count": len(ph_list),
        "unique_channels": len(set(r.get("Channel Name","") for r in ph_list)),
        "unique_themes": len(set(r["theme"] for r in ph_list)),
        "top_3_themes": top3_themes,
        "top_3_channels": top3_ch,
    })

write_csv(ANALYSIS / "phase_summary.csv", ph_rows,
    ["phase","video_count","unique_channels","unique_themes","top_3_themes","top_3_channels"])
print("  Saved: Analysis/phase_summary.csv")

print("\n  Summary:")
print(f"    Total playlist entries:  {total}")
print(f"    Active:                  {n_act}")
print(f"    Unique years:            {len(year_data)}")
print(f"    Unique channels (active):{len(ch_ctr)}")

print("\n[04] DONE")
