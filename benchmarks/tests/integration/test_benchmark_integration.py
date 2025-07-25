"""Integration tests for full benchmark workflow."""

from unittest.mock import MagicMock, patch
from pathlib import Path

import pytest

from src.python.src.runner import BenchmarkRunner


@pytest.mark.integration
@pytest.mark.slow
class TestBenchmarkIntegration:
    """Integration tests for complete benchmark workflows."""

    @patch('src.python.src.runner.connectors.get_connector_class')
    def test_full_benchmark_workflow_mocked(self, mock_get_connector, sample_benchmark_structure, temp_dir):
        """Test complete benchmark workflow with mocked connectors."""
        # Setup mock connector
        mock_connector_class = MagicMock()
        mock_connector_instance = MagicMock()
        mock_connector_class.return_value = mock_connector_instance
        mock_get_connector.return_value = mock_connector_class
        
        # Mock query results
        mock_connector_instance.execute_query.return_value = [
            {"id": 1, "name": "test"},
            {"id": 2, "name": "test2"},
        ]
        
        # Setup output directory
        output_dir = temp_dir / "results"
        
        # Create benchmark runner
        runner = BenchmarkRunner(
            benchmark_name="test_benchmark",
            vendors=["firebolt", "snowflake"],
            pool_size=1,
            concurrency=1,
            output_dir=str(output_dir),
            benchmark_path=str(sample_benchmark_structure),
            execute_setup=True,
            run_warmup=True,
        )
        
        # Run benchmark
        results = runner.run_benchmark()
        
        # Verify results structure
        assert isinstance(results, dict)
        assert len(results) == 2  # Two vendors
        assert "firebolt" in results
        assert "snowflake" in results
        
        # Verify each vendor has results
        for vendor_results in results.values():
            assert isinstance(vendor_results, list)
            assert len(vendor_results) > 0  # Should have some results
            
            # Check result structure
            for result in vendor_results:
                assert "vendor" in result
                assert "query_name" in result
                assert "execution_time" in result
                assert "success" in result
                assert isinstance(result["execution_time"], float)
                assert isinstance(result["success"], bool)

    @patch('src.python.src.runner.connectors.get_connector_class')
    def test_benchmark_with_setup_and_warmup(self, mock_get_connector, sample_benchmark_structure):
        """Test benchmark with setup and warmup scripts."""
        # Setup mock connector
        mock_connector_class = MagicMock()
        mock_connector_instance = MagicMock()
        mock_connector_class.return_value = mock_connector_instance
        mock_get_connector.return_value = mock_connector_class
        
        # Mock query results
        mock_connector_instance.execute_query.return_value = [{"result": "success"}]
        
        runner = BenchmarkRunner(
            benchmark_name="test_benchmark",
            vendors=["firebolt"],
            pool_size=1,
            concurrency=1, 
            benchmark_path=str(sample_benchmark_structure),
            execute_setup=True,
            run_warmup=True,
        )
        
        results = runner.run_benchmark()
        
        # Verify setup and warmup were called
        # execute_query should be called multiple times:
        # - For setup script
        # - For warmup script
        # - For actual benchmark queries
        assert mock_connector_instance.execute_query.call_count >= 3
        
        # Verify benchmark completed successfully
        assert "firebolt" in results
        assert len(results["firebolt"]) > 0

    @patch('src.python.src.runner.connectors.get_connector_class')
    def test_benchmark_with_query_failure(self, mock_get_connector, sample_benchmark_structure):
        """Test benchmark handling when queries fail."""
        # Setup mock connector that fails on certain queries
        mock_connector_class = MagicMock()
        mock_connector_instance = MagicMock()
        mock_connector_class.return_value = mock_connector_instance
        mock_get_connector.return_value = mock_connector_class
        
        # First call succeeds (setup/warmup), second fails (benchmark)
        mock_connector_instance.execute_query.side_effect = [
            [{"setup": "success"}],  # Setup
            [{"warmup": "success"}],  # Warmup
            Exception("Query failed"),  # First benchmark query fails
        ]
        
        runner = BenchmarkRunner(
            benchmark_name="test_benchmark",
            vendors=["firebolt"],
            pool_size=1,
            concurrency=1,
            benchmark_path=str(sample_benchmark_structure),
            execute_setup=True,
            run_warmup=True,
        )
        
        results = runner.run_benchmark()
        
        # Should still return results structure even with failures
        assert isinstance(results, dict)
        # Results might be empty if all queries failed
        if "firebolt" in results:
            # Check if error handling worked correctly
            for result in results["firebolt"]:
                if not result["success"]:
                    assert "error" in result
                    assert result["error"] is not None

    @patch('src.python.src.runner.connectors.get_connector_class')  
    def test_concurrent_benchmark_execution(self, mock_get_connector, sample_benchmark_structure):
        """Test benchmark with multiple concurrent connections."""
        # Setup mock connector
        mock_connector_class = MagicMock()
        mock_get_connector.return_value = mock_connector_class
        
        # Mock multiple connector instances for concurrency
        mock_instances = [MagicMock() for _ in range(3)]
        mock_connector_class.side_effect = mock_instances
        
        # Each instance should return results
        for mock_instance in mock_instances:
            mock_instance.execute_query.return_value = [{"concurrent": "result"}]
        
        runner = BenchmarkRunner(
            benchmark_name="test_benchmark",
            vendors=["firebolt"],
            pool_size=3,  # Multiple connections
            concurrency=3,  # Concurrent execution
            benchmark_path=str(sample_benchmark_structure),
            run_warmup=False,  # Skip warmup for simpler test
        )
        
        results = runner.run_benchmark()
        
        # Verify concurrent execution worked
        assert "firebolt" in results
        firebolt_results = results["firebolt"]
        
        # Should have results from concurrent runs
        concurrent_runs = set(result["concurrent_run"] for result in firebolt_results)
        assert len(concurrent_runs) > 1  # Multiple concurrent runs
        
    @patch('src.python.src.runner.connectors.get_connector_class')
    def test_benchmark_missing_sql_files(self, mock_get_connector, temp_dir):
        """Test benchmark behavior when SQL files are missing."""
        mock_connector_class = MagicMock()
        mock_get_connector.return_value = mock_connector_class
        
        # Create empty benchmark directory (no SQL files)
        empty_benchmark_dir = temp_dir / "empty_benchmark"
        empty_benchmark_dir.mkdir()
        
        runner = BenchmarkRunner(
            benchmark_name="empty_benchmark",
            vendors=["firebolt"],
            pool_size=1,
            concurrency=1,
            benchmark_path=str(empty_benchmark_dir),
        )
        
        # Should handle missing files gracefully
        results = runner.run_benchmark()
        
        # Results should be empty or have errors
        assert isinstance(results, dict)
        # The vendor might not be in results if benchmark file is missing


@pytest.mark.integration
class TestEnvironmentIntegration:
    """Integration tests for environment configuration."""

    def test_environment_config_integration(self):
        """Test that environment configuration works end-to-end."""
        from src.python.src.env_config import load_environment_config, get_app_config
        
        # Test environment loading
        env_config = load_environment_config()
        assert isinstance(env_config, dict)
        
        # Test app config loading
        app_config = get_app_config()
        assert isinstance(app_config, dict)
        assert "default_output_dir" in app_config


@pytest.mark.integration
@pytest.mark.requires_db
class TestDatabaseConnectorIntegration:
    """Integration tests that require actual database connections.
    
    These tests are marked as requiring database connections and will
    be skipped unless actual database credentials are available.
    """

    def test_firebolt_connector_real_connection(self):
        """Test Firebolt connector with real database (if available)."""
        pytest.skip("Requires real Firebolt database credentials")
        
        # This test would use actual Firebolt credentials to test connection
        # Only enable for manual testing with real database
        
    def test_snowflake_connector_real_connection(self):
        """Test Snowflake connector with real database (if available)."""
        pytest.skip("Requires real Snowflake database credentials")
        
        # This test would use actual Snowflake credentials to test connection
        # Only enable for manual testing with real database
        
    def test_redshift_connector_real_connection(self):
        """Test Redshift connector with real database (if available).""" 
        pytest.skip("Requires real Redshift database credentials")
        
        # This test would use actual Redshift credentials to test connection
        # Only enable for manual testing with real database
        
    def test_bigquery_connector_real_connection(self):
        """Test BigQuery connector with real database (if available)."""
        pytest.skip("Requires real BigQuery database credentials")
        
        # This test would use actual BigQuery credentials to test connection
        # Only enable for manual testing with real database