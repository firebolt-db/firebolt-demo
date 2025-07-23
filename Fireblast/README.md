# Fireblast - Firebolt Performance Demo

A **self-contained Streamlit application** that demonstrates Firebolt database performance through interactive load testing and DML operations monitoring.

## 🚀 Project

Fireblast automatically creates required database schema and provides two powerful testing interfaces:
- **QPS Load Testing**: Multi-threaded query performance with real-time metrics
- **DML Pipeline Testing**: Concurrent insert/update/delete operations with live monitoring

Perfect for evaluating Firebolt's performance characteristics or demonstrating database capabilities.

---

## Prerequisites

- **Python ≥ 3.9**
- **Firebolt Account** with API credentials
- **Two Firebolt Engines**: One for queries, one for DML operations

---

## Setup in 3 Steps

### 1. Set Up Environment

**Create a virtual environment:**

**Mac/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows:**
```cmd
python -m venv .venv
.venv\Scripts\activate
```

**Install dependencies:**
```bash
pip install -r requirements.txt
```

### 2. Create Environment Configuration
Create a `.env` file in the project root:

```bash
# Required Firebolt Configuration
FIREBOLT_ACCOUNT_NAME=your_account_name
FIREBOLT_ACCOUNT_ID=your_account_id
FIREBOLT_ACCOUNT_SECRET=your_account_secret
FIREBOLT_ACCOUNT_DATABASE_NAME=your_database_name
FIREBOLT_ACCOUNT_ENGINE_NAME=your_read_engine_name
FIREBOLT_DML_ENGINE_NAME=your_dml_engine_name
FIREBOLT_ENDPOINT=api.app.firebolt.io

# Optional Configuration
FIREBOLT_ACCOUNT_SCHEMA_NAME=public
```

> **💡 Tip**: Keep your DML engine separate from your query engine for optimal performance isolation.

### 3. Launch the Application
```bash
streamlit run streamlit_app.py
```

The app will automatically:
- ✅ Validate your credentials
- ✅ Create the required `dml_test` table schema
- ✅ Load sample application data
- ✅ Launch the interactive dashboard

---

## What the Demo Does

### **Required Workflow**

**You must start with the "Ingestion Pipeline" tab first:**
1. **Run "Ingestion Pipeline" tab** - Populates your database with test data
2. **Then use "Query Load (QPS)" tab** - Tests query performance on the populated data

**Why this order is required:**
- **Ingestion Pipeline** creates the test data that queries need
- **Query Load (QPS)** cannot produce meaningful results on an empty table
- Without data, QPS tests will return empty results and invalid performance metrics

---

### **Tab 1: Query Load (QPS) Testing** 📊
**Purpose**: Tests query performance and throughput under concurrent load
- **Best for**: Measuring read performance, query optimization testing, cache effectiveness
- **Metrics**: Queries per second, response times, percentile analysis
- **Use case**: "How fast can Firebolt handle concurrent analytical queries?"

### **Tab 2: Ingestion Pipeline (DML Operations)** 🔄
**Purpose**: Tests write performance and concurrent transaction handling
- **Best for**: Measuring write throughput, transaction conflicts, data ingestion rates
- **Metrics**: Operations per second, transaction counts, batch processing rates
- **Use case**: "How well does Firebolt handle concurrent data modifications?"

---

### **Automatic Schema Management**
On first startup, Fireblast creates the `dml_test` table with this schema:
```sql
CREATE TABLE IF NOT EXISTS dml_test (
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
PARTITION BY ltv_date;
```

### **QPS Load Testing Features**

#### **🔧 Configuration Options Explained:**

**Number of Synthetic Users (Threads)**:
- Controls concurrent query load (1-1000+ threads)
- Higher values = more concurrent queries = higher QPS potential
- **Recommended**: Start with 10-50 for initial testing
- **Performance Limits**:
  - **500+ threads**: Warning displayed, may cause performance issues
  - **1000+ threads**: Error shown, exceeds recommended limits
  - **Connection Limit**: Automatically capped at 200 concurrent database connections
- **High Load Behavior**: App automatically adjusts update intervals and uses connection pooling for >200 threads

**Use Defined Queries**:
- ✅ **Checked**: Uses your custom SQL files from `queries/` directory
- ❌ **Unchecked**: Uses random generated queries (aggregations, point lookups)
- **Best practice**: Use defined queries for realistic workload simulation

**Use Cache?**:
- ✅ **Checked**: Enables both result_cache and subresult_cache (faster responses)
- ❌ **Unchecked**: Disables result_cache but keeps subresult_cache (tests raw performance)
- **Use case**: Disable to test true query performance without result caching benefits

**Set optimizer_mode=user_guided**:
- ✅ **Checked**: Uses user-guided optimization (faster for known workloads)
- ❌ **Unchecked**: Uses automatic optimization (adapts to query patterns)
- **When to use**: Enable for predictable, well-defined query patterns

**Test Duration**: How long to run the load test (seconds)

#### **Live Metrics During Testing:**
- **Progress Bar**: Visual test completion indicator
- **Total Queries**: Cumulative query count across all threads
- **Peak QPS**: Maximum queries per second achieved
- **Response Time Metrics**: Min, Median, P90, P95 latencies
- **Live Charts**: Real-time response time and QPS visualization
- **Outlier Detection**: Queries significantly slower than median

#### **Example Defined Queries**
Fireblast includes pre-built query sets in the `queries/` directory:

**`aggregation_queries.sql`**:
- Daily app metrics summaries
- Media source performance analysis
- Time-based cohort analysis
- **Use for**: Testing analytical workload performance

**`point_lookups.sql`**:
- Single record lookups by primary key
- App-specific recent data queries
- Media source filtered queries
- **Use for**: Testing OLTP-style query performance

**`analytical_queries.sql`**:
- Complex conversion funnel analysis
- Multi-level cohort studies
- App performance ranking with CTEs
- **Use for**: Testing complex analytical query optimization

### **DML Operations Testing**

#### **Configuration Options:**

**Batch Size**:
- Controls how many records are processed per transaction
- **Higher values**: Better throughput, but higher conflict potential
- **Lower values**: More granular transactions, less conflict risk
- **Recommended**: Start with 10-50 for balanced performance

**Test Duration**: How long to run concurrent DML operations (seconds)

#### **What Happens During DML Testing:**

**3 Concurrent Worker Threads**:
1. **Insert Worker**: Adds new records with realistic test data
2. **Update Worker**: Modifies existing records (updates click counts)
3. **Delete Worker**: Removes random existing records

**Realistic Data Generation**:
- Uses actual app IDs from your `data/apps_to_use.csv` file
- Generates random but realistic media sources, attribution types
- Creates meaningful timestamp and metric values
- Simulates real-world data ingestion patterns

#### **Live Metrics During DML Testing:**
- **Operations Count**: Real-time INSERT/UPDATE/DELETE counters
- **Transaction Count**: Successfully committed transactions
- **Throughput Charts**: Operations per second over time
- **Conflict Resolution**: Graceful handling of concurrent modification conflicts

#### **💡 Best Practices:**
- **Start with Ingestion Pipeline** to populate data before QPS testing
- **Use separate engines**: Different engines for reads vs writes
- **Monitor conflicts**: Check logs for transaction conflict patterns
- **Adjust batch size**: Tune based on your conflict tolerance vs performance needs

---

##  Customizing the Demo

### **Adding Custom Queries**
1. Create a `queries/` directory in the project root
2. Add `.sql` files with your custom queries
3. Enable "Use Defined Queries" in the QPS test settings
4. Select which query files to include in your test

### **Modifying the Schema**
Edit the `ensure_schema()` function in `streamlit_app.py` to customize:
- Table name and structure
- Partitioning strategy
- Primary indexes
- Column types and constraints

### **Changing Sample Data**
Replace `data/apps_to_use.csv` with your own dataset. Ensure it has an `app_id` column for DML operations.

### **Engine Configuration**
Use different engines for different workloads:
- **Read Engine**: Optimized for analytical queries
- **DML Engine**: Optimized for transactional operations

---

## 🔧 Troubleshooting

### **"Missing Required Environment Variables"**
- **Cause**: `.env` file missing or incomplete
- **Fix**: Verify all required variables are set in your `.env` file

### **"Failed to create database schema"**
- **Cause**: Incorrect SQL syntax or insufficient database permissions
- **Fix**: This has been resolved in the latest version. Ensure your account has CREATE TABLE permissions and the DML engine is running

### **"Required data file not found"**
- **Cause**: Missing `data/apps_to_use.csv` file
- **Fix**: Ensure the data file exists or restore it from your repository

### **Connection timeouts or failures**
- **Cause**: Network issues or invalid credentials
- **Fix**: Verify your Firebolt endpoint and credentials are correct

### **No data in queries**
- **Cause**: Empty table or no data inserted yet
- **Fix**: Run the DML test first to populate data, then try QPS testing

### **Progress bar/charts disappear with high thread counts**
- **Cause**: Too many concurrent threads (>1000) overwhelming the system
- **Symptoms**: UI becomes unresponsive, charts stop updating, progress bar freezes
- **Fix**: Use recommended thread counts (10-500). The app now automatically:
  - Limits database connections to 200 maximum
  - Increases update intervals for >100 threads
  - Uses lock timeouts to prevent UI blocking
  - Shows warnings for >500 threads, errors for >1000 threads

### **"Limited to X concurrent database connections" message**
- **Cause**: Thread count exceeded database connection limits (normal behavior)
- **Effect**: Work is queued instead of creating too many connections
- **Resolution**: This is expected and prevents connection limit errors

---

## 📊 Understanding the Metrics & Live Graphs

### **QPS Testing Metrics**

#### **📈 Live Charts During Testing:**
1. **Response Time Chart**: Shows median response time over time (seconds)
   - **Y-axis**: Response time in milliseconds
   - **X-axis**: Time elapsed since test start
   - **What to look for**: Stable low latency indicates good performance

2. **Combined Performance Chart**: Multi-metric visualization
   - **Median RT**: Typical query response time
   - **P90 RT**: 90th percentile response time (outlier detection)
   - **P95 RT**: 95th percentile response time (worst-case scenarios)
   - **QPS**: Actual queries per second achieved

#### **Key Performance Indicators:**
- **Total Queries**: Cumulative query count across all threads
- **Peak QPS**: Maximum queries per second achieved during test
- **Response Times**:
  - **Min/Max**: Fastest and slowest individual queries
  - **Median**: Typical performance (50th percentile)
  - **P90**: 90% of queries complete faster than this
  - **P95**: 95% of queries complete faster than this
- **Outlier Queries**: Queries significantly slower than median (shown in table after test)

#### **What Good Performance Looks Like:**
- **Steady QPS**: Consistent queries per second without major drops
- **Low P95-Median Gap**: Small difference indicates predictable performance
- **Minimal Outliers**: Few queries in the outlier detection table
- **Stable Charts**: Response time charts without major spikes

### **DML Testing Metrics**
- **Total Operations**: Real-time INSERT/UPDATE/DELETE counts
- **Transactions**: Successfully committed transaction count
- **Throughput Charts**: Operations per second over time
- **Conflict Handling**: Automatic retry logic for transaction conflicts

### **Results Storage**
- **QPS Results**: Saved to `data/output/qps_results_YYYYMMDD_HHMMSS.json`
- **Contains**: Full response time data, timestamps, test parameters
- **Use for**: Post-test analysis, performance trending, reporting

---


## 🤝 Contributing

Found a bug or want to add a feature? Contributions welcome!

1. Fork the repository
2. Create a feature branch
3. Make your improvements
4. Submit a pull request

---

**Ready to see Firebolt in action? Run `streamlit run streamlit_app.py` and start testing!** 🔥
