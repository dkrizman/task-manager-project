# Start PostgreSQL
echo "🐘 Starting PostgreSQL..."
docker-compose -f docker-compose.dev.yml up -d db

# Wait for database to be ready
echo "⏳ Waiting for database to be ready..."
sleep 5

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✅ Virtual environment activated"
fi

# Update environment for local development
export DATABASE_URL="postgresql://postgres:password@localhost:5432/taskmanager"

# Run migrations
echo "🔄 Running database migrations..."
alembic upgrade head

# Seed database
echo "🌱 Seeding database..."
python scripts/seed_db.py

# Start the application
echo "🚀 Starting application..."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
