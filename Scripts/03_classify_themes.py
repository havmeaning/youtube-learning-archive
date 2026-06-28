#!/usr/bin/env python3
"""
03_classify_themes.py
======================
Phase 4: Classify each video into a research theme.
Uses channel name, title, tags, description, and YouTube category.
Produces:
  - Clean/youtube_history_themed.csv
  - Analysis/theme_summary.csv
  - Analysis/channel_theme_summary.csv
  - Documentation/theme_classification_rules.md
"""

import csv
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT     = Path(__file__).resolve().parent.parent
CLEAN    = ROOT / "Clean"
ANALYSIS = ROOT / "Analysis"
DOCS     = ROOT / "Documentation"

ANALYSIS.mkdir(exist_ok=True)
DOCS.mkdir(exist_ok=True)

SOURCE = CLEAN / "youtube_history_clean.csv"

# ── CLASSIFICATION RULES ─────────────────────────────────────────────────────
# Each rule: (theme_name, [keyword_patterns], [channel_name_substrings])
# Matching is case-insensitive. Patterns are regex fragments.
# Rules are checked in order; first match wins.
# A video scores +1 for each matching keyword in (title + tags + category).
# A channel name match adds +3 (strong signal).
# Theme with highest score wins.

THEME_RULES = [
    (
        "Brazilian Jiu-Jitsu",
        ["jiu.?jitsu","jiujitsu","\\bbjj\\b","grappl","takedown",
         "\\barmbar\\b","guillotine","\\bchoke\\b","half.?guard",
         "collar.?drag","ankle.?lock","no.?gi","submission","\\bsweep\\b",
         "\\bguard\\b","\\bmount\\b","back.?take","\\bdrill\\b",
         "sparring","\\broll\\b","rolling","\\bjudo\\b","wrestling",
         "closed.?guard","open.?guard","x.?guard","rubber.?guard",
         "triangle","kimura","omoplata","rear.?naked","darce","anaconda",
         "leg.?lock","heel.?hook","kneebar","toehold","berimbolo",
         "de.?la.?riva","lasso","spider.?guard","worm.?guard"],
        ["bjj","jiu-jitsu","jiu jitsu","jujitsu","roydean","chewjitsu",
         "cvbjj","jonthomasbjj","big oss","bernardo faria","grappling academy",
         "globetrotter","dubious dom","jordan teaches","knight jiu",
         "stephan kesting","the art of skill","grapplearts","flo grappling",
         "danaher","mikey musumeci","gordon ryan","john danaher",
         "jedi does","josh saunders","master class ju"],
    ),
    (
        "Discipline / Mindset",
        ["discipline","mindset","mental.?tough","accountability",
         "hard.?work","habits","morning.?routine","daily.?routine",
         "\\bfocus\\b","consistency","indomitable","self.?improvement",
         "\\bgrind\\b","motivation","champion","warrior","mental.?strength",
         "stoic","resilience","\\bwillpower\\b"],
        ["etthehiphoppreacher","jocko","andy frisella","ed mylett",
         "art of skill","evan carmichael","proactive thinker",
         "video advice","goalcast","mulligan brothers"],
    ),
    (
        "Health / Fitness",
        ["workout","\\bfitness\\b","\\bexercise\\b","\\bmuscle\\b",
         "nutrition","\\bdiet\\b","fasting","intermittent","\\bstretch\\b",
         "mobility","\\byoga\\b","physio","back.?pain","recovery",
         "\\bsleep\\b","supplement","\\bprotein\\b","calorie",
         "strength.?training","hypertrophy","cardio","\\bcalisthenics\\b",
         "pull.?up","push.?up","squat","deadlift","bench.?press"],
        ["athlean","jeff nippard","mike israetel","alan thrall",
         "mind.?pump","renaissance periodization","movement20xx",
         "kelly starrett","knees over toes"],
    ),
    (
        "Barber / Craft",
        ["\\bbarber\\b","barbershop","haircut","\\bfade\\b","\\bclipper\\b",
         "\\brazor\\b","\\btaper\\b","\\blineup\\b","hair.?style",
         "\\bgrooming\\b","hair.?cut","pompadour","skin.?fade",
         "bald.?fade","mid.?fade","high.?fade","low.?fade","temp.?fade"],
        ["bossio","seancutshair","360jeezy","youtube barber",
         "thesalonguy","geo the barber","vegas barber","rog",
         "create barber brand"],
    ),
    (
        "German Language",
        ["\\bgerman\\b","\\bdeutsch\\b","lernen","\\bb1\\b","\\bb2\\b",
         "\\bc1\\b","german.?grammar","german.?vocab","german.?lesson",
         "learn.?german","german.?speaking","german.?pronunciation",
         "german.?word","auf.?deutsch"],
        ["learn german","deutschlehrer","benjamin","german with jenny",
         "easy german","german pod","deutsch","get germanized"],
    ),
    (
        "Spiritual / Faith",
        ["\\bgod\\b","\\bprayer\\b","\\bfaith\\b","\\bbible\\b","gospel",
         "\\bsermon\\b","\\bchurch\\b","\\bholy\\b","\\bspirit\\b",
         "worship","pastor","preach","christian","salvation","scripture",
         "\\bjesus\\b","israelite","hebrew","testimony","anointed",
         "kingdom","righteous","prophecy","covenant"],
        ["td jakes","t.d. jakes","iuic","polight","brother polight",
         "morning prayer","hebrew israelite","church","ministry",
         "steven furtick","joel osteen","louie giglio"],
    ),
    (
        "Philosophy / Masculinity",
        ["masculin","\\bmen\\b","\\bman\\b","brotherhood","conviction",
         "\\bstoic","red.?pill","dating","relationship","\\bmale\\b",
         "\\bfather\\b","\\bpatriarch\\b","alpha","sigma","hypergamy",
         "modern.?man","mgtow","manosphere","what.?it.?means"],
        ["patrice","paul elam","black phillip","cult of black phillip",
         "rollo tomassi","fresh and fit","coach greg","donovan sharpe",
         "the rational male","patrick bet-david","how to be a man"],
    ),
    (
        "Finance / Wealth",
        ["invest","\\bstock\\b","\\bfinance\\b","\\bwealth\\b","\\bmoney\\b",
         "\\bbudget\\b","\\bcrypto\\b","trading","compound","\\basset\\b",
         "passive.?income","dividend","real.?estate","net.?worth",
         "financial.?freedom","retire","\\bdebt\\b","\\bsaving\\b",
         "richest.?man","babylon"],
        ["valuetainment","graham stephan","andrei jikh","meet kevin",
         "minority mindset","minority money","rich dad","kiyosaki",
         "dave ramsey","bigger pockets"],
    ),
    (
        "Politics / News",
        ["politics","government","election","democrat","republican",
         "\\btrump\\b","\\bbiden\\b","policy","geopolit","protest",
         "\\bcensorship\\b","mainstream.?media","deep.?state",
         "\\bexposed\\b","\\bcorrupt\\b","globalist","\\bwoke\\b",
         "\\bnarrative\\b","propaganda","false.?flag","\\bcovid\\b",
         "\\bpandemic\\b","vaccine","great.?reset"],
        ["redacted","we are change","sgtreport","project veritas",
         "epoch times","the hill","tim pool","jimmy dore","russell brand",
         "higherside chats","hibbeler"],
    ),
    (
        "Music",
        ["\\bmusic\\b","\\bsong\\b","\\balbum\\b","\\bbeat\\b",
         "\\brap\\b","hip.?hop","\\brnb\\b","r&b","reggae","\\blyrics\\b",
         "\\bmix\\b","\\btrack\\b","\\bartist\\b","instrumental",
         "\\bmelody\\b","\\bchord\\b","\\bguitar\\b","\\bpiano\\b",
         "\\bdrum\\b","\\bbass\\b","\\bvocal\\b"],
        ["meek mill","xtinaaguileralyrics","worldstar","genius",
         "colors","soulection","npr music","tiny desk"],
    ),
    (
        "Business / Marketing",
        ["business","marketing","entrepreneur","\\bbrand\\b","startup",
         "\\bsales\\b","customer","\\bproduct\\b","strategy","leadership",
         "management","\\bgrowth\\b","\\bscale\\b","monetize",
         "\\brevenue\\b","\\bprofit\\b","\\bpitch\\b","\\bfunnel\\b",
         "copywriting","\\bpersonal.?brand\\b"],
        ["valuetainment","evan carmichael","gary vee","garyvee",
         "neil patel","alex hormozi","mfm pod","my first million",
         "patrick bet-david","iman gadzhi"],
    ),
    (
        "Tech / AI / Systems",
        ["\\bai\\b","artificial.?intel","machine.?learn","chatgpt",
         "\\bllm\\b","\\blinux\\b","\\bpython\\b","programming",
         "\\bcoding\\b","\\bsoftware\\b","automation","\\bsystem\\b",
         "ux.?design","user.?experience","\\bworkflow\\b","technology",
         "digital","\\bprompt\\b","language.?model","neural.?network",
         "\\bgpt\\b","\\bclaude\\b","open.?ai"],
        ["lex fridman","andrej karpathy","fireship","theo","primagen",
         "the primeagen","3blue1brown","two minute papers","yannic kilcher"],
    ),
    (
        "Leadership / Military",
        ["leadership","military","\\bwarrior\\b","\\bsoldier\\b",
         "\\bwar\\b","combat","navy.?seal","army","\\bveteran\\b",
         "\\bcommand\\b","\\btactical\\b","\\bstrategy\\b","special.?forces",
         "\\bmission\\b","\\bcourage\\b","\\bhonor\\b","\\bduty\\b"],
        ["jocko","david goggins","andy stumpf","mark divine",
         "ryan holiday","the obstacle is the way"],
    ),
    (
        "Comedy / Entertainment",
        ["comedy","stand.?up","\\bfunny\\b","\\bjoke\\b","\\blaugh\\b",
         "comedian","\\bprank\\b","reaction","\\bsketch\\b","\\bskit\\b",
         "roast","savage","\\bviral\\b"],
        ["patrice","paul mooney","comedy crackhead","chappelle",
         "donnell rawlings"],
    ),
    (
        "History / Documentary",
        ["history","documentary","\\bwar\\b","empire","ancient",
         "civilization","\\bwwii\\b","\\bwwi\\b","battle","\\barchive\\b",
         "true.?story","biography","\\bdecline\\b","\\brise.?of\\b",
         "cold.?war","revolution"],
        ["hibbeler productions","real stories","timeline","chronicle"],
    ),
    (
        "Podcasts",
        ["podcast","episode","\\bep\\.","\\b#\\d+\\b","interview",
         "\\bconversation\\b","\\btalks.?with\\b","\\bshow\\b",
         "\\bguest\\b","long.?form.?interview"],
        ["jocko podcast","lex fridman","huberman","tim ferriss",
         "joe rogan","valuetainment","my first million"],
    ),
]

def score_themes(title, channel, tags, category):
    text = " ".join([
        (title    or "").lower(),
        (tags     or "").lower().replace("|", " "),
        (category or "").lower(),
    ])
    channel_l = (channel or "").lower()

    scores = {}
    for theme, kw_patterns, ch_substrings in THEME_RULES:
        kw_score = sum(1 for p in kw_patterns if re.search(p, text))
        ch_score = sum(3 for s in ch_substrings if s in channel_l)
        total = kw_score + ch_score
        if total > 0:
            scores[theme] = total

    if not scores:
        return "Other", 0
    best = max(scores, key=scores.get)
    return best, scores[best]

# ── CLASSIFY ──────────────────────────────────────────────────────────────────
print("[03] Loading clean data...")
with open(SOURCE, newline="", encoding="utf-8-sig") as f:
    rows = list(csv.DictReader(f))
print(f"  Rows loaded: {len(rows)}")

themed = []
for r in rows:
    theme, score = score_themes(
        r.get("Title",""),
        r.get("Channel Name",""),
        r.get("Tags",""),
        r.get("Category",""),
    )
    e = dict(r)
    e["theme"]       = theme
    e["theme_score"] = score
    themed.append(e)

# ── EXPORTS ───────────────────────────────────────────────────────────────────
# Themed clean dataset
out_cols = list(rows[0].keys()) + ["theme","theme_score"]
with open(CLEAN / "youtube_history_themed.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=out_cols, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(themed)
print(f"  Saved: Clean/youtube_history_themed.csv")

# Active only for summaries
active = [r for r in themed if r.get("is_available","1") == "1"]

# Theme summary
theme_counts = Counter(r["theme"] for r in active)
total_active = len(active)
with open(ANALYSIS / "theme_summary.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["theme","video_count","pct_of_active"])
    writer.writeheader()
    for theme, count in theme_counts.most_common():
        writer.writerow({"theme": theme, "video_count": count,
                         "pct_of_active": round(count/total_active*100, 2)})
print(f"  Saved: Analysis/theme_summary.csv")

# Channel-theme summary
ch_themes = defaultdict(Counter)
for r in active:
    if r.get("Channel Name","").strip():
        ch_themes[r["Channel Name"]][r["theme"]] += 1

ch_rows = []
for ch, theme_ctr in sorted(ch_themes.items(), key=lambda x: -sum(x[1].values())):
    total = sum(theme_ctr.values())
    top_theme = theme_ctr.most_common(1)[0][0]
    ch_rows.append({"channel_name": ch, "total_videos": total,
                    "primary_theme": top_theme,
                    "theme_breakdown": "; ".join(f"{t}:{c}" for t,c in theme_ctr.most_common(3))})

with open(ANALYSIS / "channel_theme_summary.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["channel_name","total_videos","primary_theme","theme_breakdown"])
    writer.writeheader()
    writer.writerows(ch_rows)
print(f"  Saved: Analysis/channel_theme_summary.csv")

# Print distribution
print("\n  Theme distribution (active videos):")
for theme, count in theme_counts.most_common():
    pct = count / total_active * 100
    print(f"    {count:5d}  {pct:5.1f}%  {theme}")

# ── RULES DOC ─────────────────────────────────────────────────────────────────
rules_md = """# Theme Classification Rules

Generated by `03_classify_themes.py`.

---

## Method

Each video is scored against 15 themes using three text signals:

| Signal | Weight | Source |
|---|---|---|
| Keyword match in title + tags + YouTube category | +1 per match | YouTube Data API |
| Channel name substring match | +3 per match | YouTube Data API |

The theme with the highest total score is assigned. If no theme scores above 0, the video is labeled **Other**.

**Priority:** Channel name matches outweigh keyword matches 3:1. A video from a known BJJ channel is classified as BJJ even if the title is generic.

---

## Themes and Rules

"""

for theme, kw_patterns, ch_substrings in THEME_RULES:
    rules_md += f"### {theme}\n\n"
    rules_md += f"**Keyword patterns ({len(kw_patterns)}):**\n"
    rules_md += ", ".join(f"`{k}`" for k in kw_patterns) + "\n\n"
    rules_md += f"**Channel signals ({len(ch_substrings)}):**\n"
    rules_md += ", ".join(f"`{c}`" for c in ch_substrings) + "\n\n"

rules_md += """---

## Known Limitations

- Videos with no title, tags, or recognizable channel will fall into **Other**.
- YouTube's own category labels are used as a secondary signal only. They are often too broad (e.g., "Education" covers BJJ, philosophy, and language learning equally).
- The **Podcasts** theme overlaps with Discipline/Mindset and Philosophy since many podcasts cover those topics. Channel signal takes precedence.
- Rule coverage is based on channels and content observed in this specific archive. It is not a general-purpose classifier.
"""

with open(DOCS / "theme_classification_rules.md", "w", encoding="utf-8") as f:
    f.write(rules_md)
print(f"  Saved: Documentation/theme_classification_rules.md")

print("\n[03] DONE")
