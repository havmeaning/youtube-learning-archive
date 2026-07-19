# Technical Report
**YouTube Learning Archive Intelligence System**
Generated: 2026-06-28

---

## Data Sources

| File | Rows | Description |
|---|---|---|
| master_table_hydrated.csv | 3,536 | One row per playlist-video pair. Includes API metadata. |
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
