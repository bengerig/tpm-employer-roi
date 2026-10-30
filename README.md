# TPM Employer ROI Tracker

A Streamlit form that collects employer training-pipeline cost data (Talent Pipeline
Management, Strategy 6) and shows a simple ROI estimate per submission and in aggregate.

## Status

**Prototype. Not production-ready.** Single file, local use only. Audited 2026-10-30
(see "History" for what changed from the earlier README).

| Feature | State |
|---|---|
| Submission form (company, contact, hiring, onboarding, training cost, retention, pilot interest) | Works |
| ROI per submission: weeks saved, savings per hire, annual savings, payback ratio | Works |
| View all submissions as a table, download all as JSON | Works |
| Aggregate metrics, industry and pilot-readiness bar charts, ROI table | Works |
| Login, per-employer isolation, database, CSV/Excel/PDF export, Plotly dashboard | **Not built.** Described by an earlier README; the modules were never committed |

## Run (local)

```bash
./run_app.sh
```

Creates `.venv`, installs `requirements.txt`, and serves on `http://127.0.0.1:8501` only.
Data is appended to `employer_submissions.json` in the repo folder (gitignored).

## Verify

```bash
python3 -c "import ast,sys; ast.parse(open('employer_roi_app.py').read())"
./run_app.sh   # then submit one test row and confirm the ROI summary appears
```

## Production readiness (blocking gaps)

- **No authentication or authorization.** Anyone who can reach the port sees and downloads every
  submission, including contact names and emails. Do not bind to `0.0.0.0` or host it publicly.
- **Storage is a flat JSON file** with no locking (concurrent submits can lose data), no backup,
  no encryption, and no retention or deletion path.
- **Validation is minimal**: three required fields and an `@` in the email.
- **ROI model limits**: only onboarding weeks saved x weekly productivity cost x annual hires.
  Turnover, retention and productivity-improvement inputs are collected but unused. "Payback" is
  training cost per hire divided by savings per hire (below 1.0 means it pays back within the first hire).
  `annual_hires_needed` defaults to 0, which makes annual savings 0.
- No privacy notice. The footer uses the "Talent Pipeline Management®" mark; confirm the license
  before any public deployment.

Before real employer data: add SSO or an authenticated host, per-employer access with an admin
aggregate view, a transactional database, input bounds, and a privacy notice.

## Files

`employer_roi_app.py` (the app), `requirements.txt`, `run_app.sh`, `.gitignore`.

## History

- 2026-01-22: a v2 app importing `database.py`, `auth.py`, `analytics.py`, `export_utils.py` was
  uploaded, but those modules were never committed, so it could not run. It was deleted and the
  v1 app restored as `employer_roi_app.py`. The README still described v2 until 2026-10-30.
- 2026-10-30: README rewritten to match the code; `run_app.sh` binds to localhost and uses a venv;
  `use_container_width` replaced with `width="stretch"` (removed in newer Streamlit);
  dependencies bounded; `.gitignore` added.

## Related

System index: [bengerig/agentic-ops](https://github.com/bengerig/agentic-ops) `SYSTEM-MAP.md`.
This repo is public; keep real submissions out of it.
