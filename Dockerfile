# --- Stage 1: Builder ---
FROM python:3.11-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies to a temporary folder
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# --- Stage 2: Final Runtime ---
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=jeeprep.settings

WORKDIR /app

# Only install runtime library for Postgres (much smaller than build-essential)
RUN apt-get update && apt-get install -y libpq5 && rm -rf /var/lib/apt/lists/*

# Copy only the compiled python packages from builder
COPY --from=builder /install /usr/local

# Copy project files
COPY . .

# Collect static
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "jeeprep.wsgi:application", "--bind", "0.0.0.0:8000"]


