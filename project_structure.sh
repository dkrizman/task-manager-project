# Create main directories
mkdir app tests scripts

# Create app subdirectories
mkdir app/api app/core app/models app/schemas app/services

# Create configuration and deployment files
touch .env .env.example .gitignore requirements.txt requirements-dev.txt
touch Dockerfile docker-compose.yml README.md

# Create main application files
touch app/__init__.py
touch app/main.py
touch app/core/__init__.py
touch app/core/config.py
touch app/core/database.py
touch app/models/__init__.py
touch app/schemas/__init__.py
touch app/api/__init__.py
touch app/services/__init__.py

# Create test files
touch tests/__init__.py
touch tests/test_main.py

# Create scripts
touch scripts/start.sh
touch scripts/test.sh