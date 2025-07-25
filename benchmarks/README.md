# Database Benchmark Suite

A comprehensive, vendor-neutral benchmarking platform for evaluating data warehouse performance across Snowflake, Redshift, Firebolt, and BigQuery.

## Overview

This tool provides standardized performance testing capabilities to help organizations make informed decisions about data warehouse selection and optimization. It supports both interactive analysis through a web interface and high-concurrency load testing for production-scale evaluation.

## Features

- **Multi-Vendor Support**: Test Snowflake, Amazon Redshift, Firebolt, and Google BigQuery
- **Dual Client Architecture**: Interactive web UI for analysis, K6 client for high-concurrency testing
- **Standardized Benchmarks**: Pre-built test suites including TPC-H and custom analytical workloads
- **Real-Time Monitoring**: Live performance metrics and comparative analysis
- **Flexible Configuration**: Environment-based credential management and customizable test parameters
- **Export Capabilities**: CSV and visual reports for analysis and documentation

## Quick Start

### Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher (for K6 client)
- Access credentials for at least one supported data warehouse



### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd database-benchmark-suite
   ```

2. **Set up the environment:**
   ```bash
   ./scripts/setup.sh
   ```

3. **Configure credentials:**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

4. **Start the web interface:**
   ```bash
   ./scripts/run-python.sh
   ```

5. **Open your browser to http://localhost:8501**

## Architecture

### Components

**Python Client (`src/python/`)**
- Streamlit-based web interface for interactive benchmarking
- Suitable for performance analysis and moderate concurrency testing (< 100 QPS)
- Real-time visualization and comparative analysis

**K6 Client (`src/k6/`)**
- High-performance testing client for concurrency evaluation
- Supports hundreds to thousands of queries per second
- Detailed performance metrics and load testing capabilities

**Benchmarks (`benchmarks/`)**
- Standardized SQL test suites organized by benchmark type
- Vendor-specific optimizations where appropriate
- Extensible framework for custom benchmarks

### Supported Databases

| Database | Connection Method | Authentication |
|----------|-------------------|----------------|
| **Snowflake** | JDBC/ODBC | Username/Password, Key Pair |
| **Amazon Redshift** | PostgreSQL Protocol | Username/Password, IAM |
| **Firebolt** | REST API | Service Account |
| **Google BigQuery** | Cloud Client Library | Service Account JSON |


### Performance Recommendations

**Concurrency Guidelines:**
- **Snowflake**: 1-10 concurrent queries (scales with warehouse size)
- **Redshift**: 1-5 concurrent queries (depends on cluster configuration)  
- **Firebolt**: 1-10 concurrent queries (optimized for concurrency)
- **BigQuery**: 1-20 concurrent queries (designed for high concurrency)

**Benchmark Configuration:**
- **Query Set Runs**: 3-5 for reliable averages, 1-3 for quick analysis
- **Warmup Queries**: Recommended for accurate cold-start performance measurement
- **Setup Scripts**: Optional table creation and data loading

## Usage

### Web Interface

1. **Start the application:**
   ```bash
   ./scripts/run-python.sh
   ```

2. **Configure test parameters:**
   - Select target databases
   - Choose benchmark suite (FireScale, TPC-H, custom)
   - Set concurrency and iteration parameters

3. **Run benchmarks:**
   - Execute setup scripts (if needed)
   - Run warmup queries (recommended)
   - Execute benchmark suite
   - View real-time results and analysis

### Command Line (K6)

```bash
# High-concurrency testing
./scripts/run-k6.sh

# Custom configuration
K6_CONFIG=custom-config.json ./scripts/run-k6.sh
```

### Docker Deployment

```bash
# Basic deployment
docker-compose up

# Development environment
docker-compose --profile dev up

# Production with monitoring
docker-compose --profile production --profile monitoring up
```

## Benchmark Suites

### FireScale
- 25-query analytical workload
- Covers aggregations, joins, window functions, and complex analytics
- Available for all supported databases

### TPC-H
- Industry-standard decision support benchmark
- Configurable data scales
- Comparative performance analysis

### Custom Benchmarks
- Extensible framework for organization-specific workloads
- SQL file-based configuration
- Vendor-specific optimization support





## Adding New Vendors

1. **Create connector class:**
   ```python
   # src/python/src/connectors/new_vendor.py
   from .base import WarehouseConnector
   
   class NewVendorConnector(WarehouseConnector):
       def connect(self):
           # Implementation
           pass
   ```

2. **Register connector:**
   ```python
   # src/python/src/connectors/__init__.py
   VENDOR_CONNECTORS = {
       'new_vendor': NewVendorConnector,
   }
   ```

3. **Add environment configuration:**
   ```python
   # src/python/src/env_config.py
   # Add vendor-specific environment variable handling
   ```

4. **Create benchmark SQL files:**
   ```bash
   mkdir benchmarks/FireScale/new_vendor
   # Add vendor-specific SQL files
   ```

## Security

- **Credential Management**: Environment variable-based configuration
- **Input Validation**: SQL injection protection and parameter sanitization
- **Network Security**: TLS/SSL connections for all database communications
- **Dependency Scanning**: Regular vulnerability assessment and updates
- **Access Control**: Non-root container execution and minimal privilege requirements

## Performance Considerations

- **Connection Pooling**: Efficient connection management for concurrent workloads
- **Query Optimization**: Vendor-specific performance tuning where applicable
- **Result Caching**: Configurable caching behavior for accurate benchmark timing
- **Resource Monitoring**: Memory and CPU usage tracking during execution

## Troubleshooting

### Common Issues

**Connection Failures:**
- Verify credentials in `.env` file
- Check network connectivity and firewall settings
- Confirm database service availability

**Performance Issues:**
- Adjust concurrency settings based on target database capabilities
- Ensure adequate system resources for test execution
- Consider database warm-up procedures

**Test Failures:**
- Review query compatibility across database vendors
- Check for vendor-specific SQL syntax requirements
- Validate benchmark data setup and schema alignment



