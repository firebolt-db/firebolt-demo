"""Database Benchmark Suite - Streamlit Application.

A comprehensive benchmarking platform for database performance comparison
across Snowflake, Redshift, Firebolt, and BigQuery.

This module provides the main Streamlit web interface for running benchmarks,
configuring database connections, and visualizing results.
"""

import logging
import queue
import threading
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

import altair as alt
import pandas as pd
import streamlit as st

try:
    # Try relative imports first (when used as module)
    from .env_config import get_app_config, load_environment_config
    from .runner import BenchmarkRunner
except ImportError:
    # Fall back to absolute imports (when run directly)
    from env_config import get_app_config, load_environment_config
    from runner import BenchmarkRunner

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# Constants
BENCHMARK_OPTIONS = ["FireScale", "FireScale_k6", "sample_benchmark", "tpch"]
VENDOR_OPTIONS = ["firebolt", "redshift", "snowflake", "google"]
VENDOR_COLORS = {
    "firebolt": "#F72A30",
    "redshift": "#FF9900", 
    "snowflake": "#29B5E8",
    "google": "#34A853",
}

# Streamlit page configuration
st.set_page_config(
    page_title="Database Benchmark Suite",
    layout="wide",
    initial_sidebar_state="expanded",
)


def initialize_session_state() -> None:
    """Initialize Streamlit session state variables."""
    session_defaults = {
        "seq_results_queue": queue.Queue(),
        "seq_results": [],
        "seq_running": False,
        "seq_error": None,
        "warmup_status": None,
        "manual_credentials": {},
        "seq_start_time": None,
        "seq_end_time": None,
        "active_runners": [],  # Track active runners for cleanup
        "current_benchmark": None,  # Track current benchmark
    }
    
    for key, default_value in session_defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value


def cleanup_active_connections() -> None:
    """Clean up any active database connections and runners."""
    try:
        # Clean up any active runners
        active_runners = st.session_state.get("active_runners", [])
        for runner in active_runners:
            try:
                if hasattr(runner, 'connectors'):
                    for vendor, connector in runner.connectors.items():
                        if hasattr(connector, 'cleanup'):
                            connector.cleanup()
                        if hasattr(connector, 'close'):
                            connector.close()
                if hasattr(runner, 'connection_pools'):
                    for vendor, pool in runner.connection_pools.items():
                        if hasattr(pool, 'close_all'):
                            pool.close_all()
            except Exception as e:
                logger.warning(f"Error during cleanup: {e}")
        
        # Clear the active runners list
        st.session_state["active_runners"] = []
        logger.info("Completed cleanup of active connections")
        
    except Exception as e:
        logger.error(f"Error during connection cleanup: {e}")


def reset_session() -> None:
    """Reset all session state variables."""
    # Clean up connections before reset
    cleanup_active_connections()
    
    keys_to_keep = {"manual_credentials"}  # Preserve user credentials
    for key in list(st.session_state.keys()):
        if key not in keys_to_keep:
            del st.session_state[key]
    initialize_session_state()
    # Don't call st.rerun() in callback - set a flag instead
    st.session_state["should_rerun"] = True


def create_credential_inputs(vendors: List[str]) -> Dict[str, Dict[str, str]]:
    """Create credential input forms for selected vendors.
    
    Args:
        vendors: List of vendor names to create inputs for
        
    Returns:
        Dictionary mapping vendor names to their credential dictionaries
    """
    manual_creds = {}
    
    for vendor in vendors:
        with st.sidebar.expander(f"🔧 {vendor.title()} Credentials"):
            if vendor == "firebolt":
                manual_creds[vendor] = {
                    "account_name": st.text_input(
                        "Account Name", key=f"{vendor}_account"
                    ),
                    "database": st.text_input("Database", key=f"{vendor}_db"),
                    "engine_name": st.text_input("Engine Name", key=f"{vendor}_engine"),
                    "service_id": st.text_input("Service ID", key=f"{vendor}_service_id"),
                    "service_secret": st.text_input(
                        "Service Secret", type="password", key=f"{vendor}_secret"
                    ),
                }
            elif vendor == "snowflake":
                manual_creds[vendor] = {
                    "account": st.text_input("Account", key=f"{vendor}_account"),
                    "user": st.text_input("User", key=f"{vendor}_user"),
                    "password": st.text_input(
                        "Password", type="password", key=f"{vendor}_password"
                    ),
                    "database": st.text_input("Database", key=f"{vendor}_database"),
                    "schema": st.text_input("Schema", key=f"{vendor}_schema"),
                    "warehouse": st.text_input("Warehouse", key=f"{vendor}_warehouse"),
                }
            elif vendor == "redshift":
                manual_creds[vendor] = {
                    "host": st.text_input("Host", key=f"{vendor}_host"),
                    "port": st.number_input("Port", value=5439, key=f"{vendor}_port"),
                    "database": st.text_input("Database", key=f"{vendor}_database"),
                    "user": st.text_input("User", key=f"{vendor}_user"),
                    "password": st.text_input(
                        "Password", type="password", key=f"{vendor}_password"
                    ),
                }
            elif vendor == "google":
                manual_creds[vendor] = {
                    "project_id": st.text_input("Project ID", key=f"{vendor}_project"),
                    "dataset": st.text_input("Dataset", key=f"{vendor}_dataset"),
                    "key_file": st.text_input("Key File Path", key=f"{vendor}_keyfile"),
                }
    
    return manual_creds


def get_effective_credentials(
    vendors: List[str], manual_credentials: Dict[str, Dict[str, str]]
) -> Dict[str, Dict[str, Any]]:
    """Get effective credentials by merging manual inputs with environment variables.
    
    Args:
        vendors: List of vendor names
        manual_credentials: Manual credential inputs from UI
        
    Returns:
        Dictionary mapping vendor names to their effective credentials
    """
    env_creds = load_environment_config()
    final_creds = {}
    
    for vendor in vendors:
        manual_vendor_creds = manual_credentials.get(vendor, {})
        # Use manual credentials if any field is filled, otherwise use env
        if any(str(v).strip() for v in manual_vendor_creds.values()):
            final_creds[vendor] = manual_vendor_creds
        else:
            final_creds[vendor] = env_creds.get(vendor, {})
    
    return final_creds


def test_database_connections(vendors: List[str]) -> None:
    """Test database connections for all selected vendors.
    
    Args:
        vendors: List of vendor names to test
    """
    st.markdown("### Connection Test Results")
    
    test_creds = get_effective_credentials(vendors, st.session_state.manual_credentials)
    
    for vendor in vendors:
        if vendor not in test_creds or not test_creds[vendor]:
            st.warning(f"⚠️ {vendor.title()}: No credentials provided")
            continue
            
        try:
            # Dynamic import to avoid loading all connectors
            if vendor == "firebolt":
                try:
                    from .connectors.firebolt import FireboltConnector
                except ImportError:
                    from connectors.firebolt import FireboltConnector
                connector = FireboltConnector(test_creds[vendor])
            elif vendor == "snowflake":
                try:
                    from .connectors.snowflake import SnowflakeConnector
                except ImportError:
                    from connectors.snowflake import SnowflakeConnector
                connector = SnowflakeConnector(test_creds[vendor])
            elif vendor == "redshift":
                try:
                    from .connectors.redshift import RedshiftConnector
                except ImportError:
                    from connectors.redshift import RedshiftConnector
                connector = RedshiftConnector(test_creds[vendor])
            elif vendor == "google":
                try:
                    from .connectors.bigquery import BigQueryConnector
                except ImportError:
                    from connectors.bigquery import BigQueryConnector
                connector = BigQueryConnector(test_creds[vendor])
            else:
                st.error(f"❌ {vendor.title()}: Unknown vendor")
                continue
            
            connector.connect()
            result = connector.execute_query("SELECT 1 AS test")
            
            # Clean up connection
            if hasattr(connector, "close"):
                connector.close()
            elif hasattr(connector, "close_connection"):
                connector.close_connection()
                
            st.success(f"✅ {vendor.title()}: Connection successful")
            
        except Exception as e:
            logger.error(f"Connection test failed for {vendor}: {e}")
            st.error(f"❌ {vendor.title()}: Connection failed - {str(e)}")


def run_benchmark_worker(
    results_queue: queue.Queue,
    vendors: List[str],
    benchmark_name: str,
    pool_size: int,
    output_dir: str,
    benchmark_path: Path,
    execute_setup: bool,
    run_warmup: bool,
    worker_id: int,
    manual_credentials: Optional[Dict[str, Dict[str, str]]] = None,
) -> None:
    """Worker function to run benchmarks in a separate thread.
    
    Args:
        results_queue: Queue for collecting benchmark results
        vendors: List of vendors to benchmark
        benchmark_name: Name of benchmark suite to run
        pool_size: Number of query iterations
        output_dir: Directory for output files
        benchmark_path: Path to benchmark SQL files
        execute_setup: Whether to run setup scripts
        run_warmup: Whether to run warmup scripts
        worker_id: Unique identifier for this worker
        manual_credentials: Optional manual credentials override
    """
    try:
        runner = BenchmarkRunner(
            benchmark_name=benchmark_name,
            creds_file=None,  # Use environment loading
            vendors=vendors,
            pool_size=pool_size,
            concurrency=1,
            output_dir=output_dir,
            benchmark_path=str(benchmark_path),
            execute_setup=execute_setup,
            results_queue=results_queue,
            run_warmup=run_warmup,
            warmup_status_callback=lambda msg: st.session_state.update(
                {"warmup_status": msg}
            ),
        )
        
        # Track this runner for cleanup
        if "active_runners" not in st.session_state:
            st.session_state["active_runners"] = []
        st.session_state["active_runners"].append(runner)
        
        # Override credentials if manual credentials provided
        if manual_credentials:
            try:
                try:
                    from . import connectors
                    from .env_config import validate_vendor_credentials
                except ImportError:
                    import connectors
                    from env_config import validate_vendor_credentials
                
                for vendor in vendors:
                    vendor_creds = manual_credentials.get(vendor, {})
                    if vendor_creds and any(str(v).strip() for v in vendor_creds.values()):
                        validate_vendor_credentials(vendor, vendor_creds)
                        connector_class = connectors.get_connector_class(vendor)
                        runner.connectors[vendor] = connector_class(config=vendor_creds)
                        runner.credentials[vendor] = vendor_creds
            except Exception as e:
                logger.error(f"Failed to override {vendor} credentials: {e}")
                
        runner.run_benchmark()
        logger.info(f"Worker {worker_id} completed successfully")
        
    except Exception as e:
        logger.error(f"Worker {worker_id} failed: {e}")
        results_queue.put({
            "vendor": "system",
            "query_name": f"worker_{worker_id}_error",
            "duration": 0,
            "rows": 0,
            "status": "error",
            "error": str(e),
            "timestamp": time.time(),
            "concurrent_run": worker_id,
        })


def create_performance_chart(data: pd.DataFrame, metric: str) -> alt.Chart:
    """Create a performance bar chart for vendors.
    
    Args:
        data: DataFrame with vendor performance data
        metric: Metric column name to chart
        
    Returns:
        Altair chart object
    """
    data_copy = data.copy()
    data_copy["color"] = data_copy["vendor"].map(VENDOR_COLORS).fillna("#888888")
    
    chart = (
        alt.Chart(data_copy)
        .mark_bar()
        .encode(
            y=alt.Y(
                "vendor:N",
                sort=None,
                title="Vendor",
                axis=alt.Axis(labelFontSize=14, ticks=True),
            ),
            x=alt.X(f"{metric}:Q", title=metric.capitalize()),
            color=alt.Color(
                "vendor:N",
                scale=alt.Scale(
                    domain=list(VENDOR_COLORS.keys()),
                    range=list(VENDOR_COLORS.values()),
                ),
                legend=None,
            ),
            tooltip=["vendor", metric],
        )
        .properties(height=120)
        .configure_axis(labelOverlap=False)
    )
    
    return chart


def display_benchmark_results(results: List[Dict[str, Any]]) -> None:
    """Display benchmark results with charts and tables.
    
    Args:
        results: List of benchmark result dictionaries
    """
    if not results:
        st.warning("No results to display.")
        return
    
    # Filter for successful results only for charts
    successful_results = [r for r in results if r.get("status") == "success"]
    
    if not successful_results:
        st.warning("No successful query results to display charts for.")
        return
        
    df = pd.DataFrame(successful_results)
    
    # Ensure data types for Arrow compatibility
    df["query_name"] = df["query_name"].astype(str)
    df["query_text"] = (
        df["query"].astype(str) if "query" in df.columns else df["query_name"].astype(str)
    )
    
    # Calculate vendor statistics
    vendor_stats = df.groupby("vendor")["duration"].agg(["max", "min", "mean", "sum"])
    vendor_stats = vendor_stats.rename(columns={"mean": "avg", "sum": "total"}).reset_index()
    
    # Display KPI charts
    st.markdown("### Performance Charts")
    kpi_cols = st.columns(4)
    metrics = ["max", "min", "avg", "total"]
    labels = ["Max Response Time (s)", "Min Response Time (s)", "Avg Response Time (s)", "Total Time (s)"]
    
    for col, metric, label in zip(kpi_cols, metrics, labels):
        with col:
            st.markdown(f"**{label}**")
            chart = create_performance_chart(vendor_stats, metric)
            st.altair_chart(chart, use_container_width=True)
    
    # Add query numbers for charts
    df["query_number"] = df.groupby("vendor")["query_name"].transform(
        lambda x: pd.factorize(x)[0] + 1
    )
    
    # Create line chart for query performance over time
    st.markdown("#### Query Duration by Vendor")
    avg_df = df.groupby(["vendor", "query_number", "query_name"], as_index=False)["duration"].mean()
    
    line_chart = (
        alt.Chart(avg_df)
        .mark_line(point=True)
        .encode(
            x=alt.X("query_number:O", title="Query Number"),
            y=alt.Y("duration:Q", title="Avg Duration (s)"),
            color=alt.Color(
                "vendor:N",
                scale=alt.Scale(
                    domain=list(VENDOR_COLORS.keys()),
                    range=list(VENDOR_COLORS.values()),
                ),
                legend=alt.Legend(title="Vendor"),
            ),
            tooltip=["vendor", "query_name", "duration", "query_number"],
        )
        .properties(height=300)
    )
    
    st.altair_chart(line_chart, use_container_width=True)
    
    # Display results table
    def truncate_query(q: str, length: int = 60) -> str:
        return q if len(q) <= length else q[:length] + "..."
    
    df["query_text_trunc"] = df["query_text"].apply(truncate_query)
    
    # Ensure proper data types
    df["vendor"] = df["vendor"].astype(str)
    df["status"] = df["status"].astype(str)
    df["query_number"] = df["query_number"].astype("Int64")
    df["duration"] = pd.to_numeric(df["duration"], errors="coerce")
    df["rows"] = pd.to_numeric(df["rows"], errors="coerce")
    
    # Include iteration information in the table if available
    table_cols = ["vendor", "query_number", "duration", "rows", "status"]
    if "iteration" in df.columns:
        table_cols.append("iteration")
    if "total_iterations" in df.columns:
        table_cols.append("total_iterations")
    table_cols.append("query_text_trunc")
    
    table_display = df[table_cols].rename(columns={"query_text_trunc": "Query Text"})
    st.markdown("### Detailed Results Table")
    st.dataframe(table_display, use_container_width=True)


def main() -> None:
    """Main application entry point."""
    # Initialize session state
    initialize_session_state()
    
    # Register cleanup function for session termination
    import atexit
    atexit.register(cleanup_active_connections)
    
    # Main title and description
    st.title("🚀 Database Benchmark Suite")
    st.markdown("""
    **Compare performance across Snowflake, Redshift, Firebolt, and BigQuery**
    
    Run comprehensive benchmarks to evaluate query performance, concurrency handling,
    and scalability across leading data warehouse platforms.
    """)
    st.divider()
    
    # Load application configuration
    try:
        app_config = get_app_config()
    except Exception as e:
        st.error(f"Failed to load application configuration: {e}")
        st.stop()
    
    # Sidebar configuration
    st.sidebar.markdown("## Configuration")
    benchmark_name = st.sidebar.selectbox(
        "Select Benchmark", BENCHMARK_OPTIONS, index=0
    )
    
    # Check if benchmark has changed and cleanup if necessary
    if st.session_state.get("current_benchmark") != benchmark_name:
        if st.session_state.get("current_benchmark") is not None:
            # Benchmark has changed, cleanup previous connections
            cleanup_active_connections()
            # Reset running state
            st.session_state["seq_running"] = False
            st.session_state["seq_results"] = []
            st.session_state["seq_error"] = None
        st.session_state["current_benchmark"] = benchmark_name
    vendors = st.sidebar.multiselect(
        "Vendors", VENDOR_OPTIONS, default=["firebolt"]
    )
    output_dir = st.sidebar.text_input(
        "Output Directory", value=app_config["default_output_dir"]
    )
    execute_setup = st.sidebar.checkbox("Execute Setup Before Benchmark", value=False)
    run_warmup = st.sidebar.checkbox("Run Warmup Scripts", value=True)
    
    # Performance settings
    st.sidebar.markdown("## Performance Settings")
    pool_size = st.sidebar.number_input(
        "Query Set Runs",
        min_value=1,
        value=app_config["default_pool_size"],
        step=1,
    )
    concurrency = st.sidebar.number_input(
        "Concurrent Queries",
        min_value=1,
        value=app_config["default_concurrency"],
        step=1,
    )
    
    # Vendor recommendations
    with st.sidebar.expander("📋 Vendor Recommendations"):
        st.markdown("""
        **Concurrent Queries:**
        - **Firebolt**: 1-10 (optimized for concurrency)
        - **Snowflake**: 1-10 (scales with warehouse size)
        - **Redshift**: 1-5 (depends on cluster configuration)
        - **BigQuery**: 1-20 (designed for high concurrency)
        
        **Query Set Runs:**
        - **Performance Testing**: 1-3 runs for quick analysis
        - **Load Testing**: 5-10 runs for stability testing
        - **Benchmarking**: 3-5 runs for reliable averages
        """)
    
    # Credentials section
    st.sidebar.markdown("## Database Credentials")
    manual_creds = create_credential_inputs(vendors)
    st.session_state.manual_credentials = manual_creds
    
    # Main action buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        run_benchmark_btn = st.button("Run Benchmark", type="primary")
    with col2:
        test_connections_btn = st.button("Test Connections")
    with col3:
        reset_btn = st.button("Reset")
    
    # Handle reset functionality
    if reset_btn or st.session_state.get("should_rerun", False):
        reset_session()
        if st.session_state.get("should_rerun", False):
            st.session_state["should_rerun"] = False
        st.rerun()
    
    # Handle connection testing
    if test_connections_btn:
        test_database_connections(vendors)
    
    # Handle benchmark execution
    if run_benchmark_btn:
        if not vendors:
            st.error("Please select at least one vendor to benchmark.")
            return
            
        st.session_state["seq_running"] = True
        st.session_state["seq_results"].clear()
        st.session_state["seq_error"] = None
        st.session_state["seq_results_queue"] = queue.Queue()
        st.session_state["seq_start_time"] = time.time()
        st.session_state["seq_end_time"] = None
        st.session_state["warmup_status"] = None
        
        # Get project root and benchmark path
        current_file = Path(__file__).absolute()
        project_root = current_file.parent.parent.parent.parent
        benchmark_path = project_root / "benchmarks" / benchmark_name
        
        if not benchmark_path.exists():
            st.error(f"Benchmark path does not exist: {benchmark_path}")
            return
        
        # Get effective credentials
        benchmark_creds = get_effective_credentials(vendors, st.session_state.manual_credentials)
        
        # Start benchmark workers
        for i in range(concurrency):
            thread = threading.Thread(
                target=run_benchmark_worker,
                args=(
                    st.session_state["seq_results_queue"],
                    vendors,
                    benchmark_name,
                    pool_size,
                    output_dir,
                    benchmark_path,
                    execute_setup,
                    run_warmup,
                    i,
                    benchmark_creds,
                ),
                daemon=True,
            )
            thread.start()
    
    # Display progress and results
    results_queue = st.session_state.get("seq_results_queue")
    if results_queue:
        while not results_queue.empty():
            st.session_state["seq_results"].append(results_queue.get())
    
    results = st.session_state.get("seq_results", [])
    
    # Calculate per-vendor progress
    queries_per_vendor = 25  # Assuming 25 queries per benchmark
    # Since we only get final iteration results in the queue, the total is just queries_per_vendor
    total_queries_per_vendor = queries_per_vendor * concurrency
    overall_total = total_queries_per_vendor * len(vendors)
    
    # Group results by vendor
    vendor_results = {}
    for result in results:
        vendor = result.get("vendor", "unknown")
        if vendor not in vendor_results:
            vendor_results[vendor] = []
        vendor_results[vendor].append(result)
    
    # Check if benchmark is complete
    completed_queries = len(results)
    if st.session_state.get("seq_running") and completed_queries >= overall_total:
        st.session_state["seq_running"] = False
        st.session_state["seq_end_time"] = time.time()
        st.session_state["warmup_status"] = None
        # Cleanup connections when benchmark completes
        cleanup_active_connections()
    
    # Display per-vendor progress bars
    if st.session_state.get("seq_running") or results:
        st.markdown("### Progress by Vendor")
        
        for vendor in vendors:
            vendor_completed = len(vendor_results.get(vendor, []))
            vendor_progress = min(1.0, vendor_completed / total_queries_per_vendor) if total_queries_per_vendor else 0
            vendor_status = (
                f"Running... {vendor_completed}/{total_queries_per_vendor} queries"
                if st.session_state.get("seq_running") and vendor_completed < total_queries_per_vendor
                else f"Complete: {vendor_completed}/{total_queries_per_vendor} queries"
            )
            
            st.markdown(f"**{vendor.title()}**")
            st.progress(vendor_progress, text=vendor_status)
    
    # Display warmup status
    if st.session_state.get("warmup_status"):
        st.info(st.session_state["warmup_status"])
    
    # Display total runtime
    if st.session_state.get("seq_start_time"):
        if st.session_state.get("seq_end_time"):
            total_time = st.session_state["seq_end_time"] - st.session_state["seq_start_time"]
        else:
            total_time = time.time() - st.session_state["seq_start_time"]
        st.markdown(f"### Total Run Time: {total_time:.2f} seconds")
    
    # Display results only when benchmark is complete or when there are meaningful results
    if results and (not st.session_state.get("seq_running") or len(results) > 5):
        st.markdown("### Live Benchmark")
        
        display_benchmark_results(results)
    
    # Display errors
    if st.session_state.get("seq_error"):
        st.error(st.session_state["seq_error"])
    
    # Auto-refresh while running
    if st.session_state.get("seq_running"):
        time.sleep(1)
        st.rerun()


if __name__ == "__main__":
    main()