"""
Firebolt Core Integration for DreamBolt
======================================

Integrates with Firebolt Core - the free, self-hosted edition of Firebolt's 
distributed query engine. Uses Docker deployment and PostgreSQL protocol.

Features:
- 🆓 Free, self-hosted Firebolt Core deployment
- 🐳 Docker-based setup and management  
- 🛢️ PostgreSQL-compliant SQL interface
- 📊 High-performance analytics capabilities
- 🔄 Seamless workload compatibility with managed Firebolt

Documentation: https://docs.firebolt.io/firebolt-core
"""
import subprocess
import time
import os
import psycopg2
import pandas as pd
from typing import Optional, Dict, Tuple, List
from pathlib import Path
from loguru import logger
import docker
from contextlib import contextmanager


class FireboltCore:
    """
    Firebolt Core manager for DreamBolt integration.
    
    Manages Docker deployment, database connections, and data operations
    using the free, self-hosted Firebolt Core edition.
    """
    
    def __init__(
        self, 
        container_name: str = "dreambolt-firebolt-core",
        port: int = 5432,
        data_dir: Optional[str] = None,
        memory_limit: str = "4g"
    ):
        """
        Initialize Firebolt Core manager.
        
        Args:
            container_name: Docker container name
            port: PostgreSQL port (default: 5432)
            data_dir: Host directory for data persistence
            memory_limit: Docker memory limit
        """
        self.container_name = container_name
        self.port = port
        self.data_dir = Path(data_dir) if data_dir else Path.cwd() / ".firebolt-data"
        self.memory_limit = memory_limit
        
        # Docker image for Firebolt Core
        self.image = "ghcr.io/firebolt-db/firebolt-core:preview-rc"
        
        # Connection details
        self.host = "localhost"
        self.database = "dreambolt"
        self.user = "firebolt"
        self.password = "firebolt"
        
        # Initialize Docker client
        try:
            self.docker_client = docker.from_env()
            logger.info("✅ Docker client initialized")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Docker client: {e}")
            logger.error("Please ensure Docker is installed and running")
            raise
    
    def setup(self) -> bool:
        """
        Set up Firebolt Core infrastructure.
        
        Returns:
            True if setup successful, False otherwise
        """
        logger.info("🚀 Setting up Firebolt Core infrastructure...")
        
        try:
            # 1. Create data directory
            self._ensure_data_directory()
            
            # 2. Pull Firebolt Core Docker image
            if not self._pull_image():
                return False
            
            # 3. Start Firebolt Core container
            if not self._start_container():
                return False
            
            # 4. Wait for service to be ready
            if not self._wait_for_ready():
                return False
            
            # 5. Initialize database
            if not self._initialize_database():
                return False
            
            logger.info("✅ Firebolt Core setup completed successfully!")
            return True
            
        except Exception as e:
            logger.error(f"❌ Firebolt Core setup failed: {e}")
            return False
    
    def _ensure_data_directory(self):
        """Create data directory for persistence."""
        self.data_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"📁 Data directory: {self.data_dir}")
    
    def _pull_image(self) -> bool:
        """Pull Firebolt Core Docker image."""
        try:
            logger.info(f"📥 Pulling Firebolt Core image: {self.image}")
            self.docker_client.images.pull(self.image)
            logger.info("✅ Image pulled successfully")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to pull image: {e}")
            return False
    
    def _start_container(self) -> bool:
        """Start Firebolt Core Docker container."""
        try:
            # Check if container already exists
            existing = self._get_container()
            if existing:
                if existing.status == "running":
                    logger.info("✅ Firebolt Core container already running")
                    return True
                else:
                    logger.info("🔄 Starting existing container...")
                    existing.start()
                    return True
            
            # Create new container
            logger.info("🐳 Creating new Firebolt Core container...")
            
            container = self.docker_client.containers.run(
                self.image,
                name=self.container_name,
                ports={5432: self.port},
                volumes={str(self.data_dir): {'bind': '/var/lib/firebolt', 'mode': 'rw'}},
                environment={
                    'FIREBOLT_DATABASE': self.database,
                    'FIREBOLT_USER': self.user,
                    'FIREBOLT_PASSWORD': self.password
                },
                mem_limit=self.memory_limit,
                detach=True,
                restart_policy={"Name": "unless-stopped"}
            )
            
            logger.info(f"✅ Container created: {container.short_id}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to start container: {e}")
            return False
    
    def _get_container(self):
        """Get existing Firebolt Core container."""
        try:
            return self.docker_client.containers.get(self.container_name)
        except docker.errors.NotFound:
            return None
    
    def _wait_for_ready(self, timeout: int = 120) -> bool:
        """Wait for Firebolt Core to be ready."""
        logger.info("⏳ Waiting for Firebolt Core to be ready...")
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                # Try to connect
                with self._get_connection() as conn:
                    with conn.cursor() as cursor:
                        cursor.execute("SELECT 1")
                        cursor.fetchone()
                
                logger.info("✅ Firebolt Core is ready!")
                return True
                
            except Exception:
                time.sleep(2)
                continue
        
        logger.error(f"❌ Firebolt Core not ready after {timeout} seconds")
        return False
    
    def _initialize_database(self) -> bool:
        """Initialize default database and schema."""
        try:
            logger.info("🗄️  Initializing database schema...")
            
            with self._get_connection() as conn:
                with conn.cursor() as cursor:
                    # Create database if not exists
                    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
                    
                    # Set default database
                    cursor.execute(f"USE {self.database}")
                    
                    # Create schema for DreamBolt tables
                    cursor.execute("CREATE SCHEMA IF NOT EXISTS dreambolt")
                    
                conn.commit()
            
            logger.info("✅ Database initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize database: {e}")
            return False
    
    @contextmanager
    def _get_connection(self):
        """Get PostgreSQL connection to Firebolt Core."""
        conn = None
        try:
            conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password,
                connect_timeout=30
            )
            yield conn
        finally:
            if conn:
                conn.close()
    
    def create_table(self, table_name: str, df: pd.DataFrame, schema: str = "dreambolt") -> bool:
        """
        Create table from DataFrame schema.
        
        Args:
            table_name: Table name
            df: DataFrame to infer schema from
            schema: Schema name (default: dreambolt)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info(f"📋 Creating table: {schema}.{table_name}")
            
            # Generate CREATE TABLE statement
            create_sql = self._generate_create_table_sql(table_name, df, schema)
            
            with self._get_connection() as conn:
                with conn.cursor() as cursor:
                    # Drop existing table if exists
                    cursor.execute(f"DROP TABLE IF EXISTS {schema}.{table_name}")
                    
                    # Create new table
                    cursor.execute(create_sql)
                    
                conn.commit()
            
            logger.info(f"✅ Table created: {schema}.{table_name}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to create table {table_name}: {e}")
            return False
    
    def load_data(self, table_name: str, df: pd.DataFrame, schema: str = "dreambolt") -> bool:
        """
        Load DataFrame data into Firebolt Core table.
        
        Args:
            table_name: Target table name
            df: DataFrame to load
            schema: Schema name (default: dreambolt)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info(f"📊 Loading {len(df)} rows into {schema}.{table_name}")
            
            with self._get_connection() as conn:
                with conn.cursor() as cursor:
                    # Use efficient batch INSERT
                    self._batch_insert(cursor, table_name, df, schema)
                    
                conn.commit()
            
            logger.info(f"✅ Data loaded successfully: {len(df)} rows")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to load data: {e}")
            return False
    
    def load_from_parquet(self, table_name: str, parquet_path: str, schema: str = "dreambolt") -> bool:
        """
        Load data from Parquet file into Firebolt Core.
        
        Args:
            table_name: Target table name
            parquet_path: Path to Parquet file
            schema: Schema name (default: dreambolt)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Read Parquet file
            df = pd.read_parquet(parquet_path)
            
            # Create table and load data
            if self.create_table(table_name, df, schema):
                return self.load_data(table_name, df, schema)
            else:
                return False
                
        except Exception as e:
            logger.error(f"❌ Failed to load from Parquet: {e}")
            return False
    
    def query(self, sql: str) -> pd.DataFrame:
        """
        Execute SQL query and return results as DataFrame.
        
        Args:
            sql: SQL query string
            
        Returns:
            DataFrame with query results
        """
        try:
            with self._get_connection() as conn:
                return pd.read_sql(sql, conn)
                
        except Exception as e:
            logger.error(f"❌ Query failed: {e}")
            return pd.DataFrame()
    
    def get_table_info(self, table_name: str, schema: str = "dreambolt") -> Dict:
        """
        Get table information and statistics.
        
        Args:
            table_name: Table name
            schema: Schema name
            
        Returns:
            Dictionary with table metadata
        """
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cursor:
                    # Get table schema
                    cursor.execute(f"""
                        SELECT column_name, data_type, is_nullable
                        FROM information_schema.columns 
                        WHERE table_schema = '{schema}' AND table_name = '{table_name}'
                        ORDER BY ordinal_position
                    """)
                    columns = cursor.fetchall()
                    
                    # Get row count
                    cursor.execute(f"SELECT COUNT(*) FROM {schema}.{table_name}")
                    row_count = cursor.fetchone()[0]
                    
                    return {
                        "schema": schema,
                        "table": table_name,
                        "columns": [{"name": col[0], "type": col[1], "nullable": col[2]} for col in columns],
                        "row_count": row_count
                    }
                    
        except Exception as e:
            logger.error(f"❌ Failed to get table info: {e}")
            return {}
    
    def _generate_create_table_sql(self, table_name: str, df: pd.DataFrame, schema: str) -> str:
        """Generate CREATE TABLE SQL from DataFrame schema."""
        column_definitions = []
        
        for col, dtype in df.dtypes.items():
            # Map pandas dtypes to Firebolt SQL types
            if dtype == 'int64':
                fb_type = 'BIGINT'
            elif dtype == 'int32':
                fb_type = 'INTEGER'
            elif dtype == 'float64':
                fb_type = 'DOUBLE PRECISION'
            elif dtype == 'float32':
                fb_type = 'REAL'
            elif dtype == 'bool':
                fb_type = 'BOOLEAN'
            elif dtype == 'datetime64[ns]':
                fb_type = 'TIMESTAMP'
            elif 'datetime' in str(dtype):
                fb_type = 'TIMESTAMP'
            else:
                # Default to TEXT for strings and unknown types
                fb_type = 'TEXT'
            
            # Clean column name for SQL compatibility
            clean_col = col.replace(' ', '_').replace('-', '_').lower()
            column_definitions.append(f'    "{clean_col}" {fb_type}')
        
        # Use first column as primary index (Firebolt best practice)
        first_col = list(df.columns)[0].replace(' ', '_').replace('-', '_').lower()
        
        create_sql = f"""
CREATE TABLE {schema}.{table_name} (
{','.join(column_definitions)}
)
PRIMARY INDEX "{first_col}"
"""
        
        return create_sql
    
    def _batch_insert(self, cursor, table_name: str, df: pd.DataFrame, schema: str):
        """Perform efficient batch INSERT."""
        # Prepare column names
        columns = [col.replace(' ', '_').replace('-', '_').lower() for col in df.columns]
        columns_str = ', '.join([f'"{col}"' for col in columns])
        
        # Prepare values placeholder
        placeholders = ', '.join(['%s'] * len(columns))
        
        # Convert DataFrame to list of tuples
        data = []
        for _, row in df.iterrows():
            # Handle NaN values
            values = []
            for val in row:
                if pd.isna(val):
                    values.append(None)
                else:
                    values.append(val)
            data.append(tuple(values))
        
        # Execute batch insert
        insert_sql = f"INSERT INTO {schema}.{table_name} ({columns_str}) VALUES ({placeholders})"
        cursor.executemany(insert_sql, data)
    
    def stop(self):
        """Stop Firebolt Core container."""
        try:
            container = self._get_container()
            if container and container.status == "running":
                logger.info("🛑 Stopping Firebolt Core container...")
                container.stop()
                logger.info("✅ Container stopped")
            else:
                logger.info("ℹ️  Container not running")
        except Exception as e:
            logger.error(f"❌ Failed to stop container: {e}")
    
    def remove(self):
        """Remove Firebolt Core container and data."""
        try:
            # Stop container first
            self.stop()
            
            # Remove container
            container = self._get_container()
            if container:
                logger.info("🗑️  Removing Firebolt Core container...")
                container.remove()
                logger.info("✅ Container removed")
            
            # Optionally remove data directory
            # Note: Commented out for safety - user can manually delete if desired
            # import shutil
            # shutil.rmtree(self.data_dir)
            # logger.info("✅ Data directory removed")
            
        except Exception as e:
            logger.error(f"❌ Failed to remove container: {e}")
    
    def status(self) -> Dict:
        """Get Firebolt Core status information."""
        try:
            container = self._get_container()
            
            if not container:
                return {"status": "not_created", "container": None}
            
            # Try to connect and get basic info
            try:
                with self._get_connection() as conn:
                    with conn.cursor() as cursor:
                        cursor.execute("SELECT version()")
                        version = cursor.fetchone()[0]
                        
                        cursor.execute("SELECT current_database()")
                        current_db = cursor.fetchone()[0]
                
                connection_status = "connected"
            except:
                connection_status = "unreachable"
                version = None
                current_db = None
            
            return {
                "status": container.status,
                "container_id": container.short_id,
                "image": container.image.tags[0] if container.image.tags else "unknown",
                "ports": container.ports,
                "connection": connection_status,
                "version": version,
                "database": current_db,
                "data_dir": str(self.data_dir)
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to get status: {e}")
            return {"status": "error", "error": str(e)}


# Convenience functions for DreamBolt integration
def setup_firebolt_core() -> FireboltCore:
    """Set up Firebolt Core with default configuration."""
    fb_core = FireboltCore()
    
    if fb_core.setup():
        return fb_core
    else:
        raise RuntimeError("Failed to set up Firebolt Core")


def get_firebolt_core() -> Optional[FireboltCore]:
    """Get existing Firebolt Core instance if running."""
    fb_core = FireboltCore()
    
    status = fb_core.status()
    if status.get("status") == "running" and status.get("connection") == "connected":
        return fb_core
    else:
        return None


if __name__ == "__main__":
    # Demo/test script
    print("🧪 Firebolt Core Integration Demo")
    
    # Initialize Firebolt Core
    fb_core = FireboltCore()
    
    # Show current status
    status = fb_core.status()
    print(f"📊 Current status: {status}")
    
    # Set up if needed
    if status.get("status") != "running":
        print("🚀 Setting up Firebolt Core...")
        if fb_core.setup():
            print("✅ Setup completed!")
        else:
            print("❌ Setup failed!")
            exit(1)
    
    # Test with sample data
    print("📊 Testing with sample data...")
    sample_df = pd.DataFrame({
        'id': [1, 2, 3, 4, 5],
        'name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'],
        'score': [95.5, 87.2, 92.8, 88.9, 91.1],
        'active': [True, False, True, True, False]
    })
    
    # Create and load table
    if fb_core.create_table("demo_table", sample_df):
        if fb_core.load_data("demo_table", sample_df):
            print("✅ Demo table created and loaded!")
            
            # Query the data
            result = fb_core.query("SELECT * FROM dreambolt.demo_table ORDER BY score DESC")
            print(f"📊 Query result:\n{result}")
            
            # Get table info
            info = fb_core.get_table_info("demo_table")
            print(f"ℹ️  Table info: {info}")
        else:
            print("❌ Failed to load demo data")
    else:
        print("❌ Failed to create demo table")
    
    print("🏁 Demo completed!") 