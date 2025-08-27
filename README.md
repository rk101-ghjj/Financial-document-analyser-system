# Financial Document Analyzer - Debug Assignment

## Project Overview
A comprehensive financial document analysis system that processes corporate reports, financial statements, and investment documents using AI-powered analysis agents.

## Getting Started

### Install Required Libraries
```sh
pip install -r requirements.txt
```

### Sample Document
The system analyzes financial documents like Tesla's Q2 2025 financial update.

**To add Tesla's financial document:**
1. Download the Tesla Q2 2025 update from: https://www.tesla.com/sites/default/files/downloads/TSLA-Q2-2025-Update.pdf
2. Save it as `data/sample.pdf` in the project directory
3. Or upload any financial PDF through the API endpoint

**Note:** Current `data/sample.pdf` is a placeholder - replace with actual Tesla financial document for proper testing.

# You're All Set!
🐛 **Debug Mode Activated!** The project has bugs waiting to be squashed - your mission is to fix them and bring it to life.

## Debugging Instructions

1. **Identify the Bug**: Carefully read the code in each file and understand the expected behavior.
2. **Fix the Bug**: Implement the necessary changes to fix the bug.
3. **Test the Fix**: Run the project and verify that the bug is resolved.
4. **Repeat**: Continue this process until all bugs are fixed.

## Expected Features
- Upload financial documents (PDF format)
- AI-powered financial analysis
- Investment recommendations
- Risk assessment
- Market insights

## Run the API

```sh
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Health check:

- GET `/` → returns status message.

Analyze document:

- POST `/analyze` (multipart/form-data)
  - file: PDF file upload
  - query: optional text, defaults to "Analyze this financial document for investment insights"

## API Response

```json
{
  "status": "success",
  "query": "...",
  "analysis": "...",
  "file_processed": "TSLA-Q2-2025-Update.pdf"
}
```

## Bugs fixed

- Fixed wrong requirements filename and added missing dependencies (`uvicorn`, `python-dotenv`, `pypdf`).
- Resolved FastAPI route name shadowing the task function; endpoint now `analyze`.
- Crew kickoff now receives both `query` and `file_path` so tools can read the uploaded PDF.
- Replaced undefined `llm` reference with environment-configured default; adjusted agent prompts to be professional and safe.
- Corrected agent `tools` parameter and removed unsafe/harmful prompt content.
- Implemented robust PDF reading via `PDFSearchTool` and cleaned whitespace handling.
- Rewrote task prompts and expected outputs to be deterministic and compliant.
- Eliminated circular import between API and worker by moving `run_crew` to `service.py`.
- Added Celery queue worker and SQLite persistence with SQLAlchemy models.
- Added safe PDF fallback using `pypdf` if `PDFSearchTool` fails.

## Notes

- Place a sample PDF at `data/sample.pdf` or upload via the `/analyze` endpoint.
- Set any necessary model API keys via environment variables (see CrewAI docs).

## Async processing and database

- Redis URL: `REDIS_URL` (default `redis://localhost:6379/0`)
- Database URL: `DATABASE_URL` (default SQLite `sqlite:///data/app.db`)

Start worker:

```sh
celery -A worker.celery_app worker --loglevel=info
```

Async endpoints:

- POST `/analyze/async` → returns `{ task_id, status: queued }`
- GET `/results/{task_id}` → returns stored result when ready

## Setup and usage

Prerequisites:

- Python 3.12
- Redis running locally or via container

Install:

```sh
pip install -r requirements.txt
```

Environment variables:

- `REDIS_URL` (default `redis://localhost:6379/0`)
- `DATABASE_URL` (default `sqlite:///data/app.db`)
- LLM provider keys as per CrewAI configuration

Run services:

```sh
celery -A worker.celery_app worker --loglevel=info
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## API documentation

Endpoints:

- GET `/` → health check
- POST `/analyze` → synchronous analysis, returns analysis and stores result
- POST `/analyze/async` → enqueues analysis, returns `task_id`
- GET `/results/{task_id}` → fetches stored result by task id

POST `/analyze` (multipart/form-data):

- `file`: PDF file
- `query`: optional text

Response:

```json
{
  "status": "success",
  "query": "...",
  "analysis": "...",
  "file_processed": "filename.pdf"
}
```

POST `/analyze/async` (multipart/form-data):

- `file`: PDF file
- `query`: optional text

Response:

```json
{ "task_id": "<celery-id>", "status": "queued" }
```

GET `/results/{task_id}`:

Response:

```json
{
  "task_id": "<celery-id>",
  "status": "completed",
  "file_name": "filename.pdf",
  "query": "...",
  "result": "...",
  "created_at": "2025-01-01T00:00:00Z"
}
```
