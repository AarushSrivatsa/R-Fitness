# Build the Vue site first. It is copied into the FastAPI image for same-origin hosting.
FROM node:22-alpine AS frontend-builder

WORKDIR /frontend
COPY frontend/package.json ./
RUN npm install --no-audit --no-fund
COPY frontend/ ./
RUN npm run build

# Install Python dependencies in an isolated stage.
FROM python:3.12-slim AS python-builder

ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /build
COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Runtime image contains only the app, runtime dependencies and built Vue assets.
FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /app

RUN addgroup --system app && adduser --system --ingroup app --home /home/app app

COPY --from=python-builder /opt/venv /opt/venv
COPY backend/alembic.ini ./alembic.ini
COPY backend/alembic ./alembic
COPY --chown=app:app backend/app ./app
COPY --from=frontend-builder --chown=app:app /frontend/dist ./frontend-dist

USER app
EXPOSE 10000

# Apply schema migrations before starting the combined API + website server.
CMD ["sh", "-c", "alembic upgrade head && exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-10000}"]
