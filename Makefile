# Makefile for Products REST API

.PHONY: help install run test test-unit test-integration test-e2e test-coverage clean lint format

help:
	@echo "Products REST API - Available Commands"
	@echo "======================================"
	@echo "make install          - Install dependencies"
	@echo "make run             - Run the development server"
	@echo "make test            - Run all tests"
	@echo "make test-unit       - Run unit tests only"
	@echo "make test-integration - Run integration tests only"
	@echo "make test-e2e        - Run E2E tests (server must be running)"
	@echo "make test-coverage   - Run tests with coverage report"
	@echo "make lint            - Run linting"
	@echo "make format          - Format code"
	@echo "make clean           - Clean up generated files"

install:
	@echo "Installing dependencies..."
	uv pip install -e .
	uv pip install -e ".[dev]"

run:
	@echo "Starting development server..."
	uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test:
	@echo "Running all tests..."
	uv run pytest -v

test-unit:
	@echo "Running unit tests..."
	uv run pytest -v -m unit

test-integration:
	@echo "Running integration tests..."
	uv run pytest -v -m integration

test-e2e:
	@echo "Running E2E tests..."
	@echo "Note: Make sure the server is running!"
	uv run pytest -v -m e2e

test-coverage:
	@echo "Running tests with coverage..."
	uv run pytest --cov=app --cov-report=html --cov-report=term

lint:
	@echo "Linting code..."
	uv run ruff check app/ tests/

format:
	@echo "Formatting code..."
	uv run black app/ tests/

clean:
	@echo "Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name ".coverage" -delete 2>/dev/null || true
