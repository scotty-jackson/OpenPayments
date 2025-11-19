#!/bin/bash

# Global Factor Lab - Prerequisites Checker
# This script checks if all required dependencies are installed

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "======================================"
echo "Global Factor Lab - Prerequisites Check"
echo "======================================"
echo ""

# Track if all prerequisites are met
ALL_OK=true

# Check Python
echo -n "Checking Python 3.9+... "
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)

    if [ "$PYTHON_MAJOR" -ge 3 ] && [ "$PYTHON_MINOR" -ge 9 ]; then
        echo -e "${GREEN}✓${NC} Found Python $PYTHON_VERSION"
    else
        echo -e "${RED}✗${NC} Python 3.9+ required (found $PYTHON_VERSION)"
        ALL_OK=false
    fi
else
    echo -e "${RED}✗${NC} Python not found"
    ALL_OK=false
fi

# Check Node.js
echo -n "Checking Node.js 18+... "
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version | sed 's/v//')
    NODE_MAJOR=$(echo $NODE_VERSION | cut -d'.' -f1)

    if [ "$NODE_MAJOR" -ge 18 ]; then
        echo -e "${GREEN}✓${NC} Found Node.js $NODE_VERSION"
    else
        echo -e "${RED}✗${NC} Node.js 18+ required (found $NODE_VERSION)"
        ALL_OK=false
    fi
else
    echo -e "${RED}✗${NC} Node.js not found"
    ALL_OK=false
fi

# Check npm
echo -n "Checking npm... "
if command -v npm &> /dev/null; then
    NPM_VERSION=$(npm --version)
    echo -e "${GREEN}✓${NC} Found npm $NPM_VERSION"
else
    echo -e "${RED}✗${NC} npm not found"
    ALL_OK=false
fi

# Check PostgreSQL
echo -n "Checking PostgreSQL... "
if command -v psql &> /dev/null; then
    PSQL_VERSION=$(psql --version | cut -d' ' -f3)
    echo -e "${GREEN}✓${NC} Found PostgreSQL $PSQL_VERSION"
else
    echo -e "${YELLOW}!${NC} PostgreSQL client not found (may still work if server is running)"
fi

# Check if PostgreSQL is running
echo -n "Checking PostgreSQL server... "
if pg_isready &> /dev/null; then
    echo -e "${GREEN}✓${NC} PostgreSQL server is running"
else
    echo -e "${YELLOW}!${NC} PostgreSQL server not running or not accessible"
    echo -e "   ${YELLOW}→${NC} Start it with: sudo systemctl start postgresql"
fi

# Check Git
echo -n "Checking Git... "
if command -v git &> /dev/null; then
    GIT_VERSION=$(git --version | cut -d' ' -f3)
    echo -e "${GREEN}✓${NC} Found Git $GIT_VERSION"
else
    echo -e "${YELLOW}!${NC} Git not found (recommended but not required)"
fi

# Check Docker (optional)
echo -n "Checking Docker (optional)... "
if command -v docker &> /dev/null; then
    DOCKER_VERSION=$(docker --version | cut -d' ' -f3 | sed 's/,//')
    echo -e "${GREEN}✓${NC} Found Docker $DOCKER_VERSION"
else
    echo -e "${YELLOW}!${NC} Docker not found (optional)"
fi

# Check Docker Compose (optional)
echo -n "Checking Docker Compose (optional)... "
if command -v docker-compose &> /dev/null || docker compose version &> /dev/null; then
    echo -e "${GREEN}✓${NC} Found Docker Compose"
else
    echo -e "${YELLOW}!${NC} Docker Compose not found (optional)"
fi

echo ""
echo "======================================"

if [ "$ALL_OK" = true ]; then
    echo -e "${GREEN}✓ All required prerequisites are installed!${NC}"
    echo ""
    echo "Next steps:"
    echo "  1. cp .env.example .env"
    echo "  2. Edit .env with your configuration"
    echo "  3. createdb global_factor_lab"
    echo "  4. cd backend && pip install -r requirements.txt"
    echo "  5. cd backend && alembic upgrade head"
    echo "  6. cd backend && python -m etl.load_factors --config ./etl/config/global_factor_sources.yaml"
    echo "  7. cd frontend && npm install"
    echo ""
    echo "Then start the application:"
    echo "  Terminal 1: cd backend && python main.py"
    echo "  Terminal 2: cd frontend && npm run dev"
    echo ""
    echo "Or use Docker:"
    echo "  docker-compose up"
else
    echo -e "${RED}✗ Some required prerequisites are missing${NC}"
    echo ""
    echo "Please install the missing dependencies:"
    echo "  - Python 3.9+: https://www.python.org/downloads/"
    echo "  - Node.js 18+: https://nodejs.org/"
    echo "  - PostgreSQL 12+: https://www.postgresql.org/download/"
fi

echo "======================================"
