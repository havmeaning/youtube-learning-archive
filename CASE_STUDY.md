# YouTube Learning Archive Intelligence System

> Converting 9.5 years of unstructured self-education activity into a governed, queryable evidence base.

## Executive summary

The YouTube Learning Archive converts a private playlist-save export into a reproducible analytical system and a portfolio-safe public package. The workflow hydrates video IDs, cleans and engineers metadata, classifies themes with transparent rules, aggregates results, and publishes documentation, charts, reports, and selected dashboard screenshots.

The project’s value is not a claim that saved videos prove learning or mastery. Its value is the implementation: a governed pipeline that turns messy personal data into auditable outputs while maintaining a clear public/private boundary.

## The problem

A playlist archive is not analysis-ready. It contains repeated video IDs across playlists, timestamps, inconsistent or missing metadata, and entries that may later be deleted, private, or restricted. It also mixes distinct evidence types: saving, watching, understanding, applying, and mastering material are not interchangeable.

The design challenge was therefore twofold:

1. Build a repeatable system for enriching, cleaning, classifying, and summarizing the archive.
2. Publish enough evidence to evaluate the work without exposing the private row-level dataset.

## The system

The public repository contains the transformation logic and aggregate outputs. The private execution environment supplies two excluded row-level inputs: a playlist-entry table and a unique-video metadata table. Six numbered Python stages inspect data, engineer features, classify themes, generate statistics, create visualizations, and produce reports; `Scripts/run_all.py` orchestrates them.

Outputs include aggregate CSV summaries, static charts, Markdown and HTML reports, privacy-treated supporting visuals, and a documented Power BI layer. The private `.pbix` file is excluded.

## Architecture and workflow

```text
Private boundary
  Playlist-save export
    -> YouTube API metadata hydration
    -> row-level cleaning and feature engineering
    -> transparent rule-based theme classification

Public boundary
  Aggregate CSVs
    -> charts and reports
    -> dashboard screenshots
    -> case study and release validation
```

The architecture intentionally makes the publication boundary visible. Scripts describe how private inputs are processed, while `.gitignore`, the manifest, the checklist, and the release validator protect excluded material.

## By the numbers

| Metric | Verified repository value |
|---|---:|
| Playlist entries processed | 3,536 |
| Unique video IDs hydrated | 2,847 |
| Active or retrievable entries | 3,101 |
| Unavailable, deleted, or private entries | 435 |
| Time span | October 2016-April 2026 (9.5 years) |
| Dominant classified theme | Brazilian Jiu-Jitsu |
| Peak activity year | 2024 |

These figures describe the private run reported by the repository. The public package does not contain the row-level source required to recompute them from scratch.

## Key findings

### Brazilian Jiu-Jitsu is the dominant classified theme

The aggregate theme summary and reports identify Brazilian Jiu-Jitsu as the largest rule-based theme. This supports a claim of persistent collection interest in that domain. It does not by itself establish that the videos were watched or that techniques were understood or performed.

### Activity peaked in 2024

The yearly summary reports 2024 as the highest-volume year for playlist additions. This is a finding about curation activity, not necessarily time spent watching or learning.

### Availability loss is material

Of 3,536 playlist entries, 435 were unavailable, deleted, private, or otherwise not retrievable in the reported run. The missing metadata constrains theme and content analysis for those entries.

### Repeated sources and themes are signals, not outcomes

Recurring channels, long-running themes, and purpose-specific playlists can indicate sustained attention and organization. They cannot independently prove comprehension, transfer to practice, demonstrated skill, or mastery.

## Methodology

The pipeline performs the following work:

1. Inspects schemas, missing values, duplicates, and availability status.
2. Parses dates, durations, counts, and categorical fields.
3. Engineers year, month, quarter, weekday, life-phase, duration, format, and availability features.
4. Applies a documented rule-based classifier using titles, tags, categories, descriptions, and higher-weight channel signals.
5. Produces grouped statistics by theme, year, month, phase, channel, and tag.
6. Generates charts and narrative reports from the aggregate results.

The classifier is deliberately transparent rather than presented as machine learning. Its rules are archive-specific and can misclassify ambiguous content.

## Privacy-by-design

The public release excludes raw Google Takeout exports, cleaned and hydrated row-level datasets, watch history, video-level URLs and timestamps, API keys, environment files, local backups, Power BI working directories, and `.pbix` files.

Tracked CSVs were reviewed by schema and structure. They are grouped summaries rather than one-row-per-video or one-row-per-playlist-entry datasets. Some aggregates name channels or tags and therefore still reveal aspects of the archive owner’s interest profile; aggregation reduces granularity but does not make the data anonymous.

The supporting BJJ visuals are face-blurred. That treatment reduces direct identifiability but cannot eliminate contextual recognition risk.

## Limitations

- Playlist saves are interest or collection signals, not automatic proof of viewing.
- Watch-history evidence is a separate data source and is not published here.
- Hydrated metadata reflects API state at the time of enrichment.
- Inferred study themes are classifier outputs, not verified intent.
- Demonstrated skill requires independent artifacts or performance evidence.
- Claimed mastery is outside the evidentiary scope of this repository.
- Deleted, private, and restricted items leave gaps that cannot be recovered from the public package.
- The public repository cannot reproduce private-run metrics without the intentionally excluded source data.
- The Channel Influence Map lacks a valid public screenshot.
- The System Architecture screenshot is genuine but stale: it says “5-page model” and “10-script pipeline.”

## Employer value

The repository provides inspectable evidence of work relevant to data and knowledge-system roles:

- API-oriented metadata enrichment design
- data cleaning and feature engineering
- transparent classification logic
- aggregate analytical modeling
- Python-based reporting and visualization
- Power BI information design
- evidence-boundary communication
- privacy-aware publication controls
- automated release validation

These artifacts demonstrate implementation and judgment in the project itself. They do not convert the archive’s subject matter into professional skill claims.

## Reproduction

Install dependencies and run the pipeline against your own private inputs:

```bash
pip install -r requirements.txt
python Scripts/run_all.py
```

The expected private inputs are documented in the [data dictionary](Documentation/data_dictionary.md) and must remain under the ignored `Raw/` directory. Validate the public package separately:

```bash
python Scripts/validate_public_release.py
```

No API calls or private inputs are required for release validation.

## Evidence and verification status

| Evidence | Public status | What it supports | What it does not support |
|---|---|---|---|
| Analysis scripts | Tracked and inspectable | Pipeline design and implementation | Successful execution without private inputs |
| Aggregate CSVs | Tracked; schema-reviewed | Reported grouped patterns | Video-level behavior or viewing |
| Charts and reports | Tracked | Presentation of aggregate outputs | Independent validation of private inputs |
| Dashboard screenshots | Five readable exports; one missing | Existence and design of exported pages | Currency of the private `.pbix` model |
| Privacy-treated BJJ visuals | Tracked | Narrow supporting context | Anonymity, causal learning, or mastery |
| Channel Influence Map | Missing | Page is documented only | Visual or content verification |

The [dashboard gallery](dashboard/README.md) records page-level screenshot status and unresolved currency issues.

## Repository navigation

- [Project overview](README.md)
- [Dashboard gallery](dashboard/README.md)
- [Technical report](Reports/technical_report.md)
- [Research findings](Reports/research_findings.md)
- [Data dictionary](Documentation/data_dictionary.md)
- [Theme rules](Documentation/theme_classification_rules.md)
- [Project manifest](PROJECT_MANIFEST.md)
- [Publication checklist](PUBLICATION_CHECKLIST.md)
