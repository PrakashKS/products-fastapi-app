# Debug Analysis Prompt — Products REST API (FastAPI, Python)

## Overview

This debug guide is tailored for the Products REST API: a FastAPI app using Python 3.12+, Motor (async MongoDB driver), Pydantic v2 for validation, and pytest-based tests. Use this as your checklist when investigating bugs or failures.

## Quick project map

- `app/main.py` — app startup
- `app/routers/` — HTTP routes (thin controllers)
- `app/services/` — business logic and use-cases
- `app/repositories/` — async DB access (Motor)
- `app/schemas/` — Pydantic v2 request/response models
- `app/models/` — domain entities
- `tests/` — `unit/`, `integration/`, `e2e/`

---

## Systematic Debug Approach

1. Reproduce reliably

- Reproduce the issue locally or in a test environment with the same data/inputs.
- Use the health endpoint: GET http://localhost:8000/health

2. Check configuration & environment

- Verify `.env` variables are set (do not commit real credentials).
- Confirm `MONGODB_URL`, `MONGODB_DATABASE`, `API_V1_PREFIX`, and `DEBUG` are correct.
- Start the app: `make run` or `uvicorn app.main:app --reload --port 8000`.

3. Inspect logs and error traces

- Check console/log output from Uvicorn. Improve logging if stack traces are insufficient.
- Ensure exceptions are mapped to proper HTTP codes (see `app/exceptions`).

4. Database connectivity & queries

- Verify MongoDB is reachable (mongosh or `mongo` CLI).
- Confirm repository methods use `await` and return expected documents.
- Look for missing indexes for slow queries and check collection sizes.
- Avoid leaking internal `_id` fields in responses.

5. Async issues (missing await, blocking code)

- Look for missing `await` on async functions (common cause of unexpected behavior).
- Avoid blocking CPU work in request handlers; use background tasks for heavy jobs.

6. Validation and Pydantic schemas

- Ensure inputs are validated by Pydantic schemas and error messages are clear.
- Check output serialization: `deletedAt` and timestamps must be in ISO UTC.

7. Timestamps & soft delete behavior

- Confirm `createdAt` is set only at creation; `updatedAt` updates on modifications.
- Soft deletes should set `deletedAt` rather than removing the document.
- Ensure list endpoints filter out soft-deleted records by default.

8. Tests & CI

- Run unit/integration tests: `make test` (or `pytest -q`) and `make test-integration` where applicable.
- Reproduce failing test locally; use `-k` to run a specific test: `pytest -q -k test_name -q`.
- For e2e tests (Playwright), run with `pytest -m e2e` or the configured `make` target.

9. E2E debugging (Playwright)

- Use Playwright's headed mode or `page.pause()` to inspect test flows.
- Ensure backend is running and seeded with test data before e2e runs.

10. Security & sensitive data

- Verify no secrets or `.env` values are printed or committed.
- Check error responses to avoid leaking implementation details.

---

## Debug Checklist

Before investigation:

- [ ] Reproduce issue consistently
- [ ] Confirm environment and config (test DB vs prod)

During investigation:

- [ ] Check logs and stack traces
- [ ] Run failing tests and reproduce locally
- [ ] Inspect DB state and queries
- [ ] Verify Pydantic validation behavior
- [ ] Look for missing `await` or blocking calls

After resolution:

- [ ] Add/adjust tests (unit/integration/e2e) to prevent regression
- [ ] Remove debug/debugging prints
- [ ] Update docs/README if behavior changed
- [ ] Ensure CI passes and add notes in PR

---

## Common Patterns & Quick Fixes

Safe wrapper for async ops:

```python
async def safe_operation(coro, context: str):
    try:
        return await coro
    except Exception as exc:
        logger.error('%s failed: %s', context, exc, exc_info=True)
        raise
```

Logging best practice:

```python
from app.config import settings
import logging
logger = logging.getLogger(settings.APP_NAME)
logger.info('Starting operation', extra={'operation': 'create_product'})
```

Testing commands

- Run all tests: `make test` or `pytest -q`
- Run unit tests: `pytest -q -m unit`
- Run integration tests: `pytest -q -m integration`
- Run a single test: `pytest -q path/to/test.py::test_name -q`
- Run e2e/Playwright: `pytest -q -m e2e`

Toolbox & quick commands

- Start app: `make run` or `uvicorn app.main:app --reload --port 8000`
- Health check: `curl -s http://localhost:8000/health`
- Inspect DB: `mongosh "${MONGODB_URL}"` or use Compass
- Run tests: `make test`

---

Remember: Start by reproducing the issue and writing a failing test where possible; fix the smallest thing to make the test pass, then refactor and add documentation. Keep fixes small and well-tested.
