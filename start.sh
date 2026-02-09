#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}   Products REST API - Quick Start     ${NC}"
echo -e "${BLUE}========================================${NC}\n"

# Check if MongoDB is running
echo -e "${YELLOW}Checking MongoDB...${NC}"
if ! pgrep -x "mongod" > /dev/null; then
    echo -e "${RED}MongoDB is not running!${NC}"
    echo -e "${YELLOW}Starting MongoDB...${NC}"
    brew services start mongodb-community 2>/dev/null || {
        echo -e "${RED}Failed to start MongoDB. Please start it manually.${NC}"
        exit 1
    }
    sleep 2
fi
echo -e "${GREEN}✓ MongoDB is running${NC}\n"

# Check if UV is installed
echo -e "${YELLOW}Checking UV package manager...${NC}"
if ! command -v uv &> /dev/null; then
    echo -e "${RED}UV is not installed!${NC}"
    echo -e "${YELLOW}Installing UV...${NC}"
    curl -LsSf https://astral.sh/uv/install.sh | sh
fi
echo -e "${GREEN}✓ UV is installed${NC}\n"

# Install dependencies
echo -e "${YELLOW}Installing dependencies...${NC}"
uv pip install -e .
uv pip install -e ".[dev]"
echo -e "${GREEN}✓ Dependencies installed${NC}\n"

# Run the application
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}   Starting FastAPI Server...          ${NC}"
echo -e "${GREEN}========================================${NC}\n"
echo -e "${BLUE}API will be available at:${NC}"
echo -e "  ${GREEN}➜${NC} API Base:     http://localhost:8000/api/v1"
echo -e "  ${GREEN}➜${NC} Swagger Docs: http://localhost:8000/docs"
echo -e "  ${GREEN}➜${NC} ReDoc:        http://localhost:8000/redoc"
echo -e "  ${GREEN}➜${NC} Health Check: http://localhost:8000/health\n"

uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
