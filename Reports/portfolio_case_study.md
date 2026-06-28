# Portfolio Case Study: YouTube History as a Personal Learning Archive

## Problem

A raw YouTube archive is difficult to interpret because it is usually just a collection of video IDs, playlist records, timestamps, and inconsistent metadata. The project goal was to turn that archive into a structured learning-history analysis while preserving privacy for public presentation.

## Method

The workflow used a two-stage approach:

1. Hydrate YouTube video IDs with metadata using the YouTube Data API v3.
2. Analyze the enriched archive through a reproducible Python pipeline.

The final analysis examined channels, themes, time periods, video formats, and availability status.

## Tools Used

- Python
- pandas
- matplotlib
- YouTube Data API v3
- Markdown reporting
- HTML reporting
- CSV-based reproducible outputs

## Data Engineering Steps

- Loaded hydrated YouTube archive files.
- Audited columns, missing values, duplicates, and unavailable records.
- Parsed timestamps into year, month, quarter, weekday, and life-phase features.
- Parsed ISO 8601 video durations into seconds and duration buckets.
- Converted numeric fields such as views and likes.
- Exported clean analysis tables and aggregate summaries.

## Classification Approach

The project used a transparent rule-based classifier instead of a black-box model. Videos were assigned themes using:

- channel names
- video titles
- tags
- descriptions
- YouTube categories

Channel-name matches were weighted more heavily than keyword matches because recurring creator identity is often a stronger signal than a single generic title.

## Key Findings From the Private Run

- The archive contained 3,536 playlist entries and 2,847 unique hydrated video IDs.
- The dominant theme was Brazilian Jiu-Jitsu.
- Discipline / mindset content appeared as a persistent long-term category.
- 2024 was the peak activity year.
- A meaningful portion of the archive was unavailable because videos had been deleted, made private, or otherwise restricted.
- The archive reflected structured, repeated study behavior rather than random accumulation.

## Limitations

- Saved videos are not always equivalent to watched videos.
- Deleted/private videos cannot be fully recovered.
- Theme classification is approximate and rule-based.
- YouTube metadata reflects the state of videos at hydration time, not necessarily when they were saved.
- Aggregate reports can still reveal personal interests, so publication requires privacy review.

## Future Improvements

- Add optional local-only notebooks for deeper analysis.
- Add tests for classifier behavior.
- Create a sample synthetic dataset so the public repo can run end-to-end without private data.
- Add an interactive dashboard.
- Compare playlist-save behavior with actual watch-history behavior, if available.
