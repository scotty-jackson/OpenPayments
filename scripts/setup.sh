#!/bin/bash

# Global Factor Lab - Automated Setup Script
# This script automates the setup process for development

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo ""
echo -e "${BLUE}======================================"
echo "Global Factor Lab - Automated Setup"
echo -e "======================================${NC}"
echo ""

# Step 1: Check prerequisites
echo -e "${BLUE}Step 1: Checking prerequisites...${NC}"
bash "$PROJECT_ROOT/scripts/check_prerequisites.sh"

echo ""
read -p "Continue with setup? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Setup cancelled."
    exit 1
fi

# Step 2: Set up environment file
echo ""
echo -e "${BLUE}Step 2: Setting up environment file...${NC}"
if [ ! -f "$PROJECT_ROOT/.env" ]; then
    cp "$PROJECT_ROOT/.env.example" "$PROJECT_ROOT/.env"
    echo -e "${GREEN}✓${NC} Created .env file from template"
    echo -e "${YELLOW}!${NC} Please edit .env and update DATABASE_URL and DATA_DIR"
    echo ""
    read -p "Press Enter after you've updated the .env file..." -r
else
    echo -e "${YELLOW}!${NC} .env file already exists, skipping"
fi

# Load environment variables
if [ -f "$PROJECT_ROOT/.env" ]; then
    export $(cat "$PROJECT_ROOT/.env" | grep -v '^#' | xargs)
fi

# Step 3: Create database
echo ""
echo -e "${BLUE}Step 3: Creating PostgreSQL database...${NC}"
DB_NAME="global_factor_lab"

if psql -lqt | cut -d \| -f 1 | grep -qw "$DB_NAME"; then
    echo -e "${YELLOW}!${NC} Database '$DB_NAME' already exists, skipping"
else
    createdb "$DB_NAME" 2>/dev/null && echo -e "${GREEN}✓${NC} Database '$DB_NAME' created" || echo -e "${RED}✗${NC} Failed to create database (it may already exist or you may need to run this as the postgres user)"
fi

# Step 4: Install backend dependencies
echo ""
echo -e "${BLUE}Step 4: Installing backend dependencies...${NC}"
cd "$PROJECT_ROOT/backend"
pip install -r requirements.txt
echo -e "${GREEN}✓${NC} Backend dependencies installed"

# Step 5: Run database migrations
echo ""
echo -e "${BLUE}Step 5: Running database migrations...${NC}"
cd "$PROJECT_ROOT/backend"
alembic upgrade head
echo -e "${GREEN}✓${NC} Database migrations completed"

# Step 6: Load sample data
echo ""
echo -e "${BLUE}Step 6: Loading sample factor data...${NC}"
cd "$PROJECT_ROOT/backend"
python -m etl.load_factors --config ./etl/config/global_factor_sources.yaml
echo -e "${GREEN}✓${NC} Sample data loaded"

# Step 7: Install frontend dependencies
echo ""
echo -e "${BLUE}Step 7: Installing frontend dependencies...${NC}"
cd "$PROJECT_ROOT/frontend"
npm install
echo -e "${GREEN}✓${NC} Frontend dependencies installed"

# Done
echo ""
echo -e "${GREEN}======================================"
echo "✓ Setup completed successfully!"
echo -e "======================================${NC}"
echo ""
echo "To start the application:"
echo ""
echo -e "${YELLOW}Option 1 - Manual (two terminals):${NC}"
echo "  Terminal 1: cd backend && python main.py"
echo "  Terminal 2: cd frontend && npm run dev"
echo ""
echo -e "${YELLOW}Option 2 - Docker Compose:${NC}"
echo "  docker-compose up"
echo ""
echo "Then open your browser to:"
echo "  Frontend: http://localhost:3000"
echo "  API Docs: http://localhost:8000/docs"
echo ""
