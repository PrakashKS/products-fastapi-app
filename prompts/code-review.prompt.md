# Code Review Guidelines — Products REST API (FastAPI, Python)

This document replaces the generic template and provides targeted code review guidelines for the Products REST API training project. Use these guidelines when reviewing PRs to ensure maintainability, correctness, and safety.

---

## 🏗️ Project Architecture & Structure

- Project layout to check:
  - `app/routers/` — FastAPI routers (thin, only request/response handling)
  - `app/services/` — Business logic and orchestration
  - `app/repositories/` — Database operations (Motor driver usage)
  - `app/models/` — Domain models/entities
  - `app/schemas/` — Pydantic v2 request/response models
  - `app/exceptions/` — Domain-specific exceptions
  - `tests/` — `unit/`, `integration/`, `e2e/`

- Enforce separation of concerns: routers → services → repositories.

---

## 🐍 Python & Pydantic Standards

- **Python version**: 3.12+ features allowed.
- **Pydantic v2**: Use for validation and serialization. Ensure schemas validate on input and control output shapes.
- **Type hints**: All public functions and methods must be typed (parameters and return types).
- **No business logic in routers or repositories**: Keep services responsible for business rules.

---

## ⚡ Async & Database (Motor)

- Ensure all DB access is async using Motor.
- Repositories should return domain objects or dicts, not FastAPI responses.
- Validate that database calls are properly awaited and that cursors are consumed safely.
- Avoid expensive synchronous operations in request handlers — push them to background tasks if needed.

---

## ⏱️ Timestamps & Soft Delete

- Validate proper handling of `createdAt`, `updatedAt`, `deletedAt`:
  - `createdAt` must be set once at creation and not changed.
  - `updatedAt` must be updated on modifications.
  - Soft deletes set `deletedAt` (do not hard delete by default).
- Ensure endpoints filter out soft-deleted records unless explicitly requested.

---

## 🔒 Security & Validation

- Validate all input with Pydantic; do not trust raw payloads.
- Check for exposure of secrets or raw DB internals (no `_id` leak).
- Ensure error responses do not leak stack traces or sensitive info.
- Confirm that any auth/permission checks exist where required (even if mocked in tests).

---

## 🧪 Testing Requirements

- **Test-first mindset**: Prefer tests that fail before implementing behavior.
- **Unit tests** (`tests/unit/`): Services, domain logic, validation rules. Use `pytest` and `pytest-asyncio`.
- **Integration tests** (`tests/integration/`): Repository and API-level interactions with a test DB fixture (see `tests/conftest.py`). Use `httpx.AsyncClient` to exercise routers.
- **E2E tests** (`tests/e2e/`): Full workflows (Playwright or HTTP-based end-to-end tests).
- Tests must assert HTTP status codes, response shapes, timestamps, and soft-delete behavior.

---

## 🛠️ Code Quality Checklist

- [ ] **Architecture**: Code follows routers → services → repositories pattern.
- [ ] **Types**: Functions and public methods are typed.
- [ ] **Validation**: All user input validated with Pydantic schemas.
- [ ] **Async**: No synchronous DB calls; no missing `await`.
- [ ] **Timestamps**: `createdAt` immutable; `updatedAt` updated; `deletedAt` used for soft delete.
- [ ] **Error Handling**: Use `app/exceptions` and map to HTTP status codes.
- [ ] **No prints**: Use logging; avoid `print()`.
- [ ] **No raw exceptions to clients**.
- [ ] **No secrets or `.env` leaks** in code or logs.
- [ ] **Tests**: Unit/integration/e2e added or updated.
- [ ] **Docs**: OpenAPI updated (routes/schemas), README or QUICKSTART updated if behavior changed.

---

## 🔍 Review Guidance & Priorities

- Blockers (must fix): security issues, leaking credentials, breaking API contracts, missing tests for critical behavior.
- High: incorrect async usage, broken DB queries, missing validation, incorrect timestamp handling.
- Medium: code-style, missing docs, minor performance issues.
- Low: naming, small refactors, test readability improvements.

---

## ✅ PR & Commit Expectations

- Branch naming: `feature/<short>` or `fix/<short>`.
- PR should include focused commits, tests first (failing), implementation, and final green tests.
- PR description must have: feature summary, acceptance criteria, test plan, migration steps (if any).
- Add changelog entry or note in PR when public API or behavior changes.

---

## 💬 How to comment on a PR

- Be specific, actionable, and kind. Cite code snippets and recommend fixes.
- Prefer small, incremental suggestions over large rewrites.
- When suggesting alternatives, explain trade-offs.

---

**Remember:** Code reviews here are about correctness, safety, and maintainability for the Products REST API. Aim to keep the API stable, well-tested, and easy to reason about.
