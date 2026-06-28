#!/usr/bin/env python3
"""
05_create_visualizations.py
============================
Phase 7: Generate all charts as PNG files.
Produces 11 charts in Charts/.
"""

import csv
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

ROOT   = Path(__file__).resolve().parent.parent
CLEAN  = ROOT / "Clean"
ANALYSIS = ROOT / "Analysis"
CHARTS = ROOT / "Charts"
CHARTS.mkdir(exist_ok=True)

# ── STYLE ─────────────────────────────────────────────────────────────────────
BG      = "#0d0d0d"
PANEL   = "#161616"
GOLD    = "#d4a843"
BLUE    = "#5b9bd5"
RED     = "#c0392b"
GREEN   = "#27ae60"
TEXT    = "#e0e0e0"
SUBTEXT = "#777777"
GRID    = "#252525"

plt.rcParams.update({
    "figure.facecolor": BG,
    "axes.facecolor":   PANEL,
    "axes.edgecolor":   GRID,
    "axes.labelcolor":  TEXT,
    "xtick.color":      TEXT,
    "ytick.color":      TEXT,
    "text.color":       TEXT,
    "grid.color":       GRID,
    "grid.linewidth":   0.5,
    "font.family":      "monospace",
    "axes.titlesize":   13,
    "axes.labelsize":   10,
    "xtick.labelsize":  9,
    "ytick.labelsize":  9,
    "legend.fontsize":  8,
    "legend.framealpha": 0.2,
})

def save(fig, name, tight=True):
    path = CHARTS / f"{name}.png"
    if tight:
        fig.tight_layout()
    fig.savefig(path, dpi=150, bbox_inches="tight",
                facecolor=BG, edgecolor="none")
    plt.close(fig)
    print(f"  Saved: Charts/{name}.png")
    return path

# ── LOAD DATA ─────────────────────────────────────────────────────────────────
print("[05] Loading data...")
with open(CLEAN / "youtube_history_themed.csv", newline="", encoding="utf-8-sig") as f:
    rows = list(csv.DictReader(f))

active = [r for r in rows if r.get("is_available","") == "1"]
n = len(active)
print(f"  Active rows: {n}")

PHASE_ORDER = [
    "Phase 1: Foundation (2016–2017)",
    "Phase 2: Expansion (2018–2019)",
    "Phase 3: Deep Study (2020–2021)",
    "Phase 4: Consolidation (2022)",
    "Phase 5: Transition (2023)",
    "Phase 6: Operator/AI (2024–2026)",
]
SHORT_PHASES = [p.split(":")[1].strip() if ":" in p else p for p in PHASE_ORDER]

charts_created = []

# ── CHART 01: TOP 20 CHANNELS ─────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(13, 8))
ch_ctr = Counter(r["Channel Name"] for r in active if r.get("Channel Name","").strip())
top20  = ch_ctr.most_common(20)
names  = [c[0] for c in reversed(top20)]
counts = [c[1] for c in reversed(top20)]
colors = [GOLD if i >= 17 else BLUE for i in range(len(names))]
bars = ax.barh(names, counts, color=colors, height=0.7, edgecolor="none")
for bar, val in zip(bars, counts):
    ax.text(val + 0.3, bar.get_y() + bar.get_height()/2,
            str(val), va="center", fontsize=8, color=TEXT)
ax.set_xlabel("Videos Saved to Playlists")
ax.set_title("Top 20 Channels by Videos Saved  |  Full Archive (2016–2026)",
             fontweight="bold", pad=12)
ax.grid(axis="x", alpha=0.3)
ax.set_xlim(0, max(counts) * 1.13)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
charts_created.append(save(fig, "01_top_20_channels"))

# ── CHART 02: THEME DISTRIBUTION ─────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(12, 7))
theme_ctr = Counter(r["theme"] for r in active)
themes_sorted = theme_ctr.most_common()
t_names  = [t[0] for t in reversed(themes_sorted)]
t_counts = [t[1] for t in reversed(themes_sorted)]
palette  = plt.cm.tab20(np.linspace(0, 1, len(t_names)))
bars = ax.barh(t_names, t_counts, color=palette, height=0.7, edgecolor="none")
for bar, val in zip(bars, t_counts):
    pct = val / n * 100
    ax.text(val + 0.5, bar.get_y() + bar.get_height()/2,
            f"{val}  ({pct:.1f}%)", va="center", fontsize=8, color=TEXT)
ax.set_xlabel("Videos (active)")
ax.set_title("Theme Distribution — Active Videos  |  Full Archive",
             fontweight="bold", pad=12)
ax.grid(axis="x", alpha=0.3)
ax.set_xlim(0, max(t_counts) * 1.22)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
charts_created.append(save(fig, "02_theme_distribution"))

# ── CHART 03: YOUTUBE CATEGORY DISTRIBUTION ───────────────────────────────────
fig, ax = plt.subplots(figsize=(11, 6))
cat_ctr = Counter(r.get("Category","").strip() for r in active if r.get("Category","").strip())
top_cats = cat_ctr.most_common(12)
c_names  = [c[0] for c in reversed(top_cats)]
c_counts = [c[1] for c in reversed(top_cats)]
bars = ax.barh(c_names, c_counts, color=BLUE, height=0.65, edgecolor="none")
for bar, val in zip(bars, c_counts):
    ax.text(val + 0.5, bar.get_y() + bar.get_height()/2,
            f"{val}", va="center", fontsize=8, color=TEXT)
ax.set_xlabel("Videos")
ax.set_title("YouTube Category Distribution  |  Active Videos",
             fontweight="bold", pad=12)
ax.grid(axis="x", alpha=0.3)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
charts_created.append(save(fig, "03_youtube_categories"))

# ── CHART 04: VIDEOS BY YEAR ──────────────────────────────────────────────────
yr_ctr = Counter(str(r.get("added_year","")) for r in rows
                 if str(r.get("added_year","")).isdigit())
years  = sorted(yr_ctr.keys())
y_vals = [yr_ctr[y] for y in years]
peak   = max(y_vals)

fig, ax = plt.subplots(figsize=(12, 5))
bar_colors = [GOLD if v == peak else BLUE for v in y_vals]
bars = ax.bar(years, y_vals, color=bar_colors, width=0.65, edgecolor="none")
for bar, val in zip(bars, y_vals):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
            str(val), ha="center", fontsize=9, color=TEXT)
ax.set_xlabel("Year")
ax.set_ylabel("Videos Added")
ax.set_title("Videos Added to Playlists — by Year  |  All Playlists",
             fontweight="bold", pad=12)
ax.grid(axis="y", alpha=0.3)
ax.set_ylim(0, peak * 1.15)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
# Annotate peak
peak_yr = years[y_vals.index(peak)]
ax.annotate(f"Peak: {peak_yr}", xy=(peak_yr, peak),
            xytext=(years.index(peak_yr)-1.5, peak * 1.05),
            arrowprops=dict(arrowstyle="->", color=GOLD), color=GOLD, fontsize=9)
charts_created.append(save(fig, "04_videos_by_year"))

# ── CHART 05: MONTHLY HEATMAP ─────────────────────────────────────────────────
month_data = defaultdict(lambda: defaultdict(int))
for r in rows:
    yr = str(r.get("added_year",""))
    mo = str(r.get("added_month",""))
    if yr.isdigit() and mo.isdigit():
        month_data[int(yr)][int(mo)] += 1

years_hm = sorted(month_data.keys())
matrix   = np.zeros((len(years_hm), 12))
for i, yr in enumerate(years_hm):
    for mo in range(1, 13):
        matrix[i, mo-1] = month_data[yr].get(mo, 0)

fig, ax = plt.subplots(figsize=(14, 5))
im = ax.imshow(matrix, cmap="YlOrRd", aspect="auto", vmin=0)
ax.set_xticks(range(12))
ax.set_xticklabels(["Jan","Feb","Mar","Apr","May","Jun",
                     "Jul","Aug","Sep","Oct","Nov","Dec"])
ax.set_yticks(range(len(years_hm)))
ax.set_yticklabels([str(y) for y in years_hm])
cbar = plt.colorbar(im, ax=ax, shrink=0.8)
cbar.set_label("Videos Added", color=TEXT)
cbar.ax.yaxis.set_tick_params(color=TEXT)
for i in range(len(years_hm)):
    for j in range(12):
        val = int(matrix[i, j])
        if val > 0:
            color = "black" if val > matrix.max() * 0.55 else TEXT
            ax.text(j, i, str(val), ha="center", va="center",
                    fontsize=7, color=color)
ax.set_title("Monthly Activity Heatmap — Videos Added per Month",
             fontweight="bold", pad=12)
charts_created.append(save(fig, "05_monthly_heatmap"))

# ── CHART 06: DURATION DISTRIBUTION ──────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 5))
dur_order = ["Under 1 min","1–5 min","5–15 min","15–30 min","30–60 min","Over 60 min","Unknown"]
dur_ctr   = Counter(r.get("duration_bucket","Unknown") for r in active)
d_vals    = [dur_ctr.get(d, 0) for d in dur_order]
d_colors  = [SUBTEXT if d == "Unknown" else BLUE if dur_order.index(d) < 3 else GOLD
             for d in dur_order]
bars = ax.bar(dur_order, d_vals, color=d_colors, width=0.65, edgecolor="none")
for bar, val in zip(bars, d_vals):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 3,
            str(val), ha="center", fontsize=9, color=TEXT)
ax.set_ylabel("Count")
ax.set_title("Video Duration Distribution  |  Active Videos",
             fontweight="bold", pad=12)
ax.grid(axis="y", alpha=0.3)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.tick_params(axis="x", rotation=15)
charts_created.append(save(fig, "06_duration_distribution"))

# ── CHART 07: THEME EVOLUTION BY YEAR ────────────────────────────────────────
fig, ax = plt.subplots(figsize=(14, 6))
top8_themes = [t[0] for t in theme_ctr.most_common(8)]
years_ev    = [y for y in years if int(y) >= 2016]

tby = defaultdict(Counter)
for r in active:
    yr = str(r.get("added_year",""))
    if yr.isdigit():
        tby[yr][r["theme"]] += 1

palette_ev = plt.cm.tab10(np.linspace(0, 0.9, len(top8_themes)))
bottom = np.zeros(len(years_ev))
for i, theme in enumerate(top8_themes):
    vals = [tby.get(yr, Counter()).get(theme, 0) for yr in years_ev]
    ax.bar(years_ev, vals, bottom=bottom, label=theme,
           color=palette_ev[i], alpha=0.9, width=0.65, edgecolor="none")
    bottom += np.array(vals)
ax.set_xlabel("Year")
ax.set_ylabel("Videos Added")
ax.set_title("Theme Evolution by Year — Top 8 Themes  |  Active Videos",
             fontweight="bold", pad=12)
ax.legend(loc="upper left", ncol=2)
ax.grid(axis="y", alpha=0.3)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
charts_created.append(save(fig, "07_theme_evolution_by_year"))

# ── CHART 08: CHANNEL EVOLUTION BY YEAR (heatmap) ────────────────────────────
top15_ch = [c[0] for c in ch_ctr.most_common(15)]
cby_matrix = np.zeros((len(top15_ch), len(years_ev)))

cby = defaultdict(Counter)
for r in active:
    yr = str(r.get("added_year",""))
    ch = r.get("Channel Name","").strip()
    if yr.isdigit() and ch in top15_ch:
        cby[yr][ch] += 1

for j, yr in enumerate(years_ev):
    for i, ch in enumerate(top15_ch):
        cby_matrix[i, j] = cby.get(yr, Counter()).get(ch, 0)

fig, ax = plt.subplots(figsize=(14, 7))
im = ax.imshow(cby_matrix, cmap="Blues", aspect="auto", vmin=0)
ax.set_xticks(range(len(years_ev)))
ax.set_xticklabels(years_ev)
ax.set_yticks(range(len(top15_ch)))
ax.set_yticklabels(top15_ch, fontsize=9)
plt.colorbar(im, ax=ax, label="Videos Saved")
for i in range(len(top15_ch)):
    for j in range(len(years_ev)):
        val = int(cby_matrix[i, j])
        if val > 0:
            color = "white" if val > cby_matrix.max() * 0.5 else "#222"
            ax.text(j, i, str(val), ha="center", va="center", fontsize=8, color=color)
ax.set_title("Top 15 Channels × Year  |  Videos Saved Heatmap",
             fontweight="bold", pad=12)
charts_created.append(save(fig, "08_channel_evolution_heatmap"))

# ── CHART 09: LIFE PHASE COMPOSITION (pie grid) ───────────────────────────────
phase_themes = defaultdict(Counter)
for r in active:
    ph = r.get("life_phase_clean","").strip()
    if ph:
        phase_themes[ph][r["theme"]] += 1

fig, axes = plt.subplots(2, 3, figsize=(16, 9))
axes = axes.flatten()
pal = plt.cm.tab20(np.linspace(0, 1, 16))

for i, (phase, short) in enumerate(zip(PHASE_ORDER, SHORT_PHASES)):
    ax = axes[i]
    data = phase_themes.get(phase, Counter())
    if not data:
        ax.set_visible(False)
        continue
    top6     = data.most_common(6)
    labels   = [t[0] for t in top6]
    vals     = [t[1] for t in top6]
    c_slice  = [pal[j % 20] for j in range(len(labels))]
    wedges, _, autotexts = ax.pie(vals, labels=None, autopct="%1.0f%%",
                                   colors=c_slice, pctdistance=0.78,
                                   startangle=90, wedgeprops=dict(width=0.55))
    for at in autotexts:
        at.set_fontsize(8)
        at.set_color("#111")
    total_ph = sum(vals)
    ax.set_title(f"{short}\n({total_ph} videos)", fontsize=10, fontweight="bold", pad=4)
    ax.legend(labels, loc="lower center", fontsize=6.5,
              bbox_to_anchor=(0.5, -0.28), ncol=2, framealpha=0)

fig.suptitle("Theme Composition by Life Phase  |  Top 6 Themes per Phase",
             fontsize=14, fontweight="bold", y=1.01)
charts_created.append(save(fig, "09_phase_composition_pies"))

# ── CHART 10: UNAVAILABLE VIDEOS BY YEAR ─────────────────────────────────────
unavail_yr = Counter(str(r.get("added_year","")) for r in rows
                     if r.get("is_available","") != "1"
                     and str(r.get("added_year","")).isdigit())
total_yr   = Counter(str(r.get("added_year","")) for r in rows
                     if str(r.get("added_year","")).isdigit())

fig, ax = plt.subplots(figsize=(12, 5))
ua_years = sorted(total_yr.keys())
ua_vals  = [unavail_yr.get(y, 0) for y in ua_years]
ua_pcts  = [unavail_yr.get(y,0)/total_yr[y]*100 for y in ua_years]

ax2 = ax.twinx()
bars = ax.bar(ua_years, ua_vals, color=RED, alpha=0.75, width=0.65, edgecolor="none", label="Unavailable (count)")
ax2.plot(ua_years, ua_pcts, color=GOLD, marker="o", linewidth=2, label="Unavailable (%)")
ax.set_xlabel("Year")
ax.set_ylabel("Unavailable Videos (count)", color=RED)
ax2.set_ylabel("Unavailable %", color=GOLD)
ax2.tick_params(axis="y", labelcolor=GOLD)
ax.tick_params(axis="y", labelcolor=RED)
ax.set_title("Unavailable / Deleted Videos by Year  |  Count and Percentage",
             fontweight="bold", pad=12)
lines1, labels1 = ax.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax.legend(lines1 + lines2, labels1 + labels2, loc="upper left")
charts_created.append(save(fig, "10_unavailable_by_year"))

# ── CHART 11: LONG-FORM VS SHORT-FORM BY YEAR ────────────────────────────────
lf_by_yr = defaultdict(int)
sf_by_yr = defaultdict(int)
md_by_yr = defaultdict(int)

for r in active:
    yr = str(r.get("added_year",""))
    if not yr.isdigit():
        continue
    ft = r.get("format_type","")
    if ft == "Long-Form":  lf_by_yr[yr] += 1
    elif ft == "Short-Form": sf_by_yr[yr] += 1
    elif ft == "Medium":   md_by_yr[yr] += 1

fig, ax = plt.subplots(figsize=(12, 5))
yr_list  = sorted(set(lf_by_yr) | set(sf_by_yr) | set(md_by_yr))
lf_vals  = [lf_by_yr.get(y,0) for y in yr_list]
sf_vals  = [sf_by_yr.get(y,0) for y in yr_list]
md_vals  = [md_by_yr.get(y,0) for y in yr_list]

x = np.arange(len(yr_list))
w = 0.28
ax.bar(x - w, sf_vals, w, label="Short-Form (<10 min)", color=BLUE, edgecolor="none")
ax.bar(x,     md_vals, w, label="Medium (10–30 min)",   color=GREEN, edgecolor="none")
ax.bar(x + w, lf_vals, w, label="Long-Form (30+ min)",  color=GOLD, edgecolor="none")
ax.set_xticks(x)
ax.set_xticklabels(yr_list)
ax.set_ylabel("Videos")
ax.set_title("Long-Form vs Short-Form by Year  |  Active Videos",
             fontweight="bold", pad=12)
ax.legend()
ax.grid(axis="y", alpha=0.3)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
charts_created.append(save(fig, "11_format_by_year"))

print(f"\n  Total charts created: {len(charts_created)}")
print("\n[05] DONE")
