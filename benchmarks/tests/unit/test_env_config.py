"""Unit tests for environment configuration module."""

import os
from unittest.mock import patch

import pytest

from src.python.src.env_config import get_app_config, load_environment_config, validate_vendor_credentials


@pytest.mark.unit
class TestEnvironmentConfig:
    """Test suite for environment configuration functions."""

    def test_load_environment_config_success(self):
        """Test successful loading of environment configuration."""
        config = load_environment_config()
        
        # Should load all vendors that have environment variables set
        assert isinstance(config, dict)
        assert "firebolt" in config
        assert "snowflake" in config
        assert "redshift" in config
        assert "google" in config

    def test_load_environment_config_firebolt_structure(self):
        """Test Firebolt configuration structure."""
        config = load_environment_config()
        firebolt_config = config["firebolt"]
        
        assert "account_name" in firebolt_config
        assert "database" in firebolt_config
        assert "engine_name" in firebolt_config
        assert "auth" in firebolt_config
        assert "id" in firebolt_config["auth"]
        assert "secret" in firebolt_config["auth"]

    def test_load_environment_config_snowflake_structure(self):
        """Test Snowflake configuration structure.""" 
        config = load_environment_config()
        snowflake_config = config["snowflake"]
        
        assert "account" in snowflake_config
        assert "user" in snowflake_config
        assert "password" in snowflake_config
        assert "database" in snowflake_config
        assert "schema" in snowflake_config
        assert "warehouse" in snowflake_config

    def test_load_environment_config_redshift_structure(self):
        """Test Redshift configuration structure."""
        config = load_environment_config()
        redshift_config = config["redshift"]
        
        assert "host" in redshift_config
        assert "port" in redshift_config
        assert "database" in redshift_config
        assert "user" in redshift_config
        assert "password" in redshift_config

    def test_load_environment_config_bigquery_structure(self):
        """Test BigQuery configuration structure."""
        config = load_environment_config()
        bigquery_config = config["google"]
        
        assert "project_id" in bigquery_config
        assert "dataset" in bigquery_config
        assert "key_file" in bigquery_config

    def test_get_app_config_success(self):
        """Test successful loading of application configuration."""
        config = get_app_config()
        
        assert isinstance(config, dict)
        assert "default_output_dir" in config
        assert "default_pool_size" in config
        assert "default_concurrency" in config
        
        # Check types
        assert isinstance(config["default_pool_size"], int)
        assert isinstance(config["default_concurrency"], int)

    def test_get_app_config_defaults(self, monkeypatch):
        """Test application configuration with default values."""
        # Remove environment variables to test defaults
        monkeypatch.delenv("DEFAULT_OUTPUT_DIR", raising=False)
        monkeypatch.delenv("DEFAULT_POOL_SIZE", raising=False)
        monkeypatch.delenv("DEFAULT_CONCURRENCY", raising=False)
        
        config = get_app_config()
        
        assert config["default_output_dir"] == "benchmark_results"
        assert config["default_pool_size"] == 5
        assert config["default_concurrency"] == 1

    def test_validate_vendor_credentials_firebolt_valid(self):
        """Test validation of valid Firebolt credentials."""
        credentials = {
            "account_name": "test_account",
            "database": "test_db", 
            "engine_name": "test_engine",
            "auth": {
                "id": "test_id",
                "secret": "test_secret",
            },
        }
        
        # Should not raise any exception
        validate_vendor_credentials("firebolt", credentials)

    def test_validate_vendor_credentials_firebolt_missing_fields(self):
        """Test validation of Firebolt credentials with missing fields."""
        credentials = {
            "account_name": "test_account",
            "database": "test_db",
            # Missing engine_name and auth
        }
        
        with pytest.raises(ValueError, match="Missing required fields"):
            validate_vendor_credentials("firebolt", credentials)

    def test_validate_vendor_credentials_snowflake_valid(self):
        """Test validation of valid Snowflake credentials."""
        credentials = {
            "account": "test_account",
            "user": "test_user",
            "password": "test_password",
            "database": "test_db",
            "schema": "test_schema",
            "warehouse": "test_warehouse",
        }
        
        # Should not raise any exception
        validate_vendor_credentials("snowflake", credentials)

    def test_validate_vendor_credentials_redshift_valid(self):
        """Test validation of valid Redshift credentials."""
        credentials = {
            "host": "test-cluster.region.redshift.amazonaws.com",
            "port": "5439",
            "database": "test_db", 
            "user": "test_user",
            "password": "test_password",
        }
        
        # Should not raise any exception
        validate_vendor_credentials("redshift", credentials)

    def test_validate_vendor_credentials_bigquery_valid(self):
        """Test validation of valid BigQuery credentials."""
        credentials = {
            "project_id": "test-project-123",
            "dataset": "test_dataset",
            "key_file": "/path/to/key.json",
        }
        
        # Should not raise any exception
        validate_vendor_credentials("google", credentials)

    def test_validate_vendor_credentials_unknown_vendor(self):
        """Test validation with unknown vendor."""
        with pytest.raises(ValueError, match="Unknown vendor"):
            validate_vendor_credentials("unknown_vendor", {})

    def test_validate_vendor_credentials_empty_credentials(self):
        """Test validation with empty credentials."""
        with pytest.raises(ValueError, match="Missing required fields"):
            validate_vendor_credentials("firebolt", {})