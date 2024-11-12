FROM python:3.11-slim AS base

FROM base AS dependencies
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    sqlite3 \
    gcc \
    && apt-get clean && rm -rf /var/lib/apt/lists/*



RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

FROM base AS app
WORKDIR /app

COPY --from=dependencies /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY . .

# EXPOSE 8000

CMD ["python", "app/main.py"]
