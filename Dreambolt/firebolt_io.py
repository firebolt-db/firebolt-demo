"""
Firebolt integration module for DreamBolt.
Handles engine management, table creation, and data loading.
"""
import pandas as pd
import os
from typing import Optional, Dict
from loguru import logger
import time

# Firebolt SDK imports with importlib to avoid Python 3.13 issues
try:
    import importlib
    firebolt_db = importlib.import_module('firebolt.db')
    firebolt_client = importlib.import_module('firebolt.client')
    firebolt_manager = importlib.import_module('firebolt.service.manager')
    
    connect = firebolt_db.connect
    DEFAULT_API_URL = firebolt_client.DEFAULT_API_URL
    ResourceManager = firebolt_manager.ResourceManager
    FIREBOLT_AVAILABLE = True
except ImportError:
    logger.info("Firebolt SDK not available - database features will use dry-run mode")
    FIREBOLT_AVAILABLE = False
    
    # Create dummy classes to prevent import errors
    def connect(*args, **kwargs):
        return None
    
    DEFAULT_API_URL = "https://api.firebolt.io"
    
    class ResourceManager:
        def __init__(self, *args, **kwargs):
            pass


class FireboltConfig:
    """Configuration for Firebolt connections."""
    
    def __init__(self):
        self.username = os.getenv('FIREBOLT_USERNAME')
        self.password = os.getenv('FIREBOLT_PASSWORD') 
        self.account_name = os.getenv('FIREBOLT_ACCOUNT_NAME')
        self.api_endpoint = os.getenv('FIREBOLT_API_ENDPOINT', DEFAULT_API_URL)
        self.default_database = os.getenv('FIREBOLT_DATABASE', 'dreambolt')
        self.default_engine = os.getenv('FIREBOLT_ENGINE', 'dreambolt_engine')
        
        if not all([self.username, self.password, self.account_name]):
            logger.warning("Missing Firebolt credentials - check environment variables")
    
    def is_configured(self) -> bool:
        """Check if all required configuration is present."""
        return all([self.username, self.password, self.account_name])


class FireboltConnector:
    """Main class for Firebolt database operations."""
    
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
        self.resource_manager = None
        
        if FIREBOLT_AVAILABLE and self.config.is_configured():
            self._initialize_connection()
        else:
            logger.warning("Firebolt not available or not configured")
    
    def _initialize_connection(self):
        """Initialize connection to Firebolt."""
        try:
            # Initialize resource manager for engine/database operations
            self.resource_manager = ResourceManager(
                username=self.config.username,
                password=self.config.password,
                account_name=self.config.account_name,
                api_endpoint=self.config.api_endpoint
            )
            
            logger.info(f"Connected to Firebolt account: {self.config.account_name}")
            
        except Exception as e:
            logger.error(f"Failed to initialize Firebolt connection: {e}")
            self.resource_manager = None
    
    def ensure_database(self, database_name: Optional[str] = None) -> bool:
        """
        Ensure database exists, create if necessary.
        
        Args:
            database_name: Database name (uses default if None)
            
        Returns:
            True if database is ready, False otherwise
        """
        if not self.resource_manager:
            logger.error("Resource manager not available")
            return False
        
        db_name = database_name or self.database_name
        
        try:
            # Check if database exists
            databases = self.resource_manager.databases.get_many()
            existing_db = next((db for db in databases if db.name == db_name), None)
            
            if existing_db:
                logger.info(f"Database '{db_name}' already exists")
                return True
            else:
                # Create new database
                logger.info(f"Creating database '{db_name}'")
                self.resource_manager.databases.create(name=db_name)
                
                # Wait for database to be ready
                self._wait_for_database(db_name)
                return True
                
        except Exception as e:
            logger.error(f"Failed to ensure database '{db_name}': {e}")
            return False
    
    def ensure_engine(self, engine_name: Optional[str] = None) -> bool:
        """
        Ensure engine exists and is running.
        
        Args:
            engine_name: Engine name (uses default if None)
            
        Returns:
            True if engine is ready, False otherwise
        """
        if not self.resource_manager:
            logger.error("Resource manager not available")
            return False
        
        eng_name = engine_name or self.engine_name
        
        try:
            # Check if engine exists
            engines = self.resource_manager.engines.get_many()
            existing_engine = next((eng for eng in engines if eng.name == eng_name), None)
            
            if existing_engine:
                logger.info(f"Engine '{eng_name}' exists")
                
                # Start engine if not running
                if existing_engine.current_status != 'Running':
                    logger.info(f"Starting engine '{eng_name}'")
                    existing_engine.start()
                    self._wait_for_engine(eng_name)
                
                return True
            else:
                # Create new engine
                logger.info(f"Creating engine '{eng_name}'")
                
                # Ensure database exists first
                self.ensure_database()
                
                engine = self.resource_manager.engines.create(
                    name=eng_name,
                    region='us-east-1',  # Default region
                    engine_type='S',     # Small engine for development
                    scale=1,
                    auto_stop=60,        # Auto-stop after 60 minutes
                    warmup='PRELOAD_INDEXES'
                )
                
                # Attach to database
                engine.attach_to_database(self.database_name)
                
                # Start engine
                engine.start()
                self._wait_for_engine(eng_name)
                
                return True
                
        except Exception as e:
            logger.error(f"Failed to ensure engine '{eng_name}': {e}")
            return False
    
    def get_connection(self):
        """Get database connection for queries."""
        if not FIREBOLT_AVAILABLE or not self.config.is_configured():
            raise ValueError("Firebolt not available or not configured")
        
        if not self.connection:
            try:
                self.connection = connect(
                    username=self.config.username,
                    password=self.config.password,
                    database=self.database_name,
                    engine_name=self.engine_name,
                    account_name=self.config.account_name,
                    api_endpoint=self.config.api_endpoint
                )
                logger.info(f"Connected to database '{self.database_name}' via engine '{self.engine_name}'")
                
            except Exception as e:
                logger.error(f"Failed to connect to database: {e}")
                raise
        
        return self.connection
    
    def ensure_table(self, table_name: str, df: pd.DataFrame, if_exists: str = 'replace') -> bool:
        """
        Ensure table exists with proper schema.
        
        Args:
            table_name: Name of the table
            df: DataFrame to infer schema from
            if_exists: What to do if table exists ('replace', 'append', 'fail')
            
        Returns:
            True if table is ready, False otherwise
        """
        try:
            # Ensure engine and database are ready
            if not self.ensure_engine():
                return False
            
            connection = self.get_connection()
            cursor = connection.cursor()
            
            # Generate CREATE TABLE statement
            table_schema = self._generate_table_schema(table_name, df)
            
            # Handle existing table
            if if_exists == 'replace':
                cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
                cursor.execute(table_schema)
                logger.info(f"Created/replaced table '{table_name}'")
            
            elif if_exists == 'append':
                # Check if table exists
                cursor.execute(f"""
                    SELECT COUNT(*) 
                    FROM information_schema.tables 
                    WHERE table_name = '{table_name}'
                """)
                
                if cursor.fetchone()[0] == 0:
                    cursor.execute(table_schema)
                    logger.info(f"Created new table '{table_name}'")
                else:
                    logger.info(f"Table '{table_name}' exists, will append data")
            
            elif if_exists == 'fail':
                cursor.execute(f"""
                    SELECT COUNT(*) 
                    FROM information_schema.tables 
                    WHERE table_name = '{table_name}'
                """)
                
                if cursor.fetchone()[0] > 0:
                    raise ValueError(f"Table '{table_name}' already exists")
                else:
                    cursor.execute(table_schema)
                    logger.info(f"Created new table '{table_name}'")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to ensure table '{table_name}': {e}")
            return False
    
    def copy_data(self, table_name: str, parquet_path: str, s3_credentials: Optional[Dict] = None) -> bool:
        """
        Copy data from Parquet file to Firebolt table.
        
        Args:
            table_name: Target table name
            parquet_path: Path to Parquet file (local or S3)
            s3_credentials: S3 credentials if needed
            
        Returns:
            True if successful, False otherwise
        """
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            
            if parquet_path.startswith('s3://'):
                # S3 copy
                copy_sql = f"""
                    COPY {table_name}
                    FROM '{parquet_path}'
                    FILE_TYPE = PARQUET
                """
                
                # Add S3 credentials if provided
                if s3_credentials:
                    copy_sql += f"""
                        AWS_KEY_ID = '{s3_credentials.get('aws_access_key_id')}'
                        AWS_SECRET_KEY = '{s3_credentials.get('aws_secret_access_key')}'
                    """
                    
                    if 'aws_session_token' in s3_credentials:
                        copy_sql += f" AWS_SESSION_TOKEN = '{s3_credentials['aws_session_token']}'"
            else:
                # For local files, we need to upload to S3 first or use INSERT statements
                # This is a simplified approach - in production, consider using S3 staging
                logger.warning("Local file copy not optimized - consider uploading to S3 first")
                return self._copy_local_file(table_name, parquet_path)
            
            cursor.execute(copy_sql)
            
            # Get row count for verification
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            row_count = cursor.fetchone()[0]
            
            logger.info(f"Successfully copied data to '{table_name}': {row_count} rows")
            return True
            
        except Exception as e:
            logger.error(f"Failed to copy data to '{table_name}': {e}")
            return False
    
    def _copy_local_file(self, table_name: str, parquet_path: str) -> bool:
        """Copy local Parquet file using INSERT statements (fallback method)."""
        try:
            # Read Parquet file
            df = pd.read_parquet(parquet_path)
            
            connection = self.get_connection()
            cursor = connection.cursor()
            
            # Generate INSERT statements in batches
            batch_size = 1000
            for i in range(0, len(df), batch_size):
                batch = df.iloc[i:i+batch_size]
                
                values_list = []
                for _, row in batch.iterrows():
                    values = []
                    for val in row:
                        if pd.isna(val):
                            values.append('NULL')
                        elif isinstance(val, str):
                            escaped_val = val.replace("'", "''")  # Escape single quotes
                            values.append(f"'{escaped_val}'")
                        else:
                            values.append(str(val))
                    
                    values_list.append(f"({', '.join(values)})")
                
                insert_sql = f"""
                    INSERT INTO {table_name} 
                    VALUES {', '.join(values_list)}
                """
                
                cursor.execute(insert_sql)
            
            logger.info(f"Inserted {len(df)} rows into '{table_name}'")
            return True
            
        except Exception as e:
            logger.error(f"Failed to copy local file: {e}")
            return False
    
    def _generate_table_schema(self, table_name: str, df: pd.DataFrame) -> str:
        """Generate CREATE TABLE statement from DataFrame schema."""
        column_definitions = []
        
        for col, dtype in df.dtypes.items():
            # Map pandas dtypes to Firebolt types
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
            elif col.startswith('embedding_'):
                fb_type = 'REAL'  # Embeddings as float
            else:
                # Default to TEXT for strings and unknown types
                fb_type = 'TEXT'
            
            column_definitions.append(f'    {col} {fb_type}')
        
        create_sql = f"""
CREATE TABLE {table_name} (
{','.join(column_definitions)}
)
PRIMARY INDEX {list(df.columns)[0]}  -- Use first column as primary index
"""
        
        return create_sql
    
    def _wait_for_database(self, database_name: str, timeout: int = 300):
        """Wait for database to be ready."""
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                databases = self.resource_manager.databases.get_many()
                db = next((d for d in databases if d.name == database_name), None)
                if db:
                    logger.info(f"Database '{database_name}' is ready")
                    return
                time.sleep(5)
            except Exception as e:
                logger.debug(f"Waiting for database: {e}")
                time.sleep(5)
        
        raise TimeoutError(f"Database '{database_name}' not ready after {timeout} seconds")
    
    def _wait_for_engine(self, engine_name: str, timeout: int = 600):
        """Wait for engine to be running."""
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                engines = self.resource_manager.engines.get_many()
                engine = next((e for e in engines if e.name == engine_name), None)
                if engine and engine.current_status == 'Running':
                    logger.info(f"Engine '{engine_name}' is running")
                    return
                time.sleep(10)
            except Exception as e:
                logger.debug(f"Waiting for engine: {e}")
                time.sleep(10)
        
        raise TimeoutError(f"Engine '{engine_name}' not running after {timeout} seconds")


if __name__ == "__main__":
    # Local smoke test
    print("🧪 Running FireboltConnector smoke test...")
    
    try:
        connector = FireboltConnector()
        config = connector.config
        
        print(f"✅ Config loaded: {config.is_configured()}")
        print(f"✅ Username: {'***' if config.username else 'Not set'}")
        print(f"✅ Account: {config.account_name or 'Not set'}")
        print(f"✅ Default database: {config.default_database}")
        print(f"✅ Default engine: {config.default_engine}")
        
        if config.is_configured():
            print("✅ Configuration appears valid")
        else:
            print("⚠️  Missing environment variables - check FIREBOLT_* settings")
        
        print("✅ Smoke test passed!")
        
    except Exception as e:
        print(f"❌ Smoke test failed: {e}")

# ⬇️ COMMIT SUGGESTION: git add -A && git commit -m "feat: add Firebolt integration with engine management" 