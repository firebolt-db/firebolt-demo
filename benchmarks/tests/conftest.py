"""Pytest configuration and shared fixtures for Database Benchmark Suite tests."""

import os
import tempfile
from pathlib import Path
from typing import Dict, Generator, List
from unittest.mock import MagicMock

import pytest


@pytest.fixture(scope="session")
def test_data_dir() -> Path:
    """Provide path to test data directory."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Provide a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


@pytest.fixture
def sample_sql_queries() -> List[str]:
    """Provide sample SQL queries for testing."""
    return [
        "SELECT 1 AS test_column",
        "SELECT COUNT(*) FROM test_table",
        "SELECT * FROM users WHERE active = true",
    ]


@pytest.fixture
def sample_benchmark_results() -> List[Dict[str, any]]:
    """Provide sample benchmark results for testing."""
    return [
        {
            "vendor": "firebolt",
            "query_name": "query_1",
            "duration": 1.25,
            "rows": 100,
            "status": "success",
            "timestamp": "2024-01-01T10:00:00",
        },
        {
            "vendor": "snowflake",
            "query_name": "query_1", 
            "duration": 2.45,
            "rows": 100,
            "status": "success",
            "timestamp": "2024-01-01T10:00:01",
        },
        {
            "vendor": "redshift",
            "query_name": "query_2",
            "duration": 0.89,
            "rows": 50,
            "status": "success", 
            "timestamp": "2024-01-01T10:00:02",
        },
    ]


@pytest.fixture
def mock_database_credentials() -> Dict[str, Dict[str, str]]:
    """Provide mock database credentials for testing."""
    return {
        "firebolt": {
            "account_name": "test_account",
            "database": "test_db",
            "engine_name": "test_engine",
            "auth": {
                "id": "test_service_id",
                "secret": "test_service_secret",
            },
        },
        "snowflake": {
            "account": "test_account",
            "user": "test_user",
            "password": "test_password",
            "database": "test_db",
            "schema": "test_schema",
            "warehouse": "test_warehouse",
        },
        "redshift": {
            "host": "test-cluster.region.redshift.amazonaws.com",
            "port": "5439",
            "database": "test_db",
            "user": "test_user",
            "password": "test_password",
        },
        "google": {
            "project_id": "test-project-123",
            "dataset": "test_dataset",
            "key_file": "/path/to/test-key.json",
        },
    }


@pytest.fixture
def mock_connector():
    """Provide a mock database connector for testing."""
    mock = MagicMock()
    mock.connect.return_value = None
    mock.execute_query.return_value = [{"test_column": 1}]
    mock.close.return_value = None
    return mock


@pytest.fixture
def sample_benchmark_config() -> Dict[str, any]:
    """Provide sample benchmark configuration."""
    return {
        "benchmark_name": "test_benchmark", 
        "vendors": ["firebolt", "snowflake"],
        "pool_size": 1,
        "concurrency": 1,
        "output_dir": "test_results",
        "execute_setup": False,
        "run_warmup": False,
    }


@pytest.fixture(autouse=True)
def mock_env_vars(monkeypatch):
    """Mock environment variables for testing."""
    test_env_vars = {
        # Firebolt
        "FIREBOLT_ACCOUNT_NAME": "test_account",
        "FIREBOLT_DATABASE": "test_db", 
        "FIREBOLT_ENGINE_NAME": "test_engine",
        "FIREBOLT_SERVICE_ID": "test_service_id",
        "FIREBOLT_SERVICE_SECRET": "test_service_secret",
        # Snowflake
        "SNOWFLAKE_ACCOUNT": "test_account",
        "SNOWFLAKE_USER": "test_user",
        "SNOWFLAKE_PASSWORD": "test_password",
        "SNOWFLAKE_DATABASE": "test_db",
        "SNOWFLAKE_SCHEMA": "test_schema", 
        "SNOWFLAKE_WAREHOUSE": "test_warehouse",
        # Redshift
        "REDSHIFT_HOST": "test-cluster.region.redshift.amazonaws.com",
        "REDSHIFT_PORT": "5439",
        "REDSHIFT_DATABASE": "test_db",
        "REDSHIFT_USER": "test_user",
        "REDSHIFT_PASSWORD": "test_password",
        # BigQuery
        "BIGQUERY_PROJECT_ID": "test-project-123",
        "BIGQUERY_DATASET": "test_dataset",
        "BIGQUERY_KEY_FILE": "/path/to/test-key.json",
        # App config
        "DEFAULT_OUTPUT_DIR": "benchmark_results",
        "DEFAULT_POOL_SIZE": "5",
        "DEFAULT_CONCURRENCY": "1",
    }
    
    for key, value in test_env_vars.items():
        monkeypatch.setenv(key, value)


@pytest.fixture
def sample_sql_file(temp_dir: Path) -> Path:
    """Create a sample SQL file for testing."""
    sql_content = """
-- Query 1: Simple select
SELECT 1 AS test_column;

-- Query 2: Table count
SELECT COUNT(*) FROM test_table;

-- Query 3: Filtered select
SELECT * FROM users 
WHERE active = true 
AND created_date > '2024-01-01';
"""
    sql_file = temp_dir / "test_queries.sql"
    sql_file.write_text(sql_content)
    return sql_file


@pytest.fixture
def sample_benchmark_structure(temp_dir: Path) -> Path:
    """Create a sample benchmark directory structure."""
    benchmark_dir = temp_dir / "test_benchmark"
    benchmark_dir.mkdir()
    
    # Create general files
    (benchmark_dir / "benchmark.sql").write_text(
        "SELECT 1 AS test;\nSELECT COUNT(*) FROM test_table;"
    )
    (benchmark_dir / "setup.sql").write_text("CREATE TABLE test_table (id INT);")
    (benchmark_dir / "warmup.sql").write_text("SELECT 1;")
    
    # Create vendor-specific files
    for vendor in ["firebolt", "snowflake", "redshift"]:
        vendor_dir = benchmark_dir / vendor
        vendor_dir.mkdir()
        (vendor_dir / "benchmark.sql").write_text(
            f"-- {vendor} specific queries\nSELECT '{vendor}' AS vendor_name;"
        )
    
    return benchmark_dir


# Pytest markers for test categorization
def pytest_configure(config):
    """Configure pytest markers."""
    config.addinivalue_line("markers", "unit: marks tests as unit tests")
    config.addinivalue_line("markers", "integration: marks tests as integration tests")
    config.addinivalue_line("markers", "slow: marks tests as slow running tests")
    config.addinivalue_line("markers", "requires_db: marks tests that require database connections")