# YouTube Learning Archive Intelligence System

> Converting 9.5 years of unstructured self-education activity into a governed, queryable evidence base.

The YouTube Learning Archive turns a private playlist-save export into a reproducible, portfolio-safe analytics package. A Python pipeline inspects and cleans the private source, enriches video IDs with YouTube metadata, engineers time and format features, applies transparent theme rules, and produces aggregate tables, charts, reports, and a Power BI presentation layer.

The public repository demonstrates data engineering, analytical modeling, documentation, and release governance without publishing raw exports, row-level personal data, API keys, or the private Power BI file. Saved videos are collection and interest signals; they are not proof that a video was watched, understood, or mastered.

## Key metrics

| Metric | Verified value |
|---|---:|
| Playlist entries processed | 3,536 |
| Unique video IDs hydrated | 2,847 |
| Active or retrievable entries | 3,101 |
| Unavailable, deleted, or private entries | 435 |
| Archive span | October 2016-April 2026 (9.5 years) |
| Dominant classified theme | Brazilian Jiu-Jitsu |
| Peak activity year | 2024 |

## Portfolio package

- [Case study](CASE_STUDY.md) - problem, architecture, methodology, findings, limitations, and employer value
- [Dashboard gallery](dashboard/README.md) - verified screenshots and page-by-page evidence status
- [Technical report](Reports/technical_report.md) - pipeline and feature-engineering details
- [Research findings](Reports/research_findings.md) - findings with explicit evidence boundaries
- [Data dictionary](Documentation/data_dictionary.md) - private input schema and data-quality notes
- [Theme classification rules](Documentation/theme_classification_rules.md) - transparent scoring logic
- [Publication checklist](PUBLICATION_CHECKLIST.md) - release safety controls

## The data problem

The private source is a playlist-save archive: repeated video IDs, timestamps, playlist labels, missing metadata, and records for videos that later became unavailable. On its own, it cannot answer which themes persisted, how collection activity changed over time, or which evidence can safely be published.

The pipeline converts that source into governed analytical outputs:

```text
Private playlist-save export
  -> metadata hydration
  -> cleaning and feature engineering
  -> rule-based theme classification
  -> aggregate statistics and charts
  -> reports and portfolio-safe dashboard screenshots
```

The private inputs are required to reproduce the reported metrics. They are intentionally absent from this public repository.

## Evidence boundary

This project distinguishes among several kinds of evidence:

- **Playlist-save activity** records collection behavior, not confirmed viewing.
- **Watch-history evidence** would be needed to establish that a video played; it is not included here.
- **Hydrated metadata** describes videos and channels at the time of API enrichment.
- **Inferred themes** are outputs of a documented rule-based classifier, not ground truth.
- **Repository artifacts** demonstrate implementation and publication-governance work.
- **Skill or mastery claims** require independent evidence beyond saved-video records.

## Repository structure

```text
Analysis/          Aggregate CSV outputs
Charts/            Aggregate PNG visualizations
Documentation/     Data dictionary and classification rules
Evidence/          Privacy-treated supporting visuals
Reports/           Markdown and HTML reports
Scripts/           Reproducible analysis and release-validation scripts
dashboard/         Power BI documentation and public screenshots
CASE_STUDY.md       Portfolio case study
```

## Reproduce with your own private data

1. Export your own YouTube playlist data.
2. Hydrate video IDs with the YouTube Data API v3 or an equivalent metadata source.
3. Keep the source files in a local, untracked `Raw/` directory.
4. Install the analysis dependencies:

```bash
pip install -r requirements.txt
```

5. Run the pipeline:

```bash
python Scripts/run_all.py
```

The pipeline expects `Raw/master_table_hydrated.csv` and `Raw/hydrated_videos.csv`. Do not commit `Raw/`, `Clean/`, hydrated datasets, or other row-level outputs.

## Validate a public release

Run the standard-library release check before publishing:

```bash
python Scripts/validate_public_release.py
```

The validator checks required documents, tracked filenames, Markdown links, screenshot dimensions and canonical names, and the Git tracked-file count. A missing Channel Influence Map export is reported as a warning; prohibited data or a tracked placeholder is a failure.

## Privacy approach

The public package excludes raw Google Takeout exports, hydrated and cleaned row-level datasets, watch history, API keys, environment files, local Power BI working directories, backups, and `.pbix` files. The tracked CSVs contain grouped analytical outputs rather than individual video records. Aggregate reports still reveal an interest profile, so every release requires a human privacy review.

The face-blurred [Modified Canto Choke evidence visuals](Evidence/modified-canto-choke/) are intentionally narrow supporting evidence. Face blurring reduces identifiability but does not guarantee anonymity because clothing, body shape, setting, and source context may remain recognizable.

## Dashboard status

Five documented Power BI pages have non-placeholder public screenshots. The Channel Influence Map page is documented, but its genuine export has not been supplied. The repository does not embed a substitute. See the [dashboard evidence table](dashboard/README.md#evidence-status) for page-level details and screenshot-currency notes.

## Limitations

- Deleted, private, or restricted videos cannot be fully recovered through the API.
- Theme classification is rule-based and depends on titles, tags, channel names, descriptions, and broad YouTube categories.
- Metadata reflects hydration-time state, not necessarily the state when an item was saved.
- Saved records do not establish viewing, comprehension, behavior change, demonstrated skill, or mastery.
- The private source data is required for end-to-end metric reproduction.
- Dashboard screenshots are public evidence of exported pages, not a substitute for the private `.pbix` model.

