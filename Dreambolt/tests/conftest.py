"""
DreamBolt Test Fixtures and Configuration
=========================================

Comprehensive test fixtures for all DreamBolt components.
Ensures deterministic, isolated, and offline-capable testing.
"""
import pytest
import pandas as pd
import tempfile
import os
import json
from pathlib import Path
from unittest.mock import Mock, patch
from typing import Dict, Any
import numpy as np

# Set deterministic random seeds for reproducible tests
np.random.seed(42)


@pytest.fixture(scope="session")
def tmp_dir_factory():
    """Factory for creating temporary directories with cleanup."""
    temp_dirs = []
    
    def create_temp_dir(prefix="dreambolt_test_"):
        temp_dir = tempfile.mkdtemp(prefix=prefix)
        temp_dirs.append(temp_dir)
        return Path(temp_dir)
    
    yield create_temp_dir
    
    # Cleanup all temporary directories
    import shutil
    for temp_dir in temp_dirs:
        if Path(temp_dir).exists():
            shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def tmp_dir(tmp_dir_factory):
    """Single temporary directory for test isolation."""
    return tmp_dir_factory()


@pytest.fixture
def sample_csv_data():
    """Standard test CSV data for consistent testing."""
    return pd.DataFrame({
        'id': [1, 2, 3, 4, 5],
        'name': ['Alice Johnson', 'Bob Smith', 'Charlie Brown', 'Diana Prince', 'Eve Wilson'],
        'age': [25, 30, 35, 28, 32],
        'salary': [75000, 85000, 95000, 70000, 90000],
        'department': ['Engineering', 'Sales', 'Engineering', 'Marketing', 'Sales'],
        'start_date': ['2020-01-15', '2019-03-22', '2018-07-10', '2021-02-01', '2020-11-30'],
        'is_active': [True, True, False, True, True],
        'rating': [4.2, 3.8, 4.5, 3.9, 4.1]
    })


@pytest.fixture
def sample_parquet_data():
    """Test Parquet data with different data types."""
    return pd.DataFrame({
        'product_id': [101, 102, 103, 104, 105],
        'product_name': ['Widget A', 'Widget B', 'Gadget X', 'Tool Y', 'Device Z'],
        'price': [19.99, 29.99, 49.99, 15.99, 39.99],
        'category': ['electronics', 'tools', 'electronics', 'tools', 'accessories'],
        'in_stock': [True, False, True, True, False],
        'stock_count': [50, 0, 25, 100, 0],
        'last_updated': pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05'])
    })


@pytest.fixture
def malformed_csv_data():
    """Test data with common data quality issues."""
    return pd.DataFrame({
        'id': [1, 2, None, 4, 'invalid'],
        'name': ['Alice', '', 'Charlie', None, 'Eve'],
        'age': [25, -5, 150, 30, None],
        'salary': [75000, None, 'high', 85000, 95000],
        'department': ['Engineering', 'Sales', None, 'Marketing', ''],
        'weird_column_name!!!': ['a', 'b', 'c', 'd', 'e'],
        '123numeric_start': [1, 2, 3, 4, 5]
    })


@pytest.fixture
def large_dataset():
    """Large dataset for performance testing."""
    np.random.seed(42)  # Deterministic
    size = 1000
    return pd.DataFrame({
        'id': range(size),
        'name': [f'User_{i}' for i in range(size)],
        'age': np.random.randint(18, 80, size),
        'salary': np.random.randint(30000, 150000, size),
        'score': np.random.random(size),
        'category': np.random.choice(['A', 'B', 'C', 'D'], size),
        'is_active': np.random.choice([True, False], size)
    })


@pytest.fixture
def sample_csv_file(tmp_dir, sample_csv_data):
    """Create temporary CSV file."""
    csv_path = tmp_dir / "test_data.csv"
    sample_csv_data.to_csv(csv_path, index=False)
    return csv_path


@pytest.fixture
def sample_parquet_file(tmp_dir, sample_parquet_data):
    """Create temporary Parquet file."""
    parquet_path = tmp_dir / "test_data.parquet"
    sample_parquet_data.to_parquet(parquet_path)
    return parquet_path


@pytest.fixture
def malformed_csv_file(tmp_dir, malformed_csv_data):
    """Create temporary malformed CSV file."""
    csv_path = tmp_dir / "malformed_data.csv"
    malformed_csv_data.to_csv(csv_path, index=False)
    return csv_path


@pytest.fixture
def empty_csv_file(tmp_dir):
    """Create empty CSV file for edge case testing."""
    csv_path = tmp_dir / "empty.csv"
    csv_path.write_text("id,name,age\n")  # Headers only
    return csv_path


@pytest.fixture
def nonexistent_file(tmp_dir):
    """Path to a file that doesn't exist."""
    return tmp_dir / "nonexistent.csv"


@pytest.fixture
def sample_s3_uri():
    """Mock S3 URI for testing."""
    return "s3://dreambolt-test-bucket/test-data.csv"


@pytest.fixture
def mock_s3_environment():
    """Mock S3 environment using moto."""
    pytest.importorskip("moto")
    from moto import mock_s3
    import boto3
    
    with mock_s3():
        # Create mock S3 environment
        s3_client = boto3.client("s3", region_name="us-east-1")
        bucket_name = "dreambolt-test-bucket"
        s3_client.create_bucket(Bucket=bucket_name)
        
        # Upload test data
        test_csv = "id,name,age\n1,Alice,25\n2,Bob,30\n"
        s3_client.put_object(
            Bucket=bucket_name,
            Key="test-data.csv",
            Body=test_csv.encode()
        )
        
        yield {
            'client': s3_client,
            'bucket': bucket_name,
            'test_uri': f"s3://{bucket_name}/test-data.csv"
        }


@pytest.fixture
def ingest_config(tmp_dir):
    """Generate fresh configuration for each test."""
    config = {
        'OPENAI_API_KEY': 'test-openai-key-12345',
        'FIREBOLT_USERNAME': 'test@example.com',
        'FIREBOLT_PASSWORD': 'test-password',
        'FIREBOLT_ACCOUNT_NAME': 'test-account',
        'FIREBOLT_DATABASE': 'test_db',
        'FIREBOLT_ENGINE': 'test_engine'
    }
    
    # Create .env file
    env_path = tmp_dir / ".env"
    with open(env_path, 'w') as f:
        for key, value in config.items():
            f.write(f"{key}={value}\n")
    
    return config


@pytest.fixture
def mock_openai_client():
    """Mock OpenAI client for API testing."""
    mock_client = Mock()
    
    # Mock embeddings response
    mock_embedding_response = Mock()
    mock_embedding_response.data = [
        Mock(embedding=[0.1] * 1536),  # Standard OpenAI embedding size
        Mock(embedding=[0.2] * 1536),
        Mock(embedding=[0.3] * 1536)
    ]
    mock_client.embeddings.create.return_value = mock_embedding_response
    
    return mock_client


@pytest.fixture
def mock_firebolt_connection():
    """Mock Firebolt database connection."""
    mock_connection = Mock()
    mock_cursor = Mock()
    
    # Configure cursor behavior
    mock_cursor.execute.return_value = None
    mock_cursor.fetchall.return_value = [("table_created",)]
    mock_cursor.description = [("result",)]
    
    mock_connection.cursor.return_value = mock_cursor
    mock_connection.commit.return_value = None
    mock_connection.close.return_value = None
    
    return mock_connection


@pytest.fixture
def mock_datadreamer():
    """Mock DataDreamer for LLM synthesis testing."""
    mock_dreamer = Mock()
    
    # Mock synthesis output
    mock_step = Mock()
    mock_step.output = {
        "synthesized_data": ["id,name,age\n6,Frank,28\n7,Grace,33\n"]
    }
    
    mock_dreamer.__enter__.return_value = mock_dreamer
    mock_dreamer.__exit__.return_value = None
    
    return mock_dreamer, mock_step


@pytest.fixture
def cli_runner():
    """CLI test runner for Typer applications."""
    from typer.testing import CliRunner
    return CliRunner()


@pytest.fixture
def isolated_cli_env(tmp_dir, ingest_config):
    """Isolated environment for CLI testing."""
    # Set environment variables
    old_env = os.environ.copy()
    
    for key, value in ingest_config.items():
        os.environ[key] = value
    
    # Set working directory
    old_cwd = os.getcwd()
    os.chdir(tmp_dir)
    
    yield tmp_dir
    
    # Restore environment
    os.environ.clear()
    os.environ.update(old_env)
    os.chdir(old_cwd)


@pytest.fixture
def performance_monitor():
    """Monitor test performance and memory usage."""
    import psutil
    import time
    
    process = psutil.Process()
    start_time = time.time()
    start_memory = process.memory_info().rss
    
    yield
    
    end_time = time.time()
    end_memory = process.memory_info().rss
    
    # Store metrics for analysis
    metrics = {
        'duration': end_time - start_time,
        'memory_delta': end_memory - start_memory,
        'peak_memory': process.memory_info().rss
    }
    
    # Optional: fail test if performance degrades significantly
    if metrics['duration'] > 30:  # 30 second threshold
        pytest.fail(f"Test took too long: {metrics['duration']:.2f}s")


@pytest.fixture(autouse=True)
def reset_logging():
    """Reset logging configuration for each test."""
    from loguru import logger
    logger.remove()  # Remove all handlers
    logger.add(lambda _: None)  # Add null handler for tests


@pytest.fixture
def mock_external_dependencies():
    """Mock all external dependencies for offline testing."""
    mocks = {}
    
    # Mock OpenAI
    with patch('openai.OpenAI') as mock_openai:
        mock_openai.return_value = Mock()
        mocks['openai'] = mock_openai
        
        # Mock Firebolt SDK
        with patch('firebolt.db.connect') as mock_firebolt:
            mock_firebolt.return_value = Mock()
            mocks['firebolt'] = mock_firebolt
            
            # Mock S3/boto3
            with patch('boto3.client') as mock_boto3:
                mock_boto3.return_value = Mock()
                mocks['boto3'] = mock_boto3
                
                yield mocks


# Test data validation helpers
def assert_dataframe_equal(df1: pd.DataFrame, df2: pd.DataFrame, check_dtype=True):
    """Enhanced DataFrame comparison with better error messages."""
    try:
        pd.testing.assert_frame_equal(df1, df2, check_dtype=check_dtype)
    except AssertionError as e:
        # Add more context to the error
        context = f"""
        DataFrame comparison failed:
        Shape 1: {df1.shape}, Shape 2: {df2.shape}
        Columns 1: {list(df1.columns)}
        Columns 2: {list(df2.columns)}
        
        Original error: {e}
        """
        raise AssertionError(context) from e


def assert_file_exists_with_content(file_path: Path, min_size: int = 0):
    """Assert file exists and has minimum content."""
    assert file_path.exists(), f"File does not exist: {file_path}"
    assert file_path.stat().st_size >= min_size, f"File too small: {file_path}"


# Pytest configuration
def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "cli: marks tests as CLI tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )


def pytest_collection_modifyitems(config, items):
    """Automatically mark tests based on their names."""
    for item in items:
        # Mark slow tests
        if "large" in item.name or "performance" in item.name:
            item.add_marker(pytest.mark.slow)
            
        # Mark integration tests
        if "integration" in item.name or "test_cli" in item.name:
            item.add_marker(pytest.mark.integration)
            
        # Mark CLI tests
        if "cli" in item.name or item.fspath.basename.startswith("test_cli"):
            item.add_marker(pytest.mark.cli)
            
        # Mark unit tests (default)
        if not any(mark.name in ["slow", "integration", "cli"] for mark in item.iter_markers()):
            item.add_marker(pytest.mark.unit) 