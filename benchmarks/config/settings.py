import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
ROOT_DIR = Path(__file__).parent.parent
env_path = ROOT_DIR / '.env'
if env_path.exists():
    load_dotenv(env_path)

# Base paths
CREDENTIALS_DIR = ROOT_DIR / "config" / "credentials"
DEFAULT_CREDS_FILE = CREDENTIALS_DIR / "credentials.json"  # Legacy support

# Default settings (now from environment variables with fallbacks)
DEFAULT_POOL_SIZE = int(os.getenv('DEFAULT_POOL_SIZE', '5'))
DEFAULT_CONCURRENCY = int(os.getenv('DEFAULT_CONCURRENCY', '1'))
DEFAULT_OUTPUT_DIR = ROOT_DIR / os.getenv('DEFAULT_OUTPUT_DIR', 'benchmark_results')

# Vendor-specific settings
VENDOR_SETTINGS = {
    'firebolt': {
        'max_retries': 3,
        'timeout': 300,
    },
    'snowflake': {
        'max_retries': 3,
        'timeout': 300,
    },
    # ... other vendor settings ...
}
