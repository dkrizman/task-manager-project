#!/bin/bash
set -e

echo "🐳 Starting Task Manager API with Docker..."

# Build and start services
docker-compose up --build -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 10

# Run migrations
echo "🔄 Running database migrations..."
docker-compose --profile migration run --rm migrate

# Show running services
echo "📊 Services Status:"
docker-compose ps

echo "✅ Application is running!"
echo "🌐 API: http://localhost:8000"
echo "📚 Docs: http://localhost:8000/docs"
echo "🐘 PostgreSQL: localhost:5432"
