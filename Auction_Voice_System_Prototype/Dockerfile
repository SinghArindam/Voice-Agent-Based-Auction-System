# ---------- build image ----------
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# system deps (for wheels that need gcc)
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# project sources
COPY backend backend
COPY agent   agent
COPY seed_fake_data.py .
# serve HTML through Nginx (separate container) but keep a copy for reference
# COPY simulate_prototype.html /app/simulate_prototype.html

EXPOSE 8000
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
