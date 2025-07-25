"""
Robust S3 client wrapper for DreamBolt.
Provides bullet-proof error handling, exponential backoff, and progress tracking.
"""
import time
import boto3
import s3fs
from typing import Optional, Dict, Any, Tuple, BinaryIO
from urllib.parse import urlparse
from botocore.exceptions import (
    NoCredentialsError, 
    ClientError, 
    BotoCoreError,
    PartialCredentialsError
)
from loguru import logger
import re
from pathlib import Path

try:
    from tqdm import tqdm
    TQDM_AVAILABLE = True
except ImportError:
    logger.warning("tqdm not available - progress bars disabled")
    TQDM_AVAILABLE = False


class S3BaseError(Exception):
    """Base exception for all S3-related errors."""
    pass


class S3AuthError(S3BaseError):
    """Authentication/authorization errors."""
    pass


class S3NotFoundError(S3BaseError):
    """File/bucket not found errors."""
    pass


class S3RateLimitError(S3BaseError):
    """Rate limit/throttling errors."""
    pass


class S3GenericError(S3BaseError):
    """Generic S3 errors."""
    pass


class S3Client:
    """
    Robust S3 client with automatic retry, region detection, and progress tracking.
    
    Features:
    - Automatic region detection from S3 URLs
    - Exponential backoff with configurable retries
    - Progress bars for large downloads
    - Custom exception hierarchy for better error handling
    - Context manager support for file operations
    """
    
    def __init__(self, max_retries: int = 3, backoff_factor: float = 2.0):
        """
        Initialize S3 client.
        
        Args:
            max_retries: Maximum number of retry attempts
            backoff_factor: Exponential backoff multiplier
        """
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self._clients: Dict[str, Any] = {}  # Region-specific clients
        self._fs: Optional[s3fs.S3FileSystem] = None
        
    def _get_client(self, region: Optional[str] = None):
        """Get or create a region-specific boto3 S3 client."""
        region = region or 'us-east-1'  # Default region
        
        if region not in self._clients:
            try:
                self._clients[region] = boto3.client('s3', region_name=region)
                logger.debug(f"Created S3 client for region: {region}")
            except Exception as e:
                raise S3AuthError(f"Failed to create S3 client for region {region}: {e}")
                
        return self._clients[region]
    
    def _get_filesystem(self) -> s3fs.S3FileSystem:
        """Get or create s3fs filesystem."""
        if self._fs is None:
            try:
                self._fs = s3fs.S3FileSystem()
                logger.debug("Created S3 filesystem")
            except Exception as e:
                raise S3AuthError(f"Failed to create S3 filesystem: {e}")
        return self._fs
    
    def parse_s3_uri(self, s3_uri: str) -> Tuple[str, str, Optional[str]]:
        """
        Parse S3 URI and detect region.
        
        Args:
            s3_uri: S3 URI like s3://bucket/key or s3://bucket.region.amazonaws.com/key
            
        Returns:
            Tuple of (bucket, key, region)
        """
        if not s3_uri.startswith('s3://'):
            raise ValueError(f"Invalid S3 URI: {s3_uri}")
            
        parsed = urlparse(s3_uri)
        bucket = parsed.netloc
        key = parsed.path.lstrip('/')
        
        # Detect region from bucket name if in format bucket.region.amazonaws.com
        region = None
        region_match = re.match(r'^[^.]+\.([^.]+)\.amazonaws\.com$', bucket)
        if region_match:
            region = region_match.group(1)
            bucket = bucket.split('.')[0]  # Extract bucket name
        
        return bucket, key, region
    
    def _retry_with_backoff(self, operation, *args, **kwargs):
        """Execute operation with exponential backoff retry."""
        last_exception = None
        
        for attempt in range(self.max_retries + 1):
            try:
                return operation(*args, **kwargs)
            except NoCredentialsError as e:
                raise S3AuthError(
                    "AWS credentials not found. Please configure credentials using:\n"
                    "1. AWS CLI: `aws configure`\n"
                    "2. Environment variables: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY\n"
                    "3. IAM roles (if running on EC2)\n"
                    f"Error: {e}"
                )
            except PartialCredentialsError as e:
                raise S3AuthError(f"Incomplete AWS credentials: {e}")
            except ClientError as e:
                error_code = e.response.get('Error', {}).get('Code', '')
                
                if error_code in ['NoSuchBucket', 'NoSuchKey']:
                    raise S3NotFoundError(f"S3 resource not found: {e}")
                elif error_code in ['AccessDenied', 'Forbidden']:
                    raise S3AuthError(f"Access denied to S3 resource: {e}")
                elif error_code in ['ThrottlingException', 'Throttling', 'TooManyRequestsException']:
                    if attempt < self.max_retries:
                        sleep_time = (self.backoff_factor ** attempt)
                        logger.warning(f"Rate limited, retrying in {sleep_time:.1f}s (attempt {attempt + 1}/{self.max_retries + 1})")
                        time.sleep(sleep_time)
                        last_exception = S3RateLimitError(f"Rate limit exceeded: {e}")
                        continue
                    else:
                        raise S3RateLimitError(f"Rate limit exceeded after {self.max_retries} retries: {e}")
                else:
                    last_exception = S3GenericError(f"S3 error: {e}")
                    if attempt < self.max_retries:
                        sleep_time = (self.backoff_factor ** attempt)
                        logger.warning(f"S3 error, retrying in {sleep_time:.1f}s (attempt {attempt + 1}/{self.max_retries + 1})")
                        time.sleep(sleep_time)
                        continue
            except BotoCoreError as e:
                last_exception = S3GenericError(f"AWS SDK error: {e}")
                if attempt < self.max_retries:
                    sleep_time = (self.backoff_factor ** attempt)
                    logger.warning(f"AWS SDK error, retrying in {sleep_time:.1f}s (attempt {attempt + 1}/{self.max_retries + 1})")
                    time.sleep(sleep_time)
                    continue
            except Exception as e:
                last_exception = S3GenericError(f"Unexpected error: {e}")
                if attempt < self.max_retries:
                    sleep_time = (self.backoff_factor ** attempt)
                    logger.warning(f"Unexpected error, retrying in {sleep_time:.1f}s (attempt {attempt + 1}/{self.max_retries + 1})")
                    time.sleep(sleep_time)
                    continue
        
        # If we get here, all retries were exhausted
        if last_exception:
            raise last_exception
        else:
            raise S3GenericError("All retry attempts exhausted")
    
    def head_object(self, s3_uri: str) -> Dict[str, Any]:
        """
        Get object metadata.
        
        Args:
            s3_uri: S3 URI
            
        Returns:
            Object metadata dictionary
        """
        bucket, key, region = self.parse_s3_uri(s3_uri)
        client = self._get_client(region)
        
        def _head_operation():
            return client.head_object(Bucket=bucket, Key=key)
        
        return self._retry_with_backoff(_head_operation)
    
    def download_file(self, s3_uri: str, local_path: str, show_progress: bool = True) -> None:
        """
        Download file from S3 with progress tracking.
        
        Args:
            s3_uri: S3 URI
            local_path: Local file path
            show_progress: Whether to show progress bar
        """
        bucket, key, region = self.parse_s3_uri(s3_uri)
        client = self._get_client(region)
        
        # Get file size for progress tracking
        try:
            metadata = self.head_object(s3_uri)
            file_size = metadata.get('ContentLength', 0)
        except S3BaseError:
            file_size = 0
            logger.warning(f"Could not get file size for {s3_uri}")
        
        def _download_operation():
            if show_progress and TQDM_AVAILABLE and file_size > 0:
                # Download with progress bar
                with tqdm(total=file_size, unit='B', unit_scale=True, desc=f"Downloading {Path(key).name}") as pbar:
                    def progress_callback(bytes_transferred):
                        pbar.update(bytes_transferred)
                    
                    client.download_file(
                        bucket, key, local_path,
                        Callback=progress_callback
                    )
            else:
                # Simple download without progress
                client.download_file(bucket, key, local_path)
        
        self._retry_with_backoff(_download_operation)
        logger.info(f"Successfully downloaded {s3_uri} to {local_path}")
    
    def open(self, s3_uri: str, mode: str = 'rb', **kwargs):
        """
        Open S3 file with context manager support.
        
        Args:
            s3_uri: S3 URI
            mode: File open mode
            **kwargs: Additional arguments for s3fs.open
            
        Returns:
            File-like object
        """
        fs = self._get_filesystem()
        
        def _open_operation():
            return fs.open(s3_uri, mode=mode, **kwargs)
        
        return self._retry_with_backoff(_open_operation)
    
    def exists(self, s3_uri: str) -> bool:
        """
        Check if S3 object exists.
        
        Args:
            s3_uri: S3 URI
            
        Returns:
            True if object exists, False otherwise
        """
        try:
            self.head_object(s3_uri)
            return True
        except S3NotFoundError:
            return False
        except S3BaseError:
            # For other errors (auth, etc.), re-raise
            raise
    
    def list_objects(self, s3_uri: str, prefix: str = "") -> list:
        """
        List objects in S3 bucket/prefix.
        
        Args:
            s3_uri: S3 URI (bucket or bucket/prefix)
            prefix: Additional prefix filter
            
        Returns:
            List of object keys
        """
        bucket, key, region = self.parse_s3_uri(s3_uri)
        client = self._get_client(region)
        
        # Combine key and prefix
        full_prefix = f"{key.rstrip('/')}/{prefix}".lstrip('/') if key else prefix
        
        def _list_operation():
            response = client.list_objects_v2(Bucket=bucket, Prefix=full_prefix)
            return [obj['Key'] for obj in response.get('Contents', [])]
        
        return self._retry_with_backoff(_list_operation)
    
    def validate_credentials(self) -> bool:
        """
        Validate AWS credentials by making a simple API call.
        
        Returns:
            True if credentials are valid, raises exception otherwise
        """
        try:
            client = self._get_client()
            
            def _validate_operation():
                # Simple operation to test credentials
                client.list_buckets()
                return True
            
            return self._retry_with_backoff(_validate_operation)
        except S3AuthError:
            return False


# Global instance for convenience
default_s3_client = S3Client()


def is_s3_uri(path: str) -> bool:
    """Check if path is an S3 URI."""
    return path.startswith('s3://')


def parse_s3_uri(s3_uri: str) -> Tuple[str, str, Optional[str]]:
    """Parse S3 URI. Convenience function."""
    return default_s3_client.parse_s3_uri(s3_uri)


# Context manager for S3 file operations
class S3File:
    """Context manager for S3 file operations."""
    
    def __init__(self, s3_uri: str, mode: str = 'rb', client: Optional[S3Client] = None, **kwargs):
        self.s3_uri = s3_uri
        self.mode = mode
        self.client = client or default_s3_client
        self.kwargs = kwargs
        self.file_obj = None
    
    def __enter__(self):
        self.file_obj = self.client.open(self.s3_uri, self.mode, **self.kwargs)
        return self.file_obj
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file_obj:
            self.file_obj.close()


if __name__ == "__main__":
    # Smoke test
    print("🧪 Running S3Client smoke test...")
    
    client = S3Client()
    
    # Test URI parsing
    bucket, key, region = client.parse_s3_uri("s3://my-bucket/path/to/file.csv")
    print(f"✅ URI parsing: bucket={bucket}, key={key}, region={region}")
    
    # Test regional URI parsing
    bucket, key, region = client.parse_s3_uri("s3://my-bucket.us-west-2.amazonaws.com/path/to/file.csv")
    print(f"✅ Regional URI parsing: bucket={bucket}, key={key}, region={region}")
    
    print("✅ S3Client smoke test passed!") 