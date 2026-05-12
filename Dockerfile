FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    python3-dev \
    musl-dev \
    libffi-dev \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /app/logs

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# Wait for DB, then migrate and start
CMD sh -c "while ! nc -z db 5432; do sleep 1; done; \
    python manage.py migrate && \
    python manage.py collectstatic --noinput && \
    gunicorn config.wsgi:application \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers ${WORKERS:-2} \
    --threads ${THREADS:-2} \
    --worker-class gthread \
    --timeout ${TIMEOUT:-120} \
    --max-requests ${MAX_REQUESTS:-1000} \
    --preload \
    --access-logfile - \
    --error-logfile -"