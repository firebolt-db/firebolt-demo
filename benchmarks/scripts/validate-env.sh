#!/bin/bash
# Environment validation script
# Checks that required environment variables are set and valid

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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

# Load .env if it exists
if [[ -f ".env" ]]; then
    # Load .env safely, handling complex values
    set -o allexport
    source .env
    set +o allexport
    print_info "Loaded .env file"
else
    print_error ".env file not found. Run ./scripts/setup.sh first."
    exit 1
fi

print_info "Validating environment variables..."

VALIDATION_ERRORS=0

# Function to check if a variable is set and not empty
check_var() {
    local var_name=$1
    local vendor=$2
    local required=${3:-true}
    
    if [[ -z "${!var_name}" ]]; then
        if [[ "$required" == "true" ]]; then
            print_error "$var_name is required for $vendor but not set"
            ((VALIDATION_ERRORS++))
        else
            print_warning "$var_name not set for $vendor (optional)"
        fi
    else
        print_status "$var_name set for $vendor"
    fi
}

# Validate Snowflake credentials (if any are set, all required ones must be set)
if [[ -n "$SNOWFLAKE_ACCOUNT" || -n "$SNOWFLAKE_USER" || -n "$SNOWFLAKE_PASSWORD" ]]; then
    print_info "Validating Snowflake credentials..."
    check_var "SNOWFLAKE_ACCOUNT" "Snowflake"
    check_var "SNOWFLAKE_USER" "Snowflake"
    check_var "SNOWFLAKE_PASSWORD" "Snowflake"
    check_var "SNOWFLAKE_DATABASE" "Snowflake" false
    check_var "SNOWFLAKE_SCHEMA" "Snowflake" false
    check_var "SNOWFLAKE_WAREHOUSE" "Snowflake" false
else
    print_warning "No Snowflake credentials configured"
fi

# Validate Redshift credentials
if [[ -n "$REDSHIFT_HOST" || -n "$REDSHIFT_USER" || -n "$REDSHIFT_PASSWORD" ]]; then
    print_info "Validating Redshift credentials..."
    check_var "REDSHIFT_HOST" "Redshift"
    check_var "REDSHIFT_DATABASE" "Redshift"
    check_var "REDSHIFT_USER" "Redshift"
    check_var "REDSHIFT_PASSWORD" "Redshift"
    check_var "REDSHIFT_PORT" "Redshift" false
else
    print_warning "No Redshift credentials configured"
fi

# Validate Firebolt credentials
if [[ -n "$FIREBOLT_ACCOUNT_NAME" || -n "$FIREBOLT_DATABASE" || -n "$FIREBOLT_SERVICE_ID" ]]; then
    print_info "Validating Firebolt credentials..."
    check_var "FIREBOLT_ACCOUNT_NAME" "Firebolt"
    check_var "FIREBOLT_DATABASE" "Firebolt"
    check_var "FIREBOLT_ENGINE_NAME" "Firebolt"
    check_var "FIREBOLT_SERVICE_ID" "Firebolt"
    check_var "FIREBOLT_SERVICE_SECRET" "Firebolt"
else
    print_warning "No Firebolt credentials configured"
fi

# Validate BigQuery credentials
if [[ -n "$BIGQUERY_PROJECT_ID" || -n "$BIGQUERY_DATASET" || -n "$BIGQUERY_KEY_FILE" || -n "$BIGQUERY_KEY_JSON" ]]; then
    print_info "Validating BigQuery credentials..."
    check_var "BIGQUERY_PROJECT_ID" "BigQuery"
    check_var "BIGQUERY_DATASET" "BigQuery"
    # Check for either key file or inline JSON
    if [[ -n "$BIGQUERY_KEY_FILE" ]]; then
        check_var "BIGQUERY_KEY_FILE" "BigQuery"
    elif [[ -n "$BIGQUERY_KEY_JSON" ]]; then
        check_var "BIGQUERY_KEY_JSON" "BigQuery"
    else
        print_error "Either BIGQUERY_KEY_FILE or BIGQUERY_KEY_JSON must be set for BigQuery"
        ((VALIDATION_ERRORS++))
    fi
else
    print_warning "No BigQuery credentials configured"
fi

# Validate application configuration
print_info "Validating application configuration..."
check_var "DEFAULT_OUTPUT_DIR" "Application" false
check_var "DEFAULT_POOL_SIZE" "Application" false
check_var "DEFAULT_CONCURRENCY" "Application" false

# Check if at least one database is configured
DATABASES_CONFIGURED=0
[[ -n "$SNOWFLAKE_ACCOUNT" ]] && ((DATABASES_CONFIGURED++))
[[ -n "$REDSHIFT_HOST" ]] && ((DATABASES_CONFIGURED++))
[[ -n "$FIREBOLT_ACCOUNT_NAME" ]] && ((DATABASES_CONFIGURED++))
[[ -n "$BIGQUERY_PROJECT_ID" ]] && ((DATABASES_CONFIGURED++))

if [[ $DATABASES_CONFIGURED -eq 0 ]]; then
    print_error "No database credentials configured. Configure at least one database in .env"
    ((VALIDATION_ERRORS++))
else
    print_status "$DATABASES_CONFIGURED database(s) configured"
fi

# Final validation result
echo
if [[ $VALIDATION_ERRORS -eq 0 ]]; then
    print_status "Environment validation passed! ✨"
    echo
    print_info "Available databases:"
    [[ -n "$SNOWFLAKE_ACCOUNT" ]] && echo "  - Snowflake"
    [[ -n "$REDSHIFT_HOST" ]] && echo "  - Redshift"
    [[ -n "$FIREBOLT_ACCOUNT_NAME" ]] && echo "  - Firebolt"
    [[ -n "$BIGQUERY_PROJECT_ID" ]] && echo "  - BigQuery"
    exit 0
else
    print_error "Environment validation failed with $VALIDATION_ERRORS error(s)"
    echo
    print_info "Please fix the errors above and run this script again."
    exit 1
fi