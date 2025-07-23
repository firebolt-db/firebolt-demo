#!/usr/bin/env python3
"""
Firebolt Core NYC Parking Violations Demo App

This Streamlit app demonstrates the power of Firebolt Core with:
- Real-time query execution and timing
- Interactive visualizations
- Performance analysis and explanations
"""

import json
import logging
import subprocess
import time
from datetime import datetime

import pandas as pd
import plotly.express as px
import streamlit as st

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Firebolt Core NYC Demo",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
)


class FireboltConnector:
    """Handles connection and queries to Firebolt Core."""

    def __init__(self):
        self.container_name = "firebolt-core"
        self._check_docker_setup()

    def _check_docker_setup(self):
        """Check if Docker and Firebolt Core container are available."""
        try:
            # Check if Docker is available
            result = subprocess.run(
                ["docker", "--version"], check=False, capture_output=True, text=True
            )
            if result.returncode != 0:
                logger.error("Docker is not available or not running")
                return False

            # Check if container exists
            result = subprocess.run(
                [
                    "docker",
                    "ps",
                    "-a",
                    "--filter",
                    f"name={self.container_name}",
                    "--format",
                    "{{.Names}}",
                ],
                check=False, capture_output=True,
                text=True,
            )

            if self.container_name not in result.stdout:
                logger.error(f"Container '{self.container_name}' not found")
                return False

            # Check if container is running
            result = subprocess.run(
                [
                    "docker",
                    "ps",
                    "--filter",
                    f"name={self.container_name}",
                    "--format",
                    "{{.Names}}",
                ],
                check=False, capture_output=True,
                text=True,
            )

            if self.container_name not in result.stdout:
                logger.warning(
                    f"Container '{self.container_name}' exists but is not running"
                )
                return False

            return True

        except Exception as e:
            logger.error(f"Docker setup check failed: {e}")
            return False

    def execute_query(
        self, query: str, timeout: int = 60
    ) -> tuple[pd.DataFrame, float, bool]:
        """
        Execute a query and return results with timing.
        Returns: (dataframe, execution_time_seconds, success)
        """
        start_time = time.time()

        try:
            # Use docker exec to run fb with Firebolt Core settings
            cmd = [
                "docker",
                "exec",
                self.container_name,
                "fb",
                "-C",
                "-c",
                query,
                "-f",
                "JSONLines_Compact",
            ]

            result = subprocess.run(
                cmd, check=False, capture_output=True, text=True, timeout=timeout
            )

            execution_time = time.time() - start_time

            if result.returncode == 0:
                # Parse JSON output
                if result.stdout.strip():
                    df = self._parse_jsonlines_output(result.stdout)
                    # Fallback: if JSON parse yielded empty DF, retry with CSV format
                    if df.empty:
                        csv_cmd = [
                            "docker",
                            "exec",
                            self.container_name,
                            "fb",
                            "-C",
                            "-c",
                            query,
                            "-f",
                            "CSV",
                        ]
                        csv_result = subprocess.run(
                            csv_cmd, check=False, capture_output=True, text=True, timeout=timeout
                        )
                        if csv_result.returncode == 0 and csv_result.stdout.strip():
                            import io

                            try:
                                df = pd.read_csv(io.StringIO(csv_result.stdout))
                            except Exception:
                                df = pd.DataFrame()
                    return df, execution_time, True
                return pd.DataFrame(), execution_time, True
            error_msg = result.stderr.strip() if result.stderr else "Unknown error"
            logger.error(f"Query failed: {error_msg}")
            return pd.DataFrame(), execution_time, False

        except subprocess.TimeoutExpired:
            logger.error(f"Query timed out after {timeout} seconds")
            return pd.DataFrame(), timeout, False
        except FileNotFoundError:
            logger.error("Docker command not found. Is Docker installed and in PATH?")
            execution_time = time.time() - start_time
            return pd.DataFrame(), execution_time, False
        except Exception as e:
            logger.error(f"Query execution error: {e}")
            execution_time = time.time() - start_time
            return pd.DataFrame(), execution_time, False

    def _parse_jsonlines_output(self, output: str) -> pd.DataFrame:
        """Parse JSONLines output from Firebolt Core into a pandas DataFrame."""
        import re

        # Clean output by removing terminal control characters and progress indicators
        cleaned_output = re.sub(r"[^\x20-\x7E\n\r\t]", "", output)

        # Split output into lines and rejoin JSON objects that may be split across lines
        lines = cleaned_output.strip().split("\n")

        # Filter and reconstruct JSON lines
        json_lines = []
        current_json = ""

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Skip timing and metadata lines
            if line.startswith("Time:") or line.startswith("Request Id:"):
                continue

            # Check if this looks like JSON
            if line.startswith("{"):
                # Start of a new JSON object
                if current_json:
                    json_lines.append(current_json)
                current_json = line
            else:
                # Continuation of current JSON object
                current_json += line

            # Check if we have a complete JSON object
            if current_json and current_json.endswith("}"):
                json_lines.append(current_json)
                current_json = ""

        # Add any remaining JSON
        if current_json:
            json_lines.append(current_json)

        columns = []
        data_rows = []

        for json_line in json_lines:
            try:
                msg = json.loads(json_line)

                if msg.get("message_type") == "START":
                    # Extract column names from START message
                    result_columns = msg.get("result_columns", [])
                    columns = [col["name"] for col in result_columns]

                elif msg.get("message_type") == "DATA":
                    # Extract data rows from DATA message
                    data = msg.get("data", [])
                    data_rows.extend(data)

            except json.JSONDecodeError:
                # Skip invalid JSON
                continue

        # Create DataFrame
        if columns and data_rows:
            df = pd.DataFrame(data_rows)
            df.columns = columns
            return df
        return pd.DataFrame()

    def test_connection(self) -> bool:
        """Test if Firebolt Core is accessible."""
        _, _, success = self.execute_query("SELECT 1 as test", timeout=10)
        return success

    def get_diagnostics(self) -> str:
        """Get diagnostic information for troubleshooting."""
        diagnostics = []

        try:
            # Check Docker status
            result = subprocess.run(
                ["docker", "--version"], check=False, capture_output=True, text=True
            )
            if result.returncode == 0:
                diagnostics.append(f"✅ Docker: {result.stdout.strip()}")
            else:
                diagnostics.append("❌ Docker: Not available")

            # Check container status
            result = subprocess.run(
                [
                    "docker",
                    "ps",
                    "-a",
                    "--filter",
                    f"name={self.container_name}",
                    "--format",
                    "table {{.Names}}\t{{.Status}}\t{{.Ports}}",
                ],
                check=False, capture_output=True,
                text=True,
            )

            if result.stdout.strip():
                diagnostics.append(f"📋 Container Status:\n{result.stdout}")
            else:
                diagnostics.append(f"❌ Container '{self.container_name}' not found")

            # Check container logs (last 10 lines)
            result = subprocess.run(
                ["docker", "logs", "--tail", "10", self.container_name],
                check=False, capture_output=True,
                text=True,
            )

            if result.returncode == 0:
                diagnostics.append(f"📄 Recent logs:\n{result.stdout}")
            else:
                diagnostics.append("❌ Cannot access container logs")

        except Exception as e:
            diagnostics.append(f"❌ Diagnostic error: {e}")

        return "\n\n".join(diagnostics)


# Initialize Firebolt connector
@st.cache_resource
def get_firebolt_connector():
    return FireboltConnector()


# Cache filter data for performance
@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_filter_data(_connector: FireboltConnector) -> dict:
    """Get all filter data in one go and cache it. Returns distinct streets, fine amounts, and vehicle makes without artificial limits."""

    filter_data = {"streets": [], "amounts": [], "cars": []}

    # Get streets – use index on street_name; no LIMIT so we fetch all distinct values
    try:
        query = (
            "SELECT DISTINCT street_name FROM violations "
            "WHERE street_name IS NOT NULL AND street_name != '' "
            "ORDER BY street_name"
        )
        df, exec_time, success = _connector.execute_query(query)
        if success and not df.empty:
            filter_data["streets"] = df["street_name"].tolist()
            logger.info(
                f"✅ Streets loaded: {len(filter_data['streets'])} items in {exec_time * 1000:.1f}ms"
            )
        else:
            logger.warning(
                f"⚠️  Street query failed or returned empty results. Success: {success}"
            )
    except Exception as e:
        logger.error(f"Error fetching streets: {e}")

    # Get amounts – fetch entire distinct list for slider range
    try:
        query = (
            "SELECT DISTINCT calculated_fine_amount FROM violations "
            "WHERE calculated_fine_amount IS NOT NULL AND calculated_fine_amount > 0 "
            "ORDER BY calculated_fine_amount"
        )
        df, exec_time, success = _connector.execute_query(query)
        if success and not df.empty:
            filter_data["amounts"] = df["calculated_fine_amount"].tolist()
            logger.info(
                f"✅ Amounts loaded: {len(filter_data['amounts'])} items in {exec_time * 1000:.1f}ms"
            )
        else:
            logger.warning(
                f"⚠️  Amount query failed or returned empty results. Success: {success}"
            )
    except Exception as e:
        logger.error(f"Error fetching amounts: {e}")

    # Get cars – remove occurrence threshold so all makes appear
    try:
        query = (
            "SELECT DISTINCT vehicle_make FROM violations "
            "WHERE vehicle_make IS NOT NULL AND LENGTH(vehicle_make) >= 2 AND vehicle_make != '' "
            "ORDER BY vehicle_make"
        )
        df, exec_time, success = _connector.execute_query(query)
        if success and not df.empty:
            filter_data["cars"] = df["vehicle_make"].tolist()
            logger.info(
                f"✅ Vehicle makes loaded: {len(filter_data['cars'])} items in {exec_time * 1000:.1f}ms"
            )
        else:
            logger.warning(
                f"⚠️  Vehicle make query failed or returned empty results. Success: {success}"
            )
    except Exception as e:
        logger.error(f"Error fetching cars: {e}")

    return filter_data


# ------------------------------- CACHE WARM-UP --------------------------------
# Cache warm-up will happen in main() to ensure proper timing
# ------------------------------------------------------------------------------


def get_available_streets(connector: FireboltConnector) -> list[str]:
    """Get list of available street names from the database."""
    filter_data = get_filter_data(connector)
    return filter_data.get("streets", [])


def get_available_amounts(connector: FireboltConnector) -> list[float]:
    """Get list of available fine amounts from the database."""
    filter_data = get_filter_data(connector)
    return filter_data.get("amounts", [])


def get_available_cars(connector: FireboltConnector) -> list[str]:
    """Get list of available vehicle makes from the database."""
    filter_data = get_filter_data(connector)
    return filter_data.get("cars", [])


@st.cache_data(ttl=60)  # Cache for 1 minute
def get_sample_data(_connector: FireboltConnector) -> tuple:
    """Get sample data for the data browser."""
    df, exec_time, success = _connector.execute_query(
        "SELECT summons_number, plate_id, registration_state, issue_date, vehicle_make, street_name, calculated_fine_amount FROM violations ORDER BY issue_date DESC LIMIT 100"
    )
    return df, exec_time, success


def show_data_browser(connector: FireboltConnector):
    """Display the current data in the violations table."""
    try:
        df, exec_time, success = get_sample_data(connector)

        if success and not df.empty:
            st.dataframe(df, use_container_width=True)

            # Show statistics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Violations", "21,563,502")
            with col2:
                st.metric("Unique Streets", int(df["street_name"].nunique()))
            with col3:
                st.metric(
                    "Average Fine", f"${float(df['calculated_fine_amount'].mean()):.2f}"
                )

            st.caption(
                f"Query executed in {exec_time * 1000:.1f}ms (showing latest 100 records)"
            )
        else:
            st.info("No data found in the violations table")
    except Exception as e:
        st.error(f"Error loading data: {e}")


# Benchmark queries - updated for violations table with filter support
BENCHMARK_QUERIES = {
    "Q1": {
        "name": "Total violations & fines summary",
        "description": "Overall statistics from the NYC dataset",
        "sql": """
            SELECT
                COUNT(*) as total_violations,
                SUM(calculated_fine_amount) as total_fines,
                AVG(calculated_fine_amount) as avg_fine,
                MIN(calculated_fine_amount) as min_fine,
                MAX(calculated_fine_amount) as max_fine
            FROM violations
            WHERE calculated_fine_amount > 0
                {street_filter}
                {amount_filter}
                {car_filter}
        """,
    },
    "Q2": {
        "name": "Revenue by street",
        "description": "Top 10 streets by revenue",
        "sql": """
            SELECT
                street_name,
                COUNT(*) as total_violations,
                SUM(calculated_fine_amount) as total_revenue,
                AVG(calculated_fine_amount) as avg_fine
            FROM violations
            WHERE street_name IS NOT NULL
                AND street_name != ''
                AND calculated_fine_amount > 0
                {street_filter}
                {amount_filter}
                {car_filter}
            GROUP BY street_name
            ORDER BY total_revenue DESC
            LIMIT 10
        """,
    },
    "Q3": {
        "name": "Vehicle make analysis",
        "description": "Violations by vehicle make",
        "sql": """
            SELECT
                vehicle_make,
                COUNT(*) as violations,
                AVG(calculated_fine_amount) as avg_fine,
                SUM(calculated_fine_amount) as total_fines
            FROM violations
            WHERE vehicle_make IS NOT NULL
                AND calculated_fine_amount > 0
                {street_filter}
                {amount_filter}
                {car_filter}
            GROUP BY vehicle_make
            ORDER BY violations DESC
            LIMIT 10
        """,
    },
    "Q4": {
        "name": "Yearly trend analysis",
        "description": "Violations by year",
        "sql": """
            SELECT
                EXTRACT(YEAR FROM issue_date) as year,
                COUNT(*) as violation_count,
                SUM(calculated_fine_amount) as total_revenue,
                AVG(calculated_fine_amount) as avg_fine
            FROM violations
            WHERE issue_date IS NOT NULL
                AND calculated_fine_amount > 0
                AND EXTRACT(YEAR FROM issue_date) BETWEEN 2010 AND 2024
                {street_filter}
                {amount_filter}
                {car_filter}
            GROUP BY EXTRACT(YEAR FROM issue_date)
            ORDER BY year
        """,
    },
    "Q5": {
        "name": "Interactive data filtering",
        "description": "Filter violations by street name, fine amount, and vehicle make",
        "sql": """
            SELECT
                summons_number,
                street_name,
                calculated_fine_amount,
                issue_date,
                vehicle_make,
                CASE
                    WHEN calculated_fine_amount > 100 THEN 'High Fine'
                    WHEN calculated_fine_amount > 50 THEN 'Medium Fine'
                    ELSE 'Low Fine'
                END as fine_category
            FROM violations
            WHERE calculated_fine_amount > 0
                {street_filter}
                {amount_filter}
                {car_filter}
            ORDER BY calculated_fine_amount DESC
            LIMIT 100
        """,
    },
}

# Sample query templates for the custom query feature
SAMPLE_QUERIES = [
    "SELECT COUNT(*) as total_violations FROM violations",
    "SELECT street_name, COUNT(*) as violations FROM violations GROUP BY street_name ORDER BY violations DESC LIMIT 10",
    "SELECT vehicle_make, AVG(calculated_fine_amount) as avg_fine FROM violations GROUP BY vehicle_make ORDER BY avg_fine DESC LIMIT 10",
    "SELECT EXTRACT(YEAR FROM issue_date) as year, COUNT(*) as violations FROM violations GROUP BY EXTRACT(YEAR FROM issue_date) ORDER BY year",
    "SELECT registration_state, COUNT(*) as violations FROM violations GROUP BY registration_state ORDER BY violations DESC LIMIT 10",
]


def main():
    """Main Streamlit app."""

    # App header
    st.title("🚗 Firebolt Core NYC Parking Demo")
    st.markdown("""
    **Explore 21.5+ million NYC parking violations with sub-second analytics!**

    This demo showcases Firebolt Core's high-performance query engine with sample NYC parking violation data loaded from S3.
    The dataset contains sample parking violation records for demonstration purposes.
    """)

    # Initialize session state
    if "running" not in st.session_state:
        st.session_state.running = False
    if "query_results" not in st.session_state:
        st.session_state.query_results = {}
    if "latest_query" not in st.session_state:
        st.session_state.latest_query = None
    if "query_execution_order" not in st.session_state:
        st.session_state.query_execution_order = []

    # Connection status
    connector = get_firebolt_connector()

    if connector.test_connection():
        st.sidebar.success("✅ Connected to Firebolt Core")

        # Ensure cache is warmed up on first connection
        if "cache_warmed" not in st.session_state:
            with st.spinner("Initializing filters..."):
                # Pre-warm the cache to ensure fast filter loading
                get_filter_data(connector)
                st.session_state.cache_warmed = True

        # The cache now self-invalidates via TTL so the manual refresh button is no longer needed.

        # Sidebar filters (only show if connected)
        st.sidebar.header("🎛️ Query Filters")

        # Get available data for filters (cached for performance)
        available_streets = get_available_streets(connector)
        available_amounts = get_available_amounts(connector)
        available_cars = get_available_cars(connector)

        # Debug: Log filter data loading status
        if len(available_streets) > 0:
            logger.info(f"✅ Loaded {len(available_streets)} street names")
        else:
            logger.warning("⚠️  No street names loaded - checking cache...")
            # Force refresh cache if no streets are loaded
            st.cache_data.clear()
            available_streets = get_available_streets(connector)
            logger.info(
                f"🔄 After cache refresh: {len(available_streets)} street names"
            )

        if len(available_cars) > 0:
            logger.info(f"✅ Loaded {len(available_cars)} vehicle makes")
        else:
            logger.warning("⚠️  No vehicle makes loaded")

        # Street filter with selectbox
        street_options = ["All Streets"] + available_streets
        selected_street = st.sidebar.selectbox(
            "Street Name",
            options=street_options,
            help="Select a street to filter violations",
            key="street_filter",
        )
        street_filter = selected_street if selected_street != "All Streets" else ""

        # Car filter with selectbox
        car_options = ["All Cars"] + available_cars
        selected_car = st.sidebar.selectbox(
            "Vehicle Make",
            options=car_options,
            help="Select a vehicle make to filter violations",
            key="car_filter",
        )
        car_filter = selected_car if selected_car != "All Cars" else ""

        # Fine amount filter
        if available_amounts:
            min_amount = min(available_amounts)
            max_amount = max(available_amounts)
            amount_range = st.sidebar.slider(
                "Fine Amount Range",
                min_value=float(min_amount),
                max_value=float(max_amount),
                value=(float(min_amount), float(max_amount)),
                help="Filter violations by fine amount",
                key="amount_filter",
            )
        else:
            amount_range = (0.0, 200.0)

        # Filter summary and reset button
        active_filters = []
        if street_filter:
            active_filters.append(f"Street: {street_filter}")
        if car_filter:
            active_filters.append(f"Car: {car_filter}")
        if amount_range != (
            min(available_amounts) if available_amounts else 0.0,
            max(available_amounts) if available_amounts else 200.0,
        ):
            active_filters.append(
                f"Amount: ${amount_range[0]:.0f}-${amount_range[1]:.0f}"
            )

        if active_filters:
            st.sidebar.info(f"🔍 Active filters: {', '.join(active_filters)}")

        if st.sidebar.button("🔄 Reset Filters"):
            st.rerun()

        # Auto-refresh filtered query when filters change
        if st.sidebar.button("🚀 Apply Filters", type="primary"):
            execute_benchmark_query(
                "Q5",
                BENCHMARK_QUERIES["Q5"],
                connector,
                street_filter,
                amount_range,
                car_filter,
            )

        # Quick filter test
        if active_filters and st.sidebar.button(
            "🔍 Quick Filter Test", help="Test filters with a quick count"
        ):
            with st.spinner("Testing filters..."):
                filter_clauses = []
                if street_filter:
                    filter_clauses.append(f"street_name = '{street_filter}'")
                if car_filter:
                    filter_clauses.append(f"vehicle_make = '{car_filter}'")
                filter_clauses.append(
                    f"calculated_fine_amount BETWEEN {amount_range[0]} AND {amount_range[1]}"
                )

                where_clause = " AND ".join(filter_clauses)
                test_query = f"SELECT COUNT(*) as filtered_count FROM violations WHERE {where_clause}"

                result_df, exec_time, success = connector.execute_query(test_query)
                if success and not result_df.empty:
                    count = result_df.iloc[0]["filtered_count"]
                    st.sidebar.success(
                        f"✅ Found {count:,} matching violations in {exec_time * 1000:.1f}ms"
                    )
                else:
                    st.sidebar.error("❌ Filter test failed")

    else:
        st.sidebar.error("❌ Cannot connect to Firebolt Core")

        # Show detailed diagnostics
        with st.expander("🔍 Connection Diagnostics", expanded=True):
            st.text(connector.get_diagnostics())

            st.markdown("""
            ### Troubleshooting Steps:

            1. **Ensure Firebolt Core is running:**
               ```bash
               ./setup_core.sh
               ```

            2. **Check container status:**
               ```bash
               docker ps | grep firebolt-core
               ```

            3. **Test direct connection:**
               ```bash
               docker exec firebolt-core fb -C -c "SELECT 1"
               ```

            4. **Restart if needed:**
               ```bash
               docker stop firebolt-core
               docker rm firebolt-core
               ./setup_core.sh
               ```
            """)

        # Set default values if not connected
        street_filter = ""
        car_filter = ""
        amount_range = (0.0, 200.0)
        active_filters = []

        st.stop()

    # Main tabs
    tab1, tab2, tab3 = st.tabs(
        ["🏃 Run Benchmarks", "📊 Visualizations", "🔍 Browse Data"]
    )

    with tab1:
        st.header("Benchmark Queries")
        st.markdown(
            "Click any button to execute queries and see sub-second performance!"
        )

        # Show current filter settings
        if active_filters:
            with st.expander("🔍 Current Filter Settings", expanded=True):
                st.markdown("**Active Filters:**")
                if street_filter:
                    st.markdown(f"- **Street Name:** {street_filter}")
                if car_filter:
                    st.markdown(f"- **Vehicle Make:** {car_filter}")
                st.markdown(
                    f"- **Fine Amount Range:** ${amount_range[0]:.0f} - ${amount_range[1]:.0f}"
                )

        # Create columns for benchmark buttons
        cols = st.columns(3)

        # Query execution buttons
        for i, (query_id, query_info) in enumerate(BENCHMARK_QUERIES.items()):
            col_idx = i % 3

            with cols[col_idx]:
                if st.button(
                    f"{query_id}: {query_info['name']}", key=f"btn_{query_id}"
                ):
                    execute_benchmark_query(
                        query_id,
                        query_info,
                        connector,
                        street_filter,
                        amount_range,
                        car_filter,
                    )

        # Custom query toggle button (placed next to Q5)
        st.markdown("---")
        col1, col2 = st.columns([3, 1])

        with col1:
            st.subheader("💻 Custom Query")

        with col2:
            # Initialize session state for custom query visibility
            if "show_custom_query" not in st.session_state:
                st.session_state.show_custom_query = False

            if st.button("🔧 Toggle Custom Query", key="toggle_custom_query"):
                st.session_state.show_custom_query = (
                    not st.session_state.show_custom_query
                )

        # Show custom query section if toggled on
        if st.session_state.show_custom_query:
            # Query input area
            col1, col2 = st.columns([3, 1])

            with col1:
                # Initialize session state for custom query
                if "custom_query_input" not in st.session_state:
                    st.session_state.custom_query_input = ""

                custom_sql = st.text_area(
                    "Enter your custom SQL query:",
                    value=st.session_state.custom_query_input,
                    height=100,
                    placeholder="SELECT * FROM violations WHERE street_name = 'Broadway' LIMIT 10",
                    help="Write any SQL query. Optionally apply current filters.",
                )

                # Sample queries dropdown
                sample_query = st.selectbox(
                    "Or choose a sample query:",
                    options=[""] + SAMPLE_QUERIES,
                    help="Select a sample query to get started",
                )

                if sample_query:
                    custom_sql = sample_query
                    st.session_state.custom_query_input = sample_query

                # Filter application checkbox
                apply_filters = st.checkbox(
                    "Apply current filters to this query",
                    value=False,
                    help="Check this to apply street, car, and amount filters to your custom query",
                )

            with col2:
                st.write("**Query Tools:**")

                if st.button(
                    "🚀 Execute Query", type="primary", disabled=not custom_sql.strip()
                ):
                    if custom_sql.strip():
                        execute_custom_query(
                            connector,
                            custom_sql,
                            apply_filters,
                            street_filter,
                            amount_range,
                            car_filter,
                        )
                        st.session_state.custom_query_input = custom_sql

                if st.button("🔄 Clear Results"):
                    st.session_state.query_results = {}
                    st.session_state.latest_query = None
                    st.session_state.query_execution_order = []
                    st.success("All results cleared!")

                if st.button("📋 Clear Query"):
                    st.session_state.custom_query_input = ""
                    st.rerun()
        else:
            pass  # Custom query section is hidden

        # Show query stats
        if st.session_state.query_results:
            st.info(
                f"📊 **Total queries executed:** {len(st.session_state.query_results)}"
            )
        else:
            st.info("*No queries executed yet*")

        # Display results table
        if st.session_state.query_results:
            st.subheader("📈 Execution Results")

            results_data = []
            for query_id, result in st.session_state.query_results.items():
                # Handle both regular queries and custom queries
                if query_id.startswith("CQ_"):
                    description = result.get("name", "Custom Query")
                else:
                    description = BENCHMARK_QUERIES.get(query_id, {}).get(
                        "name", "Unknown Query"
                    )

                results_data.append(
                    {
                        "Query": query_id,
                        "Description": description,
                        "Execution Time (ms)": f"{result['execution_time'] * 1000:.1f}",
                        "Rows Returned": result["row_count"],
                        "Status": "✅ Success" if result["success"] else "❌ Failed",
                        "Timestamp": result["timestamp"].strftime("%H:%M:%S"),
                    }
                )

            # Sort by execution order (most recent first)
            results_data.sort(key=lambda x: x["Timestamp"], reverse=True)
            results_df = pd.DataFrame(results_data)
            st.dataframe(results_df, use_container_width=True)

            # Show latest query result using proper tracking
            if (
                st.session_state.latest_query
                and st.session_state.latest_query in st.session_state.query_results
            ):
                latest_query = st.session_state.latest_query
                latest_result = st.session_state.query_results[latest_query]

                # Get the query name for display
                if latest_query.startswith("CQ_"):
                    query_name = latest_result.get("name", "Custom Query")
                else:
                    query_name = BENCHMARK_QUERIES.get(latest_query, {}).get(
                        "name", "Unknown Query"
                    )

                st.subheader(f"📊 Latest Query Results: {latest_query}")
                st.markdown(f"**Query:** {query_name}")
                st.markdown(
                    f"**Executed at:** {latest_result['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}"
                )
                st.markdown(
                    f"**Execution time:** {latest_result['execution_time'] * 1000:.1f}ms"
                )
                st.markdown(f"**Rows returned:** {latest_result['row_count']}")

                # Show SQL for custom queries
                if latest_query.startswith("CQ_"):
                    if latest_result.get("filters_applied") and latest_result.get(
                        "original_sql"
                    ):
                        st.markdown("**Original SQL:**")
                        st.code(latest_result["original_sql"], language="sql")
                        st.markdown("**Executed SQL (with filters):**")
                        st.code(latest_result["sql"], language="sql")
                    else:
                        st.markdown("**Executed SQL:**")
                        st.code(latest_result["sql"], language="sql")

                if latest_result["success"] and not latest_result["data"].empty:
                    st.dataframe(latest_result["data"], use_container_width=True)
                elif latest_result["success"] and latest_result["data"].empty:
                    # Inform user when the query ran successfully but returned an empty set
                    st.info("Query executed successfully, but returned no rows, likely due to a slow initial load. Please re-run to ensure full results.")
                    if latest_query.startswith("CQ_") and latest_result.get(
                        "filters_applied"
                    ):
                        st.info(
                            "💡 **Tip:** Try unchecking 'Apply current filters' if you're getting no results."
                        )
                else:
                    st.error("Query failed to execute.")
            else:
                st.info(
                    "No queries executed yet. Click any query button above to start!"
                )

    with tab2:
        st.header("Data Visualizations")

        if not st.session_state.query_results:
            st.info("🚀 Run some benchmark queries first to see visualizations!")
            st.markdown("""
            **Available Visualizations:**
            - **Q1**: Overall statistics with key metrics
            - **Q2**: Revenue breakdown by street with bar charts
            - **Q3**: Vehicle make analysis with violation counts
            - **Q4**: Yearly trend analysis with time series
            - **Q5**: Interactive filtered results with scatter plots

            Click the benchmark query buttons in the **Run Benchmarks** tab to generate data for visualizations.
            """)
        else:
            # Show summary of available results
            st.markdown(
                f"**Available Results:** {', '.join(st.session_state.query_results.keys())}"
            )

            # Create visualizations for all available results
            create_visualizations()

    with tab3:
        st.header("Browse Data")

        # Show current data in the table
        st.subheader("🔍 Current Data in violations Table")

        if st.button("🔄 Refresh Data", help="Reload data from the database"):
            # Trigger a rerun to ensure fresh data only (Streamlit 1.30+)
            st.rerun()

        # Always show the latest data (single call)
        show_data_browser(connector)

        # Data information section
        st.subheader("📊 Dataset Information")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Dataset Details:**")
            st.info("""
            - **Source**: Sample NYC parking violation dataset
            - **Total Records**: 21,563,502 violations
            - **Format**: Parquet files optimized for analytics
            - **Size**: ~500MB compressed parquet files
            - **Location**: S3 bucket (public access)
            """)


def execute_benchmark_query(
    query_id: str,
    query_info: dict,
    connector: FireboltConnector,
    street_filter: str,
    amount_range: tuple,
    car_filter: str = "",
):
    """Execute a benchmark query with timing."""

    with st.spinner(f"Executing {query_id}..."):
        # Prepare query with filters for ALL queries
        sql = query_info["sql"]

        # Apply filters to all queries
        street_clause = f"AND street_name = '{street_filter}'" if street_filter else ""
        amount_clause = f"AND calculated_fine_amount BETWEEN {amount_range[0]} AND {amount_range[1]}"
        car_clause = f"AND vehicle_make = '{car_filter}'" if car_filter else ""

        sql = sql.format(
            street_filter=street_clause,
            amount_filter=amount_clause,
            car_filter=car_clause,
        )

        # Execute query
        result_df, execution_time, success = connector.execute_query(sql)

        # Store results and update latest query tracking
        st.session_state.query_results[query_id] = {
            "data": result_df,
            "execution_time": execution_time,
            "row_count": len(result_df) if success else 0,
            "success": success,
            "timestamp": datetime.now(),
        }

        # Update latest query and execution order
        st.session_state.latest_query = query_id
        if query_id in st.session_state.query_execution_order:
            st.session_state.query_execution_order.remove(query_id)
        st.session_state.query_execution_order.append(query_id)

        if success:
            st.success(f"✅ {query_id} completed in {execution_time * 1000:.1f}ms")
        else:
            st.error(f"❌ {query_id} failed")


def execute_custom_query(
    connector: FireboltConnector,
    custom_sql: str,
    apply_filters: bool,
    street_filter: str,
    amount_range: tuple,
    car_filter: str = "",
):
    """Execute a custom user query with optional filters."""
    query_id = f"CQ_{int(time.time())}"  # Unique ID for custom query

    with st.spinner("Executing custom query..."):
        # Prepare query with filters if requested
        sql = custom_sql.strip()
        original_sql = custom_sql.strip()

        # Only apply filters if explicitly requested and the query references violations table
        if apply_filters and "violations" in sql.lower():
            # Simple approach: add WHERE clause or extend existing WHERE clause
            if street_filter or car_filter or amount_range != (0.0, 200.0):
                conditions = []

                if street_filter:
                    conditions.append(f"street_name = '{street_filter}'")
                if car_filter:
                    conditions.append(f"vehicle_make = '{car_filter}'")
                if amount_range != (0.0, 200.0):
                    conditions.append(
                        f"calculated_fine_amount BETWEEN {amount_range[0]} AND {amount_range[1]}"
                    )

                if conditions:
                    filter_clause = " AND ".join(conditions)

                    # Simple logic: if query has WHERE, add AND conditions, otherwise add WHERE
                    if " WHERE " in sql.upper() or " where " in sql:
                        sql = sql.rstrip(";") + f" AND ({filter_clause})"
                    else:
                        sql = sql.rstrip(";") + f" WHERE {filter_clause}"

        # Execute query
        result_df, execution_time, success = connector.execute_query(sql)

        # Store results
        st.session_state.query_results[query_id] = {
            "data": result_df,
            "execution_time": execution_time,
            "row_count": len(result_df) if success else 0,
            "success": success,
            "timestamp": datetime.now(),
            "name": "Custom Query",  # Store the template name
            "sql": sql,  # Store the actual SQL executed
            "original_sql": original_sql,  # Store the original SQL
            "filters_applied": apply_filters,
        }

        # Update latest query and execution order
        st.session_state.latest_query = query_id
        if query_id in st.session_state.query_execution_order:
            st.session_state.query_execution_order.remove(query_id)
        st.session_state.query_execution_order.append(query_id)

        if success:
            st.success(f"✅ Custom query completed in {execution_time * 1000:.1f}ms")
            if apply_filters and sql != original_sql:
                st.info("🔍 Filters were applied to your query")
        else:
            st.error("❌ Custom query failed")

        return query_id


def create_visualizations():
    """Create visualizations from query results."""

    visualizations_shown = 0

    # Show all available visualizations from most recent to oldest
    if not st.session_state.query_results:
        st.info("🚀 Run some benchmark queries first to see visualizations!")
        return

    # Sort query results by timestamp (most recent first)
    sorted_results = sorted(
        st.session_state.query_results.items(),
        key=lambda x: x[1]["timestamp"],
        reverse=True,
    )

    for query_id, result in sorted_results:
        data = result["data"]
        if data.empty or not result["success"]:
            continue

        # Get query name for display
        if query_id.startswith("CQ_"):
            query_name = result.get("name", "Custom Query")
        else:
            query_name = BENCHMARK_QUERIES.get(query_id, {}).get(
                "name", "Unknown Query"
            )

        # Create appropriate visualization based on data structure
        st.subheader(f"📊 {query_name} ({query_id})")
        st.markdown(
            f"*Executed at: {result['timestamp'].strftime('%H:%M:%S')} | Execution time: {result['execution_time'] * 1000:.1f}ms*"
        )

        # Overall statistics (Q1 and similar)
        if "total_violations" in data.columns and len(data) == 1:
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                violations = data.iloc[0]["total_violations"]
                st.metric(
                    "Total Violations",
                    f"{int(violations):,}" if violations is not None else "N/A",
                )
            with col2:
                fines = data.iloc[0].get("total_fines", 0)
                st.metric(
                    "Total Fines",
                    f"${float(fines):,.2f}" if fines is not None else "N/A",
                )
            with col3:
                avg_fine = data.iloc[0].get("avg_fine", 0)
                st.metric(
                    "Average Fine",
                    f"${float(avg_fine):.2f}" if avg_fine is not None else "N/A",
                )
            with col4:
                min_fine = data.iloc[0].get("min_fine", 0)
                max_fine = data.iloc[0].get("max_fine", 0)
                if min_fine is not None and max_fine is not None:
                    st.metric(
                        "Fine Range", f"${float(min_fine):.0f} - ${float(max_fine):.0f}"
                    )
                else:
                    st.metric("Fine Range", "N/A")
            visualizations_shown += 1

        # Street revenue breakdown (Q2 and similar)
        elif "street_name" in data.columns and "total_revenue" in data.columns:
            fig = px.bar(
                data,
                x="street_name",
                y="total_revenue",
                color="avg_fine",
                title=f"{query_name} - Revenue by Street",
                labels={
                    "total_revenue": "Total Revenue ($)",
                    "street_name": "Street Name",
                    "avg_fine": "Avg Fine ($)",
                },
                color_continuous_scale="viridis",
            )
            fig.update_layout(height=400, xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
            visualizations_shown += 1

        # Vehicle make analysis (Q3 and similar)
        elif "vehicle_make" in data.columns and "violations" in data.columns:
            fig = px.bar(
                data,
                x="vehicle_make",
                y="avg_fine",
                color="violations",
                title=f"{query_name} - Average Fine by Vehicle Make",
                labels={
                    "vehicle_make": "Vehicle Make",
                    "avg_fine": "Average Fine ($)",
                    "violations": "Number of Violations",
                },
            )
            fig.update_layout(height=400, xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
            visualizations_shown += 1

        # Yearly trend analysis (Q4 and similar)
        elif "year" in data.columns and "violation_count" in data.columns:
            fig = px.line(
                data,
                x="year",
                y="violation_count",
                title=f"{query_name} - Violations Over Time",
                labels={"year": "Year", "violation_count": "Number of Violations"},
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
            visualizations_shown += 1

        # Interactive filtering (Q5 and similar)
        elif "fine_category" in data.columns:
            # Check if required columns exist for scatter plot
            if (
                "calculated_fine_amount" in data.columns
                and "issue_date" in data.columns
            ):
                fig = px.scatter(
                    data,
                    x="calculated_fine_amount",
                    y="issue_date",
                    color="fine_category",
                    hover_data=["street_name", "vehicle_make"]
                    if "street_name" in data.columns and "vehicle_make" in data.columns
                    else None,
                    title=f"{query_name} - Filtered Violations",
                    labels={
                        "calculated_fine_amount": "Fine Amount ($)",
                        "issue_date": "Issue Date",
                    },
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
                visualizations_shown += 1
            # Fallback: create a bar chart for fine categories
            elif "violation_count" in data.columns:
                fig = px.bar(
                    data,
                    x="fine_category",
                    y="violation_count",
                    title=f"{query_name} - Violations by Fine Category",
                    labels={
                        "fine_category": "Fine Category",
                        "violation_count": "Violation Count",
                    },
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
                visualizations_shown += 1

        # Generic visualization for other data types
        else:
            # Try to create a generic bar chart if we have numeric data
            numeric_cols = data.select_dtypes(include=["int64", "float64"]).columns
            if len(numeric_cols) >= 2:
                fig = px.bar(
                    data.head(20),  # Limit to top 20 for readability
                    x=data.columns[0],
                    y=numeric_cols[0],
                    title=f"{query_name} - Data Visualization",
                    labels={
                        data.columns[0]: data.columns[0],
                        numeric_cols[0]: numeric_cols[0],
                    },
                )
                fig.update_layout(height=400, xaxis_tickangle=-45)
                st.plotly_chart(fig, use_container_width=True)
                visualizations_shown += 1

        # Always show the data table
        st.dataframe(data, use_container_width=True)
        st.markdown("---")

    # Fallback message if no visualizations were shown
    if visualizations_shown == 0:
        st.warning("⚠️ No visualizations available. This might happen if:")
        st.markdown("""
        - Query results are empty or failed
        - Data contains only null values
        - There was an error processing the query results

        Try running the benchmark queries again or check the connection status.
        """)


if __name__ == "__main__":
    main()
