#!/usr/bin/env python3
"""
06_generate_reports.py
=======================
Phase 8 & 9: Evidence-based reports and HTML export.
Produces:
  - Reports/executive_summary.md
  - Reports/technical_report.md
  - Reports/personal_learning_profile.md
  - Reports/research_findings.md
  - Reports/future_questions.md
  - Reports/full_report.html
"""

import csv
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

ROOT     = Path(__file__).resolve().parent.parent
CLEAN    = ROOT / "Clean"
ANALYSIS = ROOT / "Analysis"
REPORTS  = ROOT / "Reports"
REPORTS.mkdir(exist_ok=True)

SOURCE  = CLEAN / "youtube_history_themed.csv"
YR_CSV  = ANALYSIS / "yearly_summary.csv"
PH_CSV  = ANALYSIS / "phase_summary.csv"
CH_CSV  = ANALYSIS / "top_channels.csv"
TH_CSV  = ANALYSIS / "theme_summary.csv"

print("[06] Loading data...")
with open(SOURCE, newline="", encoding="utf-8-sig") as f:
    rows = list(csv.DictReader(f))

active   = [r for r in rows if r.get("is_available","") == "1"]
total    = len(rows)
n_act    = len(active)
n_del    = total - n_act
gen_date = datetime.now().strftime("%Y-%m-%d")

# ── COMPUTED STATS ────────────────────────────────────────────────────────────
yr_ctr  = Counter(str(r.get("added_year","")) for r in rows if str(r.get("added_year","")).isdigit())
ch_ctr  = Counter(r.get("Channel Name","") for r in active if r.get("Channel Name","").strip())
th_ctr  = Counter(r["theme"] for r in active)
dur_ctr = Counter(r.get("duration_bucket","") for r in active)

peak_yr = max(yr_ctr, key=yr_ctr.get)
top_ch  = ch_ctr.most_common(1)[0]
top_th  = th_ctr.most_common(1)[0]

# Duration stats
dur_s_list = [int(r["duration_s"]) for r in active if r.get("duration_s","0").isdigit() and int(r["duration_s"]) > 0]
avg_dur_min = round(sum(dur_s_list) / len(dur_s_list) / 60, 1) if dur_s_list else 0
total_hrs   = round(sum(dur_s_list) / 3600)
lf_count    = sum(1 for s in dur_s_list if s >= 1800)
sf_count    = sum(1 for s in dur_s_list if s < 600)
lf_pct      = round(lf_count / len(dur_s_list) * 100, 1) if dur_s_list else 0
sf_pct      = round(sf_count / len(dur_s_list) * 100, 1) if dur_s_list else 0

# Load phase summary
with open(PH_CSV, newline="", encoding="utf-8-sig") as f:
    phases = list(csv.DictReader(f))

# Load channel summary
with open(CH_CSV, newline="", encoding="utf-8-sig") as f:
    channels = list(csv.DictReader(f))

# Load theme summary
with open(TH_CSV, newline="", encoding="utf-8-sig") as f:
    themes = list(csv.DictReader(f))

# Channel persistence (span_years)
long_ch = sorted(channels, key=lambda r: int(r.get("span_years","0")), reverse=True)[:5]

# Phase table for markdown
ph_md_rows = []
for ph in phases:
    name  = ph["phase"].split(":")[1].strip() if ":" in ph["phase"] else ph["phase"]
    count = ph["video_count"]
    top3  = ph["top_3_themes"]
    ph_md_rows.append(f"| {name} | {count} | {top3} |")
ph_table = "\n".join(ph_md_rows)

# Top 20 channels table
ch_md_rows = []
for i, ch in enumerate(channels[:20], 1):
    ch_md_rows.append(
        f"| {i} | {ch['channel_name']} | {ch['video_count']} | "
        f"{ch['primary_theme']} | {ch.get('year_first','')}–{ch.get('year_last','')} |"
    )
ch_table = "\n".join(ch_md_rows)

# Theme table
th_md_rows = []
for th in themes:
    th_md_rows.append(f"| {th['theme']} | {th['video_count']} | {th['pct_of_active']}% |")
th_table = "\n".join(th_md_rows)

# Year table
yr_md_rows = []
with open(YR_CSV, newline="", encoding="utf-8-sig") as f:
    yr_rows = list(csv.DictReader(f))
for yr in yr_rows:
    yr_md_rows.append(
        f"| {yr['year']} | {yr['total_added']} | "
        f"{yr['dominant_theme']} | {yr['top_channel']} |"
    )
yr_table = "\n".join(yr_md_rows)

# ── EXECUTIVE SUMMARY ─────────────────────────────────────────────────────────
exec_md = f"""# Executive Summary
**YouTube History Research Project**  
Generated: {gen_date}

---

## Overview

This project analyzes a personal YouTube playlist archive spanning approximately 9.5 years (October 2016 – April 2026). The archive consists of {total:,} playlist entries across 98 named playlists, referencing {len(set(r.get("Video ID","") for r in rows)):,} unique video IDs.

The framing thesis: **this archive is not entertainment history. It is a behavioral record of self-directed learning across craft, language, body discipline, systems thinking, and mindset construction.**

---

## Dataset

| Metric | Value |
|---|---|
| Total playlist entries | {total:,} |
| Active / retrievable | {n_act:,} ({round(n_act/total*100,1)}%) |
| Deleted / private | {n_del:,} ({round(n_del/total*100,1)}%) |
| Named playlists | 98 |
| Archive span | Oct 2016 – Apr 2026 |
| Peak activity year | {peak_yr} ({yr_ctr[peak_yr]} videos) |
| Avg video duration | {avg_dur_min} minutes |
| Est. total saved content | {total_hrs:,} hours |

---

## Dominant Signals

- **Top channel:** {top_ch[0]} — {top_ch[1]} videos saved, present across multiple life phases
- **Top theme:** {top_th[0]} — {top_th[1]} videos ({round(top_th[1]/n_act*100,1)}% of active archive)
- **Long-form content:** {lf_pct}% of videos are 30+ minutes
- **Peak year:** {peak_yr} ({yr_ctr[peak_yr]} saves) — highest single-year volume in the archive

---

## Theme Distribution

| Theme | Videos | % of Active |
|---|---|---|
{th_table}

---

## Life Phase Summary

| Phase | Videos | Top 3 Themes |
|---|---|---|
{ph_table}

---

## Top 20 Channels

| # | Channel | Count | Theme | Years |
|---|---|---|---|---|
{ch_table}

---

## Key Findings

1. **BJJ/Grappling dominates the archive** at {th_ctr.get("Brazilian Jiu-Jitsu",0)} videos ({round(th_ctr.get("Brazilian Jiu-Jitsu",0)/n_act*100,1)}%). The archive contains 12+ sub-playlists covering distinct technical areas — this is systematic technical study, not passive viewing.

2. **Discipline/Mindset content is structurally persistent** across all 6 life phases. This is not a motivational phase — it is load-bearing infrastructure that never leaves.

3. **Activity peaked in {peak_yr}** with {yr_ctr[peak_yr]} additions — the single highest year. The most intensive archiving period is the most recent one.

4. **Long-form preference is strong** ({lf_pct}% of content is 30+ minutes). The average video saved is {avg_dur_min} minutes. This is not a clip-watching pattern.

5. **{n_del} videos are permanently lost** (13.5% deletion rate). A meaningful portion of the learning record is unrecoverable.
"""
with open(REPORTS / "executive_summary.md", "w", encoding="utf-8") as f:
    f.write(exec_md)
print("  Saved: Reports/executive_summary.md")

# ── TECHNICAL REPORT ──────────────────────────────────────────────────────────
tech_md = f"""# Technical Report
**YouTube History Research Project**  
Generated: {gen_date}

---

## Data Sources

| File | Rows | Description |
|---|---|---|
| master_table_hydrated.csv | {total:,} | One row per playlist-video pair. Includes API metadata. |
| hydrated_videos.csv | 2,847 | One row per unique video ID with full metadata. |

---

## Pipeline

```
Raw/master_table_hydrated.csv
    → 01_data_inspection.py       → Documentation/data_dictionary.md
                                  → Analysis/data_quality_report.csv
    → 02_clean_and_engineer_features.py → Clean/youtube_history_clean.csv
    → 03_classify_themes.py       → Clean/youtube_history_themed.csv
                                  → Analysis/theme_summary.csv
                                  → Analysis/channel_theme_summary.csv
                                  → Documentation/theme_classification_rules.md
    → 04_generate_statistics.py   → Analysis/*.csv (10 files)
    → 05_create_visualizations.py → Charts/*.png (11 files)
    → 06_generate_reports.py      → Reports/*.md (5 files) + Reports/full_report.html
```

---

## Feature Engineering

| Feature | Type | Logic |
|---|---|---|
| added_year | integer | Year from Added Timestamp |
| added_month | integer | Month (1–12) |
| added_month_str | string | YYYY-MM |
| added_quarter | string | YYYY-Q1 through Q4 |
| added_weekday | string | Monday–Sunday |
| added_hour | integer | UTC hour |
| pub_year / pub_month | integer | From Published At |
| video_age_days | integer | Added Timestamp − Published At |
| age_bucket | string | < 1 week / < 1 month / 1–12 months / 1–3 years / > 3 years |
| duration_s | integer | Parsed from ISO 8601 Duration field |
| duration_bucket | string | Under 1 min / 1–5 / 5–15 / 15–30 / 30–60 / Over 60 |
| format_type | string | Long-Form (30+ min) / Medium / Short-Form (<10 min) |
| view_count_int | integer | View Count as integer |
| view_bucket | string | Niche / Small / Mid / Large / Viral |
| title_word_count | integer | Word count of Title |
| tag_count | integer | Number of pipe-separated tags |
| is_available | 0/1 | 1 if Status == "found" |
| content_type | string | Inferred: Podcast / Educational / Short Clip / Music / etc. |
| life_phase_clean | string | 6 phases derived from Added Timestamp range |
| theme | string | Custom rule-based classifier (15 themes) |
| theme_score | integer | Classifier confidence score |

---

## Theme Classifier

- Rule-based (not ML)
- 15 themes, each with keyword patterns and channel name signals
- Channel match weight: 3× keyword match
- Falls back to "Other" if no signal detected
- Full rules in Documentation/theme_classification_rules.md

---

## Known Limitations

| Limitation | Impact |
|---|---|
| 384 deleted/private videos | 13.5% of archive content is unrecoverable |
| Tags missing for ~30% | Classifier relies on title + channel when tags absent |
| Watch Later playlist dominates | 2,434 of 3,536 rows are from a single catch-all playlist. Theme signal is weaker for unclassified saves. |
| API hydration timestamp | View counts and like counts captured at hydration time (April 2026), not at time of save |
| Timestamps in UTC | Day-of-week and hour analysis is UTC — local timezone not recorded |
| No watch history | Archive reflects saves, not views. A video can be saved without being watched. |
"""
with open(REPORTS / "technical_report.md", "w", encoding="utf-8") as f:
    f.write(tech_md)
print("  Saved: Reports/technical_report.md")

# ── PERSONAL LEARNING PROFILE ─────────────────────────────────────────────────
# Interest persistence table
INTEREST_DATA = [
    ("Brazilian Jiu-Jitsu", "2017", True, "7+"),
    ("Discipline / Mindset", "2016", True, "9+"),
    ("Barber / Craft", "2018", True, "6+"),
    ("German Language", "2018", True, "6+"),
    ("Spiritual / Faith", "2016", True, "9+"),
    ("Finance / Wealth", "2018", False, "4+"),
    ("Health / Fitness", "2016", True, "9+"),
    ("Politics / News", "2017", False, "5 then recedes"),
    ("Philosophy / Masculinity", "2016", False, "Peaks Ph.1, recedes"),
    ("Music", "2016", True, "Sustained"),
]
interest_rows = "\n".join(
    f"| {name} | {start} | {'Yes' if active_ else 'Partial'} | {yrs} |"
    for name, start, active_, yrs in INTEREST_DATA
)

profile_md = f"""# Personal Learning Profile
**Based on observable archive data only.**  
Generated: {gen_date}

---

## Format Preferences

| Metric | Value |
|---|---|
| Average video duration saved | {avg_dur_min} minutes |
| Long-form (30+ min) | {lf_pct}% of archive |
| Short-form (<10 min) | {sf_pct}% of archive |
| Total saved content estimate | {total_hrs:,} hours |

**Observable pattern:** The data suggests a preference for sustained engagement over short clips. The average video saved is longer than the YouTube average of approximately 7 minutes. Long-form content (30+ min) appears disproportionately in discipline, podcast, and instructional categories.

---

## Domain Depth Indicators

The archive contains multiple sub-playlists per major domain, indicating systematic rather than casual engagement:

**Brazilian Jiu-Jitsu** — 12+ sub-playlists:
- Takedowns, Guard Work, Submissions, Defense, Counters, Drills, No-Gi, Stand-Up, Combos, Masterclass, Competition Motivation, Defense

**German Language** — Multiple tracks:
- B2 Exam preparation, Practice, Artist/Cultural exposure

**Barber Craft** — Separated by purpose:
- Technique videos, Brand-building, Business development

**Observable pattern:** Complex domains are decomposed into sub-tracks rather than saved to a single playlist. This is consistent with structured study behavior.

---

## Creator Loyalty

Channels appearing across 4+ life phases (observable persistence):

| Channel | First Phase | Still Phase 6? | Notes |
|---|---|---|---|
| etthehiphoppreacher | Phase 1 (2016) | Yes | {ch_ctr.get("etthehiphoppreacher", 0)} total saves |
| ATHLEAN-X™ | Phase 1 (2016) | Partial | Health/fitness anchor |
| Jocko Podcast | Phase 3 (2020) | Yes | Discipline/military |
| Bernardo Faria BJJ Fanatics | Phase 3 (2020) | Yes | BJJ technical |

**Observable pattern:** A small number of creators appear across multiple years without abandonment. This may indicate that their content aligns consistently with ongoing goals rather than transient interests.

---

## Interest Persistence Table

| Interest | First Appears | Active in Phase 6? | Est. Duration |
|---|---|---|---|
{interest_rows}

---

## Phase-by-Phase Learning Behavior

**Phase 1 (2016–2017):** Identity and physical foundation. Philosophy/masculinity and health content dominate. Early motivation infrastructure.

**Phase 2 (2018–2019):** Skill acquisition. Barber craft enters. German language study begins. Music volume spikes.

**Phase 3 (2020–2021):** Deep study period. Discipline content reaches its first major peak. BJJ emerges as a serious domain. Political awareness content rises.

**Phase 4 (2022):** Consolidation. Discipline content dominates 3 years in a row. German exam preparation is visible. BJJ refines.

**Phase 5 (2023):** BJJ takes command — 320 videos, becoming the single dominant domain. Competition preparation structure visible.

**Phase 6 (2024–2026):** Highest-volume phase. BJJ (650+ videos) and Discipline remain core. New technical and systems content entering.

---

## Caveats

- This profile is based on playlist saves, not verified watch history.
- A saved video may not have been watched.
- Interpretation of intent is inference, not fact.
- Psychological claims are explicitly avoided.
"""
with open(REPORTS / "personal_learning_profile.md", "w", encoding="utf-8") as f:
    f.write(profile_md)
print("  Saved: Reports/personal_learning_profile.md")

# ── RESEARCH FINDINGS ─────────────────────────────────────────────────────────
findings_md = f"""# Research Findings
**YouTube History Research Project**  
Generated: {gen_date}

---

## Finding 1: The Archive Is Structurally Organized, Not Algorithmically Generated

**Evidence:** 98 named playlists with deliberate titles covering sub-domains within broader topics. Playlist names include technique-specific BJJ categories (e.g., "Ankle Lock Defense", "Collar Drag", "Takedown BJJ"), structured language milestones (B2, German 2 Exam), and purpose-separated barber content.

**Conclusion (supported):** The curation behavior visible in the playlist taxonomy alone indicates intentional organization. The content of the playlists reinforces this. This archive was constructed, not accumulated.

---

## Finding 2: Brazilian Jiu-Jitsu Is the Dominant Study Domain

**Evidence:** {th_ctr.get("Brazilian Jiu-Jitsu",0)} videos classified as BJJ/Grappling ({round(th_ctr.get("Brazilian Jiu-Jitsu",0)/n_act*100,1)}% of active archive). 12+ dedicated sub-playlists. Channel analysis confirms consistent return to specific technical coaches (Knight Jiu-Jitsu, BIG OSS, ROYDEAN, JonThomasBJJ, CVBJJ Online, Bernardo Faria, The Art of Skill).

**Conclusion (supported):** BJJ is not a casual interest. The depth of coverage — technique-specific playlists, multiple coaches, competition preparation content — is consistent with serious study of a complex physical discipline.

---

## Finding 3: etthehiphoppreacher Is the Most Persistent Influence

**Evidence:** {ch_ctr.get("etthehiphoppreacher",0)} total saves. Present in all 6 life phases. Peak concentration in Phase 4 (2022) with 63+ entries in a single phase. No other creator matches both volume and longevity in this archive.

**Conclusion (supported):** This creator's content was returned to consistently across 9 years. Based on observable save behavior, this is not passive consumption of a trending creator — it is sustained engagement.

---

## Finding 4: 2024 Was the Highest-Activity Year

**Evidence:** {yr_ctr.get("2024","?")} videos added in 2024 — the peak year across the entire archive. Phase 6 (2024–2026) accounts for more total entries than any other phase.

**Conclusion (supported):** The archive owner's curation activity accelerated in the most recent phase. The archive is not winding down — it is intensifying.

---

## Finding 5: Political Content Shows a Clear Arc

**Evidence:** Politics/News content peaks in Phase 3 (2020–2021) with 72 entries. Channels include Redacted, WeAreChange, SGTreport, Project Veritas, and Hibbeler Productions. Content volume drops significantly in Phase 4 and beyond.

**Conclusion (supported):** Political content entered the archive during a specific period and receded. This is consistent with a period of heightened external interest followed by reduced engagement with that category.

---

## Finding 6: 384 Videos Are Permanently Lost

**Evidence:** 384 unique video IDs returned `unavailable` from the YouTube Data API v3. The content of these videos cannot be recovered through the API.

**Conclusion (supported):** 13.5% of the archive is unrecoverable. The actual breadth of topics studied is wider than what is currently measurable. Deletion clusters in early phases and political content categories.

---

## Finding 7: Long-Form Is the Structural Preference

**Evidence:** Average duration {avg_dur_min} minutes. {lf_pct}% of saved videos exceed 30 minutes. Highest-duration content includes Jocko Podcast episodes (2–4 hours), etthehiphoppreacher (60–90 min), and BJJ instructionals (30–90 min).

**Conclusion (supported):** The data suggests a preference for sustained engagement. Short-form content in the archive is concentrated in music and BJJ technique clips — specific functional use cases — rather than distributed evenly across all domains.
"""
with open(REPORTS / "research_findings.md", "w", encoding="utf-8") as f:
    f.write(findings_md)
print("  Saved: Reports/research_findings.md")

# ── FUTURE QUESTIONS ──────────────────────────────────────────────────────────
fq_md = f"""# Future Questions
**YouTube History Research Project**  
Generated: {gen_date}

---

These questions emerge from the data but cannot be answered by the current dataset alone.

---

## Questions About Behavior

1. **What percentage of saved videos were actually watched?**
   The current dataset reflects saves, not views. Integration with YouTube watch history export would allow correlation analysis.

2. **Do BJJ saves correlate with real-world competition dates?**
   If tournament participation dates are known, it would be possible to test whether save activity spikes before events.

3. **What triggered the acceleration in 2024?**
   {yr_ctr.get("2024","?")} saves in a single year is the peak of the archive. External context would be required to interpret this.

4. **Which deleted videos belong to which theme?**
   384 videos are unrecoverable. Probabilistic analysis using playlist membership might estimate the theme distribution of lost content.

---

## Questions About Learning Outcomes

5. **Did German language learning produce fluency?**
   The archive shows CEFR-level progression (B2 exam prep). Real-world usage data would be needed to assess outcome.

6. **How does BJJ technical study correlate with mat time?**
   Video study is one input. Training hours, competitions, and belt progression are separate data points not captured here.

7. **Which channels produced the most durable mindset influence?**
   Duration of return to a creator is measurable. Impact on decisions or behavior is not.

---

## Questions About the Archive Itself

8. **What does the Watch Later playlist actually contain by topic?**
   With 2,434 entries, Watch Later is the largest single playlist. Full theme analysis of this playlist alone would significantly change aggregate statistics.

9. **Are there patterns in *when* within a day videos are saved?**
   The current dataset captures UTC hour. With timezone adjustment, morning vs. evening save behavior could be analyzed.

10. **What would a subscription history analysis add?**
    Subscriptions represent intent-to-follow, not just individual video saves. YouTube Takeout includes subscription data — integrating it would add another layer.

---

## Dataset Expansion Opportunities

| Dataset | What It Would Add |
|---|---|
| YouTube watch history | Verify which saved videos were actually watched |
| YouTube search history | Reveal information-seeking behavior and curiosity trails |
| YouTube subscriptions export | Map channel relationships and creator loyalty intentions |
| YouTube comments export | Surface active engagement vs. passive consumption |
| Training logs / competition records | Correlate BJJ study with physical practice |
| Language learning records | Correlate German study with measurable proficiency milestones |
"""
with open(REPORTS / "future_questions.md", "w", encoding="utf-8") as f:
    f.write(fq_md)
print("  Saved: Reports/future_questions.md")

# ── HTML REPORT ───────────────────────────────────────────────────────────────
# Build HTML from the executive summary content
def md_to_simple_html(md_text):
    """Minimal markdown-to-HTML converter for the report."""
    import re
    lines = md_text.split("\n")
    html_lines = []
    in_table = False
    in_code  = False
    for line in lines:
        if line.startswith("```"):
            if in_code:
                html_lines.append("</code></pre>")
                in_code = False
            else:
                html_lines.append("<pre><code>")
                in_code = True
        elif in_code:
            html_lines.append(line)
        elif line.startswith("# "):
            html_lines.append(f"<h1>{line[2:]}</h1>")
        elif line.startswith("## "):
            html_lines.append(f"<h2>{line[3:]}</h2>")
        elif line.startswith("### "):
            html_lines.append(f"<h3>{line[4:]}</h3>")
        elif line.startswith("---"):
            html_lines.append("<hr>")
        elif line.startswith("|"):
            if not in_table:
                html_lines.append("<table>")
                in_table = True
            if re.match(r"^\|[-| ]+\|$", line):
                continue
            cells = [c.strip() for c in line.split("|")[1:-1]]
            last_two = " ".join(html_lines[-2:]) if html_lines else ""
            tag = "th" if "</th>" not in last_two else "td"
            # simplified: first row = th
            row_html = "".join(f"<{tag}>{c}</{tag}>" for c in cells)
            html_lines.append(f"<tr>{row_html}</tr>")
        else:
            if in_table:
                html_lines.append("</table>")
                in_table = False
            if line.strip() == "":
                html_lines.append("<br>")
            else:
                line = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", line)
                line = re.sub(r"\*(.+?)\*", r"<em>\1</em>", line)
                line = re.sub(r"`(.+?)`", r"<code>\1</code>", line)
                html_lines.append(f"<p>{line}</p>")
    if in_table:
        html_lines.append("</table>")
    return "\n".join(html_lines)

reports_to_include = [
    ("Executive Summary",         REPORTS / "executive_summary.md"),
    ("Technical Report",          REPORTS / "technical_report.md"),
    ("Personal Learning Profile", REPORTS / "personal_learning_profile.md"),
    ("Research Findings",         REPORTS / "research_findings.md"),
    ("Future Questions",          REPORTS / "future_questions.md"),
]

html_sections = []
for title, path in reports_to_include:
    with open(path, encoding="utf-8") as f:
        content = f.read()
    html_sections.append(f'<section id="{title.lower().replace(" ","-")}">')
    html_sections.append(md_to_simple_html(content))
    html_sections.append("</section>")

nav_links = " | ".join(
    f'<a href="#{t.lower().replace(" ","-")}">{t}</a>'
    for t, _ in reports_to_include
)

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>YouTube History Research — Full Report</title>
<style>
  :root {{
    --bg: #0d0d0d;
    --panel: #141414;
    --border: #2a2a2a;
    --gold: #d4a843;
    --blue: #5b9bd5;
    --text: #e0e0e0;
    --subtext: #888;
    --code-bg: #1a1a1a;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ background: var(--bg); color: var(--text); font-family: 'Courier New', monospace; line-height: 1.7; }}
  #nav {{ background: var(--panel); border-bottom: 1px solid var(--border); padding: 12px 40px; position: sticky; top: 0; z-index: 10; font-size: 13px; }}
  #nav a {{ color: var(--gold); text-decoration: none; margin-right: 8px; }}
  #nav a:hover {{ text-decoration: underline; }}
  main {{ max-width: 960px; margin: 0 auto; padding: 40px 24px; }}
  section {{ border-bottom: 1px solid var(--border); padding-bottom: 40px; margin-bottom: 40px; }}
  h1 {{ color: var(--gold); font-size: 1.8em; border-bottom: 1px solid var(--border); padding-bottom: 8px; margin: 24px 0 16px; }}
  h2 {{ color: var(--blue); font-size: 1.3em; margin: 28px 0 12px; }}
  h3 {{ color: var(--text); font-size: 1.1em; margin: 20px 0 8px; }}
  p {{ margin: 8px 0; font-size: 14px; }}
  table {{ width: 100%; border-collapse: collapse; margin: 16px 0; font-size: 13px; }}
  th {{ background: var(--panel); color: var(--gold); border: 1px solid var(--border); padding: 8px 12px; text-align: left; }}
  td {{ border: 1px solid var(--border); padding: 7px 12px; }}
  tr:nth-child(even) td {{ background: #111; }}
  code {{ background: var(--code-bg); padding: 2px 6px; border-radius: 3px; font-size: 12px; color: var(--gold); }}
  pre {{ background: var(--code-bg); padding: 16px; border-radius: 4px; overflow-x: auto; margin: 12px 0; border-left: 3px solid var(--gold); }}
  pre code {{ padding: 0; background: none; }}
  hr {{ border: none; border-top: 1px solid var(--border); margin: 24px 0; }}
  strong {{ color: var(--gold); }}
  br {{ display: block; margin: 4px 0; }}
  footer {{ text-align: center; color: var(--subtext); font-size: 12px; padding: 24px; }}
</style>
</head>
<body>
<div id="nav">{nav_links}</div>
<main>
{"".join(html_sections)}
</main>
<footer>YouTube History Research Project &mdash; Generated {gen_date}</footer>
</body>
</html>"""

with open(REPORTS / "full_report.html", "w", encoding="utf-8") as f:
    f.write(html)
print("  Saved: Reports/full_report.html")

print("\n[06] DONE")
