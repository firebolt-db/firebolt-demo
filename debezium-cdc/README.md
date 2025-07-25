# Real-Time Sports Odds Tracking with Debezium CDC

A complete demonstration of real-time Change Data Capture (CDC) from PostgreSQL to Firebolt using Debezium, showcasing live sports betting odds data streaming and visualization.

## Table of Contents

- [Features / Demo Highlights](#features--demo-highlights)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Configuration Details](#configuration-details)
- [Running the Demo](#running-the-demo)
- [Troubleshooting Guide](#troubleshooting-guide)
- [Project Structure](#project-structure)
- [Contributing / License](#contributing--license)

## Features / Demo Highlights

- **Real-time CDC pipeline** from PostgreSQL to Firebolt using Debezium
- **Live data visualization** with Streamlit showing streaming odds updates
- **Simulated sports betting data** with multiple bookmakers and games
- **Auto-refreshing dashboard** displaying odds changes in real-time
- **Complete Docker setup** for easy local development
- **Scalable architecture** using Kafka for message streaming

## Prerequisites

- **OS**: Linux, macOS, or Windows with WSL2
- **Docker & Docker Compose**: Latest version
- **Node.js**: Version 16 or higher
- **Python**: Version 3.8 or higher
- **Firebolt Account**: Access to Firebolt cloud platform
- **Firebolt JDBC Driver**: Download from [releases](https://github.com/firebolt-db/jdbc/releases)

## Quick Start

### 1. Clone the repository
```bash
git clone <repository-url>
cd "debezium cdc"
```

### 2. Download Firebolt JDBC Driver
```bash
# Create lib directory
mkdir -p firebolt_jdbc_lib

# Download the latest JDBC driver (example for v3.6.2)
wget -O firebolt_jdbc_lib/firebolt-jdbc-3.6.2.jar \
  https://github.com/firebolt-db/jdbc/releases/download/v3.6.2/firebolt-jdbc-3.6.2.jar
```

### 3. Configure Docker volumes
```bash
# Update docker-compose.yml with your absolute path
# Replace the volumes line in set-up/docker-compose.yml:
# From: /Users/stephenberg/firebolt_jdbc_lib/firebolt-jdbc-3.6.2.jar:/kafka/libs/firebolt-jdbc-3.6.2.jar
# To: $(pwd)/firebolt_jdbc_lib/firebolt-jdbc-3.6.2.jar:/kafka/libs/firebolt-jdbc-3.6.2.jar
```

### 4. Set up Firebolt configuration
```bash
# Create environment file
cp env.example .env
# Edit .env with your Firebolt credentials (see Configuration Details below)
```

### 5. Install Node.js dependencies
```bash
cd fake-sports-data
npm install
cd ..
```

### 6. Create Python virtual environment
```bash
cd streamlit
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate

pip install -r requirements.txt

cd ..
```

### 7. Start the infrastructure
```bash
cd set-up
docker compose up -d
cd ..
```

### 8. Set up database schema
```bash
# Create tables in PostgreSQL (optional - tables will be created by data scripts)
docker exec -i set-up-postgres-1 psql -U admin -d postgres < setup_database.sql
```

### 9. Set up Kafka connectors
```bash
# Wait for services to start (about 30-60 seconds)
sleep 60

# Create source connector (PostgreSQL)
curl -X POST http://localhost:8083/connectors \
  -H "Content-Type: application/json" \
  -d @set-up/source-connector.json

# Create sink connector (Firebolt)
curl -X POST http://localhost:8083/connectors \
  -H "Content-Type: application/json" \
  -d @set-up/firebolt-sink-connector.json
```

### 10. Initialize database with sample data
```bash
cd fake-sports-data
node insert_fake_data.js
cd ..
```

### 11. Launch the demo
```bash
cd streamlit
source .venv/bin/activate
streamlit run streamlitui.py
```

### 12. Start real-time data generation
```bash
# In a new terminal
cd fake-sports-data
node ingest_data.js
```

## Configuration Details

### Environment Variables (.env file)

Create a `.env` file in the project root:

```env
# Firebolt Configuration
FIREBOLT_ACCOUNT=your-account-name
FIREBOLT_ENGINE_INGESTION=your-ingestion-engine
FIREBOLT_ENGINE_ANALYTICS=your-analytics-engine
FIREBOLT_DATABASE=your-database-name
FIREBOLT_CLIENT_ID=your-client-id
FIREBOLT_CLIENT_SECRET=your-client-secret

# PostgreSQL Configuration (for Docker)
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin
POSTGRES_DB=postgres

# Kafka Configuration
KAFKA_BROKER=localhost:9092
```

### Firebolt Database Setup

Before running the demo, ensure your Firebolt database has the required schema:

```sql
-- Connect to your Firebolt database and run:
CREATE DATABASE IF NOT EXISTS demo_debezium_cdc;

-- Tables will be auto-created by the sink connector
-- but you can verify with:
-- SHOW TABLES;
```

### Docker Compose Customization

Update `set-up/docker-compose.yml` volumes section:
```yaml
volumes:
  - /absolute/path/to/your/project/firebolt_jdbc_lib/firebolt-jdbc-3.6.2.jar:/kafka/libs/firebolt-jdbc-3.6.2.jar
```

## Running the Demo

### Demo Flow

1. **Start Infrastructure**: Docker containers provide Kafka, PostgreSQL, and connectors
2. **Initialize Data**: Run `insert_fake_data.js` to create initial games and odds
3. **Launch Visualization**: Streamlit app connects to Firebolt and displays data
4. **Generate Live Data**: Run `ingest_data.js` to simulate real-time odds updates
5. **Watch Real-time Updates**: Odds changes appear instantly in the Streamlit dashboard

### Verification Commands

```bash
# Check connector status
curl -X GET http://localhost:8083/connectors/postgres-source-connector/status
curl -X GET http://localhost:8083/connectors/firebolt-sink-connector/status

# Monitor Kafka topics
docker exec -it set-up-kafka-1 kafka-console-consumer.sh \
  --bootstrap-server localhost:9092 \
  --topic cdc.public.odds_history \
  --from-beginning

# Check PostgreSQL data
docker exec -it set-up-postgres-1 psql -U admin -d postgres \
  -c "SELECT COUNT(*) FROM games; SELECT COUNT(*) FROM odds_history;"
```

## Troubleshooting Guide

| Error | Cause | Solution |
|-------|-------|----------|
| `ERROR: Cannot find JDBC driver` | Missing Firebolt JDBC jar | Download JDBC driver and update docker-compose.yml path |
| `Connection refused to Firebolt` | Invalid credentials or network | Check Firebolt credentials in .env and connector config |
| `Connector failed to start` | Service dependencies not ready | Wait 60s after `docker compose up`, then retry connector setup |
| `No module named 'streamlit'` | Python dependencies not installed | Activate venv and run `pip install -r requirements.txt` |
| `pip install -r requirements.txt` fails | Package version conflicts | Try: `pip install --prefer-binary -r requirements.txt` |
| `pandas compilation error on Python 3.13` | Source compilation incompatibility | Use `--prefer-binary` flag and pandas>=2.2.0 |
| `DLL load failed while importing _bcrypt` | streamlit_authenticator compatibility | Install specific bcrypt version: `pip install bcrypt==4.0.1` |
| `Building wheel for cryptography failed` | Missing Rust compiler | Install Rust: `curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh` |
| `firebolt-sdk version conflict` | Outdated SDK version | Use latest version: `pip install firebolt-sdk --upgrade` |
| `ECONNREFUSED localhost:5432` | PostgreSQL not accessible | Ensure Docker containers are running with `docker ps` |
| `Topics not found` | Connectors not configured | Verify connector status and recreate if needed |
| `Empty dashboard in Streamlit` | No data in Firebolt | Run `insert_fake_data.js` and check connector logs |
| `Permission denied: firebolt-jdbc-*.jar` | File permissions issue | Check file permissions: `chmod 644 firebolt_jdbc_lib/*.jar` |

### Python Package Installation Issues

If `pip install -r requirements.txt` fails, try these alternative approaches:

```bash
# Option 1: Use binary wheels (recommended - avoids compilation)
pip install --upgrade pip
pip install --prefer-binary -r requirements.txt

# Option 2: Try minimal requirements (no version constraints)
pip install -r requirements-minimal.txt

# Option 3: Install packages individually
pip install streamlit>=1.28.0 pandas>=2.2.0 firebolt-sdk plotly>=5.15.0 numerize fastavro

# Option 4: Install with no cache (if dependency conflicts persist)
pip install --no-cache-dir -r requirements.txt

# Option 5: For Apple Silicon Macs (if cryptography fails)
export LDFLAGS="-L$(brew --prefix openssl)/lib"
export CPPFLAGS="-I$(brew --prefix openssl)/include"
pip install cryptography
pip install -r requirements.txt
```

### Debug Commands

```bash
# View connector logs
docker logs set-up-connect-1

# Check Kafka Connect status
curl -X GET http://localhost:8083/connectors

# PostgreSQL connection test
docker exec -it set-up-postgres-1 psql -U admin -d postgres -c "\dt"

# Python environment debugging
python -c "import streamlit; print(streamlit.__version__)"
python -c "import firebolt; print('Firebolt SDK installed successfully')"
```

## Project Structure

```
debezium cdc/
├── Demo - Postgres CDC Sync to Firebolt.md    # Original demo documentation
├── fake-sports-data/                          # Node.js data generation scripts
│   ├── package.json                          # Node dependencies
│   ├── package-lock.json                     # Node version lock file
│   ├── insert_fake_data.js                   # Initial data seeding
│   └── ingest_data.js                         # Real-time data generation
├── set-up/                                    # Infrastructure configuration
│   ├── docker-compose.yml                    # Docker services definition
│   ├── source-connector.json                 # Debezium source connector config
│   └── firebolt-sink-connector.json          # Firebolt sink connector config
├── streamlit/                                 # Python visualization app
│   ├── requirements.txt                      # Python dependencies (with versions)
│   ├── requirements-minimal.txt              # Minimal dependencies (fallback option)
│   └── streamlitui.py                         # Main Streamlit application
├── firebolt_jdbc_lib/                         # JDBC driver directory (create this)
│   └── firebolt-jdbc-3.6.2.jar              # Download from Firebolt releases
├── setup_database.sql                        # PostgreSQL schema setup script
├── env.example                               # Environment variables template
├── .env                                       # Your environment variables (create this)
└── README.md                                  # This comprehensive guide
```

## Contributing / License

This is a demonstration project for showcasing Debezium CDC capabilities with Firebolt.

For questions or issues:
- Check the [Firebolt Debezium documentation](https://docs.firebolt.io/Guides/integrations/debezium.html)
- Review Kafka Connect logs for connector issues
- Ensure all prerequisites are properly installed

**Note**: This demo uses hard-coded test credentials for Firebolt in the original configuration. In production, always use environment variables and proper secrets management.
