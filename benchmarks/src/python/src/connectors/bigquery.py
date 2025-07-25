"""Google BigQuery Database Connector.

This module provides a connector for Google BigQuery data warehouse, handling
authentication, connection management, and query execution using the
Google Cloud Client Library.
"""

import json
import logging
from typing import Any, Dict, List, Optional

from google.cloud import bigquery
from google.oauth2 import service_account

from .base import WarehouseConnector

logger = logging.getLogger(__name__)


class BigQueryConnector(WarehouseConnector):
    """Connector for Google BigQuery data warehouse."""

    def __init__(self, config: Dict[str, Any]):
        """Initialize BigQuery connector with configuration parameters.

        Args:
            config: Configuration dictionary containing:
                - project_id: Google Cloud project ID
                - dataset: Optional default dataset name
                - key_file: Path to service account JSON key file, OR
                - key: Dictionary with service account key data
                - location: Optional location/region

        Raises:
            ValueError: If required configuration parameters are missing
        """
        self.config = config
        self._validate_config()
        self._client = None

    def _validate_config(self) -> None:
        """Validate that required configuration parameters are present.

        Raises:
            ValueError: If required parameters are missing
        """
        required_params = ["project_id"]
        missing_params = [param for param in required_params if param not in self.config]
        if missing_params:
            raise ValueError(f"Missing required configuration parameters: {missing_params}")

        # Must have either key_file or key
        if not self.config.get("key_file") and not self.config.get("key"):
            raise ValueError("Either 'key_file' or 'key' must be provided for authentication")

    def connect(self) -> None:
        """Establish connection to BigQuery.

        Raises:
            Exception: If connection fails
        """
        if self._client:
            return  # Already connected

        try:
            logger.info(f"Connecting to BigQuery project: {self.config['project_id']}")

            # Load credentials
            credentials = self._load_credentials()

            # Set up default dataset if provided
            default_config = None
            if self.config.get("dataset"):
                project_id = self.config["project_id"]
                dataset_id = self.config["dataset"]
                default_dataset = f"{project_id}.{dataset_id}"
                default_config = bigquery.QueryJobConfig(default_dataset=default_dataset)

            # Create client
            self._client = bigquery.Client(
                project=self.config["project_id"],
                credentials=credentials,
                default_query_job_config=default_config,
                location=self.config.get("location"),
            )

            # Test connection
            datasets = list(self._client.list_datasets(max_results=1))
            logger.info("BigQuery connection established successfully")

        except Exception as e:
            logger.error(f"BigQuery connection failed: {e}")
            raise Exception(f"BigQuery connection failed: {e}") from e

    def _load_credentials(self) -> service_account.Credentials:
        """Load service account credentials from file or config.

        Returns:
            Google Cloud service account credentials

        Raises:
            Exception: If credentials cannot be loaded
        """
        try:
            if self.config.get("key_file"):
                # Load from file
                key_file = self.config["key_file"]
                logger.debug(f"Loading credentials from file: {key_file}")
                return service_account.Credentials.from_service_account_file(key_file)
            elif self.config.get("key"):
                # Load from dictionary
                key_data = self.config["key"]
                if isinstance(key_data, str):
                    # Parse JSON string
                    key_data = json.loads(key_data)
                logger.debug("Loading credentials from configuration")
                return service_account.Credentials.from_service_account_info(key_data)
            else:
                raise ValueError("No valid credentials configuration found")

        except Exception as e:
            raise Exception(f"Failed to load BigQuery credentials: {e}") from e

    def execute_query(
        self,
        query: str,
        parameters: Optional[Dict[str, Any]] = None,
        dry_run: bool = False,
    ) -> List[Dict[str, Any]]:
        """Execute a SQL query on BigQuery.

        Args:
            query: SQL query string to execute
            parameters: Optional query parameters for parameterized queries
            dry_run: If True, validates query but doesn't run it

        Returns:
            List of dictionaries containing query results

        Raises:
            Exception: If query execution fails
        """
        if not self._client:
            self.connect()

        try:
            logger.debug(f"Executing BigQuery query: {query[:200]}...")

            # Configure job
            job_config = bigquery.QueryJobConfig(
                use_query_cache=False,  # Disable cache for accurate benchmarking
                dry_run=dry_run,
            )

            # Add parameters if provided
            if parameters:
                job_config.query_parameters = [
                    bigquery.ScalarQueryParameter(k, self._get_param_type(v), v)
                    for k, v in parameters.items()
                ]

            # Execute query
            query_job = self._client.query(query, job_config=job_config)

            if dry_run:
                bytes_processed = query_job.total_bytes_processed
                logger.debug(f"Dry run: {bytes_processed} bytes would be processed")
                return [{"bytes_processed": bytes_processed}]

            # Get results
            results = [dict(row.items()) for row in query_job]
            logger.debug(f"Query returned {len(results)} rows")
            return results

        except Exception as e:
            logger.error(f"BigQuery query failed: {e}")
            raise Exception(f"Error executing BigQuery query: {e}") from e

    def _get_param_type(self, value: Any) -> str:
        """Map Python types to BigQuery parameter types.

        Args:
            value: Parameter value

        Returns:
            BigQuery parameter type string
        """
        type_map = {
            str: "STRING",
            int: "INT64",
            float: "FLOAT64",
            bool: "BOOL",
            dict: "RECORD",
            list: "ARRAY",
        }
        return type_map.get(type(value), "STRING")

    def close(self) -> None:
        """Close the BigQuery connection if it exists."""
        if self._client:
            try:
                self._client.close()
                logger.debug("BigQuery connection closed")
            except Exception as e:
                logger.warning(f"Error closing BigQuery connection: {e}")
            finally:
                self._client = None