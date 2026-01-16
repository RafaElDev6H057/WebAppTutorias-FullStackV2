# =========================================
# Stage 1: Base Python Image
# =========================================
FROM python:3.12-slim AS base

WORKDIR /code

# Install system dependencies INCLUDING curl for healthcheck
RUN apt-get update && apt-get install -y \
  gcc \
  postgresql-client \
  curl \
  && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# =========================================
# Stage 2: Development
# =========================================
FROM base AS development

WORKDIR /code

# Copy application code
COPY . .

EXPOSE 8000

# Use FastAPI dev mode with hot reload
CMD ["fastapi", "dev", "app/main.py", "--host", "0.0.0.0", "--port", "8000"]

# =========================================
# Stage 3: Production
# =========================================
FROM base AS production

WORKDIR /code

# Copy application code
COPY . .

EXPOSE 8000

# Health check with curl (now available)
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Use Uvicorn for production
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
