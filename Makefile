.PHONY: help install install-dev install-frontend setup venv lint format typecheck test test-unit test-integration test-api test-ml cov pre-commit docker-build docker-up docker-down docker-logs api worker migrate clean

PYTHON := python
PIP := $(PYTHON) -m pip
COMPOSE := docker compose

help: ## Show available commands
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

venv: ## Create Python virtual environment
	$(PYTHON) -m venv .venv
	@echo "Activate with: source .venv/bin/activate (Linux/macOS) or .venv\\Scripts\\activate (Windows)"

install: ## Install production Python dependencies
	$(PIP) install --upgrade pip
	$(PIP) install -e .

install-dev: ## Install Python dependencies including dev tools
	$(PIP) install --upgrade pip
	$(PIP) install -e ".[dev]"
	pre-commit install

install-all: ## Install full stack including ML/geospatial dependencies
	$(PIP) install --upgrade pip
	$(PIP) install -e ".[all]"
	pre-commit install

install-frontend: ## Install frontend Node.js dependencies
	cd frontend && npm ci

setup: venv install-dev install-frontend ## Full local development setup
	@if [ ! -f .env ]; then cp .env.example .env && echo "Created .env from .env.example"; fi

lint: ## Run Ruff linter
	ruff check backend scripts
	ruff format --check backend scripts

format: ## Auto-format Python code
	ruff format backend scripts
	ruff check --fix backend scripts

typecheck: ## Run mypy static type checker
	mypy backend

test: ## Run full test suite with coverage
	pytest

test-unit: ## Run unit tests only
	pytest backend/tests/unit -m unit

test-integration: ## Run integration tests only
	pytest backend/tests/integration -m integration

test-api: ## Run API tests only
	pytest backend/tests -m api

test-ml: ## Run ML validation tests only
	pytest backend/tests -m ml

cov: ## Generate HTML coverage report
	pytest --cov-report=html
	@echo "Coverage report: htmlcov/index.html"

pre-commit: ## Run all pre-commit hooks
	pre-commit run --all-files

docker-build: ## Build all Docker images
	$(COMPOSE) build

docker-up: ## Start all services in detached mode
	$(COMPOSE) up -d

docker-down: ## Stop and remove containers
	$(COMPOSE) down

docker-logs: ## Tail logs from all services
	$(COMPOSE) logs -f

api: ## Run FastAPI development server locally
	uvicorn backend.api.main:app --host 0.0.0.0 --port 8000 --reload

worker: ## Run Celery worker locally
	celery -A backend.workers.celery_app worker --loglevel=info

migrate: ## Apply database migrations (placeholder for Alembic in Phase 2)
	@echo "Database migrations will be configured in Phase 2."

clean: ## Remove build artifacts and caches
	rm -rf .pytest_cache .mypy_cache .ruff_cache htmlcov coverage.xml .coverage
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
