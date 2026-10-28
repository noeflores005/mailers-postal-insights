# Mailers — Postal Insights

Double-click **Open Mailers.cmd** or open **dashboard.html** in Brave, Chrome or Edge. Keep the data, reports and demo folders alongside it. The dashboard works offline without Python, an account, installation or an API key.

For a local web-server preview, run `python app.py`. It opens the browser and listens only on 127.0.0.1. Press Ctrl+C to stop. If the port is occupied, use `python app.py --port 8770`.

## Submission

- Dashboard: dashboard.html
- Presentation: Mailers Final Presentation.pptx
- Speaking script and backup demo route: PRESENTATION.md and demo/
- Form-ready description: SUBMISSION.md
- Source definitions, evaluation and limitations: METHODS.md
- Source PDFs, hashes, text extracts and CSV data: reports/ and data/

## Rebuild

Only re-extracting PDF text requires `python -m pip install -r requirements.txt`. Other data scripts use Python's standard library. Run `python ingest.py`, `python build_data.py`, `python finish_data.py`, then `python test_data.py`. Adapt ingest.py source paths if you move laptops. The HTML loads data/dashboard-data.js after rebuilding.

## Using Codex

Keep this chat for project changes, or choose this folder as a local project in Codex. Describe the outcome and checks: “Add a comparison of two mail markets and verify units,” or “Rebuild from this new report and show the differences.” Review the changed files, try the dashboard and report any problems. The saved local files are the application; Codex helps edit and check them.

## Scope

Student submission prototype, not an official USPS product. Forecast scenarios use aggregate history through 2023; newer per-household data remains separate. NLP is extractive TextRank, not generative AI. Historical classifications are not fully harmonized. No measured 50% efficiency improvement is claimed. See METHODS.md.
