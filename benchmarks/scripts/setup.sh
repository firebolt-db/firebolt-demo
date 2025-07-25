#!/bin/bash
# Setup script for Database Benchmark Tools
# Sets up the development environment and validates configuration

set -e  # Exit on any error

echo "🚀 Setting up Database Benchmark Tools..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

# Check if we're in the right directory
if [[ ! -f "README.md" || ! -d "benchmarks" ]]; then
    print_error "Please run this script from the project root directory"
    exit 1
fi

# Check for required tools
print_info "Checking system requirements..."

# Check Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    print_status "Python $PYTHON_VERSION found"
else
    print_error "Python 3 is required but not found"
    exit 1
fi

# Check Node.js for K6 client
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    print_status "Node.js $NODE_VERSION found"
else
    print_warning "Node.js not found - K6 client will not work"
fi

# Check K6
if command -v k6 &> /dev/null; then
    K6_VERSION=$(k6 version | head -1)
    print_status "K6 found: $K6_VERSION"
else
    print_warning "K6 not found - install from https://k6.io/docs/getting-started/installation/"
fi

# Create .env file from example if it doesn't exist
if [[ ! -f ".env" ]]; then
    if [[ -f ".env.example" ]]; then
        cp .env.example .env
        print_status "Created .env file from .env.example"
        print_warning "Please edit .env with your actual database credentials"
    else
        print_error ".env.example not found"
        exit 1
    fi
else
    print_status ".env file exists"
fi

# Setup Python environment
print_info "Setting up Python environment..."

# Check if virtual environment exists
if [[ ! -d "venv" ]]; then
    print_info "Creating Python virtual environment..."
    python3 -m venv venv
    print_status "Virtual environment created"
fi

# Activate virtual environment
source venv/bin/activate
print_status "Virtual environment activated"

# Install Python dependencies
print_info "Installing Python dependencies..."
pip install --upgrade pip
pip install -r src/python/requirements.txt
print_status "Python dependencies installed"

# Setup Node.js environment for K6 client
if command -v npm &> /dev/null; then
    print_info "Setting up Node.js dependencies for K6 client..."
    cd src/k6
    npm install
    print_status "Node.js dependencies installed"
    cd ../..
fi

# Validate environment
print_info "Validating environment..."
./scripts/validate-env.sh

print_status "Setup complete!"
echo
print_info "Next steps:"
echo "1. Edit .env with your database credentials"
echo "2. Run './scripts/run-python.sh' to start the Streamlit UI"
echo "3. Run './scripts/run-k6.sh' to start the K6 client"
echo "4. Run './scripts/test-all.sh' to validate everything works"