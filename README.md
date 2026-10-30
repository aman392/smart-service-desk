# ServiceOps — AI-assisted work order intake

Small field-service operations prototype. Enter a synthetic repair, installation, or quotation request; inspect extracted fields; and see whether basic business rules flag it for review. **The app never dispatches a technician.**

## Features
- Streamlit form with session history and JSON/CSV exports
- Deterministic local demo, without API credentials (clearly labeled)
- Optional real Gemini extraction with structured JSON schema
- Independent validation of phone number, address, asset ID, and urgency
- Two documented prompt versions for future side-by-side evaluation
- Unit tests for a few key validation paths

## Local setup (Windows PowerShell)
```powershell
cd path\to\serviceops-ai
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```
Visit http://localhost:8501. Demo mode works with no key.

## Gemini setup (optional)
1. Get an API key in Google AI Studio. Check model availability and the free tier for your account.
2. Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml` and replace the placeholder locally.
3. Restart Streamlit, choose **Gemini API**, and test a **synthetic** message. Never commit the secrets file.
4. The default model identifier is `gemini-3.5-flash-lite`; change it in the sidebar if your account offers a different supported model.

## Tests
```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

## Limitations
- Sample mode is regex-based, not an LLM. Its extraction is intentionally limited.
- Validation checks are conservative but cannot guarantee complete correctness, fraud prevention, or grounding of all model fields.
- Session state is temporary; no database or persistent history.
- Prompt V1 and V2 have not been experimentally benchmarked. The UI displays them for inspection only.
- API requests in free tiers may have rate limits and privacy implications: use synthetic data.
- Public deployments must configure GEMINI_API_KEY through hosting secrets, not in Git.
