# FitBuddy – AI Fitness Plan Generator

FitBuddy is a FastAPI + Jinja2 + SQLite application for generating personalized 7-day workout plans, nutrition/recovery tips, and feedback-based plan updates using Gemini.

## Architecture
- Frontend: HTML + Jinja2
- Backend: FastAPI
- AI: Gemini REST API
- Database: SQLite + SQLAlchemy
- Routes: `/`, `/generate-workout`, `/submit-feedback`, `/view-all-users`

## Windows 7 / Python 3.8 compatibility
The project avoids modern Python 3.10+ union syntax and built-in generic syntax. It also avoids the `google-genai` Python SDK because current releases require newer Python versions. Gemini is called through the official REST `generateContent` endpoint instead.

## Run
```text
py -m pip install -r requirements.txt
py -m uvicorn app.main:app --reload
```
Then open `http://127.0.0.1:8000`.

## API key
Copy `.env.example` to `.env` if needed and set your own `GEMINI_API_KEY`. Never share or commit the real key.
