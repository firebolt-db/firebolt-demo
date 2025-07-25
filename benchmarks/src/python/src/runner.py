"""Database Benchmark Runner Module.

This module provides the core benchmarking functionality for running
performance tests across different database vendors. It handles query
execution, connection pooling, warmup procedures, and result collection.
"""

import csv
import itertools
import json
import logging
import os
import random
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from queue import Queue
from typing import Any, Dict, List, Optional

try:
    # Try relative imports first (when used as module)
    from . import connectors
    from . import exporters
    from .env_config import load_environment_config, validate_vendor_credentials
except ImportError:
    # Fall back to absolute imports (when run directly)
    import connectors
    import exporters
    from env_config import load_environment_config, validate_vendor_credentials

# Constants
DEFAULT_ITERATIONS_PER_QUERY = 1

logger = logging.getLogger(__name__)


@dataclass
class QueryResult:
    """Results from executing a single query."""

    query_number: int
    execution_time: float
    concurrent_run: int
    success: bool
    vendor: Optional[str] = None
    query_name: Optional[str] = None
    error: Optional[str] = None


@dataclass
class ConcurrentQueryResult:
    """Results from concurrent query execution for stress testing."""

    query_name: str
    query_id: int
    has_error: bool
    num_output_rows: int
    start_unix_time: float
    stop_unix_time: float


class ConnectionPool:
    """Thread-safe connection pool for database connectors."""

    def __init__(self, connector: Any, credentials: Dict[str, Any], pool_size: int = 5):
        """Initialize the connection pool.

        Args:
            connector: Database connector class
            credentials: Database credentials dictionary
            pool_size: Maximum number of connections in pool
        """
        self.connector = connector
        self.credentials = credentials
        self.pool_size = pool_size
        self.connections = Queue(maxsize=pool_size)
        self._lock = threading.Lock()
        self._fill_pool()

    def _fill_pool(self) -> None:
        """Fill the connection pool with initialized connections."""
        for _ in range(self.pool_size):
            connector_instance = self.connector.__class__(config=self.credentials)
            connector_instance.connect()
            self.connections.put(connector_instance)

    def get_connection(self) -> Any:
        """Get a connection from the pool.

        Returns:
            Database connector instance
        """
        return self.connections.get()

    def return_connection(self, connector: Any) -> None:
        """Return a connection to the pool.

        Args:
            connector: Database connector instance to return
        """
        self.connections.put(connector)

    def close_all(self) -> None:
        """Close all connections in the pool."""
        while not self.connections.empty():
            connector = self.connections.get()
            connector.close()


class BenchmarkRunner:
    """Main benchmark runner for database performance testing."""

    def __init__(
        self,
        benchmark_name: str,
        creds_file: Optional[str] = None,
        vendors: Optional[List[str]] = None,
        pool_size: int = DEFAULT_ITERATIONS_PER_QUERY,
        concurrency: int = 1,
        output_dir: str = "benchmark_results",
        execute_setup: bool = False,
        benchmark_path: str = "",
        results_queue: Optional[Queue] = None,
        run_warmup: bool = True,
        warmup_status_callback: Optional[callable] = None,
    ):
        """Initialize the benchmark runner.

        Args:
            benchmark_name: Name of the benchmark suite to run
            creds_file: Path to credentials file (deprecated, use environment vars)
            vendors: List of database vendors to test
            pool_size: Number of query iterations per benchmark
            concurrency: Number of concurrent threads
            output_dir: Directory for output files
            execute_setup: Whether to run setup scripts before benchmarking
            benchmark_path: Path to benchmark SQL files
            results_queue: Optional queue for real-time result streaming
            run_warmup: Whether to run warmup scripts
            warmup_status_callback: Callback for warmup status updates
        """
        self.benchmark_name = benchmark_name
        self.vendors = vendors or []
        self.concurrency = concurrency
        self.pool_size = max(pool_size, concurrency)  # Ensure sufficient connections
        self.output_dir = output_dir
        self.execute_setup = execute_setup
        self.benchmark_path = benchmark_path
        self.connection_pools: Dict[str, ConnectionPool] = {}
        self.results_queue = results_queue
        self.run_warmup = run_warmup
        self.warmup_status_callback = warmup_status_callback

        self.logger = logging.getLogger(f"{__name__}.{benchmark_name}")

        # Load credentials
        self._load_credentials(creds_file)

        # Initialize connectors
        self._initialize_connectors()

    def _load_credentials(self, creds_file: Optional[str]) -> None:
        """Load database credentials from file or environment.

        Args:
            creds_file: Optional path to JSON credentials file (legacy support)
        """
        if creds_file and os.path.exists(creds_file) and creds_file.endswith(".json"):
            # Legacy JSON loading
            with open(creds_file, "r", encoding="utf-8") as f:
                self.credentials = json.load(f)
            self.logger.info("Loaded credentials from JSON file")
        else:
            # Environment variable loading
            self.credentials = load_environment_config()
            self.logger.info("Loaded credentials from environment variables")

    def _initialize_connectors(self) -> None:
        """Initialize database connectors for all vendors."""
        self.connectors = {}

        for vendor in self.vendors:
            if vendor not in self.credentials:
                available_vendors = list(self.credentials.keys())
                raise ValueError(
                    f"No credentials found for vendor: {vendor}. "
                    f"Available vendors: {available_vendors}"
                )

            # Validate credentials
            validate_vendor_credentials(vendor, self.credentials[vendor])

            # Initialize connector
            connector_class = connectors.get_connector_class(vendor)
            self.connectors[vendor] = connector_class(config=self.credentials[vendor])

            self.logger.info(f"Initialized {vendor} connector")

    def _load_queries(self, query_file: str) -> List[str]:
        """Load SQL queries from a file.

        Args:
            query_file: Path to SQL file containing queries

        Returns:
            List of SQL query strings
        """
        if isinstance(query_file, (str, bytes, os.PathLike)):
            with open(query_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
                queries = []
                current_query = []

                for line in lines:
                    line = line.strip()
                    if not line:
                        continue

                    # Remove inline comments
                    line = line.split("--")[0].strip()
                    if not line:
                        continue

                    # Check for query terminator
                    if line.endswith(";"):
                        current_query.append(line[:-1])  # Remove semicolon
                        queries.append(" ".join(current_query).strip())
                        current_query = []
                    else:
                        current_query.append(line)

                # Handle remaining query without semicolon
                if current_query:
                    queries.append(" ".join(current_query).strip())

                return queries

        elif isinstance(query_file, list):
            return query_file
        else:
            raise TypeError("query_file must be a file path or list of queries")

    def _get_sql_file(self, vendor: str, file_type: str) -> Path:
        """Get the SQL file path for a vendor and file type.

        Args:
            vendor: Database vendor name
            file_type: Type of SQL file (benchmark, setup, warmup)

        Returns:
            Path to the SQL file
        """
        # Try vendor-specific file first
        vendor_file = Path(self.benchmark_path) / vendor / f"{file_type}.sql"
        if vendor_file.exists():
            return vendor_file

        # Fall back to general file
        general_file = Path(self.benchmark_path) / f"{file_type}.sql"
        return general_file

    def _run_query(
        self, vendor: str, query_name: str, query: str, concurrent_run: int, iteration: int = 1, total_iterations: int = 1
    ) -> Dict[str, Any]:
        """Execute a single query and return its results.

        Args:
            vendor: Database vendor name
            query_name: Name/identifier for the query
            query: SQL query string
            concurrent_run: Concurrent run identifier

        Returns:
            Dictionary containing query results
        """
        start_time = time.time()
        connection = None

        try:
            connection = self.connection_pools[vendor].get_connection()
            results = connection.execute_query(query)
            duration = time.time() - start_time

            result = {
                "vendor": vendor,
                "query_name": query_name,
                "query": query,
                "duration": duration,
                "rows": len(results) if results else 0,
                "status": "success",
                "timestamp": datetime.now().isoformat(),
                "concurrent_run": concurrent_run,
                "iteration": iteration,
                "total_iterations": total_iterations,
            }

            # Only send to results queue if it's the final iteration (for UI display)
            if self.results_queue and iteration == total_iterations:
                self.results_queue.put(result)

            return result

        except Exception as e:
            duration = time.time() - start_time
            self.logger.error(f"Query failed for {vendor} ({query_name}): {e}")

            error_result = {
                "vendor": vendor,
                "query_name": query_name,
                "query": query,
                "duration": duration,
                "rows": 0,
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "concurrent_run": concurrent_run,
                "iteration": iteration,
                "total_iterations": total_iterations,
            }

            # Only send to results queue if it's the final iteration (for UI display)
            if self.results_queue and iteration == total_iterations:
                self.results_queue.put(error_result)

            return error_result

        finally:
            if connection:
                self.connection_pools[vendor].return_connection(connection)

    def _run_concurrent_query(
        self, vendor: str, query: str, query_number: int, iteration: int = 1, total_iterations: int = 1
    ) -> List[QueryResult]:
        """Run a query with configured concurrency level.

        Args:
            vendor: Database vendor name
            query: SQL query string
            query_number: Query number identifier

        Returns:
            List of QueryResult objects
        """
        results = []

        with ThreadPoolExecutor(max_workers=self.concurrency) as executor:
            future_to_query = {
                executor.submit(self._run_query, vendor, str(query_number), query, i + 1, iteration, total_iterations): query
                for i in range(self.concurrency)
            }

            for future in as_completed(future_to_query):
                try:
                    result = future.result()
                    results.append(
                        QueryResult(
                            query_number=query_number,
                            execution_time=result["duration"],
                            success=result["status"] == "success",
                            error=result.get("error"),
                            vendor=result["vendor"],
                            query_name=result["query_name"],
                            concurrent_run=result["concurrent_run"],
                        )
                    )
                except Exception as e:
                    self.logger.error(f"Error in concurrent execution: {e}")
                    results.append(
                        QueryResult(
                            query_number=query_number,
                            execution_time=0.0,
                            success=False,
                            error=str(e),
                            vendor=vendor,
                            query_name=str(query_number),
                            concurrent_run=0,
                        )
                    )

        return results

    def _execute_setup_script(self, vendor: str) -> bool:
        """Execute setup SQL script for a vendor.

        Args:
            vendor: Database vendor name

        Returns:
            True if setup succeeded, False otherwise
        """
        try:
            setup_file = self._get_sql_file(vendor, "setup")
            if not setup_file.exists():
                self.logger.info(f"No setup file found for {vendor}")
                return True

            setup_queries = self._load_queries(str(setup_file))
            if not setup_queries:
                self.logger.info(f"No setup queries found for {vendor}")
                return True

            self.logger.info(f"Executing setup script for {vendor}: {setup_file}")

            for query in setup_queries:
                self.connectors[vendor].execute_query(query)

            self.logger.info(f"Setup completed for {vendor}")
            return True

        except Exception as e:
            self.logger.error(f"Setup failed for {vendor}: {e}")
            return False

    def _execute_warmup_script(self, vendor: str) -> bool:
        """Execute warmup SQL script for a vendor.

        Args:
            vendor: Database vendor name

        Returns:
            True if warmup succeeded, False otherwise
        """
        if not self.run_warmup:
            return True

        try:
            warmup_file = self._get_sql_file(vendor, "warmup")
            if not warmup_file.exists():
                self.logger.info(f"No warmup file found for {vendor}")
                return True

            warmup_queries = self._load_queries(str(warmup_file))
            if not warmup_queries:
                self.logger.info(f"No warmup queries found for {vendor}")
                return True

            self.logger.info(f"Starting warmup for {vendor}")

            total = len(warmup_queries)
            for idx, query in enumerate(warmup_queries):
                if self.warmup_status_callback:
                    msg = f"Warming up database ({vendor}): Step {idx+1} of {total}"
                    self.warmup_status_callback(msg)

                try:
                    self.connectors[vendor].execute_query(query)
                except Exception as query_error:
                    self.logger.warning(
                        f"Warmup query {idx+1} failed for {vendor}: {query_error}"
                    )
                    # Continue with remaining warmup queries

            if self.warmup_status_callback:
                self.warmup_status_callback(None)

            self.logger.info(f"Warmup completed for {vendor}")
            return True

        except Exception as e:
            self.logger.error(f"Warmup failed for {vendor}: {e}")
            if self.warmup_status_callback:
                self.warmup_status_callback(None)
            return False

    def run_benchmark(self) -> Dict[str, List[Dict[str, Any]]]:
        """Run the complete benchmark suite.

        Returns:
            Dictionary mapping vendor names to their benchmark results
        """
        results = {}
        # Use pool_size as the number of iterations for each query
        num_iterations = self.pool_size if self.concurrency == 1 else 1

        def run_vendor_benchmark(vendor: str) -> tuple[str, List[Dict[str, Any]]]:
            """Run benchmark for a single vendor.

            Args:
                vendor: Database vendor name

            Returns:
                Tuple of (vendor_name, results_list)
            """
            if vendor not in self.connectors:
                self.logger.warning(f"Skipping {vendor} - connector not implemented")
                return vendor, []

            self.logger.info(f"Running benchmark for {vendor}")

            # Execute setup script if requested
            if self.execute_setup and not self._execute_setup_script(vendor):
                self.logger.warning(f"Skipping {vendor} benchmark due to setup failure")
                return vendor, []

            # Execute warmup script
            if not self._execute_warmup_script(vendor):
                self.logger.warning(f"Skipping {vendor} benchmark due to warmup failure")
                return vendor, []

            vendor_results = []

            try:
                # Create connection pool
                self.connection_pools[vendor] = ConnectionPool(
                    self.connectors[vendor], self.credentials[vendor], self.pool_size
                )

                # Load benchmark queries
                benchmark_file = self._get_sql_file(vendor, "benchmark")
                if not benchmark_file.exists():
                    raise ValueError(f"No benchmark file found for {vendor}")

                benchmark_queries = self._load_queries(str(benchmark_file))
                if not benchmark_queries:
                    raise ValueError(f"No benchmark queries found for {vendor}")

                self.logger.info(f"Loaded {len(benchmark_queries)} queries for {vendor}")

                # Run benchmark queries
                for query_number, query in enumerate(benchmark_queries, 1):
                    last_iteration_results = []
                    for iteration in range(num_iterations):
                        self.logger.debug(
                            f"Running query {query_number}, iteration {iteration + 1}"
                        )
                        query_results = self._run_concurrent_query(
                            vendor, query, query_number, iteration + 1, num_iterations
                        )
                        # Only keep the last iteration for visualization
                        if iteration == num_iterations - 1:
                            last_iteration_results.extend(query_results)
                        vendor_results.extend(query_results)

                # Convert to CSV-exportable format
                csv_data = [
                    {
                        "vendor": result.vendor,
                        "query_name": result.query_name,
                        "execution_time": result.execution_time,
                        "concurrent_run": result.concurrent_run,
                        "success": result.success,
                        "error": result.error,
                    }
                    for result in vendor_results
                ]

                return vendor, csv_data

            except Exception as e:
                self.logger.error(f"Benchmark failed for {vendor}: {e}")
                return vendor, []

            finally:
                # Cleanup
                if vendor in self.connection_pools:
                    self.connection_pools[vendor].close_all()
                if vendor in self.connectors:
                    self.connectors[vendor].close()

        # Run all vendors in parallel
        with ThreadPoolExecutor(max_workers=len(self.vendors)) as executor:
            future_to_vendor = {
                executor.submit(run_vendor_benchmark, vendor): vendor
                for vendor in self.vendors
            }

            for future in as_completed(future_to_vendor):
                vendor, csv_data = future.result()
                if csv_data:
                    results[vendor] = csv_data

        # Export results
        if results:
            self._export_results(results)
        else:
            self.logger.warning("No results were generated from the benchmark")

        return results

    def _export_results(self, results: Dict[str, List[Dict[str, Any]]]) -> None:
        """Export benchmark results to files.

        Args:
            results: Dictionary mapping vendor names to their results
        """
        try:
            # Ensure output directory exists
            os.makedirs(self.output_dir, exist_ok=True)

            # Export CSV results
            csv_exporter = exporters.CSVExporter()
            csv_exporter.export(results, self.output_dir)

            # Export visual results
            visual_exporter = exporters.VisualExporter(self.output_dir)
            visual_exporter.export(results, self.output_dir)

            self.logger.info(f"Results exported to {self.output_dir}")

        except Exception as e:
            self.logger.error(f"Failed to export results: {e}")


class ConcurrentBenchmarkRunner:
    """Benchmark runner for high-concurrency stress testing."""

    def __init__(
        self,
        benchmark_name: str,
        creds_file: str,
        vendor: str,
        concurrency: int,
        benchmark_duration_secs: int,
        output_dir: str,
        benchmark_path: str,
        seed: int,
    ):
        """Initialize concurrent benchmark runner.

        Args:
            benchmark_name: Name of benchmark suite
            creds_file: Path to credentials file
            vendor: Single vendor to test
            concurrency: Number of concurrent threads
            benchmark_duration_secs: Duration to run benchmark
            output_dir: Output directory for results
            benchmark_path: Path to benchmark files
            seed: Random seed for reproducibility
        """
        self.benchmark_name = benchmark_name
        self.vendor = vendor
        self.concurrency = concurrency
        self.benchmark_duration_secs = benchmark_duration_secs
        self.output_dir = output_dir
        self.benchmark_path = benchmark_path
        self.seed = seed

        self.logger = logging.getLogger(f"{__name__}.concurrent")
        self.connector_class = connectors.get_connector_class(vendor)

        # Load credentials
        self._load_credentials(creds_file)

        # Load queries
        self._load_queries()

    def _load_credentials(self, creds_file: str) -> None:
        """Load credentials for the vendor."""
        if creds_file and os.path.exists(creds_file) and creds_file.endswith(".json"):
            with open(creds_file, "r", encoding="utf-8") as f:
                all_credentials = json.load(f)
                if self.vendor not in all_credentials:
                    raise ValueError(f"No credentials found for vendor: {self.vendor}")
                self.credentials = all_credentials[self.vendor]
        else:
            all_credentials = load_environment_config()
            if self.vendor not in all_credentials:
                available = list(all_credentials.keys())
                raise ValueError(
                    f"No credentials found for vendor: {self.vendor}. "
                    f"Available vendors: {available}"
                )
            validate_vendor_credentials(self.vendor, all_credentials[self.vendor])
            self.credentials = all_credentials[self.vendor]

    def _load_queries(self) -> None:
        """Load queries from JSON file."""
        general_file = Path(self.benchmark_path) / "queries.json"
        vendor_file = Path(self.benchmark_path) / self.vendor / "queries.json"
        queries_file = vendor_file if vendor_file.exists() else general_file

        with open(queries_file, "r", encoding="utf-8") as f:
            self.queries = json.load(f)

        if not self.queries:
            raise ValueError(f"No benchmark queries found for vendor: {self.vendor}")

        self.query_names = list(self.queries.keys())
        self.logger.info(f"Loaded {len(self.query_names)} queries for {self.vendor}")

    def _run_worker(self, worker_id: int, seed: int) -> None:
        """Worker thread function for concurrent execution.

        Args:
            worker_id: Unique identifier for this worker
            seed: Random seed for this worker
        """
        rng = random.Random(seed)
        query_names_shuffled = rng.sample(self.query_names, len(self.query_names))

        connector = self.connector_class(config=self.credentials)
        connector.connect()
        results = []

        # Wait for all workers to be ready
        self.start_barrier.wait()

        query_id = 0

        # Run queries until stopped
        for query_name in itertools.cycle(query_names_shuffled):
            if self.stop_event.is_set():
                self.worker_thread_results[worker_id] = results
                connector.close()
                return

            random_query_variation = rng.choice(self.queries[query_name])

            try:
                start_time = time.time()
                query_results = connector.execute_query(random_query_variation)
                stop_time = time.time()
                has_error = False
                num_output_rows = len(query_results) if query_results else 0

            except Exception as e:
                has_error = True
                start_time = stop_time = time.time()
                num_output_rows = 0
                self.logger.error(f"Query {query_name} failed for {self.vendor}: {e}")

            if not self.stop_event.is_set():
                results.append(
                    ConcurrentQueryResult(
                        query_name=query_name,
                        query_id=query_id,
                        has_error=has_error,
                        num_output_rows=num_output_rows,
                        start_unix_time=start_time,
                        stop_unix_time=stop_time,
                    )
                )
                query_id += 1

    def _write_csv(self) -> None:
        """Write concurrent benchmark results to CSV file."""
        os.makedirs(self.output_dir, exist_ok=True)
        csv_file_path = os.path.join(self.output_dir, f"{self.vendor}_concurrency.csv")

        with open(csv_file_path, mode="w", newline="", encoding="utf-8") as csv_file:
            field_names = [
                "worker_id",
                "query_name", 
                "query_id",
                "has_error",
                "num_output_rows",
                "start_unix_time",
                "stop_unix_time",
            ]
            writer = csv.DictWriter(csv_file, fieldnames=field_names)
            writer.writeheader()

            for worker_id, worker_results in enumerate(self.worker_thread_results):
                if not worker_results:
                    self.logger.warning(f"No results found for worker {worker_id}")

                for result in worker_results:
                    row = {
                        "worker_id": worker_id,
                        "query_name": result.query_name,
                        "query_id": result.query_id,
                        "has_error": result.has_error,
                        "num_output_rows": result.num_output_rows,
                        "start_unix_time": result.start_unix_time,
                        "stop_unix_time": result.stop_unix_time,
                    }
                    writer.writerow(row)

        self.logger.info(f"Concurrency results exported to {csv_file_path}")

    def run_benchmark(self) -> None:
        """Run the concurrent benchmark."""
        self.logger.info(f"Running concurrency benchmark for {self.vendor}")

        self.start_barrier = threading.Barrier(self.concurrency)
        self.stop_event = threading.Event()
        self.worker_thread_results = [[] for _ in range(self.concurrency)]

        # Generate random seeds for workers
        rng = random.Random(self.seed)
        random_seeds = rng.sample(range(42_000_000), self.concurrency)

        # Start worker threads
        threads = []
        for i in range(self.concurrency):
            thread = threading.Thread(target=self._run_worker, args=(i, random_seeds[i]))
            threads.append(thread)
            thread.start()

        # Let workers run for specified duration
        time.sleep(self.benchmark_duration_secs)
        self.stop_event.set()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        # Export results
        self._write_csv()
        self.logger.info(f"Finished concurrency benchmark for {self.vendor}")