#!/bin/bash
# Security scanning script for the database benchmark suite
# Runs various security checks and vulnerability scans

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
if [[ ! -f "README.md" || ! -d "src" ]]; then
    print_error "Please run this script from the project root directory"
    exit 1
fi

print_info "🔐 Running security scans for Database Benchmark Suite..."
echo

# Activate virtual environment
if [[ -d "venv" ]]; then
    source venv/bin/activate
    print_status "Activated virtual environment"
else
    print_warning "Virtual environment not found - creating one"
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements-dev.txt
fi

echo

# 1. Dependency vulnerability scanning with safety
print_info "=== Dependency Vulnerability Scanning ==="
if command -v safety &> /dev/null; then
    print_info "Running safety scan on dependencies..."
    if safety check --json > safety_report.json 2>/dev/null; then
        print_status "Safety scan completed - no critical vulnerabilities found"
        rm -f safety_report.json
    else
        print_warning "Safety scan found vulnerabilities - check safety_report.json"
    fi
else
    print_warning "Safety not installed - installing..."
    pip install safety
    safety check
fi

echo

# 2. Code security scanning with bandit
print_info "=== Code Security Scanning ==="
if command -v bandit &> /dev/null; then
    print_info "Running bandit security scan on Python code..."
    if bandit -r src/ -f json -o bandit_report.json --severity-level medium 2>/dev/null; then
        print_status "Bandit scan completed"
        # Check if there are any findings
        if [[ -f "bandit_report.json" ]]; then
            issues=$(jq '.results | length' bandit_report.json 2>/dev/null || echo "0")
            if [[ "$issues" -gt 0 ]]; then
                print_warning "Found $issues security issues - check bandit_report.json"
            else
                print_status "No security issues found"
                rm -f bandit_report.json
            fi
        fi
    else
        print_warning "Bandit scan found issues - check bandit_report.json"
    fi
else
    print_warning "Bandit not installed - installing..."
    pip install bandit[toml]
    bandit -r src/ --severity-level medium
fi

echo

# 3. Secret scanning
print_info "=== Secret Scanning ==="
print_info "Checking for potential secrets in code..."

# Check for common secret patterns
secret_patterns=(
    "password\s*=\s*['\"][^'\"]+['\"]"
    "api[_-]?key\s*=\s*['\"][^'\"]+['\"]"
    "secret\s*=\s*['\"][^'\"]+['\"]"
    "token\s*=\s*['\"][^'\"]+['\"]"
    "-----BEGIN [A-Z ]*PRIVATE KEY-----"
)

secrets_found=false
for pattern in "${secret_patterns[@]}"; do
    if grep -r -i -E "$pattern" src/ 2>/dev/null | grep -v "test" | grep -v "example"; then
        print_warning "Found potential secret pattern: $pattern"
        secrets_found=true
    fi
done

if ! $secrets_found; then
    print_status "No hardcoded secrets found in source code"
fi

echo

# 4. File permission checks
print_info "=== File Permission Checks ==="
print_info "Checking for overly permissive files..."

# Check for files with world-writable permissions
world_writable=$(find . -type f -perm -o+w 2>/dev/null | grep -v ".git" | head -10)
if [[ -n "$world_writable" ]]; then
    print_warning "Found world-writable files:"
    echo "$world_writable"
else
    print_status "No world-writable files found"
fi

echo

# 5. Configuration file checks
print_info "=== Configuration Security Checks ==="

# Check if .env file exists and has appropriate permissions
if [[ -f ".env" ]]; then
    env_perms=$(stat -c "%a" .env 2>/dev/null || stat -f "%A" .env 2>/dev/null || echo "unknown")
    if [[ "$env_perms" == "600" || "$env_perms" == "-rw-------" ]]; then
        print_status ".env file has secure permissions (600)"
    else
        print_warning ".env file permissions should be 600 (current: $env_perms)"
        print_info "Run: chmod 600 .env"
    fi
else
    print_info ".env file not found (using .env.example for reference)"
fi

# Check .env.example doesn't contain real credentials
if [[ -f ".env.example" ]]; then
    if grep -q "your_" .env.example && grep -q "test_" .env.example; then
        print_status ".env.example contains placeholder values"
    else
        print_warning ".env.example may contain real credentials - please verify"
    fi
fi

echo

# 6. Git security checks
print_info "=== Git Security Checks ==="

# Check if sensitive files are being tracked by git
sensitive_files=(".env" "*.key" "*.pem" "*.p12" "*credentials*" "*secret*")
git_tracking_sensitive=false

for pattern in "${sensitive_files[@]}"; do
    if git ls-files | grep -i "$pattern" 2>/dev/null | grep -v "example" | grep -v "template"; then
        print_warning "Git is tracking potentially sensitive files matching: $pattern"
        git_tracking_sensitive=true
    fi
done

if ! $git_tracking_sensitive; then
    print_status "No sensitive files found in git tracking"
fi

# Check .gitignore coverage
if [[ -f ".gitignore" ]]; then
    if grep -q ".env" .gitignore && grep -q "*.key" .gitignore; then
        print_status ".gitignore properly excludes sensitive files"
    else
        print_warning ".gitignore should include .env, *.key, *.pem patterns"
    fi
fi

echo

# 7. Docker security (if Dockerfile exists)
if [[ -f "Dockerfile" ]]; then
    print_info "=== Docker Security Checks ==="
    
    # Check for USER instruction
    if grep -q "^USER" Dockerfile; then
        print_status "Dockerfile uses non-root user"
    else
        print_warning "Dockerfile should include USER instruction for non-root execution"
    fi
    
    # Check for COPY --chown
    if grep -q "COPY.*--chown" Dockerfile; then
        print_status "Dockerfile uses --chown for secure file ownership"
    fi
    
    echo
fi

# Summary
echo
print_info "=== Security Scan Summary ==="
print_status "Security scans completed"

# Clean up temporary files
rm -f safety_report.json bandit_report.json

echo
print_info "Security recommendations:"
echo "  • Keep dependencies updated regularly"
echo "  • Never commit real credentials to git"
echo "  • Use environment variables for sensitive configuration"
echo "  • Set restrictive file permissions on sensitive files"
echo "  • Run security scans before each release"
echo "  • Monitor for new vulnerabilities in dependencies"

echo
print_info "To run individual scans:"
echo "  • Dependency scan: safety check"
echo "  • Code scan: bandit -r src/"
echo "  • Full scan: ./scripts/security-scan.sh"