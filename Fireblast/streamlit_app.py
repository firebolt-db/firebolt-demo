import os
import tempfile
import json
import random
import time
import pandas as pd
from datetime import datetime
from firebolt.db.connection import connect
from firebolt.client.auth.client_credentials import ClientCredentials
import streamlit as st
from firebolt.utils.exception import FireboltStructuredError
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor
import numpy as np

# Configure Streamlit page
st.set_page_config(page_title="Firebolt Demo App", layout="wide")

# Load environment variables
load_dotenv()

def validate_credentials():
    """Validate all required Firebolt credentials are present."""
    required_vars = [
        "FIREBOLT_ACCOUNT_NAME",
        "FIREBOLT_ACCOUNT_ID", 
        "FIREBOLT_ACCOUNT_SECRET",
        "FIREBOLT_ACCOUNT_DATABASE_NAME",
        "FIREBOLT_ACCOUNT_ENGINE_NAME",
        "FIREBOLT_DML_ENGINE_NAME",
        "FIREBOLT_ENDPOINT"
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        st.error(f"""
        ❌ **Missing Required Environment Variables**
        
        Please create a `.env` file in the project root with the following variables:
        
        ```
        {chr(10).join(f'{var}=...' for var in missing_vars)}
        ```
        
        **Complete .env template:**
        ```
        FIREBOLT_ACCOUNT_NAME=your_account_name
        FIREBOLT_ACCOUNT_ID=your_account_id
        FIREBOLT_ACCOUNT_SECRET=your_account_secret
        FIREBOLT_ACCOUNT_DATABASE_NAME=your_database_name
        FIREBOLT_ACCOUNT_ENGINE_NAME=your_read_engine_name
        FIREBOLT_ACCOUNT_SCHEMA_NAME=public
        FIREBOLT_DML_ENGINE_NAME=your_dml_engine_name
        FIREBOLT_ENDPOINT=api.app.firebolt.io
        ```
        """)
        st.stop()

def ensure_schema():
    """Create the required dml_test table if it doesn't exist."""
    try:
        # Type hints: we've validated these exist in validate_credentials()
        auth = ClientCredentials(
            client_id=str(FIREBOLT_ACCOUNT_ID), 
            client_secret=str(FIREBOLT_ACCOUNT_SECRET)
        )
        conn = connect(
            auth=auth,
            account_name=str(FIREBOLT_ACCOUNT_NAME),
            database=str(FIREBOLT_DATABASE),
            engine_name=str(FIREBOLT_DML_ENGINE),
            api_endpoint=str(FIREBOLT_ENDPOINT)
        )
        cur = conn.cursor()
        
        # Create table with exact schema specified in requirements
        create_table_sql = f"""
        CREATE TABLE IF NOT EXISTS {DML_TABLE} (
            id               BIGINT  NOT NULL,
            ltv_date         DATE    NOT NULL,
            app_id           TEXT    NOT NULL,
            media_source     TEXT    NOT NULL,
            attribution_type TEXT    NOT NULL,
            clicks_count     BIGINT  DEFAULT 0,
            impressions_count BIGINT DEFAULT 0,
            installs_count    BIGINT DEFAULT 0,
            inappevents_count BIGINT DEFAULT 0,
            launches_count    BIGINT DEFAULT 0
        )
        PRIMARY INDEX id, ltv_date, media_source
        PARTITION BY ltv_date
        """
        
        cur.execute(create_table_sql)
        conn.commit()
        conn.close()
        
        # Show success message only on first creation
        if 'schema_created' not in st.session_state:
            st.success("✅ Database schema verified and ready!")
            st.session_state.schema_created = True
            
    except Exception as e:
        st.error(f"❌ Failed to create database schema: {str(e)}")
        st.stop()

def load_app_data():
    """Load app data with error handling."""
    try:
        if not os.path.exists("data/apps_to_use.csv"):
            st.error("❌ Required data file `data/apps_to_use.csv` not found!")
            st.stop()
        return pd.read_csv("data/apps_to_use.csv")
    except Exception as e:
        st.error(f"❌ Failed to load app data: {str(e)}")
        st.stop()

# Validate credentials first
validate_credentials()

# Load Firebolt credentials
FIREBOLT_ACCOUNT_NAME = os.getenv("FIREBOLT_ACCOUNT_NAME")
FIREBOLT_ACCOUNT_ID = os.getenv("FIREBOLT_ACCOUNT_ID")
FIREBOLT_ACCOUNT_SECRET = os.getenv("FIREBOLT_ACCOUNT_SECRET")
FIREBOLT_DATABASE = os.getenv("FIREBOLT_ACCOUNT_DATABASE_NAME")
FIREBOLT_ENGINE = os.getenv("FIREBOLT_ACCOUNT_ENGINE_NAME")
FIREBOLT_DML_ENGINE = os.getenv("FIREBOLT_DML_ENGINE_NAME")
FIREBOLT_ENDPOINT = os.getenv("FIREBOLT_ENDPOINT")

# Define schema and table names from environment
SCHEMA = os.getenv("FIREBOLT_ACCOUNT_SCHEMA_NAME", "public")
DML_TABLE = f"{FIREBOLT_DATABASE}.{SCHEMA}.dml_test"

# Ensure database schema exists
ensure_schema()

# Load app data safely
_apps_df = load_app_data()
APP_IDS = _apps_df["app_id"].tolist()
MEDIA_SOURCES = ["3bc36bb9f1bded2703684dae170581dc",
                 "e391b3d1930968f4cce0d5dee539d256",
                 "b935fcce8f277b6c60cd7598349c64e8"]
ATTRIBUTION_TYPES = ["install", "reengagement", "reinstall"]

# Helper to reset session state
def reset_session():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()  # Fixed: replaced deprecated st.experimental_rerun()

# Create tabs
tabs = st.tabs(["Query Load (QPS)", "Ingestion Pipeline"])

# ---- Tab 1: QPS Load Testing ----
with tabs[0]:
    # Tab 1 header with logo
    col_logo, col_title = st.columns([1, 4])
    with col_logo:
        st.image("firebolt-logo.png", width=100)
    with col_title:
        st.header("QPS Load Testing")

    # Collapsible settings
    with st.expander("QPS Test Settings", expanded=False):
        use_defined_queries = st.checkbox("Use Defined Queries", value=False, key="qps_use_defined_queries")
        selected_query_files = []
        defined_queries = []
        queries_dir = "queries"
        sql_files = []
        if os.path.isdir(queries_dir):
            sql_files = [f for f in os.listdir(queries_dir) if f.endswith(".sql")]
        if use_defined_queries:
            if sql_files:
                for sql_file in sql_files:
                    checked = st.checkbox(sql_file, value=False, key=f"qps_query_{sql_file}")
                    if checked:
                        selected_query_files.append(sql_file)
                # Load the SQL from selected files
                for fname in selected_query_files:
                    with open(os.path.join(queries_dir, fname), "r") as f:
                        defined_queries.append(f.read())
            else:
                st.warning("No 'queries' folder found. Please create a 'queries' folder with .sql files.")

        # Set minimum users to number of defined queries if using defined queries
        min_users = len(defined_queries) if use_defined_queries and defined_queries else 1
        users = st.number_input(
            "Number of synthetic users (threads)",
            min_value=min_users, value=min_users, step=1, key="qps_users"
        )
        use_cache = st.checkbox("Use cache?", value=True, key="qps_use_cache")
        optimizer_user_guided = st.checkbox("Set optimizer_mode=user_guided", value=False, key="qps_optimizer_user_guided")
        duration = st.number_input(
            "Test duration (seconds)",
            min_value=1, value=30, step=1, key="qps_duration"
        )

    # Always-visible run button
    run_test = st.button("Run QPS Test")

    if run_test:
        # Validate reasonable thread count
        if users > 500:
            st.warning(f"⚠️ {users} concurrent threads is very high and may cause performance issues or connection limits. Consider starting with 50-100 threads for initial testing.")
            if users > 1000:
                st.error(f"🚫 {users} threads exceeds recommended limits. This may crash the application or exceed database connection limits. Maximum recommended: 500 threads.")
                st.stop()
        # Always set cache settings before running test
        auth = ClientCredentials(client_id=str(FIREBOLT_ACCOUNT_ID), client_secret=str(FIREBOLT_ACCOUNT_SECRET))
        conn = connect(auth=auth, account_name=str(FIREBOLT_ACCOUNT_NAME),
                       database=str(FIREBOLT_DATABASE), engine_name=str(FIREBOLT_ENGINE),
                       api_endpoint=str(FIREBOLT_ENDPOINT))
        cur = conn.cursor()
        if optimizer_user_guided:
            cur.execute("SET advanced_mode=1")
            cur.execute("SET lqp2_explain_options=no_variable_types")
            cur.execute("SET optimizer_mode=user_guided")

        if not use_cache:
            cur.execute("SET enable_result_cache = FALSE")
            cur.execute("SET enable_subresult_cache = TRUE")
            print("Cache is DISABLED")
        else:
            cur.execute("SET enable_result_cache = TRUE")
            cur.execute("SET enable_subresult_cache = TRUE")
            print("Cache is ENABLED")

        # Warm-up phase (skip if using defined queries)
        if not (use_defined_queries and defined_queries):
            status_box = st.empty()
            status_box.info("Warming up cluster...")
            # Only run warmup query if not using defined queries
            if not (use_defined_queries and defined_queries):
                cur.execute(f"SELECT * FROM {DML_TABLE} LIMIT 1")
                cur.fetchall()
                # Determine current max id for random query lookups
                cur.execute(f"SELECT COALESCE(MAX(id), 0) FROM {DML_TABLE}")
                next_id = cur.fetchone()[0]
            else:
                next_id = 0
            status_box.success("Warm-up complete. Starting test...")
            time.sleep(3)
            status_box.empty()
        else:
            # Only get next_id if not using defined queries
            if not (use_defined_queries and defined_queries):
                cur.execute(f"SELECT COALESCE(MAX(id), 0) FROM {DML_TABLE}")
                next_id = cur.fetchone()[0]
            else:
                next_id = 0

        # Query generator and log
        query_log = []
        import numpy as _np

        if use_defined_queries and defined_queries:
            # Use user-selected queries, loop through them in round-robin
            def make_defined_query():
                idx = 0
                while True:
                    yield defined_queries[idx % len(defined_queries)]
                    idx += 1
            defined_query_gen = make_defined_query()
        else:
            def make_random_query():
                rnd = random.random()
                # 10% static repeat query
                if rnd < 0.1:
                    return f"SELECT * FROM {DML_TABLE} LIMIT 100"
                # 20% aggregation query
                elif rnd < 0.3:
                    return (f"SELECT media_source, COUNT(*) AS cnt, AVG(clicks_count) AS avg_clicks "
                            f"FROM {DML_TABLE} "
                            f"WHERE ltv_date = '{datetime.utcnow().date().isoformat()}' "
                            "GROUP BY media_source")
                # 70% random id lookup
                else:
                    rand_id = random.randint(1, next_id)
                    return f"SELECT * FROM {DML_TABLE} WHERE id = {rand_id}"

        # Setup with thread safety
        response_times = []
        timestamps = []
        from threading import Lock
        data_lock = Lock()
        start_time = time.time()
        end_time = start_time + duration

        kpi_row1_container = st.empty()
        kpi_row2_container = st.empty()
        progress = st.progress(0)
        chart_area = st.empty()
        stats_chart = st.empty()

        # Worker
        def worker(use_cache, end_time, response_times, timestamps, auth, query=None, defined_queries=None):
            conn_w = connect(auth=auth, account_name=str(FIREBOLT_ACCOUNT_NAME),
                             database=str(FIREBOLT_DATABASE), engine_name=str(FIREBOLT_ENGINE),
                             api_endpoint=str(FIREBOLT_ENDPOINT))
            cur_w = conn_w.cursor()
            if not use_cache:
                cur_w.execute("SET enable_result_cache = TRUE")
                cur_w.execute("SET enable_subresult_cache = FALSE")
            else:
                cur_w.execute("SET enable_subresult_cache = TRUE")
                cur_w.execute("SET enable_result_cache = TRUE")
            if use_defined_queries and defined_queries:
                # If a specific query is assigned, use it; otherwise, pick randomly
                if query is not None:
                    sql_to_run = query
                    while time.time() < end_time:
                        sql = sql_to_run
                        t0 = time.time()
                        try:
                            cur_w.execute(sql)
                            cur_w.fetchall()
                        except Exception:
                            continue
                        rt = (time.time() - t0) * 1000
                        timestamp = time.time()
                        with data_lock:
                            response_times.append(rt)
                            timestamps.append(timestamp)
                            query_log.append({"sql": sql, "rt": rt})
                else:
                    # Extra threads: pick a random query each time
                    while time.time() < end_time:
                        sql = random.choice(defined_queries)
                        t0 = time.time()
                        try:
                            cur_w.execute(sql)
                            cur_w.fetchall()
                        except Exception:
                            continue
                        rt = (time.time() - t0) * 1000
                        timestamp = time.time()
                        with data_lock:
                            response_times.append(rt)
                            timestamps.append(timestamp)
                            query_log.append({"sql": sql, "rt": rt})
            else:
                while time.time() < end_time:
                    sql = make_random_query()
                    t0 = time.time()
                    try:
                        cur_w.execute(sql)
                        cur_w.fetchall()
                    except Exception:
                        continue
                    rt = (time.time() - t0) * 1000
                    timestamp = time.time()
                    with data_lock:
                        response_times.append(rt)
                        timestamps.append(timestamp)
                        query_log.append({"sql": sql, "rt": rt})

        # Launch with reasonable connection limits
        # Limit concurrent DB connections to prevent overwhelming Firebolt
        max_db_connections = min(users, 200)  # Cap at 200 concurrent connections
        exec_pool = ThreadPoolExecutor(max_workers=max_db_connections)
        
        # If users > max_db_connections, we'll queue work rather than create too many connections
        work_items = []
        if use_defined_queries and defined_queries:
            # Assign one thread per defined query, then cycle for extra users
            for i in range(users):
                query_idx = i % len(defined_queries) if defined_queries else 0
                query = defined_queries[query_idx] if defined_queries else None
                work_items.append((use_cache, end_time, response_times, timestamps, auth, query, defined_queries))
        else:
            for _ in range(users):
                work_items.append((use_cache, end_time, response_times, timestamps, auth, None, None))
        
        # Submit work with connection limiting
        futures = []
        for work_item in work_items:
            future = exec_pool.submit(worker, *work_item)
            futures.append(future)
            
        if users > max_db_connections:
            st.info(f"🔧 Limited to {max_db_connections} concurrent database connections (requested {users} threads). Work will be queued to prevent connection limits.")

        # Live update loop with improved resilience for high loads
        update_interval = 2 if users > 100 else 1  # Slower updates for high thread counts
        last_update = 0
        
        while time.time() < end_time:
            current_time = time.time()
            elapsed = current_time - start_time
            
            # Always update progress bar (lightweight)
            try:
                progress.progress(min(elapsed / duration, 1.0))
            except Exception:
                pass  # Don't let progress bar issues stop the test
            
            # Only update metrics and charts at intervals to reduce lock contention
            if current_time - last_update >= update_interval:
                last_update = current_time
                
                # Get thread-safe copies for calculations with timeout
                rt_copy = []
                ts_copy = []
                try:
                    # Use a shorter timeout for high loads to prevent UI blocking
                    lock_timeout = 0.1 if users > 200 else 1.0
                    if data_lock.acquire(timeout=lock_timeout):
                        try:
                            rt_copy = response_times.copy()
                            ts_copy = timestamps.copy()
                        finally:
                            data_lock.release()
                    else:
                        # If we can't get the lock quickly, show last known metrics
                        continue
                except Exception:
                    continue  # Skip this update if there are issues
                
                total = len(rt_copy)
                if rt_copy and ts_copy and len(rt_copy) == len(ts_copy):
                    try:
                        # Calculate QPS grouping with error handling
                        ts_series = pd.Series(ts_copy)
                        group = pd.Series(rt_copy).groupby((ts_series - start_time).astype(int)).count()
                        peak = group.max() if not group.empty else 0
                        cur_min, cur_max = round(min(rt_copy),2), round(max(rt_copy),2)
                        p90 = round(np.percentile(rt_copy, 90), 2)
                        p95 = round(np.percentile(rt_copy, 95), 2)
                        median_rt = round(np.median(rt_copy), 2)
                        
                        # Update metrics
                        cols1 = kpi_row1_container.columns(4)
                        cols2 = kpi_row2_container.columns(3)

                        cols1[0].metric("Total Queries", total)
                        cols1[1].metric("Peak QPS", int(peak))
                        cols1[2].metric("Min RT (ms)", cur_min)
                        cols1[3].metric("Max RT (ms)", cur_max)

                        cols2[0].metric("Median RT (ms)", median_rt)
                        cols2[1].metric("P90 RT (ms)", p90)
                        cols2[2].metric("P95 RT (ms)", p95)

                        # Update charts with error handling
                        try:
                            dfp = pd.DataFrame({'timestamp': ts_copy, 'rt': rt_copy})
                            dfp['sec'] = (dfp['timestamp'] - start_time).astype(int)
                            
                            # Only update charts if we have meaningful data
                            if len(dfp) > 1:
                                med = dfp.groupby('sec')['rt'].median().reset_index()
                                chart_area.line_chart(med.set_index('sec'))

                                qps_df = dfp.groupby('sec').size().reset_index().rename(columns={0: 'qps'})
                                rt_df = dfp.groupby('sec')['rt'].agg([
                                    ('median', 'median'),
                                    ('p90', lambda x: np.percentile(x, 90)),
                                    ('p95', lambda x: np.percentile(x, 95))
                                ]).reset_index()
                                chart_data = pd.merge(rt_df, qps_df, on='sec', how='left').set_index('sec')
                                stats_chart.line_chart(chart_data)
                        except Exception as e:
                            # Chart update failed, but continue with metrics
                            pass
                            
                    except Exception as e:
                        # Calculation failed, show basic metrics
                        cols1 = kpi_row1_container.columns(4)
                        cols1[0].metric("Total Queries", total)
                        cols1[1].metric("Status", "Processing...")
                else:
                    # No data yet or data mismatch - show zero metrics
                    cols1 = kpi_row1_container.columns(4)
                    cols2 = kpi_row2_container.columns(3)

                    cols1[0].metric("Total Queries", total)
                    cols1[1].metric("Peak QPS", 0)
                    cols1[2].metric("Min RT (ms)", 0)
                    cols1[3].metric("Max RT (ms)", 0)
                    cols2[0].metric("Median RT (ms)", 0)
                    cols2[1].metric("P90 RT (ms)", 0)
                    cols2[2].metric("P95 RT (ms)", 0)
            
            # Sleep with shorter intervals for high loads
            time.sleep(0.5 if users > 200 else 1)

        exec_pool.shutdown()

        # Display slow queries at end
        df_log = pd.DataFrame(query_log)
        if not df_log.empty:
            thr = df_log["rt"].median() + 2 * df_log["rt"].std()
            outliers = df_log[df_log["rt"] > thr]
            st.subheader("Outlier Queries (rt > {:.1f} ms)".format(thr))
            st.dataframe(outliers)

        # Save results to output dir
        os.makedirs("data/output", exist_ok=True)
        out_file = f"data/output/qps_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        stats_data = {
            "response_times": response_times,
            "timestamps": timestamps,
            "start_time": start_time,
            "end_time": end_time
        }
        with open(out_file, "w") as f:
            json.dump(stats_data, f)

        # Show reset button
        if st.button("Reset"): 
            reset_session()
# ---- Tab 2: DML Operations Testing ----
with tabs[1]:
    # Tab 2 header with logo
    col_logo, col_title = st.columns([1, 4])
    with col_logo:
        st.image("firebolt-logo.png", width=100)
    with col_title:
        st.header("DML Operations Testing")

    # Collapsible DML settings
    with st.expander("DML Operations Settings", expanded=False):
        batch_size = st.number_input(
            "Batch size", min_value=1, value=10, step=1, key="dml_batch_size"
        )
        duration = st.number_input(
            "Test duration (seconds)", min_value=1, value=30, step=1, key="dml_duration"
        )
    # Always-visible run button
    run_dml = st.button("Run DML Test")

    if run_dml:
        st.info("Launching 3 DML threads…")

        # Use constants already loaded at startup
        # (No need to reload - data is already validated and loaded)

        # shared counters
        from threading import Lock
        counters = {"ins": 0, "upd": 0, "del": 0, "tx": 0}
        lock = Lock()

        # worker factory
        def make_worker(op_type, sql_fn, size):
            def worker():
                print(f"🚀 {op_type}_worker started with batch size {size}")
                auth = ClientCredentials(client_id=FIREBOLT_ACCOUNT_ID,
                                         client_secret=FIREBOLT_ACCOUNT_SECRET)
                conn = connect(auth=auth,
                               account_name=FIREBOLT_ACCOUNT_NAME,
                               database=FIREBOLT_DATABASE,
                               engine_name=FIREBOLT_DML_ENGINE,
                               api_endpoint=FIREBOLT_ENDPOINT)
                cur = conn.cursor()
                while time.time() < end_time:
                    print(f"🔁 {op_type}_worker tick; deleting up to {size} rows")
                    sql, params = sql_fn(size)
                    cur.execute(sql, params) if params else cur.execute(sql)
                    conn.commit()
                    with lock:
                        counters[op_type] += size
                        counters["tx"] += 1
                conn.close()
            return worker

        # define SQL generators
        def gen_insert_sql(n):
            now_iso = datetime.utcnow().isoformat()
            rows = [
                f"({next_id + i}, '{now_iso}', '{random.choice(APP_IDS)}',"
                f" '{random.choice(MEDIA_SOURCES)}','{random.choice(ATTRIBUTION_TYPES)}',"
                f" {random.randint(1,10)}, {random.randint(10,100)},"
                f" {random.randint(0,5)}, {random.randint(0,20)}, {random.randint(0,5)})"
                for i in range(n)
            ]
            return (
                f"INSERT INTO {DML_TABLE} "
                "(id, ltv_date, app_id, media_source, attribution_type, "
                "clicks_count, impressions_count, installs_count, "
                "inappevents_count, launches_count) VALUES "
                + ",".join(rows),
                None
            )


        # custom update worker
        def update_worker():
            print("🔄 update_worker started (per-row mode)")
            auth = ClientCredentials(client_id=FIREBOLT_ACCOUNT_ID,
                                     client_secret=FIREBOLT_ACCOUNT_SECRET)
            conn = connect(auth=auth,
                           account_name=FIREBOLT_ACCOUNT_NAME,
                           database=FIREBOLT_DATABASE,
                           engine_name=FIREBOLT_DML_ENGINE,
                           api_endpoint=FIREBOLT_ENDPOINT)
            cur = conn.cursor()
            while time.time() < end_time:
                # select a single id to update
                cur.execute(f"SELECT id FROM {DML_TABLE} ORDER BY RANDOM() LIMIT 1")
                row = cur.fetchone()
                if not row:
                    print("update_worker: no rows to update yet")
                    time.sleep(0.1)
                    continue
                id_val = row[0]
                new_val = random.randint(1, 100)
                try:
                    cur.execute(
                        f"UPDATE {DML_TABLE} SET clicks_count = %s WHERE id = %s",
                        (new_val, id_val)
                    )
                    conn.commit()
                    with lock:
                        counters["upd"] += 1
                        counters["tx"] += 1
                except FireboltStructuredError as fe:
                    print(f"Conflict updating id {id_val}, skipping: {fe}")
                time.sleep(0.05)
            conn.close()


        def delete_worker():
            print("🚀 delete_worker started (per-row mode)")
            auth = ClientCredentials(client_id=FIREBOLT_ACCOUNT_ID,
                                     client_secret=FIREBOLT_ACCOUNT_SECRET)
            conn = connect(auth=auth,
                           account_name=FIREBOLT_ACCOUNT_NAME,
                           database=FIREBOLT_DATABASE,
                           engine_name=FIREBOLT_DML_ENGINE,
                           api_endpoint=FIREBOLT_ENDPOINT)
            cur = conn.cursor()
            while time.time() < end_time:
                # select a single id to delete
                cur.execute(f"SELECT id FROM {DML_TABLE} ORDER BY RANDOM() LIMIT 1")
                row = cur.fetchone()
                if not row:
                    print("delete_worker: no rows to delete yet")
                    time.sleep(0.1)
                    continue
                id_val = row[0]
                try:
                    cur.execute(
                        f"DELETE FROM {DML_TABLE} WHERE id = %s",
                        (id_val,)
                    )
                    conn.commit()
                    with lock:
                        counters["del"] += 1
                        counters["tx"] += 1
                except FireboltStructuredError as fe:
                    print(f"Conflict deleting id {id_val}, skipping: {fe}")
                time.sleep(0.05)
            conn.close()

        # fetch starting id
        cur = connect(auth=ClientCredentials(client_id=FIREBOLT_ACCOUNT_ID,
                                             client_secret=FIREBOLT_ACCOUNT_SECRET),
                      account_name=FIREBOLT_ACCOUNT_NAME,
                      database=FIREBOLT_DATABASE,
                      engine_name=FIREBOLT_DML_ENGINE,
                      api_endpoint=FIREBOLT_ENDPOINT).cursor()
        cur.execute(f"SELECT COALESCE(MAX(id), 0) FROM {DML_TABLE}")
        next_id = cur.fetchone()[0] + 1

        # compute sizes and time window
        insert_size = batch_size
        update_size = int(batch_size * 0.3)
        delete_size = int(batch_size * 0.2)
        start_time = time.time()
        end_time = start_time + duration

        col_ins, col_upd, col_del, col_tx = st.columns(4)
        ins_placeholder = col_ins.empty()
        upd_placeholder = col_upd.empty()
        del_placeholder = col_del.empty()
        tx_placeholder  = col_tx.empty()
        chart_area = st.empty()

        # launch threads
        from threading import Thread
        threads = [
            Thread(target=make_worker("ins",  gen_insert_sql, insert_size), daemon=True),
            Thread(target=update_worker, daemon=True),
            Thread(target=delete_worker, daemon=True),
        ]
        for t in threads: t.start()

        # live UI loop
        last = {"ins": 0, "upd": 0, "del": 0, "tx": 0}
        secs = []
        ins_list = []
        upd_list = []
        del_list = []
        tx_list = []

        while time.time() < end_time:
            time.sleep(1)
            with lock:
                curr = counters.copy()
            # compute deltas
            delta_ins = curr["ins"] - last["ins"]
            delta_upd = curr["upd"] - last["upd"]
            delta_del = curr["del"] - last["del"]
            delta_tx  = curr["tx"]  - last["tx"]
            last = curr
            # record
            now = time.time()
            secs.append(int(now - start_time))
            ins_list.append(delta_ins)
            upd_list.append(delta_upd)
            del_list.append(delta_del)
            tx_list.append(delta_tx)
            # update KPI placeholders (in place)
            ins_placeholder.metric("Total Inserts", curr["ins"])
            upd_placeholder.metric("Total Updates", curr["upd"])
            del_placeholder.metric("Total Deletes", curr["del"])
            tx_placeholder.metric("Transactions", curr["tx"])
            # redraw chart
            df = pd.DataFrame({
                "sec": secs,
                "Inserts": ins_list,
                "Updates": upd_list,
                "Deletes": del_list
            }).set_index("sec")
            chart_area.bar_chart(df)

        if st.button("Reset"):
            reset_session()