# Feature Implementation Prompt

## Purpose

This prompt guides model contributors to implement new features in a disciplined, test-first way for the Products REST API project. Follow these instructions exactly to ensure high quality, backward-compatible, and well-tested changes.

---

## Before you implement — ask clarifying questions (required) 💬

Always gather enough context before writing any test or code. At minimum ask the user:

- What's the primary goal and acceptance criteria for the feature?
- Who are the consumers (API clients, internal services, UI) and how will they use it?
- What are the expected inputs, outputs, and error conditions?
- Are any backwards-incompatible changes allowed, or must we be strictly backwards-compatible?
- Are there performance, security, or data-migration constraints?
- Which environments should be used for integration/e2e testing (local, staging)?
- Any design preferences (keep logic in service layer, new endpoint vs extending existing)?

Wait for clear answers before proceeding. If the user isn't sure, propose 2–3 concrete options and recommend one.

---

## Test-first workflow (TDD) ✅

All features must follow a test-first approach:

1. **Write tests first**: Add failing tests that express the feature's acceptance criteria.
   - Unit tests for service/domain logic (`tests/unit/`)
   - Integration tests for repo/database interactions (`tests/integration/`)
   - API / contract tests for endpoints (`tests/integration/test_product_api.py` or `tests/e2e/`)
2. **Run tests** and confirm they fail for the expected reason.
3. **Implement minimal code** to make tests pass. Keep changes small and focused.
4. **Refactor** for clarity and remove duplication while keeping tests green.
5. **Add/update documentation** (README, OpenAPI schema, CHANGELOG) and update any example requests.
6. **Run full test suite** and linters (`make test`, `make lint`) before opening a PR.

---

## Testing guidelines 🔬

- Use `pytest` markers: `@pytest.mark.unit`, `@pytest.mark.integration`, `@pytest.mark.e2e` as appropriate.
- Prefer parameterized unit tests to cover edge cases.
- For integration tests, use the provided test fixtures (see `tests/conftest.py`) and avoid touching production DB.
- Mock external dependencies (HTTP, queues) with `respx`/`pytest-mock` or similar.
- For API tests, assert HTTP status codes, response schema, and critical business fields (timestamps, ids, deletedAt behavior).

---

## Implementation standards 🔧

- Follow the project's clean architecture: routers → services → repositories → database.
- Keep business logic in `app/services/` and persistence in `app/repositories/` only.
- Use async/await for DB operations (Motor) and tests.
- Update Pydantic schemas in `app/schemas/` and add model validations when needed.
- Ensure timestamps (`createdAt`, `updatedAt`, `deletedAt`) are handled correctly and immutable where specified.

---

## PR & commit expectations 📦

- Use a short, descriptive branch name: `feature/<short-feature>` or `fix/<short-bug>`.
- Include tests and documentation in the same PR.
- Provide a clear PR description: feature summary, acceptance criteria, test coverage, and any migration steps.
- Keep commits small and focused; prefer several small commits over one large one.

---

## Helpful templates & checklists ✅

- When proposing a feature, include:
  - Short description and motivation
  - Acceptance criteria (explicit)
  - Example requests/responses
  - A list of tests you will add
- PR checklist (add to PR description):
  - [ ] Tests added/updated
  - [ ] Documentation updated
  - [ ] Linting passed
  - [ ] All tests passing locally

---

## Example interaction (minimal)

User: "I want endpoint to bulk-update product stock by category."
Model should reply: "Clarifying Qs: Do you want this to be atomic? What should happen for invalid product IDs? Do we allow partial success? Rate limits? Which response shape do you expect?"
After answers, model writes failing tests covering votes for atomicity / partial success, implements minimal service + repo changes, adds endpoint, updates schemas and docs, and finishes with passing tests.

---

## Enforcement

Do not proceed to writing production code until the acceptance criteria and test plan are explicit and acknowledged by the user.

---

If you need to propose a specific feature to implement now, ask the clarifying questions above and present 2–3 design options with your recommended approach.
