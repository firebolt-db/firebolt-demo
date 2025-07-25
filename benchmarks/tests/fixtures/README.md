# Test Fixtures

This directory contains test data and fixtures used by the test suite.

## Contents

- `sample_queries.sql` - Sample SQL queries for testing
- `sample_credentials.json` - Sample credential structure (no real credentials)
- `sample_benchmark_results.json` - Sample benchmark output data

## Usage

Test fixtures are automatically loaded by pytest through the `conftest.py` configuration.
Fixtures are available as pytest fixtures in test functions.

## Adding New Fixtures

1. Add the fixture file to this directory
2. Update `conftest.py` to load the fixture if needed
3. Use the fixture in your tests