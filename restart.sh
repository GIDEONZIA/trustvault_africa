#!/bin/bash
set -e

echo "🔴 Stopping TrustVault Africa..."
docker compose down -v

echo "🗑️  Cleaning old images..."
docker rmi trustvault-web trustvault-worker 2>/dev/null || true

echo "🔨 Rebuilding..."
docker compose build --no-cache

echo "🟢 Starting database and cache..."
docker compose up -d db redis

echo "⏳ Waiting for database..."
sleep 5

echo "📦 Running migrations..."
docker compose run --rm web python manage.py migrate

echo "🎨 Collecting static files..."
docker compose run --rm web python manage.py collectstatic --noinput

echo "🚀 Starting web, worker, and scheduler..."
docker compose up -d web worker beat

echo "✅ TrustVault Africa is live!"
docker compose ps

echo ""
echo "🔗 Admin: http://localhost:8000/admin/"
echo "🔗 API: http://localhost:8000/api/"