#!/bin/bash
# Launch the Python Streamlit UI for database benchmarking

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Check if we're in the right directory
if [[ ! -f "README.md" || ! -d "benchmarks" ]]; then
    print_error "Please run this script from the project root directory"
    exit 1
fi

# Validate environment before starting
print_info "Validating environment..."
if ./scripts/validate-env.sh > /dev/null 2>&1; then
    print_status "Environment validation passed"
else
    print_error "Environment validation failed"
    echo "Run './scripts/validate-env.sh' for details"
    exit 1
fi

# Check if virtual environment exists
if [[ ! -d "venv" ]]; then
    print_error "Virtual environment not found. Run './scripts/setup.sh' first."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate
print_status "Activated Python virtual environment"

# Check if Streamlit is installed
if ! command -v streamlit &> /dev/null; then
    print_error "Streamlit not found. Run './scripts/setup.sh' to install dependencies."
    exit 1
fi

# Load environment variables
if [[ -f ".env" ]]; then
    export $(grep -v '^#' .env | xargs)
    print_status "Loaded environment variables"
fi

# Change to the Python client directory
cd src/python

print_info "Starting Streamlit UI..."
print_info "The UI will be available at http://localhost:${STREAMLIT_SERVER_PORT:-8501}"
echo
print_info "Press Ctrl+C to stop the server"
echo

# Start Streamlit
exec streamlit run src/main.py \
    --server.port=${STREAMLIT_SERVER_PORT:-8501} \
    --server.address=${STREAMLIT_SERVER_ADDRESS:-localhost}