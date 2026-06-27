# PyroCast

**Real-Time Physics-Informed Wildfire Spread Prediction Platform**

PyroCast is an enterprise-grade wildfire intelligence platform that predicts active fire spread over the next 12–24 hours by combining NASA FIRMS satellite detections, NOAA HRRR weather forecasts, USGS LANDFIRE terrain data, and Physics-Informed Neural Networks (PINNs).

---

## Architecture Overview

```
PyroCast/
├── backend/                 # Python FastAPI application
│   ├── api/                 # REST API routes and application factory
│   ├── config/              # Environment-based settings (Pydantic)
│   ├── core/                # Logging, middleware, exceptions
│   ├── models/              # SQLAlchemy ORM models
│   ├── schemas/             # Pydantic request/response schemas
│   ├── services/            # Business logic layer
│   ├── repositories/        # Database access layer
│   ├── workers/             # Celery background tasks
│   ├── ml/                  # PINN models and training
│   ├── physics/             # Rothermel and fire behavior equations
│   ├── pipelines/           # Data ingestion and feature engineering
│   ├── utils/               # Shared utilities (Redis, etc.)
│   └── tests/               # Unit, integration, and API tests
├── frontend/                # Next.js 15 dashboard
├── scripts/                 # Database initialization scripts
├── models/checkpoints/      # ML model weights (gitignored artifacts)
├── .github/workflows/       # CI/CD pipelines
└── docker-compose.yml       # Local development stack
```

---

## Tech Stack

| Layer        | Technology                                      |
| ------------ | ----------------------------------------------- |
| Backend      | Python 3.12, FastAPI, Pydantic, Uvicorn         |
| AI/ML        | PyTorch, NumPy, Rasterio, scikit-learn          |
| Geospatial   | GeoPandas, Shapely, PyProj, GDAL, Herbie, xarray |
| Database     | PostgreSQL 16 + PostGIS                         |
| Cache/Queue  | Redis, Celery                                   |
| Frontend     | Next.js 15, React 19, TailwindCSS, Mapbox GL    |
| DevOps       | Docker, GitHub Actions, pre-commit              |

---

## Prerequisites

- Python 3.12+
- Node.js 22+
- Docker & Docker Compose
- Make (optional, recommended)

---

## Quick Start

### 1. Clone and configure environment

```bash
cp .env.example .env
# Edit .env — set SECRET_KEY (min 32 chars), NASA_FIRMS_API_KEY, MAPBOX_ACCESS_TOKEN
```

### 2. Local development (without Docker)

```bash
# Backend
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
pre-commit install
make api

# Frontend (separate terminal)
cd frontend && npm install && npm run dev
```

### 3. Docker Compose (full stack)

```bash
cp .env.example .env
docker compose up -d
```

| Service  | URL                          |
| -------- | ---------------------------- |
| API      | http://localhost:8000        |
| API Docs | http://localhost:8000/docs   |
| Frontend | http://localhost:3000        |
| Postgres | localhost:5432               |
| Redis    | localhost:6379               |

---

## Environment Variables

See [`.env.example`](.env.example) for the full list. Required variables:

| Variable              | Description                              |
| --------------------- | ---------------------------------------- |
| `SECRET_KEY`          | Application secret (minimum 32 chars)    |
| `NASA_FIRMS_API_KEY`  | NASA FIRMS API key for fire detections   |
| `MAPBOX_ACCESS_TOKEN` | Mapbox token for geospatial visualization |
| `DATABASE_URL`        | PostgreSQL async connection string       |
| `REDIS_URL`           | Redis connection string                  |

---

## Development Commands

```bash
make help              # List all available commands
make lint              # Run Ruff linter and format check
make format            # Auto-format Python code
make typecheck         # Run mypy
make test              # Run full test suite with coverage
make test-unit         # Unit tests only
make test-api          # API endpoint tests
make docker-up         # Start all Docker services
make docker-down       # Stop Docker services
make pre-commit        # Run all pre-commit hooks
```

---

## API Endpoints (Phase 1)

| Method | Path      | Description                    |
| ------ | --------- | ------------------------------ |
| GET    | `/health` | Liveness probe                 |
| GET    | `/ready`  | Readiness probe with checks    |
| GET    | `/docs`   | OpenAPI interactive docs       |

---

## Testing

```bash
# Full suite
pytest

# By category
pytest -m unit
pytest -m integration
pytest -m api

# With HTML coverage report
pytest --cov-report=html
```

---

## Project Phases

| Phase | Scope                                           | Status      |
| ----- | ----------------------------------------------- | ----------- |
| 1     | Project foundation, config, Docker, CI            | **Current** |
| 2     | Database models, migrations, auth                 | Planned     |
| 3     | NASA FIRMS data ingestion                       | Planned     |
| 4     | NOAA HRRR weather retrieval                     | Planned     |
| 5     | LANDFIRE terrain pipeline                       | Planned     |
| 6     | Feature engineering & raster harmonization      | Planned     |
| 7     | PINN model architecture & physics loss          | Planned     |
| 8     | Simulation API & Celery workers                 | Planned     |
| 9     | Interactive dashboard & map visualization       | Planned     |
| 10    | Production deployment & monitoring              | Planned     |

---

## License

Proprietary — All rights reserved.
