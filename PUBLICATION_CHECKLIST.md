# Publication checklist

Use this checklist before pushing a public release of the YouTube Learning Archive.

## Automated validation

- [ ] Run `python Scripts/validate_public_release.py`.
- [ ] Confirm the command exits successfully and review every warning.
- [ ] Run `git diff --check`.
- [ ] Run `python -m compileall Scripts`.
- [ ] Record the tracked-file count reported by the validator for the release review.

## Privacy checks

- [ ] No `Raw/`, `Clean/`, Takeout, backup, or private working directory is tracked.
- [ ] No playlist-entry, watch-history, hydrated, clean, or themed row-level dataset is tracked.
- [ ] No video-level IDs, URLs, titles, timestamps, descriptions, or personal account exports were added.
- [ ] No API key, secret, `.env`, or environment-specific credential file is tracked.
- [ ] No `.pbix` file or private Power BI working directory is tracked.
- [ ] Every tracked CSV has been reviewed as an aggregate output, not trusted by filename alone.
- [ ] Aggregate channel and tag outputs have received a human disclosure-risk review.
- [ ] Privacy-treated evidence visuals remain acceptable for public release despite residual contextual identification risk.

## Documentation checks

- [ ] `README.md`, `CASE_STUDY.md`, `PROJECT_MANIFEST.md`, and this checklist exist.
- [ ] The root README links to the case study and dashboard gallery.
- [ ] Saved playlist activity is not described as verified watch history.
- [ ] Inferred themes are not described as proof of intent, skill, or mastery.
- [ ] Metrics remain consistent: 3,536 entries; 2,847 unique IDs; 3,101 retrievable; 435 unavailable; 9.5 years; Brazilian Jiu-Jitsu dominant; 2024 peak.
- [ ] Relative Markdown links resolve without machine-specific local paths.
- [ ] No mojibake or other text-encoding artifacts remain.

## Dashboard evidence checks

- [ ] Every embedded screenshot is readable and non-placeholder.
- [ ] Screenshot filenames use canonical lowercase names.
- [ ] No missing page is represented by a generated or reconstructed substitute.
- [ ] A genuine `channel_influence_map.png` export has been supplied manually, or the missing-evidence warning remains prominent.
- [ ] The stale labels inside `system_architecture.png` are corrected by a genuine re-export, or the limitation remains prominent.
- [ ] Screenshot contents have been reviewed for row-level or identifying information.

## GitHub checks

- [ ] Work is on a non-default branch.
- [ ] Only intentional files are staged.
- [ ] Commit history is reviewed for previously published sensitive material.
- [ ] The pull request lists validation results and unresolved evidence limitations.
- [ ] The pull request explicitly confirms that no raw data or `.pbix` file was added.
