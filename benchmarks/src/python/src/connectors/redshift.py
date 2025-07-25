"""Amazon Redshift Database Connector.

This module provides a connector for Amazon Redshift data warehouse, handling
authentication, connection management, and query execution using psycopg2.
"""

import logging
from typing import Any, Dict, List, Optional

import psycopg2
import psycopg2.extras

from .base import WarehouseConnector

logger = logging.getLogger(__name__)


class RedshiftConnector(WarehouseConnector):
    """Connector for Amazon Redshift data warehouse."""

    def __init__(self, config: Dict[str, Any]):
        """Initialize Redshift connector with configuration parameters.

        Args:
            config: Configuration dictionary containing:
                - host: Redshift cluster endpoint
                - port: Port number (usually 5439)
                - database: Database name
                - user: Username for authentication
                - password: Password for authentication

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
        required_params = ["host", "port", "database", "user", "password"]
        missing_params = [param for param in required_params if param not in self.config]
        if missing_params:
            raise ValueError(f"Missing required configuration parameters: {missing_params}")

    def connect(self) -> None:
        """Establish connection to Redshift database.

        Raises:
            Exception: If connection fails
        """
        if self._conn:
            return  # Already connected

        try:
            logger.info(f"Connecting to Redshift cluster: {self.config['host']}")

            # Build connection parameters
            conn_params = {
                "host": self.config["host"],
                "port": int(self.config["port"]),
                "dbname": self.config["database"],
                "user": self.config["user"],
                "password": self.config["password"],
                "connect_timeout": 30,  # 30 second timeout
                "application_name": "database-benchmark-suite",
            }

            # Establish connection
            self._conn = psycopg2.connect(**conn_params)
            self._cursor = self._conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            # Configure for benchmarking - disable caching for accurate timing
            try:
                self._cursor.execute("SET enable_result_cache_for_session TO off")
                self._conn.commit()
                logger.debug("Disabled result cache for accurate benchmarking")
            except Exception as e:
                logger.warning(f"Could not disable result cache: {e}")

            # Test connection
            self._cursor.execute("SELECT 1 AS connection_test")
            logger.info("Redshift connection established successfully")

        except Exception as e:
            logger.error(f"Redshift connection failed: {e}")
            raise Exception(f"Redshift connection failed: {e}") from e

    def execute_query(self, query: str, parameters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Execute a SQL query on Redshift.

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
            logger.debug(f"Executing Redshift query: {query[:200]}...")

            if parameters:
                self._cursor.execute(query, parameters)
            else:
                self._cursor.execute(query)

            if self._cursor.description:
                results = self._cursor.fetchall()
                # Convert RealDictRow objects to regular dictionaries
                results_list = [dict(row) for row in results]
                logger.debug(f"Query returned {len(results_list)} rows")
                return results_list
            else:
                logger.debug("Query completed (no results returned)")
                return []

        except Exception as e:
            logger.error(f"Redshift query failed: {e}")
            # Rollback transaction on error
            if self._conn:
                try:
                    self._conn.rollback()
                except Exception:
                    pass
            raise Exception(f"Error executing Redshift query: {e}") from e

    def close(self) -> None:
        """Close the Redshift connection if it exists."""
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
                logger.debug("Redshift connection closed")
            except Exception as e:
                logger.warning(f"Error closing connection: {e}")
            finally:
                self._conn = None