# ServiceOps — AI-assisted work order intake

# Smart Service Desk

A Python application for organizing and reviewing incoming service requests.

It uses Google's Gemini API to extract information such as the request type, equipment ID, priority, contact details, and service location from customer messages. The extracted information is checked against basic validation rules to identify requests that need additional details before processing.

## Features
- Extracts service request details using the Gemini API.
- Supports a local demo mode without an API key.
- Checks contact numbers, service locations, and other required information.
- Identifies incomplete requests and flags them for manual review.
- Displays structured results in JSON format.
- Maintains a temporary history of processed requests.
- Supports downloading individual results as JSON and session history as CSV.
- Includes two prompt configurations for experimenting with extraction behavior.
- Includes automated tests for core validation rules.

## Local setup (Windows PowerShell)
```powershell
cd path\to\serviceops-ai
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```
Visit http://localhost:8501. Demo mode works with no key.

## Gemini API Configuration
1. Get an API key in Google AI Studio. Check model availability and the free tier for your account.
2. Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml` and replace the placeholder locally.
3. Restart Streamlit, choose **Gemini API**, and test a **synthetic** message. Never commit the secrets file.
4. The default model identifier is `gemini-3.5-flash-lite`; change it in the sidebar if your account offers a different supported model.

## Tests
```powershell
.\.venv\Scripts\python.exe -m pytest -q
```


## Current Limitations
- The application focuses on request intake and validation. Scheduling and dispatch management are outside its current scope.
- Request history is stored only during the active session.
- Demo mode uses simple pattern matching and is less flexible than Gemini extraction.
- AI-generated results may occasionally be inaccurate, so requests requiring clarification are flagged for review.
- The two prompt versions are available for comparison, but a formal evaluation has not yet been completed.
- Gemini API availability and usage limits depend on the configured account.
