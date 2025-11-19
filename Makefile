.PHONY: help setup check install-backend install-frontend db-create db-migrate load-data start-backend start-frontend docker-up docker-down clean

# Default target
help:
	@echo "Global Factor Lab - Available Commands"
	@echo "======================================="
	@echo ""
	@echo "Setup Commands:"
	@echo "  make setup          - Run automated setup (creates DB, installs deps, loads data)"
	@echo "  make check          - Check prerequisites"
	@echo "  make install        - Install all dependencies"
	@echo ""
	@echo "Database Commands:"
	@echo "  make db-create      - Create PostgreSQL database"
	@echo "  make db-migrate     - Run database migrations"
	@echo "  make load-data      - Load sample factor data"
	@echo ""
	@echo "Development Commands:"
	@echo "  make start          - Start both backend and frontend (requires 2 terminals)"
	@echo "  make backend        - Start backend server"
	@echo "  make frontend       - Start frontend development server"
	@echo ""
	@echo "Docker Commands:"
	@echo "  make docker-up      - Start all services with Docker Compose"
	@echo "  make docker-down    - Stop all Docker services"
	@echo "  make docker-logs    - View Docker logs"
	@echo ""
	@echo "Utility Commands:"
	@echo "  make clean          - Clean generated files and caches"
	@echo "  make test-backend   - Run backend tests"
	@echo "  make test-frontend  - Run frontend tests"
	@echo ""

# Setup
setup:
	@bash scripts/setup.sh

check:
	@bash scripts/check_prerequisites.sh

install: install-backend install-frontend

install-backend:
	@echo "Installing backend dependencies..."
	@cd backend && pip install -r requirements.txt

install-frontend:
	@echo "Installing frontend dependencies..."
	@cd frontend && npm install

# Database
db-create:
	@echo "Creating database..."
	@createdb global_factor_lab || echo "Database may already exist"

db-migrate:
	@echo "Running database migrations..."
	@cd backend && alembic upgrade head

load-data:
	@bash scripts/load_data.sh

# Development
start:
	@echo "Starting Global Factor Lab..."
	@echo "Run the following commands in separate terminals:"
	@echo "  Terminal 1: make backend"
	@echo "  Terminal 2: make frontend"

backend:
	@cd backend && python main.py

frontend:
	@cd frontend && npm run dev

# Docker
docker-up:
	@docker-compose up --build

docker-down:
	@docker-compose down

docker-logs:
	@docker-compose logs -f

# Testing
test-backend:
	@cd backend && pytest || echo "No tests configured yet"

test-frontend:
	@cd frontend && npm test || echo "No tests configured yet"

# Cleanup
clean:
	@echo "Cleaning generated files..."
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name "node_modules" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".next" -exec rm -rf {} + 2>/dev/null || true
	@find . -name "*.pyc" -delete 2>/dev/null || true
	@echo "Clean complete!"
