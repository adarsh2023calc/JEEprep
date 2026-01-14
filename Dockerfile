FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=jeeprep.settings

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy project
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Collect static files
RUN python manage.py collectstatic --noinput



EXPOSE 8000

CMD ["gunicorn", "jeeprep.wsgi:application", "--bind", "0.0.0.0:8000"]

