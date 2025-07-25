#!/bin/bash
# Launch the K6 high-concurrency benchmark client

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

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Check if we're in the right directory
if [[ ! -f "README.md" || ! -d "benchmarks" ]]; then
    print_error "Please run this script from the project root directory"
    exit 1
fi

# Check for required tools
if ! command -v node &> /dev/null; then
    print_error "Node.js is required but not found"
    exit 1
fi

if ! command -v k6 &> /dev/null; then
    print_error "K6 is required but not found"
    print_info "Install K6 from: https://k6.io/docs/getting-started/installation/"
    exit 1
fi

# Validate environment
print_info "Validating environment..."
if ./scripts/validate-env.sh > /dev/null 2>&1; then
    print_status "Environment validation passed"
else
    print_error "Environment validation failed"
    echo "Run './scripts/validate-env.sh' for details"
    exit 1
fi

# Load environment variables
if [[ -f ".env" ]]; then
    export $(grep -v '^#' .env | xargs)
    print_status "Loaded environment variables"
fi

# Change to the K6 client directory
cd src/k6

# Check if node_modules exists
if [[ ! -d "node_modules" ]]; then
    print_warning "Node.js dependencies not found. Installing..."
    npm install
    print_status "Dependencies installed"
fi

print_info "Starting K6 benchmark client..."
echo
print_info "This will start in two phases:"
print_info "1. Connection server (runs in background)"
print_info "2. K6 benchmark execution"
echo

# Start the connection server in the background
print_info "Starting connection server..."
node connections-cluster.js &
SERVER_PID=$!
print_status "Connection server started (PID: $SERVER_PID)"

# Give the server a moment to start
sleep 2

# Trap to kill the server when script exits
trap "kill $SERVER_PID 2>/dev/null" EXIT

print_info "Starting K6 benchmark..."
k6 run fb-benchmark-k6.js

print_status "K6 benchmark completed"