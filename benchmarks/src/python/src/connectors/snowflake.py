"""Snowflake Database Connector.

This module provides a connector for Snowflake data warehouse, handling
authentication, connection management, and query execution.
"""

import logging
from typing import Any, Dict, List, Optional

import snowflake.connector

from .base import WarehouseConnector

logger = logging.getLogger(__name__)


class SnowflakeConnector(WarehouseConnector):
    """Connector for Snowflake data warehouse."""

    def __init__(self, config: Dict[str, Any]):
        """Initialize Snowflake connector with configuration parameters.

        Args:
            config: Configuration dictionary containing:
                - account: Snowflake account identifier
                - user: Username for authentication
                - password: Password for authentication
                - warehouse: Optional warehouse name
                - database: Optional database name
                - schema: Optional schema name

        Raises:
            ValueError: If required configuration parameters are missing
        """
        self.config = config
        self._validate_config()
        self._conn = None
        self._cursor = None

    def _validate_config(self) -> None:
        """Validate that required configuration parameters are present.

        Raises:
            ValueError: If required parameters are missing
        """
        required_params = ["account", "user", "password"]
        missing_params = [param for param in required_params if param not in self.config]
        if missing_params:
            raise ValueError(f"Missing required configuration parameters: {missing_params}")

    def connect(self) -> None:
        """Establish connection to Snowflake database.

        Raises:
            Exception: If connection fails
        """
        if self._conn:
            return  # Already connected

        try:
            logger.info(f"Connecting to Snowflake account: {self.config['account']}")

            # Build connection parameters
            conn_params = {
                "account": self.config["account"],
                "user": self.config["user"],
                "password": self.config["password"],
                "telemetry": False,  # Disable telemetry for benchmarking
            }

            # Add optional parameters if provided
            optional_params = ["warehouse", "database", "schema"]
            for param in optional_params:
                if param in self.config and self.config[param]:
                    conn_params[param] = self.config[param]

            # Establish connection
            self._conn = snowflake.connector.connect(**conn_params)
            self._cursor = self._conn.cursor(snowflake.connector.DictCursor)

            # Configure for benchmarking - disable caching for accurate timing
            try:
                self._cursor.execute("ALTER SESSION SET USE_CACHED_RESULT = FALSE")
                logger.debug("Disabled result cache for accurate benchmarking")
            except Exception as e:
                logger.warning(f"Could not disable result cache: {e}")

            # Test connection
            self._cursor.execute("SELECT 1 AS connection_test")
            logger.info("Snowflake connection established successfully")

        except Exception as e:
            logger.error(f"Snowflake connection failed: {e}")
            raise Exception(f"Snowflake connection failed: {e}") from e

    def execute_query(self, query: str, parameters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Execute a SQL query on Snowflake.

        Args:
            query: SQL query string to execute
            parameters: Optional query parameters for parameterized queries

        Returns:
            List of dictionaries containing query results

        Raises:
            Exception: If query execution fails
        """
        if not self._conn or not self._cursor:
            self.connect()

        try:
            logger.debug(f"Executing Snowflake query: {query[:200]}...")

            if parameters:
                self._cursor.execute(query, parameters)
            else:
                self._cursor.execute(query)

            if self._cursor.description:
                results = self._cursor.fetchall()
                logger.debug(f"Query returned {len(results)} rows")
                return results
            else:
                logger.debug("Query completed (no results returned)")
                return []

        except Exception as e:
            logger.error(f"Snowflake query failed: {e}")
            raise Exception(f"Error executing Snowflake query: {e}") from e

    def cleanup(self) -> None:
        """Perform cleanup operations before closing connection."""
        if self._cursor and self.config.get("warehouse"):
            try:
                warehouse = self.config["warehouse"]
                self._cursor.execute(f"ALTER WAREHOUSE {warehouse} SUSPEND")
                logger.info(f"Suspended Snowflake warehouse: {warehouse}")
            except Exception as e:
                logger.warning(f"Error suspending warehouse: {e}")

    def close(self) -> None:
        """Close the Snowflake connection if it exists."""
        # Perform cleanup before closing
        self.cleanup()
        
        if self._cursor:
            try:
                self._cursor.close()
            except Exception as e:
                logger.warning(f"Error closing cursor: {e}")
            finally:
                self._cursor = None

        if self._conn:
            try:
                self._conn.close()
                logger.debug("Snowflake connection closed")
            except Exception as e:
                logger.warning(f"Error closing connection: {e}")
            finally:
                self._conn = None