"""Unit tests for benchmark runner module."""

import json
import tempfile
from pathlib import Path
from queue import Queue
from unittest.mock import MagicMock, mock_open, patch

import pytest

from src.python.src.runner import BenchmarkRunner, ConnectionPool, QueryResult


@pytest.mark.unit
class TestConnectionPool:
    """Test suite for ConnectionPool class."""

    def test_connection_pool_init(self, mock_connector):
        """Test connection pool initialization."""
        credentials = {"test": "credentials"}
        pool_size = 3
        
        with patch.object(ConnectionPool, '_fill_pool'):
            pool = ConnectionPool(mock_connector, credentials, pool_size)
            
            assert pool.connector == mock_connector
            assert pool.credentials == credentials
            assert pool.pool_size == pool_size

    def test_connection_pool_fill_pool(self, mock_connector):
        """Test connection pool filling with connections."""
        credentials = {"test": "credentials"}
        pool_size = 2
        
        # Mock the connector class to return new instances
        mock_connector.__class__ = MagicMock()
        mock_instance1 = MagicMock()
        mock_instance2 = MagicMock() 
        mock_connector.__class__.side_effect = [mock_instance1, mock_instance2]
        
        pool = ConnectionPool(mock_connector, credentials, pool_size)
        
        # Verify connections were created and added to pool
        assert pool.connections.qsize() == pool_size
        mock_instance1.connect.assert_called_once()
        mock_instance2.connect.assert_called_once()

    def test_connection_pool_get_return_connection(self, mock_connector):
        """Test getting and returning connections from pool."""
        credentials = {"test": "credentials"}
        
        with patch.object(ConnectionPool, '_fill_pool'):
            pool = ConnectionPool(mock_connector, credentials, 1)
            
            # Add a mock connection to the pool
            mock_conn = MagicMock()
            pool.connections.put(mock_conn)
            
            # Get connection
            retrieved_conn = pool.get_connection()
            assert retrieved_conn == mock_conn
            assert pool.connections.empty()
            
            # Return connection
            pool.return_connection(mock_conn)
            assert pool.connections.qsize() == 1


@pytest.mark.unit
class TestBenchmarkRunner:
    """Test suite for BenchmarkRunner class."""

    def test_benchmark_runner_init_with_env_creds(self, sample_benchmark_config):
        """Test BenchmarkRunner initialization with environment credentials."""
        with patch('src.python.src.runner.load_environment_config') as mock_load_env, \
             patch('src.python.src.runner.validate_vendor_credentials') as mock_validate, \
             patch('src.python.src.runner.connectors.get_connector_class') as mock_get_connector:
            
            mock_load_env.return_value = {"firebolt": {"test": "creds"}}
            mock_connector_class = MagicMock()
            mock_get_connector.return_value = mock_connector_class
            
            runner = BenchmarkRunner(
                benchmark_name="test_benchmark",
                vendors=["firebolt"],
                pool_size=1,
                concurrency=1,
            )
            
            assert runner.benchmark_name == "test_benchmark"
            assert runner.vendors == ["firebolt"]
            assert runner.pool_size == 1
            assert runner.concurrency == 1
            mock_load_env.assert_called_once()
            mock_validate.assert_called_once()

    def test_benchmark_runner_init_with_json_creds(self, temp_dir):
        """Test BenchmarkRunner initialization with JSON credentials file."""
        # Create test credentials file
        creds = {"firebolt": {"test": "creds"}}
        creds_file = temp_dir / "test_creds.json"
        creds_file.write_text(json.dumps(creds))
        
        with patch('src.python.src.runner.validate_vendor_credentials') as mock_validate, \
             patch('src.python.src.runner.connectors.get_connector_class') as mock_get_connector:
            
            mock_connector_class = MagicMock()
            mock_get_connector.return_value = mock_connector_class
            
            runner = BenchmarkRunner(
                benchmark_name="test_benchmark",
                creds_file=str(creds_file),
                vendors=["firebolt"],
            )
            
            assert runner.credentials == creds
            mock_validate.assert_called_once()

    def test_benchmark_runner_missing_vendor_credentials(self):
        """Test BenchmarkRunner initialization with missing vendor credentials."""
        with patch('src.python.src.runner.load_environment_config') as mock_load_env:
            mock_load_env.return_value = {"snowflake": {"test": "creds"}}
            
            with pytest.raises(ValueError, match="No credentials found for vendor: firebolt"):
                BenchmarkRunner(
                    benchmark_name="test_benchmark",
                    vendors=["firebolt"],
                )

    def test_load_queries_from_file(self, sample_sql_file):
        """Test loading SQL queries from a file."""
        with patch('src.python.src.runner.load_environment_config') as mock_load_env, \
             patch('src.python.src.runner.validate_vendor_credentials'), \
             patch('src.python.src.runner.connectors.get_connector_class') as mock_get_connector:
            
            mock_load_env.return_value = {"firebolt": {"test": "creds"}}
            mock_get_connector.return_value = MagicMock()
            
            runner = BenchmarkRunner(
                benchmark_name="test_benchmark", 
                vendors=["firebolt"],
            )
            
            queries = runner._load_queries(str(sample_sql_file))
            
            assert len(queries) == 3
            assert "SELECT 1 AS test_column" in queries[0]
            assert "SELECT COUNT(*) FROM test_table" in queries[1]
            assert "SELECT * FROM users" in queries[2]

    def test_load_queries_from_list(self, sample_sql_queries):
        """Test loading SQL queries from a list."""
        with patch('src.python.src.runner.load_environment_config') as mock_load_env, \
             patch('src.python.src.runner.validate_vendor_credentials'), \
             patch('src.python.src.runner.connectors.get_connector_class') as mock_get_connector:
            
            mock_load_env.return_value = {"firebolt": {"test": "creds"}}
            mock_get_connector.return_value = MagicMock()
            
            runner = BenchmarkRunner(
                benchmark_name="test_benchmark",
                vendors=["firebolt"],
            )
            
            queries = runner._load_queries(sample_sql_queries)
            
            assert queries == sample_sql_queries

    def test_load_queries_invalid_input(self):
        """Test loading queries with invalid input type."""
        with patch('src.python.src.runner.load_environment_config') as mock_load_env, \
             patch('src.python.src.runner.validate_vendor_credentials'), \
             patch('src.python.src.runner.connectors.get_connector_class') as mock_get_connector:
            
            mock_load_env.return_value = {"firebolt": {"test": "creds"}}
            mock_get_connector.return_value = MagicMock()
            
            runner = BenchmarkRunner(
                benchmark_name="test_benchmark",
                vendors=["firebolt"],
            )
            
            with pytest.raises(TypeError, match="query_file must be a file path or list"):
                runner._load_queries(123)  # Invalid type

    def test_get_sql_file_vendor_specific(self, sample_benchmark_structure):
        """Test getting vendor-specific SQL file.""" 
        with patch('src.python.src.runner.load_environment_config') as mock_load_env, \
             patch('src.python.src.runner.validate_vendor_credentials'), \
             patch('src.python.src.runner.connectors.get_connector_class') as mock_get_connector:
            
            mock_load_env.return_value = {"firebolt": {"test": "creds"}}
            mock_get_connector.return_value = MagicMock()
            
            runner = BenchmarkRunner(
                benchmark_name="test_benchmark",
                vendors=["firebolt"],
                benchmark_path=str(sample_benchmark_structure),
            )
            
            sql_file = runner._get_sql_file("firebolt", "benchmark")
            
            assert sql_file.name == "benchmark.sql"
            assert "firebolt" in str(sql_file)

    def test_get_sql_file_general_fallback(self, sample_benchmark_structure):
        """Test falling back to general SQL file when vendor-specific doesn't exist."""
        with patch('src.python.src.runner.load_environment_config') as mock_load_env, \
             patch('src.python.src.runner.validate_vendor_credentials'), \
             patch('src.python.src.runner.connectors.get_connector_class') as mock_get_connector:
            
            mock_load_env.return_value = {"bigquery": {"test": "creds"}}
            mock_get_connector.return_value = MagicMock()
            
            runner = BenchmarkRunner(
                benchmark_name="test_benchmark", 
                vendors=["bigquery"],
                benchmark_path=str(sample_benchmark_structure),
            )
            
            sql_file = runner._get_sql_file("bigquery", "benchmark")
            
            assert sql_file.name == "benchmark.sql"
            assert "bigquery" not in str(sql_file)  # Should be general file

    def test_run_query_success(self, mock_connector):
        """Test successful query execution."""
        with patch('src.python.src.runner.load_environment_config') as mock_load_env, \
             patch('src.python.src.runner.validate_vendor_credentials'), \
             patch('src.python.src.runner.connectors.get_connector_class') as mock_get_connector:
            
            mock_load_env.return_value = {"firebolt": {"test": "creds"}}
            mock_get_connector.return_value = MagicMock()
            
            runner = BenchmarkRunner(
                benchmark_name="test_benchmark",
                vendors=["firebolt"],
            )
            
            # Mock connection pool
            mock_pool = MagicMock()
            mock_pool.get_connection.return_value = mock_connector
            runner.connection_pools["firebolt"] = mock_pool
            
            # Mock connector response
            mock_connector.execute_query.return_value = [{"test": "result"}]
            
            result = runner._run_query("firebolt", "test_query", "SELECT 1", 1)
            
            assert result["vendor"] == "firebolt"
            assert result["query_name"] == "test_query"
            assert result["query"] == "SELECT 1"
            assert result["status"] == "success"
            assert result["rows"] == 1
            assert result["concurrent_run"] == 1

    def test_run_query_failure(self, mock_connector):
        """Test query execution failure."""
        with patch('src.python.src.runner.load_environment_config') as mock_load_env, \
             patch('src.python.src.runner.validate_vendor_credentials'), \
             patch('src.python.src.runner.connectors.get_connector_class') as mock_get_connector:
            
            mock_load_env.return_value = {"firebolt": {"test": "creds"}}
            mock_get_connector.return_value = MagicMock()
            
            runner = BenchmarkRunner(
                benchmark_name="test_benchmark",
                vendors=["firebolt"],
            )
            
            # Mock connection pool
            mock_pool = MagicMock()
            mock_pool.get_connection.return_value = mock_connector
            runner.connection_pools["firebolt"] = mock_pool
            
            # Mock connector to raise exception
            mock_connector.execute_query.side_effect = Exception("Query failed")
            
            result = runner._run_query("firebolt", "test_query", "SELECT 1", 1)
            
            assert result["vendor"] == "firebolt"
            assert result["query_name"] == "test_query"
            assert result["status"] == "error"
            assert "Query failed" in result["error"]

    def test_execute_setup_script_success(self, sample_benchmark_structure):
        """Test successful setup script execution."""
        with patch('src.python.src.runner.load_environment_config') as mock_load_env, \
             patch('src.python.src.runner.validate_vendor_credentials'), \
             patch('src.python.src.runner.connectors.get_connector_class') as mock_get_connector:
            
            mock_load_env.return_value = {"firebolt": {"test": "creds"}}
            mock_connector_instance = MagicMock()
            mock_get_connector.return_value = MagicMock(return_value=mock_connector_instance)
            
            runner = BenchmarkRunner(
                benchmark_name="test_benchmark",
                vendors=["firebolt"],
                benchmark_path=str(sample_benchmark_structure),
            )
            
            success = runner._execute_setup_script("firebolt")
            
            assert success is True
            mock_connector_instance.execute_query.assert_called()

    def test_execute_warmup_script_disabled(self, sample_benchmark_structure):
        """Test warmup script execution when disabled."""
        with patch('src.python.src.runner.load_environment_config') as mock_load_env, \
             patch('src.python.src.runner.validate_vendor_credentials'), \
             patch('src.python.src.runner.connectors.get_connector_class') as mock_get_connector:
            
            mock_load_env.return_value = {"firebolt": {"test": "creds"}}
            mock_get_connector.return_value = MagicMock()
            
            runner = BenchmarkRunner(
                benchmark_name="test_benchmark",
                vendors=["firebolt"],
                benchmark_path=str(sample_benchmark_structure),
                run_warmup=False,  # Disabled
            )
            
            success = runner._execute_warmup_script("firebolt")
            
            assert success is True  # Should return True immediately


@pytest.mark.unit
class TestQueryResult:
    """Test suite for QueryResult dataclass."""

    def test_query_result_creation(self):
        """Test QueryResult dataclass creation."""
        result = QueryResult(
            query_number=1,
            execution_time=1.23,
            concurrent_run=1,
            success=True,
            vendor="firebolt",
            query_name="test_query",
        )
        
        assert result.query_number == 1
        assert result.execution_time == 1.23
        assert result.concurrent_run == 1
        assert result.success is True
        assert result.vendor == "firebolt"
        assert result.query_name == "test_query"
        assert result.error is None  # Default value

    def test_query_result_with_error(self):
        """Test QueryResult dataclass with error."""
        result = QueryResult(
            query_number=1,
            execution_time=0.0,
            concurrent_run=1,
            success=False,
            error="Test error message",
        )
        
        assert result.success is False
        assert result.error == "Test error message"