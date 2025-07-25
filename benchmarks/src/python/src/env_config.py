"""
Environment-based configuration loader for database benchmarks.
Replaces JSON-based credential loading with secure environment variables.
"""
import os
import json
from typing import Dict, Any, Optional
from dotenv import load_dotenv


def load_environment_config(env_file: Optional[str] = None) -> Dict[str, Any]:
    """
    Load database credentials and configuration from environment variables.
    
    Args:
        env_file: Optional path to .env file. If None, loads from system environment.
        
    Returns:
        Dict containing credentials for all vendors in the same format as the old JSON structure.
        
    Raises:
        ValueError: If required environment variables are missing.
    """
    # Load .env file if specified
    if env_file:
        load_dotenv(env_file)
    else:
        # Try to load .env from project root
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        env_path = os.path.join(project_root, '.env')
        if os.path.exists(env_path):
            load_dotenv(env_path)
    
    credentials = {}
    
    # Snowflake configuration
    if _has_vendor_env_vars('SNOWFLAKE'):
        credentials['snowflake'] = {
            'account': os.getenv('SNOWFLAKE_ACCOUNT'),
            'user': os.getenv('SNOWFLAKE_USER'),
            'password': os.getenv('SNOWFLAKE_PASSWORD'),
            'database': os.getenv('SNOWFLAKE_DATABASE'),
            'schema': os.getenv('SNOWFLAKE_SCHEMA'),
            'warehouse': os.getenv('SNOWFLAKE_WAREHOUSE')
        }
    
    # Redshift configuration
    if _has_vendor_env_vars('REDSHIFT'):
        credentials['redshift'] = {
            'host': os.getenv('REDSHIFT_HOST'),
            'port': int(os.getenv('REDSHIFT_PORT', '5439')),
            'database': os.getenv('REDSHIFT_DATABASE'),
            'user': os.getenv('REDSHIFT_USER'),
            'password': os.getenv('REDSHIFT_PASSWORD')
        }
    
    # Firebolt configuration
    if _has_vendor_env_vars('FIREBOLT'):
        credentials['firebolt'] = {
            'account_name': os.getenv('FIREBOLT_ACCOUNT_NAME'),
            'database': os.getenv('FIREBOLT_DATABASE'),
            'engine_name': os.getenv('FIREBOLT_ENGINE_NAME'),
            'auth': {
                'id': os.getenv('FIREBOLT_SERVICE_ID'),
                'secret': os.getenv('FIREBOLT_SERVICE_SECRET')
            }
        }
    
    # BigQuery configuration
    if _has_vendor_env_vars('BIGQUERY'):
        bigquery_key_file = os.getenv('BIGQUERY_KEY_FILE')
        bigquery_key = None
        
        # Load JSON key from file if path is provided
        if bigquery_key_file and os.path.exists(bigquery_key_file):
            try:
                with open(bigquery_key_file, 'r') as f:
                    bigquery_key = json.load(f)
            except (json.JSONDecodeError, IOError):
                bigquery_key = bigquery_key_file  # Use path as fallback
        else:
            # Fallback: check for inline JSON (for backward compatibility)
            bigquery_key_json = os.getenv('BIGQUERY_KEY_JSON')
            if bigquery_key_json:
                try:
                    bigquery_key = json.loads(bigquery_key_json)
                except json.JSONDecodeError:
                    bigquery_key = bigquery_key_json
                
        credentials['google'] = {  # Note: using 'google' to match existing code
            'project_id': os.getenv('BIGQUERY_PROJECT_ID'),
            'dataset': os.getenv('BIGQUERY_DATASET'),
            'key': bigquery_key
        }
    
    return credentials


def _has_vendor_env_vars(vendor_prefix: str) -> bool:
    """
    Check if environment variables exist for a given vendor.
    
    Args:
        vendor_prefix: Vendor prefix like 'SNOWFLAKE', 'REDSHIFT', etc.
        
    Returns:
        True if at least one environment variable with the prefix exists.
    """
    env_vars = os.environ
    return any(key.startswith(f'{vendor_prefix}_') for key in env_vars)


def get_app_config() -> Dict[str, Any]:
    """
    Get application configuration from environment variables.
    
    Returns:
        Dict containing application configuration.
    """
    return {
        'default_output_dir': os.getenv('DEFAULT_OUTPUT_DIR', 'benchmark_results'),
        'default_pool_size': int(os.getenv('DEFAULT_POOL_SIZE', '5')),
        'default_concurrency': int(os.getenv('DEFAULT_CONCURRENCY', '1')),
        'debug_mode': os.getenv('DEBUG_MODE', 'false').lower() == 'true',
        'streamlit_port': int(os.getenv('STREAMLIT_SERVER_PORT', '8501')),
        'streamlit_address': os.getenv('STREAMLIT_SERVER_ADDRESS', 'localhost')
    }


def validate_vendor_credentials(vendor: str, credentials: Dict[str, Any]) -> None:
    """
    Validate that required credentials are present for a vendor.
    
    Args:
        vendor: Vendor name ('snowflake', 'redshift', 'firebolt', 'google')
        credentials: Credentials dictionary for the vendor
        
    Raises:
        ValueError: If required credentials are missing.
    """
    required_fields = {
        'snowflake': ['account', 'user', 'password'],
        'redshift': ['host', 'database', 'user', 'password'],
        'firebolt': ['account_name', 'database', 'engine_name', 'auth'],
        'google': ['project_id', 'dataset', 'key']
    }
    
    if vendor not in required_fields:
        raise ValueError(f"Unknown vendor: {vendor}")
    
    missing_fields = []
    for field in required_fields[vendor]:
        if field not in credentials or not credentials[field]:
            missing_fields.append(field)
    
    if missing_fields:
        raise ValueError(f"Missing required credentials for {vendor}: {missing_fields}")
    
    # Special validation for firebolt auth structure
    if vendor == 'firebolt' and 'auth' in credentials:
        auth = credentials['auth']
        if not isinstance(auth, dict) or 'id' not in auth or 'secret' not in auth:
            raise ValueError("Firebolt auth must contain 'id' and 'secret' fields")