# Project manifest

This repository is the public, GitHub-safe package for the YouTube Learning Archive Intelligence System.

## Included

- Root overview and portfolio case study
- Reproducible Python analysis scripts
- Aggregate analysis CSVs
- Aggregate PNG charts
- Dashboard documentation and verified public screenshots
- Data dictionary and classification rules
- Markdown and HTML reports
- Privacy-treated supporting visuals
- Publication checklist and automated release validator

## Excluded

- Raw Google Takeout exports
- Playlist-entry and watch-history row-level datasets
- `Raw/` and `Clean/` working directories
- `master_table.csv` and `master_table_hydrated.csv`
- `hydrated_videos.csv`
- `youtube_history_clean.csv` and `youtube_history_themed.csv`
- API keys and environment files
- Power BI `.pbix` files and private working directories
- Local backups and caches

## Dashboard evidence

Five of the six documented dashboard pages have readable, non-placeholder screenshots. The Channel Influence Map export is missing. The System Architecture export is readable but contains stale “5-page model” and “10-script pipeline” labels. See [dashboard/README.md](dashboard/README.md) for the full evidence table.

## Tracked-file count

The tracked-file count changes as the package evolves and is therefore not recorded as a static claim. Verify it at release time with:

```bash
git ls-files | python -c "import sys; print(sum(1 for _ in sys.stdin))"
```

The release validator reports the same count without printing file contents:

```bash
python Scripts/validate_public_release.py
```

## Publication note

Run the validator and complete [PUBLICATION_CHECKLIST.md](PUBLICATION_CHECKLIST.md) before publishing. Automated checks support but do not replace a human review of aggregate disclosure risk, screenshot currency, and commit history.
