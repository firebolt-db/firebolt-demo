#!/bin/bash
# Comprehensive test suite for the database benchmark tools
# Validates the entire setup and runs basic functionality tests

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

TESTS_PASSED=0
TESTS_FAILED=0

# Test execution function
run_test() {
    local test_name="$1"
    local test_command="$2"
    
    print_info "Running test: $test_name"
    
    if eval "$test_command" > /dev/null 2>&1; then
        print_status "$test_name"
        ((TESTS_PASSED++))
    else
        print_error "$test_name"
        ((TESTS_FAILED++))
    fi
}

# Check if we're in the right directory
if [[ ! -f "README.md" || ! -d "benchmarks" ]]; then
    print_error "Please run this script from the project root directory"
    exit 1
fi

print_info "🧪 Running comprehensive test suite..."
echo

# Environment and setup tests
print_info "=== Environment Tests ==="
run_test "Environment validation" "./scripts/validate-env.sh"
run_test ".env file exists" "[[ -f '.env' ]]"
run_test "Python virtual environment exists" "[[ -d 'venv' ]]"
run_test "Benchmarks directory structure" "[[ -d 'benchmarks/FireScale' ]]"
run_test "Python source files exist" "[[ -f 'src/python/src/main.py' ]]"
run_test "K6 source files exist" "[[ -f 'src/k6/connections-server.js' ]]"

echo

# Dependency tests
print_info "=== Dependency Tests ==="
run_test "Python 3 available" "command -v python3"
run_test "Virtual environment activation" "source venv/bin/activate && python --version"
run_test "Python dependencies installed" "source venv/bin/activate && python -c 'import streamlit, pandas, firebolt'"
run_test "Node.js available" "command -v node"

if command -v npm &> /dev/null; then
    run_test "K6 dependencies installed" "[[ -d 'src/k6/node_modules' ]]"
else
    print_warning "npm not available, skipping K6 dependency test"
fi

if command -v k6 &> /dev/null; then
    run_test "K6 executable available" "command -v k6"
else
    print_warning "K6 not available, skipping K6 tests"
fi

echo

# Configuration tests
print_info "=== Configuration Tests ==="
source venv/bin/activate
run_test "Python env_config module loads" "cd src/python/src && python -c 'import env_config'"
run_test "Environment config loads" "cd src/python/src && python -c 'from env_config import load_environment_config; load_environment_config()'"
run_test "App config loads" "cd src/python/src && python -c 'from env_config import get_app_config; get_app_config()'"

echo

# Import tests
print_info "=== Import Tests ==="
run_test "Runner module imports" "cd src/python/src && python -c 'import runner'"
run_test "Connectors module imports" "cd src/python/src && python -c 'import connectors'"
run_test "Exporters module imports" "cd src/python/src && python -c 'import exporters'"

echo

# Benchmark structure tests
print_info "=== Benchmark Structure Tests ==="
run_test "FireScale benchmark files" "[[ -f 'benchmarks/FireScale/firebolt/benchmark.sql' ]]"
run_test "Sample benchmark files" "[[ -f 'benchmarks/sample_benchmark/benchmark.sql' ]]"
run_test "TPCH benchmark files" "[[ -f 'benchmarks/tpch/firebolt/benchmark.sql' ]]"

echo

# Quick smoke tests (if databases are configured)
print_info "=== Smoke Tests ==="

# Load environment variables for testing
if [[ -f ".env" ]]; then
    export $(grep -v '^#' .env | xargs)
fi

# Test Python client initialization (without actually connecting to DBs)
run_test "Python benchmark runner initialization" "cd src/python/src && python -c 'from runner import BenchmarkRunner; from env_config import load_environment_config; creds = load_environment_config(); print(f\"Available vendors: {list(creds.keys())}\")'"

# Test Streamlit app loads (syntax check)
run_test "Streamlit app syntax check" "cd src/python/src && python -m py_compile main.py"

# Test K6 client syntax
if command -v node &> /dev/null; then
    run_test "K6 connections server syntax" "cd src/k6 && node -c connections-server.js"
fi

echo
print_info "=== Test Summary ==="

if [[ $TESTS_FAILED -eq 0 ]]; then
    print_status "All tests passed! ($TESTS_PASSED/$((TESTS_PASSED + TESTS_FAILED))) ✨"
    echo
    print_info "Your environment is ready for database benchmarking!"
    print_info "Next steps:"
    echo "  • Run './scripts/run-python.sh' to start the Streamlit UI"
    echo "  • Run './scripts/run-k6.sh' to test the K6 client"
    echo "  • Edit .env with your database credentials if not done already"
    exit 0
else
    print_error "$TESTS_FAILED test(s) failed out of $((TESTS_PASSED + TESTS_FAILED)) total"
    echo
    print_info "Please fix the failed tests and run again."
    exit 1
fi