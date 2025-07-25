"""
Firebolt Integration for DreamBolt with Firebolt Core Support
============================================================

Enhanced Firebolt integration supporting both:
1. Managed Firebolt (cloud) - original implementation
2. Firebolt Core (self-hosted) - new Docker-based integration

Firebolt Core Features:
- 🆓 Free, self-hosted edition
- 🐳 Docker deployment (ghcr.io/firebolt-db/firebolt-core:preview-rc)
- 🛢️ PostgreSQL-compliant SQL interface
- 📊 High-performance analytics capabilities

Documentation: https://docs.firebolt.io/firebolt-core
"""
import pandas as pd
import os
import subprocess
import time
from typing import Optional, Dict
from loguru import logger
from pathlib import Path
from contextlib import contextmanager

# Optional Docker and PostgreSQL support for Firebolt Core
try:
    import docker
    import psycopg2
    DOCKER_AVAILABLE = True
    logger.info("✅ Docker and PostgreSQL support available")
except ImportError:
    DOCKER_AVAILABLE = False
    logger.info("ℹ️  Docker/PostgreSQL not available - Core features disabled")


class FireboltConfig:
    """Configuration for Firebolt connections (Managed and Core)."""
    
    def __init__(self):
        # Managed Firebolt configuration
        self.username = os.getenv('FIREBOLT_USERNAME')
        self.password = os.getenv('FIREBOLT_PASSWORD') 
        self.account_name = os.getenv('FIREBOLT_ACCOUNT_NAME')
        self.default_database = os.getenv('FIREBOLT_DATABASE', 'dreambolt')
        self.default_engine = os.getenv('FIREBOLT_ENGINE', 'dreambolt_engine')
        
        # Firebolt Core configuration
        self.use_core = os.getenv('FIREBOLT_USE_CORE', 'true').lower() == 'true'
        self.core_port = int(os.getenv('FIREBOLT_CORE_PORT', '5432'))
        self.core_container = os.getenv('FIREBOLT_CORE_CONTAINER', 'dreambolt-firebolt-core')
        self.core_image = os.getenv('FIREBOLT_CORE_IMAGE', 'ghcr.io/firebolt-db/firebolt-core:preview-rc')
        
        # Auto-detect mode
        if self.use_core:
            logger.info("🐳 Firebolt Core mode enabled")
        elif not all([self.username, self.password, self.account_name]):
            logger.info("ℹ️  Managed Firebolt credentials not configured - will use Core mode if available")
            self.use_core = True
    
    def is_configured(self) -> bool:
        """Check if any Firebolt configuration is present."""
        if self.use_core and DOCKER_AVAILABLE:
            return True
        return all([self.username, self.password, self.account_name])


class FireboltConnector:
    """Enhanced Firebolt database connector with Core and Managed support."""
    
    def __init__(self, engine: Optional[str] = None, database: Optional[str] = None):
        """
        Initialize Firebolt connector.
        
        Args:
            engine: Firebolt engine name (optional)
            database: Database name (optional)
        """
        self.config = FireboltConfig()
        self.engine_name = engine or self.config.default_engine
        self.database_name = database or self.config.default_database
        self.connection = None
        
        # Initialize appropriate backend
        if self.config.use_core and DOCKER_AVAILABLE:
            logger.info("🚀 Initializing Firebolt Core backend")
            self.backend = "core"
            self._init_core()
        elif self.config.is_configured():
            logger.info("☁️  Initializing Managed Firebolt backend")
            self.backend = "managed"
            self._init_managed()
        else:
            logger.info("🎭 No configuration found - running in simulation mode")
            self.backend = "simulation"
    
    def _init_core(self):
        """Initialize Firebolt Core backend."""
        try:
            self.docker_client = docker.from_env()
            self.core_host = "localhost"
            self.core_user = "firebolt"
            self.core_password = "firebolt"
            logger.info("✅ Firebolt Core backend initialized")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Core backend: {e}")
            self.backend = "simulation"
    
    def _init_managed(self):
        """Initialize Managed Firebolt backend (simulation)."""
        logger.info(f"✅ Managed Firebolt configured for account: {self.config.account_name}")
    
    def setup_core(self) -> bool:
        """
        Set up Firebolt Core infrastructure with Docker.
        
        Returns:
            True if successful, False otherwise
        """
        if self.backend != "core":
            logger.error("❌ Core setup only available in Core mode")
            return False
        
        logger.info("🚀 Setting up Firebolt Core infrastructure...")
        
        try:
            # 1. Ensure Docker is available
            self.docker_client.ping()
            
            # 2. Create data directory
            data_dir = Path.cwd() / ".firebolt-core-data"
            data_dir.mkdir(exist_ok=True)
            logger.info(f"📁 Data directory: {data_dir}")
            
            # 3. Pull Firebolt Core image
            logger.info(f"📥 Pulling image: {self.config.core_image}")
            self.docker_client.images.pull(self.config.core_image)
            
            # 4. Check if container exists
            existing = self._get_core_container()
            if existing:
                if existing.status == "running":
                    logger.info("✅ Firebolt Core already running")
                    return self._wait_for_core_ready()
                else:
                    logger.info("🔄 Starting existing container...")
                    existing.start()
                    return self._wait_for_core_ready()
            
            # 5. Create and start new container
            logger.info("🐳 Creating Firebolt Core container...")
            container = self.docker_client.containers.run(
                self.config.core_image,
                name=self.config.core_container,
                ports={5432: self.config.core_port},
                volumes={str(data_dir): {'bind': '/var/lib/firebolt', 'mode': 'rw'}},
                environment={
                    'POSTGRES_DB': self.database_name,
                    'POSTGRES_USER': self.core_user,
                    'POSTGRES_PASSWORD': self.core_password
                },
                mem_limit="4g",
                detach=True,
                restart_policy={"Name": "unless-stopped"}
            )
            
            logger.info(f"✅ Container created: {container.short_id}")
            
            # 6. Wait for readiness
            if self._wait_for_core_ready():
                logger.info("✅ Firebolt Core setup completed!")
                return True
            else:
                logger.error("❌ Firebolt Core failed to become ready")
                return False
                
        except Exception as e:
            logger.error(f"❌ Firebolt Core setup failed: {e}")
            return False
    
    def _get_core_container(self):
        """Get existing Firebolt Core container."""
        try:
            return self.docker_client.containers.get(self.config.core_container)
        except docker.errors.NotFound:
            return None
        except Exception:
            return None
    
    def _wait_for_core_ready(self, timeout: int = 120) -> bool:
        """Wait for Firebolt Core to be ready."""
        logger.info("⏳ Waiting for Firebolt Core to be ready...")
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                with self._get_core_connection() as conn:
                    with conn.cursor() as cursor:
                        cursor.execute("SELECT 1")
                        cursor.fetchone()
                logger.info("✅ Firebolt Core is ready!")
                return True
            except Exception:
                time.sleep(3)
                continue
        
        logger.error(f"❌ Firebolt Core not ready after {timeout} seconds")
        return False
    
    @contextmanager
    def _get_core_connection(self):
        """Get PostgreSQL connection to Firebolt Core."""
        conn = None
        try:
            conn = psycopg2.connect(
                host=self.core_host,
                port=self.config.core_port,
                database=self.database_name,
                user=self.core_user,
                password=self.core_password,
                connect_timeout=10
            )
            yield conn
        finally:
            if conn:
                conn.close()
    
    def ensure_database(self, database_name: Optional[str] = None) -> bool:
        """
        Ensure database exists.
        
        Args:
            database_name: Database name (uses default if None)
            
        Returns:
            True if successful
        """
        db_name = database_name or self.database_name
        
        if self.backend == "core":
            try:
                with self._get_core_connection() as conn:
                    with conn.cursor() as cursor:
                        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
                        cursor.execute("CREATE SCHEMA IF NOT EXISTS dreambolt")
                    conn.commit()
                logger.info(f"✅ Database ensured: {db_name}")
                return True
            except Exception as e:
                logger.error(f"❌ Failed to ensure database: {e}")
                return False
        else:
            logger.info(f"🎭 Simulating database creation: {db_name}")
            return True
    
    def ensure_engine(self, engine_name: Optional[str] = None) -> bool:
        """
        Ensure engine exists (Core mode auto-manages).
        
        Args:
            engine_name: Engine name (uses default if None)
            
        Returns:
            True if successful
        """
        eng_name = engine_name or self.engine_name
        
        if self.backend == "core":
            # Firebolt Core auto-manages engines
            logger.info(f"✅ Engine ready: {eng_name} (auto-managed)")
            return True
        else:
            logger.info(f"🎭 Simulating engine startup: {eng_name}")
            return True
    
    def get_connection(self):
        """Get database connection."""
        if self.backend == "core":
            try:
                return self._get_core_connection()
            except Exception as e:
                logger.error(f"❌ Failed to get Core connection: {e}")
                return MockConnection()
        else:
            logger.info("🎭 Using simulated connection")
            return MockConnection()
    
    def ensure_table(self, table_name: str, df: pd.DataFrame, if_exists: str = 'replace') -> bool:
        """
        Ensure table exists with proper schema.
        
        Args:
            table_name: Table name
            df: DataFrame to infer schema from
            if_exists: What to do if table exists
            
        Returns:
            True if successful
        """
        if self.backend == "core":
            try:
                with self._get_core_connection() as conn:
                    with conn.cursor() as cursor:
                        # Generate CREATE TABLE statement
                        create_sql = self._generate_create_table_sql(table_name, df)
                        
                        if if_exists == 'replace':
                            cursor.execute(f"DROP TABLE IF EXISTS dreambolt.{table_name}")
                        
                        cursor.execute(create_sql)
                    conn.commit()
                
                logger.info(f"✅ Table created: dreambolt.{table_name}")
                return True
            except Exception as e:
                logger.error(f"❌ Failed to create table: {e}")
                return False
        else:
            logger.info(f"🎭 Simulating table creation: {table_name}")
            logger.info(f"   - Columns: {len(df.columns)}")
            logger.info(f"   - Schema: {dict(df.dtypes.astype(str))}")
            return True
    
    def copy_data(self, table_name: str, parquet_path: str, s3_credentials: Optional[Dict] = None) -> bool:
        """
        Copy data from Parquet file to table.
        
        Args:
            table_name: Target table name
            parquet_path: Path to Parquet file
            s3_credentials: S3 credentials (ignored in Core)
            
        Returns:
            True if successful
        """
        if self.backend == "core":
            try:
                # Read Parquet and insert data
                df = pd.read_parquet(parquet_path)
                
                with self._get_core_connection() as conn:
                    with conn.cursor() as cursor:
                        # Prepare batch insert
                        columns = [col.replace(' ', '_').replace('-', '_').lower() for col in df.columns]
                        placeholders = ', '.join(['%s'] * len(columns))
                        columns_str = ', '.join([f'"{col}"' for col in columns])
                        
                        # Convert DataFrame to list of tuples
                        data = []
                        for _, row in df.iterrows():
                            values = [None if pd.isna(val) else val for val in row]
                            data.append(tuple(values))
                        
                        # Execute batch insert
                        insert_sql = f"INSERT INTO dreambolt.{table_name} ({columns_str}) VALUES ({placeholders})"
                        cursor.executemany(insert_sql, data)
                    
                    conn.commit()
                
                logger.info(f"✅ Data loaded: {len(df)} rows into {table_name}")
                return True
            except Exception as e:
                logger.error(f"❌ Failed to load data: {e}")
                return False
        else:
            logger.info(f"🎭 Simulating data copy to: {table_name}")
            logger.info(f"   - Source: {parquet_path}")
            
            # Try to get actual row count for realism
            try:
                df = pd.read_parquet(parquet_path)
                row_count = len(df)
                logger.info(f"   - Rows: {row_count} (actual count from file)")
            except Exception:
                logger.info("   - Rows: [simulated count]")
            
            return True
    
    def query(self, sql: str) -> pd.DataFrame:
        """Execute SQL query and return DataFrame."""
        if self.backend == "core":
            try:
                with self._get_core_connection() as conn:
                    return pd.read_sql(sql, conn)
            except Exception as e:
                logger.error(f"❌ Query failed: {e}")
                return pd.DataFrame()
        else:
            logger.info(f"🎭 Simulating query: {sql[:50]}...")
            return pd.DataFrame({"result": ["simulated_data"]})
    
    def _generate_create_table_sql(self, table_name: str, df: pd.DataFrame) -> str:
        """Generate CREATE TABLE SQL from DataFrame schema."""
        column_definitions = []
        
        for col, dtype in df.dtypes.items():
            # Map pandas dtypes to PostgreSQL/Firebolt types
            if dtype == 'int64':
                pg_type = 'BIGINT'
            elif dtype == 'int32':
                pg_type = 'INTEGER'
            elif dtype == 'float64':
                pg_type = 'DOUBLE PRECISION'
            elif dtype == 'float32':
                pg_type = 'REAL'
            elif dtype == 'bool':
                pg_type = 'BOOLEAN'
            elif 'datetime' in str(dtype):
                pg_type = 'TIMESTAMP'
            else:
                pg_type = 'TEXT'
            
            # Clean column name
            clean_col = col.replace(' ', '_').replace('-', '_').lower()
            column_definitions.append(f'    "{clean_col}" {pg_type}')
        
        create_sql = f"""
CREATE TABLE IF NOT EXISTS dreambolt.{table_name} (
{','.join(column_definitions)}
)
"""
        return create_sql
    
    def core_status(self) -> Dict:
        """Get Firebolt Core status."""
        if self.backend != "core":
            return {"backend": self.backend, "core_available": False}
        
        try:
            container = self._get_core_container()
            if not container:
                return {"status": "not_created", "backend": "core"}
            
            # Try connection
            try:
                with self._get_core_connection() as conn:
                    with conn.cursor() as cursor:
                        cursor.execute("SELECT version()")
                        version = cursor.fetchone()[0]
                connection_status = "connected"
            except:
                connection_status = "unreachable"
                version = None
            
            return {
                "backend": "core",
                "status": container.status,
                "container_id": container.short_id,
                "image": self.config.core_image,
                "port": self.config.core_port,
                "connection": connection_status,
                "version": version,
                "database": self.database_name
            }
        except Exception as e:
            return {"backend": "core", "error": str(e)}
    
    def stop_core(self):
        """Stop Firebolt Core container."""
        if self.backend != "core":
            logger.warning("⚠️  Stop operation only available in Core mode")
            return
        
        try:
            container = self._get_core_container()
            if container and container.status == "running":
                logger.info("🛑 Stopping Firebolt Core...")
                container.stop()
                logger.info("✅ Firebolt Core stopped")
        except Exception as e:
            logger.error(f"❌ Failed to stop Core: {e}")


class MockConnection:
    """Mock database connection for simulation."""
    
    def cursor(self):
        return MockCursor()
    
    def close(self):
        pass
    
    def commit(self):
        pass


class MockCursor:
    """Mock database cursor for simulation."""
    
    def execute(self, sql: str):
        logger.debug(f"🎭 Mock SQL execution: {sql[:100]}...")
    
    def executemany(self, sql: str, data):
        logger.debug(f"🎭 Mock batch execution: {len(data)} rows")
    
    def fetchone(self):
        return [0]
    
    def fetchall(self):
        return [[0]]
    
    def close(self):
        pass


# Convenience functions
def setup_firebolt_core() -> FireboltConnector:
    """Set up Firebolt Core and return connector."""
    connector = FireboltConnector()
    
    if connector.backend == "core":
        if connector.setup_core():
            return connector
        else:
            raise RuntimeError("Failed to set up Firebolt Core")
    else:
        logger.warning("⚠️  Firebolt Core not available - using simulation mode")
        return connector


if __name__ == "__main__":
    # Enhanced smoke test for both backends
    print("🧪 Running enhanced FireboltConnector smoke test...")
    
    connector = FireboltConnector()
    config = connector.config
    
    print(f"✅ Backend: {connector.backend}")
    print(f"✅ Config loaded: {config.is_configured()}")
    print(f"✅ Use Core: {config.use_core}")
    print(f"✅ Docker available: {DOCKER_AVAILABLE}")
    
    if connector.backend == "core":
        print("🚀 Testing Firebolt Core functionality...")
        
        # Show status
        status = connector.core_status()
        print(f"📊 Core status: {status}")
        
        # Setup if needed
        if status.get("status") != "running":
            print("🛠️  Setting up Firebolt Core...")
            if connector.setup_core():
                print("✅ Setup successful!")
            else:
                print("❌ Setup failed!")
    
    # Test basic operations
    connector.ensure_database()
    connector.ensure_engine()
    
    # Test with sample data
    import tempfile
    sample_df = pd.DataFrame({
        'id': [1, 2, 3],
        'name': ['Alice', 'Bob', 'Charlie'],
        'score': [95.5, 87.2, 92.8]
    })
    
    with tempfile.NamedTemporaryFile(suffix='.parquet', delete=False) as f:
        sample_df.to_parquet(f.name)
        
        connector.ensure_table('test_table', sample_df)
        connector.copy_data('test_table', f.name)
    
    # Test query
    result = connector.query("SELECT COUNT(*) as row_count FROM dreambolt.test_table")
    print(f"📊 Query result: {result}")
    
    print("✅ Enhanced smoke test completed!") 