# Builder stage
FROM python:3.12 as builder

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev

RUN pip install poetry

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN poetry install --no-root --no-dev

COPY . /app/

# Builder stage
FROM python:3.12 as runtime

RUN apt-get update && apt-get install -y libpq-dev && apt-get clean && rm -rf /var/lib/apt/lists/*

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

COPY --from=builder /app /app

CMD ["uvicorn", "src.main:app"]
