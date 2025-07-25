# Multi-stage Dockerfile for Database Benchmark Suite
# Provides both Python (Streamlit) and K6 clients in a single container

# Stage 1: Python environment
FROM python:3.11-slim as python-base

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"

# Create application directory
WORKDIR /app

# Create non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copy Python requirements first for better caching
COPY src/python/requirements.txt ./requirements.txt
COPY requirements-dev.txt ./requirements-dev.txt

# Install Python dependencies
RUN python -m venv .venv && \
    .venv/bin/pip install --no-cache-dir --upgrade pip && \
    .venv/bin/pip install --no-cache-dir -r requirements.txt

# Stage 2: Node.js environment for K6
FROM node:18-slim as node-base

WORKDIR /app/k6

# Copy K6 package files
COPY src/k6/package*.json ./

# Install Node.js dependencies
RUN npm ci --only=production && \
    npm cache clean --force

# Stage 3: K6 installation
FROM grafana/k6:latest as k6-binary

# Stage 4: Final runtime image
FROM python:3.11-slim as runtime

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    libpq5 \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH" \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Create application directory
WORKDIR /app

# Copy Python virtual environment from python-base stage
COPY --from=python-base --chown=appuser:appuser /app/.venv /app/.venv

# Copy K6 binary from k6-binary stage
COPY --from=k6-binary /usr/bin/k6 /usr/local/bin/k6

# Copy Node.js dependencies from node-base stage
COPY --from=node-base --chown=appuser:appuser /app/k6/node_modules /app/src/k6/node_modules

# Copy application source code
COPY --chown=appuser:appuser src/ ./src/
COPY --chown=appuser:appuser benchmarks/ ./benchmarks/
COPY --chown=appuser:appuser scripts/ ./scripts/
COPY --chown=appuser:appuser .env.example ./
COPY --chown=appuser:appuser README.md CONTRIBUTING.md LICENSE pyproject.toml ./

# Make scripts executable
RUN chmod +x scripts/*.sh

# Create directories for output and logs
RUN mkdir -p /app/benchmark_results /app/logs && \
    chown -R appuser:appuser /app/benchmark_results /app/logs

# Switch to non-root user
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Expose Streamlit port
EXPOSE 8501

# Default command runs Streamlit
CMD ["python", "-m", "streamlit", "run", "src/python/src/main.py", "--server.port=8501", "--server.address=0.0.0.0"]

# Labels for metadata
LABEL org.opencontainers.image.title="Database Benchmark Suite"
LABEL org.opencontainers.image.description="Comprehensive benchmarking suite for data warehouses"
LABEL org.opencontainers.image.vendor="Database Benchmark Suite Contributors"
LABEL org.opencontainers.image.licenses="MIT"
LABEL org.opencontainers.image.source="https://github.com/your-org/database-benchmark-suite"