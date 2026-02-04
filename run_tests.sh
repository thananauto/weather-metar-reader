#!/bin/bash

# METAR Weather Reader - Test Runner Script
# Runs the complete test suite with coverage reporting

echo "🧪 METAR Weather Reader - Test Suite"
echo "======================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}⚠️  Virtual environment not found. Creating...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
echo -e "${BLUE}🔧 Activating virtual environment...${NC}"
source venv/bin/activate

# Install/upgrade dependencies
echo -e "${BLUE}📦 Installing dependencies...${NC}"
pip install -q -r requirements.txt

# Run tests with different options based on arguments
if [ "$1" == "quick" ]; then
    echo -e "${BLUE}⚡ Running quick tests (no coverage)...${NC}"
    echo ""
    pytest tests/ -v --tb=short
elif [ "$1" == "unit" ]; then
    echo -e "${BLUE}🧩 Running unit tests only...${NC}"
    echo ""
    pytest tests/ -v -m unit
elif [ "$1" == "coverage" ]; then
    echo -e "${BLUE}📊 Running tests with detailed coverage...${NC}"
    echo ""
    pytest tests/ -v --cov=src/metar_app --cov-report=term-missing --cov-report=html
    echo ""
    echo -e "${GREEN}✅ Coverage report generated in htmlcov/index.html${NC}"
else
    echo -e "${BLUE}🚀 Running full test suite...${NC}"
    echo ""
    pytest tests/

    # Check test result
    if [ $? -eq 0 ]; then
        echo ""
        echo -e "${GREEN}✅ All tests passed!${NC}"
        echo ""
        echo "📊 Coverage report: htmlcov/index.html"
    else
        echo ""
        echo -e "${YELLOW}⚠️  Some tests failed. Check the output above.${NC}"
        exit 1
    fi
fi

echo ""
echo "======================================"
echo "Test run complete!"
