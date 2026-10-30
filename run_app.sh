#!/bin/bash
# Local, single-user run. Binds to 127.0.0.1 only: the app has no login and shows every
# submission (names, emails, costs) to anyone who can reach it. See README "Production readiness".
set -e
cd "$(dirname "$0")"
[ -d .venv ] || python3 -m venv .venv
.venv/bin/pip install -q -r requirements.txt
echo "TPM Employer ROI app: http://127.0.0.1:8501 (local only, no login)"
exec .venv/bin/streamlit run employer_roi_app.py --server.address 127.0.0.1 --server.port 8501 --server.headless true
