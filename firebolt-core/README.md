# Firebolt Core NYC Parking Demo

Analyze 21.5 million New York City parking violations with sub‑second queries.

## Features

* Sub‑second analytical queries on 21.5 million rows
* Interactive Streamlit dashboard for ad‑hoc exploration
* Five benchmark workloads illustrating typical analytics patterns
* Helper scripts for setup, data loading, status checks, and cleanup
* Real‑time visual feedback while queries run

## Prerequisites

* **Docker Engine** with at least 16 GB RAM
* **Python 3.11** or later
* macOS, Linux, or Windows 10/11 with WSL 2
* Reliable broadband connection to pull the 4.5 GB dataset

## Installation

1. **Clone the repository.** Downloading the code locally lets you build the containers and run the dashboard.

   ```bash
   cd firebolt-core
   ```

2. **Create a Python virtual environment.** Isolating dependencies prevents version conflicts with other projects.

   ```bash
   python3 -m venv .venv           # Windows: .venv\Scripts\activate
   ```

3. **Install Python dependencies.**

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Start Firebolt Core.** This script launches the database container and primes it for incoming data. Once it finishes, **open a new terminal window or tab** in the same project directory for the remaining steps.

   ```bash
   chmod +x setup_core.sh
   ./setup_core.sh --auto-run
   # Watch for: "Firebolt Core is ready!"
   ```

5. **Load the NYC parking dataset.** The dataset arrives compressed from S3, then imports into a partitioned table.

   ```bash
   chmod +x load_data.sh
   ./load_data.sh
   # Expect: "Data loading completed successfully!"
   ```

6. **Launch the Streamlit dashboard.** The dashboard provides visual exploration and benchmark controls.

   ```bash
   streamlit run app/streamlit_app.py
   # Open http://localhost:8501 in your browser
   ```

### Typical Pitfalls and Quick Fixes

* **Port 8501 already in use** – Another Streamlit session is running. Run `lsof -ti:8501 | xargs kill -9` then rerun.
* **`relation violations does not exist`** – Data load failed or ran in the wrong container. Rerun `./load_data.sh` and confirm output.
* **`firebolt-core` container exited** – Docker memory limit too low. Allocate at least 6 GB in Docker Desktop settings.

## Usage

### Run Benchmarks

```bash
./check_status.sh      # Confirms database, data, and Python env are ready
# In the Streamlit UI, click "Run All Benchmarks"
```

The dashboard streams results every second so you can watch latency drop as indexes kick in.

### Explore the Data

* Use the sidebar filters (street, vehicle make, fine amount) and observe instant updates.
* Click any bar or line in the charts to drill into raw rows behind that aggregate.
* Download a slice by selecting “Export to CSV” in the Data tab.

### Direct SQL Access

Run ad‑hoc queries without leaving your terminal.

```bash
# Open an interactive shell
docker exec -it firebolt-core fb -C

# Example: total tickets in 2024
SELECT COUNT(*)
FROM violations
WHERE issue_date BETWEEN '2024-01-01' AND '2024-12-31';
```

### Cleanup

Free disk space and stop all containers when finished.

```bash
chmod +x cleanup.sh
./cleanup.sh
```

Running cleanup is helpful on shared machines so teammates start with a clean slate.
