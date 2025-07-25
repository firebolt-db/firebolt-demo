"""
Comprehensive tests for S3 functionality with robust error handling.
Tests S3Client wrapper, ingestion pipeline, and error scenarios.
"""
import pytest
import pandas as pd
import tempfile
import os
from unittest.mock import patch, MagicMock
from pathlib import Path

# Moto for S3 mocking
import boto3
from moto import mock_s3

# Import our S3 components
try:
    from src.utils.s3_client import (
        S3Client,
        S3File,
        is_s3_uri,
        parse_s3_uri,
        S3BaseError,
        S3AuthError,
        S3NotFoundError,
        S3RateLimitError,
        S3GenericError
    )
    S3_IMPORTS_AVAILABLE = True
except ImportError:
    S3_IMPORTS_AVAILABLE = False

from ingest import DataIngester, SchemaInfo
from botocore.exceptions import NoCredentialsError, ClientError


@pytest.mark.skipif(not S3_IMPORTS_AVAILABLE, reason="S3 components not available")
class TestS3Client:
    """Test S3Client wrapper functionality."""
    
    def test_is_s3_uri(self):
        """Test S3 URI detection."""
        assert is_s3_uri("s3://bucket/key")
        assert is_s3_uri("s3://my-bucket/path/to/file.csv")
        assert not is_s3_uri("local/path/file.csv")
        assert not is_s3_uri("https://example.com/file.csv")
        assert not is_s3_uri("")
    
    def test_parse_s3_uri_basic(self):
        """Test basic S3 URI parsing."""
        client = S3Client()
        bucket, key, region = client.parse_s3_uri("s3://my-bucket/path/to/file.csv")
        
        assert bucket == "my-bucket"
        assert key == "path/to/file.csv"
        assert region is None
    
    def test_parse_s3_uri_with_region(self):
        """Test S3 URI parsing with region detection."""
        client = S3Client()
        bucket, key, region = client.parse_s3_uri("s3://my-bucket.us-west-2.amazonaws.com/path/to/file.csv")
        
        assert bucket == "my-bucket"
        assert key == "path/to/file.csv"
        assert region == "us-west-2"
    
    def test_parse_s3_uri_invalid(self):
        """Test invalid S3 URI handling."""
        client = S3Client()
        
        with pytest.raises(ValueError, match="Invalid S3 URI"):
            client.parse_s3_uri("not-s3://bucket/key")
        
        with pytest.raises(ValueError, match="Invalid S3 URI"):
            client.parse_s3_uri("local/path/file.csv")


@pytest.mark.skipif(not S3_IMPORTS_AVAILABLE, reason="S3 components not available")
@mock_s3
class TestS3Integration:
    """Test S3 integration with mocked AWS S3."""
    
    @pytest.fixture(autouse=True)
    def setup_s3_mock(self):
        """Set up mock S3 environment."""
        # Create mock S3 service
        self.s3_client_boto = boto3.client("s3", region_name="us-east-1")
        self.bucket_name = "test-dreambolt-bucket"
        
        # Create test bucket
        self.s3_client_boto.create_bucket(Bucket=self.bucket_name)
        
        # Create test CSV data
        self.test_csv_data = pd.DataFrame({
            'id': [1, 2, 3],
            'name': ['Alice', 'Bob', 'Charlie'],
            'score': [95.5, 87.2, 92.8]
        })
        
        # Upload test CSV to mock S3
        csv_content = self.test_csv_data.to_csv(index=False)
        self.s3_client_boto.put_object(
            Bucket=self.bucket_name,
            Key="test-data.csv",
            Body=csv_content
        )
    
    def test_s3_client_exists(self):
        """Test S3 object existence checking."""
        client = S3Client()
        
        # Test existing object
        assert client.exists(f"s3://{self.bucket_name}/test-data.csv")
        
        # Test non-existing object
        assert not client.exists(f"s3://{self.bucket_name}/non-existent.csv")
    
    def test_s3_client_head_object(self):
        """Test S3 object metadata retrieval."""
        client = S3Client()
        
        metadata = client.head_object(f"s3://{self.bucket_name}/test-data.csv")
        assert 'ContentLength' in metadata
        assert metadata['ContentLength'] > 0
    
    def test_data_ingester_s3_csv_success(self):
        """Test successful CSV ingestion from S3."""
        ingester = DataIngester()
        s3_uri = f"s3://{self.bucket_name}/test-data.csv"
        
        if not ingester.s3_client:
            pytest.skip("S3 client not available in DataIngester")
        
        df, schema_info = ingester.load_data(s3_uri)
        
        # Verify data loaded correctly
        assert len(df) == 3
        assert list(df.columns) == ['id', 'name', 'score']
        assert df['name'].tolist() == ['Alice', 'Bob', 'Charlie']
        
        # Verify schema analysis
        assert isinstance(schema_info, SchemaInfo)
        assert 'id' in schema_info.column_types


class TestDataIngesterS3Fallback:
    """Test DataIngester behavior when S3 is not available."""
    
    def test_s3_detection_fallback(self):
        """Test S3 URI detection when S3 components unavailable."""
        ingester = DataIngester()
        
        # S3 URI detection should work regardless
        assert ingester._is_s3_uri("s3://bucket/key")
        assert not ingester._is_s3_uri("local/path/file.csv")


if __name__ == "__main__":
    # Run a quick smoke test
    print("🧪 Running S3 comprehensive test smoke test...")
    
    if S3_IMPORTS_AVAILABLE:
        # Test basic functionality
        assert is_s3_uri("s3://bucket/key")
        assert not is_s3_uri("local/path")
        
        bucket, key, region = parse_s3_uri("s3://test-bucket/path/file.csv")
        assert bucket == "test-bucket"
        assert key == "path/file.csv"
        
        print("✅ S3 comprehensive test smoke test passed!")
    else:
        print("⚠️ S3 imports not available - skipping advanced tests") 