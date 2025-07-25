"""Unit tests for database connector modules."""

import json
from unittest.mock import MagicMock, patch

import pytest

from src.python.src.connectors.base import WarehouseConnector
from src.python.src.connectors.firebolt import FireboltConnector
from src.python.src.connectors.snowflake import SnowflakeConnector
from src.python.src.connectors.redshift import RedshiftConnector
from src.python.src.connectors.bigquery import BigQueryConnector


@pytest.mark.unit
class TestWarehouseConnector:
    """Test suite for WarehouseConnector base class."""

    def test_abstract_base_class(self):
        """Test that WarehouseConnector cannot be instantiated directly."""
        with pytest.raises(TypeError):
            WarehouseConnector()

    def test_context_manager_protocol(self):
        """Test that the base class provides context manager methods."""
        class TestConnector(WarehouseConnector):
            def connect(self):
                pass
            
            def execute_query(self, query, parameters=None):
                return []
            
            def close(self):
                pass

        connector = TestConnector()
        
        # Test context manager entry
        assert connector.__enter__() == connector
        
        # Test context manager exit
        assert connector.__exit__(None, None, None) is False


@pytest.mark.unit 
class TestFireboltConnector:
    """Test suite for FireboltConnector class."""

    def test_firebolt_connector_init_valid_config(self):
        """Test FireboltConnector initialization with valid config."""
        config = {
            "engine_name": "test_engine",
            "database": "test_db",
            "account_name": "test_account",
            "auth": {
                "id": "test_id",
                "secret": "test_secret",
            },
        }
        
        connector = FireboltConnector(config)
        
        assert connector.config == config
        assert connector._conn is None
        assert connector.cursor is None

    def test_firebolt_connector_init_missing_required_params(self):
        """Test FireboltConnector initialization with missing required parameters."""
        config = {
            "engine_name": "test_engine",
            "database": "test_db",
            # Missing account_name and auth
        }
        
        with pytest.raises(ValueError, match="Missing required configuration parameters"):
            FireboltConnector(config)

    def test_firebolt_connector_init_invalid_auth_structure(self):
        """Test FireboltConnector initialization with invalid auth structure."""
        config = {
            "engine_name": "test_engine", 
            "database": "test_db",
            "account_name": "test_account",
            "auth": {
                "id": "test_id",
                # Missing secret
            },
        }
        
        with pytest.raises(ValueError, match="auth must contain 'id' and 'secret' keys"):
            FireboltConnector(config)

    @patch('src.python.src.connectors.firebolt.connect')
    @patch('src.python.src.connectors.firebolt.ClientCredentials')
    def test_firebolt_connector_connect_success(self, mock_credentials, mock_connect):
        """Test successful Firebolt connection."""
        config = {
            "engine_name": "test_engine",
            "database": "test_db", 
            "account_name": "test_account",
            "auth": {
                "id": "test_id",
                "secret": "test_secret",
            },
        }
        
        # Mock connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn
        
        connector = FireboltConnector(config)
        connector.connect()
        
        # Verify connection was established
        assert connector._conn == mock_conn
        assert connector.cursor == mock_cursor
        
        # Verify connection parameters
        mock_connect.assert_called_once_with(
            engine_name="test_engine",
            database="test_db",
            account_name="test_account",
            auth=mock_credentials.return_value
        )
        
        # Verify cache was disabled
        mock_cursor.execute.assert_called()

    @patch('src.python.src.connectors.firebolt.connect')
    def test_firebolt_connector_connect_already_connected(self, mock_connect):
        """Test connecting when already connected."""
        config = {
            "engine_name": "test_engine",
            "database": "test_db",
            "account_name": "test_account", 
            "auth": {"id": "test_id", "secret": "test_secret"},
        }
        
        connector = FireboltConnector(config)
        connector._conn = MagicMock()  # Simulate existing connection
        
        connector.connect()
        
        # Should not attempt new connection
        mock_connect.assert_not_called()

    def test_firebolt_connector_execute_query_auto_connect(self):
        """Test query execution with automatic connection."""
        config = {
            "engine_name": "test_engine",
            "database": "test_db",
            "account_name": "test_account",
            "auth": {"id": "test_id", "secret": "test_secret"},
        }
        
        with patch.object(FireboltConnector, 'connect') as mock_connect:
            connector = FireboltConnector(config)
            
            # Mock cursor for query execution
            mock_cursor = MagicMock()
            mock_cursor.description = True
            mock_cursor.fetchall.return_value = [{"test": "result"}]
            connector.cursor = mock_cursor
            connector._conn = MagicMock()
            
            result = connector.execute_query("SELECT 1")
            
            # Should auto-connect if not connected
            mock_connect.assert_called_once()
            assert result == [{"test": "result"}]

    def test_firebolt_connector_close(self):
        """Test closing Firebolt connection."""
        config = {
            "engine_name": "test_engine",
            "database": "test_db", 
            "account_name": "test_account",
            "auth": {"id": "test_id", "secret": "test_secret"},
        }
        
        connector = FireboltConnector(config)
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        connector._conn = mock_conn
        connector.cursor = mock_cursor
        
        connector.close()
        
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()
        assert connector._conn is None
        assert connector.cursor is None


@pytest.mark.unit
class TestSnowflakeConnector:
    """Test suite for SnowflakeConnector class."""

    def test_snowflake_connector_init_valid_config(self):
        """Test SnowflakeConnector initialization with valid config."""
        config = {
            "account": "test_account",
            "user": "test_user", 
            "password": "test_password",
            "database": "test_db",
            "schema": "test_schema",
            "warehouse": "test_warehouse",
        }
        
        connector = SnowflakeConnector(config)
        
        assert connector.config == config
        assert connector._conn is None
        assert connector._cursor is None

    def test_snowflake_connector_missing_required_params(self):
        """Test SnowflakeConnector with missing required parameters."""
        config = {
            "account": "test_account",
            # Missing user and password
        }
        
        with pytest.raises(ValueError, match="Missing required configuration parameters"):
            SnowflakeConnector(config)

    @patch('src.python.src.connectors.snowflake.snowflake.connector.connect')
    def test_snowflake_connector_connect_success(self, mock_connect):
        """Test successful Snowflake connection."""
        config = {
            "account": "test_account",
            "user": "test_user",
            "password": "test_password",
            "database": "test_db",
            "schema": "test_schema", 
            "warehouse": "test_warehouse",
        }
        
        # Mock connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn
        
        connector = SnowflakeConnector(config)
        connector.connect()
        
        # Verify connection was established
        assert connector._conn == mock_conn
        assert connector._cursor == mock_cursor
        
        # Verify connection parameters
        mock_connect.assert_called_once()
        call_args = mock_connect.call_args[1]
        assert call_args["account"] == "test_account"
        assert call_args["user"] == "test_user"
        assert call_args["password"] == "test_password"
        assert call_args["telemetry"] is False

    def test_snowflake_connector_close(self):
        """Test closing Snowflake connection."""
        config = {
            "account": "test_account",
            "user": "test_user",
            "password": "test_password",
        }
        
        connector = SnowflakeConnector(config)
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        connector._conn = mock_conn
        connector._cursor = mock_cursor
        
        connector.close()
        
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()
        assert connector._conn is None
        assert connector._cursor is None


@pytest.mark.unit
class TestRedshiftConnector:
    """Test suite for RedshiftConnector class."""

    def test_redshift_connector_init_valid_config(self):
        """Test RedshiftConnector initialization with valid config."""
        config = {
            "host": "test-cluster.region.redshift.amazonaws.com",
            "port": "5439",
            "database": "test_db",
            "user": "test_user",
            "password": "test_password",
        }
        
        connector = RedshiftConnector(config)
        
        assert connector.config == config
        assert connector._conn is None
        assert connector._cursor is None

    def test_redshift_connector_missing_required_params(self):
        """Test RedshiftConnector with missing required parameters."""
        config = {
            "host": "test-cluster.region.redshift.amazonaws.com",
            # Missing port, database, user, password
        }
        
        with pytest.raises(ValueError, match="Missing required configuration parameters"):
            RedshiftConnector(config)

    @patch('src.python.src.connectors.redshift.psycopg2.connect')
    def test_redshift_connector_connect_success(self, mock_connect):
        """Test successful Redshift connection."""
        config = {
            "host": "test-cluster.region.redshift.amazonaws.com",
            "port": "5439",
            "database": "test_db",
            "user": "test_user", 
            "password": "test_password",
        }
        
        # Mock connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn
        
        connector = RedshiftConnector(config)
        connector.connect()
        
        # Verify connection was established
        assert connector._conn == mock_conn
        assert connector._cursor == mock_cursor
        
        # Verify connection parameters
        mock_connect.assert_called_once()
        call_args = mock_connect.call_args[1]
        assert call_args["host"] == "test-cluster.region.redshift.amazonaws.com"
        assert call_args["port"] == 5439  # Should be converted to int
        assert call_args["dbname"] == "test_db"


@pytest.mark.unit
class TestBigQueryConnector:
    """Test suite for BigQueryConnector class."""

    def test_bigquery_connector_init_valid_config(self):
        """Test BigQueryConnector initialization with valid config."""
        config = {
            "project_id": "test-project-123",
            "dataset": "test_dataset", 
            "key_file": "/path/to/key.json",
        }
        
        connector = BigQueryConnector(config)
        
        assert connector.config == config
        assert connector._client is None

    def test_bigquery_connector_missing_required_params(self):
        """Test BigQueryConnector with missing required parameters."""
        config = {
            # Missing project_id and authentication
        }
        
        with pytest.raises(ValueError, match="Missing required configuration parameters"):
            BigQueryConnector(config)

    def test_bigquery_connector_missing_auth(self):
        """Test BigQueryConnector with missing authentication."""
        config = {
            "project_id": "test-project-123",
            # Missing key_file or key
        }
        
        with pytest.raises(ValueError, match="Either 'key_file' or 'key' must be provided"):
            BigQueryConnector(config)

    @patch('src.python.src.connectors.bigquery.bigquery.Client')
    @patch('src.python.src.connectors.bigquery.service_account.Credentials.from_service_account_file')
    def test_bigquery_connector_connect_with_key_file(self, mock_creds, mock_client):
        """Test BigQuery connection with key file."""
        config = {
            "project_id": "test-project-123",
            "dataset": "test_dataset",
            "key_file": "/path/to/key.json",
        }
        
        mock_client_instance = MagicMock()
        mock_client.return_value = mock_client_instance
        mock_client_instance.list_datasets.return_value = []
        
        connector = BigQueryConnector(config)
        connector.connect()
        
        # Verify credentials were loaded from file
        mock_creds.assert_called_once_with("/path/to/key.json")
        
        # Verify client was created
        mock_client.assert_called_once()
        assert connector._client == mock_client_instance

    @patch('src.python.src.connectors.bigquery.bigquery.Client')
    @patch('src.python.src.connectors.bigquery.service_account.Credentials.from_service_account_info')
    def test_bigquery_connector_connect_with_key_dict(self, mock_creds, mock_client):
        """Test BigQuery connection with key dictionary."""
        key_data = {"type": "service_account", "project_id": "test-project"}
        config = {
            "project_id": "test-project-123",
            "dataset": "test_dataset",
            "key": key_data,
        }
        
        mock_client_instance = MagicMock()
        mock_client.return_value = mock_client_instance
        mock_client_instance.list_datasets.return_value = []
        
        connector = BigQueryConnector(config)
        connector.connect()
        
        # Verify credentials were loaded from dict
        mock_creds.assert_called_once_with(key_data)
        
        # Verify client was created
        assert connector._client == mock_client_instance

    def test_bigquery_connector_get_param_type(self):
        """Test BigQuery parameter type mapping."""
        config = {
            "project_id": "test-project-123",
            "key_file": "/path/to/key.json",
        }
        
        connector = BigQueryConnector(config)
        
        assert connector._get_param_type("string_value") == "STRING"
        assert connector._get_param_type(123) == "INT64"
        assert connector._get_param_type(12.34) == "FLOAT64"
        assert connector._get_param_type(True) == "BOOL"
        assert connector._get_param_type({}) == "RECORD"
        assert connector._get_param_type([]) == "ARRAY"
        assert connector._get_param_type(None) == "STRING"  # Default