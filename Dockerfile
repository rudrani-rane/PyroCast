# syntax=docker/dockerfile:1

# =============================================================================
# PyroCast Backend — Multi-stage production Dockerfile
# =============================================================================

FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# -----------------------------------------------------------------------------
# Builder stage — install Python dependencies
# -----------------------------------------------------------------------------
FROM base AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gdal-bin \
    libgdal-dev \
    && rm -rf /var/lib/apt/lists/*

ENV GDAL_CONFIG=/usr/bin/gdal-config

COPY pyproject.toml README.md ./
COPY backend ./backend

RUN pip install --upgrade pip && \
    pip install --prefix=/install -e ".[ml]"

# -----------------------------------------------------------------------------
# Production runtime
# -----------------------------------------------------------------------------
FROM base AS production

RUN groupadd --gid 1000 pyrocast && \
    useradd --uid 1000 --gid pyrocast --create-home pyrocast

COPY --from=builder /install /usr/local
COPY pyproject.toml README.md ./
COPY backend ./backend

RUN chown -R pyrocast:pyrocast /app

USER pyrocast

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "backend.api.main:app", "--host", "0.0.0.0", "--port", "8000"]

# -----------------------------------------------------------------------------
# Development runtime (includes reload)
# -----------------------------------------------------------------------------
FROM production AS development

USER root
RUN pip install --no-cache-dir -e ".[dev]"
USER pyrocast

CMD ["uvicorn", "backend.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
