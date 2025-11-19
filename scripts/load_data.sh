#!/bin/bash

# Global Factor Lab - Data Loading Script
# Convenient wrapper for running the ETL pipeline

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo ""
echo -e "${BLUE}Global Factor Lab - Data Loading${NC}"
echo "===================================="
echo ""

# Default config path
CONFIG="${1:-$PROJECT_ROOT/backend/etl/config/global_factor_sources.yaml}"

if [ ! -f "$CONFIG" ]; then
    echo -e "${YELLOW}Error: Config file not found: $CONFIG${NC}"
    echo ""
    echo "Usage: $0 [config_file]"
    echo ""
    echo "Example:"
    echo "  $0"
    echo "  $0 /path/to/custom_config.yaml"
    exit 1
fi

echo "Config file: $CONFIG"
echo "Data directory: ${DATA_DIR:-$PROJECT_ROOT/data}"
echo ""

# Change to backend directory
cd "$PROJECT_ROOT/backend"

# Load environment variables if .env exists
if [ -f "$PROJECT_ROOT/.env" ]; then
    export $(cat "$PROJECT_ROOT/.env" | grep -v '^#' | xargs)
fi

# Run ETL
echo -e "${BLUE}Running ETL pipeline...${NC}"
echo ""

python -m etl.load_factors --config "$CONFIG"

echo ""
echo -e "${GREEN}✓ Data loading completed!${NC}"
echo ""
echo "You can now start the application:"
echo "  cd backend && python main.py"
echo ""
