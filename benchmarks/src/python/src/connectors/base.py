"""Base connector class for database warehouse connections.

This module defines the abstract interface that all database connectors
must implement to ensure consistent behavior across different vendors.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class WarehouseConnector(ABC):
    """Abstract base class for database warehouse connectors."""

    @abstractmethod
    def connect(self) -> None:
        """Establish connection to the warehouse.
        
        Raises:
            Exception: If connection fails
        """
        pass

    @abstractmethod
    def execute_query(self, query: str, parameters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Execute a SQL query and return results.
        
        Args:
            query: SQL query string to execute
            parameters: Optional dictionary of query parameters
            
        Returns:
            List of dictionaries containing query results
            
        Raises:
            Exception: If query execution fails
        """
        pass

    @abstractmethod
    def close(self) -> None:
        """Close the database connection.
        
        Should be safe to call multiple times.
        """
        pass

    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
        return False