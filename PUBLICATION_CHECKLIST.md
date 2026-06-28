# Publication Checklist

Use this before uploading the project to GitHub or sharing it publicly.

## Privacy Checks

- [ ] `Raw/` folder is not included.
- [ ] `Clean/` folder is not included.
- [ ] No row-level YouTube history CSVs are included.
- [ ] No API keys are present.
- [ ] No `.env` file is present.
- [ ] No personal account export files are present.
- [ ] No full watch-history or playlist-entry dataset is included.

## File Checks

- [ ] `README.md` exists.
- [ ] `.gitignore` exists.
- [ ] `requirements.txt` exists.
- [ ] `Scripts/` contains the reproducible pipeline scripts.
- [ ] `Documentation/` contains the data dictionary and classification rules.
- [ ] `Reports/` contains markdown reports.
- [ ] `Charts/` contains PNG outputs.
- [ ] `Analysis/` contains aggregate CSV summaries only.

## Data Leakage Checks

Search the project folder for sensitive strings before publishing:

```powershell
Select-String -Path .\* -Pattern "AIza","YOUTUBE_API_KEY","api_key","master_table","youtube_history_clean","youtube_history_themed" -Recurse
```

Review every match manually.

## GitHub Checks

- [ ] Repository description is clear.
- [ ] README explains that raw data is excluded for privacy.
- [ ] Scripts are documented.
- [ ] Reports do not expose anything you are uncomfortable sharing.
- [ ] Charts are safe to publish.
- [ ] Commit history does not contain removed private files.

## Final Review

- [ ] Open the repo in a clean folder.
- [ ] Confirm excluded files are truly absent.
- [ ] Zip or commit only the public-safe folder.
- [ ] Keep the private project folder offline or in private storage.
