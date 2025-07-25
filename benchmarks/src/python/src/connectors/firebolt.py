"""Firebolt Database Connector.

This module provides a connector for Firebolt data warehouse, handling
authentication, connection management, and query execution.
"""

import logging
from typing import Any, Dict, List, Optional

from firebolt.client.auth import ClientCredentials
from firebolt.db import connect

from .base import WarehouseConnector

logger = logging.getLogger(__name__)


class FireboltConnector(WarehouseConnector):
    """Connector for Firebolt data warehouse."""

    def __init__(self, config: Dict[str, Any]):
        """Initialize Firebolt connector with configuration parameters.

        Args:
            config: Configuration dictionary containing:
                - engine_name: Firebolt engine name
                - database: Database name
                - account_name: Account name
                - auth: Dictionary with 'id' and 'secret' keys for authentication

        Raises:
            ValueError: If required configuration parameters are missing
        """
        self.config = config
        self._validate_config()
        self._conn = None
        self.cursor = None

    def _validate_config(self) -> None:
        """Validate that required configuration parameters are present.

        Raises:
            ValueError: If required parameters are missing
        """
        required_params = ["engine_name", "database", "account_name", "auth"]
        missing_params = [param for param in required_params if param not in self.config]
        if missing_params:
            raise ValueError(f"Missing required configuration parameters: {missing_params}")

        # Validate auth structure
        auth = self.config.get("auth", {})
        if not isinstance(auth, dict) or not auth.get("id") or not auth.get("secret"):
            raise ValueError("auth must contain 'id' and 'secret' keys")

    def connect(self) -> None:
        """Establish connection to Firebolt database.

        Raises:
            Exception: If connection fails
        """
        if self._conn:
            return  # Already connected

        try:
            logger.info(f"Connecting to Firebolt engine: {self.config['engine_name']}")

            # Create connection with authentication
            self._conn = connect(
                engine_name=self.config["engine_name"],
                database=self.config["database"],
                account_name=self.config["account_name"],
                auth=ClientCredentials(
                    self.config["auth"]["id"], self.config["auth"]["secret"]
                ),
            )
            self.cursor = self._conn.cursor()

            # Configure for benchmarking - disable caching for accurate timing
            try:
                self.cursor.execute("SET enable_result_cache=false")
                logger.debug("Disabled result cache for accurate benchmarking")
            except Exception as e:
                logger.warning(f"Could not disable result cache: {e}")

            # Test connection
            self.cursor.execute("SELECT 1 AS connection_test")
            logger.info("Firebolt connection established successfully")

        except Exception as e:
            # Provide specific error context
            if "401" in str(e) or "Unauthorized" in str(e):
                raise Exception(
                    f"Firebolt authentication failed - check service credentials: {e}"
                ) from e
            elif "engine" in str(e).lower():
                engine_name = self.config.get("engine_name", "unknown")
                raise Exception(
                    f"Firebolt engine connection failed - check engine name '{engine_name}': {e}"
                ) from e
            else:
                raise Exception(f"Firebolt connection failed: {e}") from e

    def execute_query(self, query: str, parameters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Execute a SQL query on Firebolt.

        Args:
            query: SQL query string to execute
            parameters: Optional query parameters for parameterized queries

        Returns:
            List of dictionaries containing query results

        Raises:
            Exception: If query execution fails
        """
        if not self._conn or not self.cursor:
            self.connect()

        try:
            logger.debug(f"Executing Firebolt query: {query[:200]}...")

            if parameters:
                self.cursor.execute(query, parameters)
            else:
                self.cursor.execute(query)

            if self.cursor.description:
                results = self.cursor.fetchall()
                logger.debug(f"Query returned {len(results)} rows")
                return results
            else:
                logger.debug("Query completed (no results returned)")
                return []

        except Exception as e:
            error_msg = str(e).lower()
            logger.error(f"Firebolt query failed: {e}")

            # Handle specific error types
            if "timeout" in error_msg or "timed out" in error_msg:
                raise Exception(f"Query timed out: {e}") from e
            elif "connection" in error_msg or "disconnected" in error_msg:
                # Attempt reconnection and retry once
                logger.info("Connection lost, attempting to reconnect...")
                self._conn = None
                self.cursor = None
                self.connect()

                try:
                    if parameters:
                        self.cursor.execute(query, parameters)
                    else:
                        self.cursor.execute(query)

                    if self.cursor.description:
                        results = self.cursor.fetchall()
                        logger.info(f"Query succeeded after reconnect: {len(results)} rows")
                        return results
                    else:
                        logger.info("Query completed after reconnect (no results)")
                        return []

                except Exception as retry_e:
                    raise Exception(f"Query failed even after reconnect: {retry_e}") from retry_e
            else:
                raise Exception(f"Error executing query: {e}") from e

    def cleanup(self) -> None:
        """Perform cleanup operations before closing connection."""
        if self.cursor and self.config.get("engine_name"):
            try:
                engine_name = self.config["engine_name"]
                self.cursor.execute(f"STOP ENGINE {engine_name}")
                logger.info(f"Stopped Firebolt engine: {engine_name}")
            except Exception as e:
                logger.warning(f"Error stopping engine: {e}")

    def close(self) -> None:
        """Close the Firebolt connection if it exists."""
        # Perform cleanup before closing
        self.cleanup()
        
        if self.cursor:
            try:
                self.cursor.close()
            except Exception as e:
                logger.warning(f"Error closing cursor: {e}")
            finally:
                self.cursor = None

        if self._conn:
            try:
                self._conn.close()
                logger.debug("Firebolt connection closed")
            except Exception as e:
                logger.warning(f"Error closing connection: {e}")
            finally:
                self._conn = None