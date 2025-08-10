FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml .

RUN pip install uv

COPY ./src ./src
COPY ./alembic ./alembic
COPY ./alembic.ini .

RUN uv pip install --system --no-cache-dir .

ENV PYTHONPATH=/app/src

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
