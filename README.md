# YouTube History Research Project

A reproducible personal data analysis project that turns an enriched YouTube archive into a learning-history case study.

This public package is designed for portfolio review. It includes scripts, charts, documentation, reports, aggregate summary tables, and selected privacy-treated evidence visuals. It intentionally excludes raw YouTube export files and row-level personal viewing-history datasets.

## Project Goal

The project analyzes a curated YouTube archive as a record of self-directed learning. It asks:

- Which creators and themes appeared most often?
- How did interests evolve over time?
- Which domains became sustained study areas?
- What does the archive show about learning behavior, without making unsupported psychological claims?

## Data Source

The private source data came from a YouTube history / playlist archive that was hydrated with the YouTube Data API v3. The hydration added metadata such as video title, channel, published date, category, duration, view count, tags, and availability status.

Public release note: raw and row-level datasets are excluded from this package.

## Key Findings

- Total playlist entries analyzed in the private run: 3,536
- Unique video IDs hydrated: 2,847
- Active/retrievable entries in final analysis: 3,101
- Unavailable/deleted/private entries: 435
- Dominant theme: Brazilian Jiu-Jitsu
- Peak activity year: 2024
- The archive shows repeated long-term study signals across skill, discipline, craft, and systems-oriented content.

## Evidence Visuals

- [Modified Canto Choke Evidence Visuals](Evidence/modified-canto-choke/) â€” face-blurred visual sequence supporting the Brazilian Jiu-Jitsu learning-archive case study.
- Main archive image: [`archive_main_picture_face_blurred.png`](Evidence/modified-canto-choke/archive_main_picture_face_blurred.png)

## Folder Structure

```text
YouTube Research Public/
    Analysis/          Aggregate CSV outputs only
    Charts/            PNG visualizations
    Documentation/     Data dictionary and classification rules
    Evidence/          Privacy-treated evidence visuals
    Reports/           Markdown and HTML reports
    Scripts/           Reproducible analysis scripts
    README.md
    requirements.txt
    .gitignore
    PUBLICATION_CHECKLIST.md
```

## How to Reproduce With Your Own Data

1. Export your YouTube data.
2. Hydrate video IDs using the YouTube Data API v3 or an equivalent metadata source.
3. Place your private input files in a local `Raw/` folder.
4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Run the pipeline:

```bash
python Scripts/run_all.py
```

Do not commit `Raw/`, `Clean/`, or row-level CSV outputs to a public repository.

## Privacy Approach

This public package excludes:

- raw YouTube exports
- hydrated full row-level datasets
- clean/themed row-level personal history files
- API keys
- environment files
- Python cache files

Only aggregate summaries, reports, charts, scripts, documentation, and privacy-treated evidence visuals are included.

## Limitations

- Deleted/private videos cannot be recovered through the YouTube API.
- Theme classification is rule-based, not machine learning.
- Classification quality depends on title, tags, channel names, and descriptions.
- YouTube categories are broad and often not specific enough for research themes.
- Saved videos are not the same as watched videos, unless the source archive explicitly records watch events.
- Face blurring reduces identifiability but does not guarantee anonymity because clothing, body shape, gym context, and source-video context may still be recognizable.

## Suggested GitHub Use

This package can be published as a portfolio project demonstrating:

- API-based data enrichment
- data cleaning
- feature engineering
- rule-based classification
- visualization
- reproducible reporting
- privacy-aware public release practices
- evidence packaging with public/private data separation

## Power BI Dashboard

A Power BI dashboard has been added under `/dashboard`.

It contains a portfolio-safe visualization layer for the YouTube Learning Archive, including:

- Knowledge Intelligence Overview
- Operator Evolution Timeline
- Channel Influence Map

Raw personal data is excluded for privacy.
