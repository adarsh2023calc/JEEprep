FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory to project root
WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy project
COPY . /app/

# Install Python deps
RUN pip install --no-cache-dir -r requirements.txt

# Collect static
RUN python jeeprep/manage.py collectstatic --noinput

EXPOSE 8000

ENV DJANGO_SETTINGS_MODULE=jeeprep.settings

cd jeeprep

CMD ["gunicorn", "jeeprep.wsgi:application", "--bind", "0.0.0.0:8000"]
