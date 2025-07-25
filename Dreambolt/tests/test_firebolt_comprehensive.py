"""
Comprehensive Firebolt Database Tests
===================================

Tests for all Firebolt connector functionality with mocking.
"""
import pytest
import pandas as pd
from unittest.mock import patch, Mock, MagicMock

from firebolt_io import FireboltConnector, FireboltConfig
from firebolt_io_simple import FireboltConnector as SimpleFireboltConnector


class TestFireboltConfig:
    """Test Firebolt configuration class."""
    
    def test_config_initialization_with_env(self, ingest_config):
        """Test config initialization with environment variables."""
        with patch.dict('os.environ', ingest_config):
            config = FireboltConfig()
            
            assert config.username == ingest_config['FIREBOLT_USERNAME']
            assert config.password == ingest_config['FIREBOLT_PASSWORD']
            assert config.account_name == ingest_config['FIREBOLT_ACCOUNT_NAME']
            assert config.is_configured()
    
    def test_config_initialization_without_env(self):
        """Test config initialization without environment variables."""
        with patch.dict('os.environ', {}, clear=True):
            config = FireboltConfig()
            
            assert config.username is None
            assert config.password is None
            assert config.account_name is None
            assert not config.is_configured()
    
    def test_config_partial_env(self):
        """Test config with partial environment variables."""
        partial_config = {'FIREBOLT_USERNAME': 'test@example.com'}
        
        with patch.dict('os.environ', partial_config, clear=True):
            config = FireboltConfig()
            
            assert config.username == 'test@example.com'
            assert not config.is_configured()  # Missing password and account


class TestFireboltConnector:
    """Test main FireboltConnector class."""
    
    def test_initialization_with_config(self, ingest_config):
        """Test connector initialization with valid config."""
        with patch.dict('os.environ', ingest_config):
            with patch('firebolt_io.FIREBOLT_AVAILABLE', True), \
                 patch('firebolt_io.ResourceManager') as mock_rm:
                
                connector = FireboltConnector()
                
                assert connector.engine_name == ingest_config['FIREBOLT_ENGINE']
                assert connector.database_name == ingest_config['FIREBOLT_DATABASE']
                mock_rm.assert_called_once()
    
    def test_initialization_without_firebolt_sdk(self):
        """Test connector initialization without Firebolt SDK."""
        with patch('firebolt_io.FIREBOLT_AVAILABLE', False):
            connector = FireboltConnector()
            
            assert connector.resource_manager is None
    
    def test_initialization_custom_params(self):
        """Test connector initialization with custom parameters."""
        custom_engine = "custom_engine"
        custom_database = "custom_db"
        
        connector = FireboltConnector(engine=custom_engine, database=custom_database)
        
        assert connector.engine_name == custom_engine
        assert connector.database_name == custom_database
    
    def test_ensure_database_exists(self, mock_firebolt_connection):
        """Test ensuring database exists when it already exists."""
        with patch('firebolt_io.FIREBOLT_AVAILABLE', True):
            connector = FireboltConnector()
            connector.resource_manager = Mock()
            
            # Mock existing database
            mock_db = Mock()
            mock_db.name = "test_db"
            connector.resource_manager.databases.get_many.return_value = [mock_db]
            
            result = connector.ensure_database("test_db")
            
            assert result is True
            connector.resource_manager.databases.get_many.assert_called_once()
    
    def test_ensure_database_create_new(self, mock_firebolt_connection):
        """Test creating new database when it doesn't exist."""
        with patch('firebolt_io.FIREBOLT_AVAILABLE', True):
            connector = FireboltConnector()
            connector.resource_manager = Mock()
            
            # Mock no existing databases
            connector.resource_manager.databases.get_many.return_value = []
            connector.resource_manager.databases.create.return_value = Mock()
            
            with patch.object(connector, '_wait_for_database') as mock_wait:
                result = connector.ensure_database("new_db")
                
                assert result is True
                connector.resource_manager.databases.create.assert_called_once_with(name="new_db")
                mock_wait.assert_called_once_with("new_db")
    
    def test_ensure_database_without_resource_manager(self):
        """Test ensure_database without resource manager."""
        connector = FireboltConnector()
        connector.resource_manager = None
        
        result = connector.ensure_database("test_db")
        
        assert result is False
    
    def test_ensure_engine_exists_running(self):
        """Test ensuring engine exists and is running."""
        connector = FireboltConnector()
        connector.resource_manager = Mock()
        
        # Mock existing running engine
        mock_engine = Mock()
        mock_engine.name = "test_engine"
        mock_engine.current_status = "Running"
        connector.resource_manager.engines.get_many.return_value = [mock_engine]
        
        result = connector.ensure_engine("test_engine")
        
        assert result is True
        connector.resource_manager.engines.get_many.assert_called_once()
    
    def test_ensure_engine_exists_not_running(self):
        """Test ensuring engine exists but is not running."""
        connector = FireboltConnector()
        connector.resource_manager = Mock()
        
        # Mock existing stopped engine
        mock_engine = Mock()
        mock_engine.name = "test_engine"
        mock_engine.current_status = "Stopped"
        connector.resource_manager.engines.get_many.return_value = [mock_engine]
        
        with patch.object(connector, '_wait_for_engine') as mock_wait:
            result = connector.ensure_engine("test_engine")
            
            assert result is True
            mock_engine.start.assert_called_once()
            mock_wait.assert_called_once_with("test_engine")
    
    def test_ensure_engine_create_new(self):
        """Test creating new engine when it doesn't exist."""
        connector = FireboltConnector()
        connector.resource_manager = Mock()
        
        # Mock no existing engines
        connector.resource_manager.engines.get_many.return_value = []
        mock_new_engine = Mock()
        connector.resource_manager.engines.create.return_value = mock_new_engine
        
        with patch.object(connector, '_wait_for_engine') as mock_wait:
            result = connector.ensure_engine("new_engine")
            
            assert result is True
            connector.resource_manager.engines.create.assert_called_once()
            mock_new_engine.start.assert_called_once()
            mock_wait.assert_called_once_with("new_engine")
    
    def test_get_connection_success(self, ingest_config):
        """Test getting database connection successfully."""
        with patch.dict('os.environ', ingest_config):
            with patch('firebolt_io.FIREBOLT_AVAILABLE', True), \
                 patch('firebolt_io.connect') as mock_connect:
                
                mock_connection = Mock()
                mock_connect.return_value = mock_connection
                
                connector = FireboltConnector()
                connection = connector.get_connection()
                
                assert connection == mock_connection
                mock_connect.assert_called_once()
    
    def test_get_connection_not_available(self):
        """Test getting connection when Firebolt is not available."""
        with patch('firebolt_io.FIREBOLT_AVAILABLE', False):
            connector = FireboltConnector()
            
            with pytest.raises(ValueError, match="Firebolt not available"):
                connector.get_connection()
    
    def test_get_connection_cached(self, ingest_config):
        """Test that connection is cached after first call."""
        with patch.dict('os.environ', ingest_config):
            with patch('firebolt_io.FIREBOLT_AVAILABLE', True), \
                 patch('firebolt_io.connect') as mock_connect:
                
                mock_connection = Mock()
                mock_connect.return_value = mock_connection
                
                connector = FireboltConnector()
                
                # First call
                connection1 = connector.get_connection()
                # Second call
                connection2 = connector.get_connection()
                
                assert connection1 == connection2
                mock_connect.assert_called_once()  # Should only be called once
    
    def test_ensure_table_success(self, sample_csv_data):
        """Test ensuring table exists successfully."""
        connector = FireboltConnector()
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_connection.cursor.return_value = mock_cursor
        
        with patch.object(connector, 'ensure_engine', return_value=True), \
             patch.object(connector, 'get_connection', return_value=mock_connection), \
             patch.object(connector, '_generate_table_schema', return_value="CREATE TABLE..."):
            
            result = connector.ensure_table("test_table", sample_csv_data)
            
            assert result is True
            mock_cursor.execute.assert_called()
            mock_connection.commit.assert_called()
    
    def test_ensure_table_engine_failure(self, sample_csv_data):
        """Test ensure_table when engine setup fails."""
        connector = FireboltConnector()
        
        with patch.object(connector, 'ensure_engine', return_value=False):
            result = connector.ensure_table("test_table", sample_csv_data)
            
            assert result is False
    
    def test_generate_table_schema(self, sample_csv_data):
        """Test table schema generation."""
        connector = FireboltConnector()
        
        schema = connector._generate_table_schema("test_table", sample_csv_data)
        
        assert isinstance(schema, str)
        assert "CREATE TABLE" in schema.upper()
        assert "test_table" in schema
        assert "id" in schema  # Should include column from sample data
    
    def test_infer_firebolt_type_mappings(self):
        """Test data type mapping to Firebolt types."""
        connector = FireboltConnector()
        
        # Test various pandas dtypes
        assert connector._infer_firebolt_type("int64") == "BIGINT"
        assert connector._infer_firebolt_type("float64") == "DOUBLE"
        assert connector._infer_firebolt_type("object") == "TEXT"
        assert connector._infer_firebolt_type("bool") == "BOOLEAN"
        assert connector._infer_firebolt_type("datetime64[ns]") == "TIMESTAMP"
        assert connector._infer_firebolt_type("unknown_type") == "TEXT"  # Default
    
    def test_copy_data_success(self, sample_csv_data, tmp_dir):
        """Test copying data to Firebolt successfully."""
        # Create a parquet file
        parquet_file = tmp_dir / "test.parquet"
        sample_csv_data.to_parquet(parquet_file, index=False)
        
        connector = FireboltConnector()
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_connection.cursor.return_value = mock_cursor
        
        with patch.object(connector, 'get_connection', return_value=mock_connection):
            result = connector.copy_data("test_table", str(parquet_file))
            
            assert result is True
            mock_cursor.execute.assert_called()
            mock_connection.commit.assert_called()
    
    def test_copy_data_file_not_found(self):
        """Test copy_data with non-existent file."""
        connector = FireboltConnector()
        
        result = connector.copy_data("test_table", "/nonexistent/file.parquet")
        
        assert result is False
    
    def test_copy_data_unsupported_format(self, tmp_dir):
        """Test copy_data with unsupported file format."""
        txt_file = tmp_dir / "test.txt"
        txt_file.write_text("not a parquet file")
        
        connector = FireboltConnector()
        
        result = connector.copy_data("test_table", str(txt_file))
        
        assert result is False


class TestSimpleFireboltConnector:
    """Test simplified FireboltConnector for fallback scenarios."""
    
    def test_simple_initialization(self):
        """Test SimpleFireboltConnector initialization."""
        connector = SimpleFireboltConnector()
        assert hasattr(connector, 'config')
    
    def test_simple_dry_run_mode(self, sample_csv_data):
        """Test simple connector in dry run mode."""
        connector = SimpleFireboltConnector()
        
        # Most operations should succeed in dry run mode
        result = connector.ensure_table("test_table", sample_csv_data, dry_run=True)
        
        # Should return True for dry run
        assert result is True
    
    def test_simple_mock_connection(self):
        """Test simple connector mock connection."""
        from firebolt_io_simple import MockConnection, MockCursor
        
        mock_conn = MockConnection()
        mock_cursor = mock_conn.cursor()
        
        assert isinstance(mock_cursor, MockCursor)
        
        # Test mock operations
        mock_cursor.execute("SELECT 1")
        result = mock_cursor.fetchall()
        assert result == [("Mock result",)]


class TestFireboltEdgeCases:
    """Test edge cases and error conditions."""
    
    def test_connection_timeout(self, ingest_config):
        """Test handling connection timeouts."""
        with patch.dict('os.environ', ingest_config):
            with patch('firebolt_io.FIREBOLT_AVAILABLE', True), \
                 patch('firebolt_io.connect', side_effect=TimeoutError("Connection timeout")):
                
                connector = FireboltConnector()
                
                with pytest.raises(TimeoutError):
                    connector.get_connection()
    
    def test_resource_manager_error(self, ingest_config):
        """Test handling resource manager errors."""
        with patch.dict('os.environ', ingest_config):
            with patch('firebolt_io.FIREBOLT_AVAILABLE', True), \
                 patch('firebolt_io.ResourceManager', side_effect=Exception("API Error")):
                
                connector = FireboltConnector()
                
                assert connector.resource_manager is None
    
    def test_database_creation_error(self):
        """Test handling database creation errors."""
        connector = FireboltConnector()
        connector.resource_manager = Mock()
        
        # Mock database creation failure
        connector.resource_manager.databases.get_many.return_value = []
        connector.resource_manager.databases.create.side_effect = Exception("Creation failed")
        
        result = connector.ensure_database("test_db")
        
        assert result is False
    
    def test_engine_start_error(self):
        """Test handling engine start errors."""
        connector = FireboltConnector()
        connector.resource_manager = Mock()
        
        # Mock engine that fails to start
        mock_engine = Mock()
        mock_engine.name = "test_engine"
        mock_engine.current_status = "Stopped"
        mock_engine.start.side_effect = Exception("Start failed")
        connector.resource_manager.engines.get_many.return_value = [mock_engine]
        
        result = connector.ensure_engine("test_engine")
        
        assert result is False
    
    def test_sql_execution_error(self, sample_csv_data):
        """Test handling SQL execution errors."""
        connector = FireboltConnector()
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_cursor.execute.side_effect = Exception("SQL Error")
        mock_connection.cursor.return_value = mock_cursor
        
        with patch.object(connector, 'ensure_engine', return_value=True), \
             patch.object(connector, 'get_connection', return_value=mock_connection):
            
            result = connector.ensure_table("test_table", sample_csv_data)
            
            assert result is False
    
    def test_very_large_table_schema(self, tmp_dir):
        """Test handling very large table schemas."""
        # Create DataFrame with many columns
        large_df = pd.DataFrame({
            f'col_{i}': [1, 2, 3] for i in range(1000)
        })
        
        connector = FireboltConnector()
        
        schema = connector._generate_table_schema("large_table", large_df)
        
        assert isinstance(schema, str)
        assert "CREATE TABLE" in schema.upper()
        assert len(schema) > 1000  # Should be a large schema
    
    def test_unicode_table_names(self, sample_csv_data):
        """Test handling Unicode table names."""
        connector = FireboltConnector()
        
        # Table names with Unicode characters
        unicode_name = "测试表_名称"
        
        schema = connector._generate_table_schema(unicode_name, sample_csv_data)
        
        assert isinstance(schema, str)
        # Should handle Unicode gracefully (may sanitize or escape)


class TestFireboltPerformance:
    """Performance tests for Firebolt operations."""
    
    @pytest.mark.slow
    def test_large_schema_generation(self, large_dataset, performance_monitor):
        """Test schema generation with large datasets."""
        connector = FireboltConnector()
        
        schema = connector._generate_table_schema("large_table", large_dataset)
        
        assert isinstance(schema, str)
        assert "CREATE TABLE" in schema.upper()
    
    def test_connection_pooling_simulation(self, ingest_config):
        """Test simulated connection pooling behavior."""
        with patch.dict('os.environ', ingest_config):
            with patch('firebolt_io.FIREBOLT_AVAILABLE', True), \
                 patch('firebolt_io.connect') as mock_connect:
                
                mock_connection = Mock()
                mock_connect.return_value = mock_connection
                
                connector = FireboltConnector()
                
                # Multiple connection requests should reuse connection
                connections = [connector.get_connection() for _ in range(10)]
                
                # All should be the same instance
                assert all(conn == connections[0] for conn in connections)
                # Connect should only be called once
                mock_connect.assert_called_once() 