FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

RUN uv pip install --system --no-cache \
    fastapi \
    uvicorn \
    websockets \
    sqlalchemy \
    pandas \
    dotenv\
    psycopg2-binary \
    faststream[rabbit]

COPY . .

CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}