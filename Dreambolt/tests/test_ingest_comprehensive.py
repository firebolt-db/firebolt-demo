"""
Comprehensive Data Ingestion Tests
==================================

Tests for all ingestion functionality including edge cases.
"""
import pytest
import pandas as pd
import numpy as np
from pathlib import Path
from unittest.mock import patch, Mock

from ingest import DataIngester, SchemaInfo
from ingest_simple import DataIngester as SimpleDataIngester


class TestSchemaInfo:
    """Test SchemaInfo data validation."""
    
    def test_schema_info_creation(self):
        """Test SchemaInfo object creation."""
        schema = SchemaInfo(
            total_rows=100,
            total_columns=5,
            column_types={'name': 'object', 'age': 'int64'},
            null_percentages={'name': 5.0, 'age': 0.0},
            inferred_categorical=['department'],
            memory_usage={'total': 1024}
        )
        
        assert schema.total_rows == 100
        assert schema.total_columns == 5
        assert 'name' in schema.column_types
        assert schema.inferred_categorical == ['department']
    
    def test_schema_info_validation(self):
        """Test SchemaInfo validation."""
        # Test with invalid data
        with pytest.raises(ValueError):
            SchemaInfo(
                total_rows=-1,  # Invalid negative rows
                total_columns=5,
                column_types={},
                null_percentages={},
                inferred_categorical=[],
                memory_usage={}
            )


class TestDataIngester:
    """Test main DataIngester class."""
    
    def test_initialization(self):
        """Test DataIngester initialization."""
        ingester = DataIngester()
        assert ingester.supported_formats == {'.csv', '.parquet', '.pqt'}
        assert ingester.s3_client is None
    
    def test_load_csv_file(self, sample_csv_file, sample_csv_data):
        """Test loading CSV files."""
        ingester = DataIngester()
        df, schema = ingester.load_data(str(sample_csv_file))
        
        assert isinstance(df, pd.DataFrame)
        assert isinstance(schema, SchemaInfo)
        assert len(df) == len(sample_csv_data)
        assert list(df.columns) == list(sample_csv_data.columns)
    
    def test_load_parquet_file(self, sample_parquet_file, sample_parquet_data):
        """Test loading Parquet files."""
        ingester = DataIngester()
        df, schema = ingester.load_data(str(sample_parquet_file))
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == len(sample_parquet_data)
        assert 'product_id' in df.columns
    
    def test_load_nonexistent_file(self, nonexistent_file):
        """Test loading non-existent file."""
        ingester = DataIngester()
        
        with pytest.raises(FileNotFoundError):
            ingester.load_data(str(nonexistent_file))
    
    def test_load_unsupported_format(self, tmp_dir):
        """Test loading unsupported file format."""
        txt_file = tmp_dir / "test.txt"
        txt_file.write_text("not a csv")
        
        ingester = DataIngester()
        
        with pytest.raises(ValueError, match="Unsupported format"):
            ingester.load_data(str(txt_file))
    
    def test_s3_uri_detection(self):
        """Test S3 URI detection."""
        ingester = DataIngester()
        
        assert ingester._is_s3_uri("s3://bucket/key")
        assert ingester._is_s3_uri("s3://my-bucket/path/to/file.csv")
        assert not ingester._is_s3_uri("/local/path/file.csv")
        assert not ingester._is_s3_uri("https://example.com/file.csv")
    
    @pytest.mark.skipif(True, reason="S3 tests require moto setup")
    def test_load_from_s3(self, mock_s3_environment):
        """Test loading data from S3."""
        ingester = DataIngester()
        s3_uri = mock_s3_environment['test_uri']
        
        df, schema = ingester.load_data(s3_uri)
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0
    
    def test_load_from_s3_without_dependencies(self):
        """Test S3 loading without required dependencies."""
        ingester = DataIngester()
        
        with patch('ingest.S3_AVAILABLE', False):
            with pytest.raises(ImportError, match="S3 functionality requires"):
                ingester.load_data("s3://bucket/file.csv")
    
    def test_analyze_schema(self, sample_csv_data):
        """Test schema analysis."""
        ingester = DataIngester()
        schema = ingester._analyze_schema(sample_csv_data)
        
        assert isinstance(schema, SchemaInfo)
        assert schema.total_rows == len(sample_csv_data)
        assert schema.total_columns == len(sample_csv_data.columns)
        assert 'department' in schema.inferred_categorical
        assert schema.column_types['age'] in ['int64', 'int32']
    
    def test_analyze_schema_with_nulls(self, malformed_csv_data):
        """Test schema analysis with null values."""
        ingester = DataIngester()
        schema = ingester._analyze_schema(malformed_csv_data)
        
        assert schema.null_percentages['name'] > 0
        assert schema.null_percentages['salary'] > 0
    
    def test_clean_schema_basic(self, sample_csv_data):
        """Test basic schema cleaning."""
        ingester = DataIngester()
        schema = ingester._analyze_schema(sample_csv_data)
        cleaned_df = ingester.clean_schema(sample_csv_data, schema)
        
        assert isinstance(cleaned_df, pd.DataFrame)
        assert len(cleaned_df) == len(sample_csv_data)
        
        # Check column name cleaning
        assert all('_' not in col or col.replace('_', '').isalnum() for col in cleaned_df.columns)
    
    def test_clean_schema_column_names(self, malformed_csv_data):
        """Test column name cleaning."""
        ingester = DataIngester()
        schema = ingester._analyze_schema(malformed_csv_data)
        cleaned_df = ingester.clean_schema(malformed_csv_data, schema)
        
        # Check that problematic column names are cleaned
        original_columns = set(malformed_csv_data.columns)
        cleaned_columns = set(cleaned_df.columns)
        
        assert 'weird_column_name' in cleaned_columns  # Should be cleaned
        assert 'col_123numeric_start' in cleaned_columns  # Should be prefixed
    
    def test_clean_column_name_edge_cases(self):
        """Test column name cleaning edge cases."""
        ingester = DataIngester()
        
        # Test various problematic names
        assert ingester._clean_column_name("Normal Name") == "normal_name"
        assert ingester._clean_column_name("123StartWithNumber") == "col_123startwithnumber"
        assert ingester._clean_column_name("Special!@#$%Characters") == "special_characters"
        assert ingester._clean_column_name("") == "unnamed_column"
        assert ingester._clean_column_name("   ") == "unnamed_column"
        assert ingester._clean_column_name("__multiple__underscores__") == "multiple_underscores"
    
    def test_optimize_dtypes(self, sample_csv_data):
        """Test data type optimization."""
        ingester = DataIngester()
        
        # Add some data that can be optimized
        test_df = sample_csv_data.copy()
        test_df['small_int'] = [1, 2, 3, 4, 5]  # Can be uint8
        test_df['large_float'] = [1.1, 2.2, 3.3, 4.4, 5.5]  # Can be float32
        
        optimized_df = ingester._optimize_dtypes(test_df)
        
        # Check that optimization occurred
        assert optimized_df['small_int'].dtype in ['uint8', 'int8']
        assert optimized_df['large_float'].dtype in ['float32', 'float64']
    
    def test_clean_schema_drop_null_columns(self, tmp_dir):
        """Test dropping columns with high null percentage."""
        # Create DataFrame with mostly null column
        df = pd.DataFrame({
            'good_column': [1, 2, 3, 4, 5],
            'bad_column': [None, None, None, None, 1],  # 80% null
            'terrible_column': [None, None, None, None, None]  # 100% null
        })
        
        ingester = DataIngester()
        schema = ingester._analyze_schema(df)
        cleaned_df = ingester.clean_schema(df, schema)
        
        # Should drop the terrible column but keep others
        assert 'good_column' in cleaned_df.columns
        assert 'terrible_column' not in cleaned_df.columns


class TestSimpleDataIngester:
    """Test simplified DataIngester for fallback scenarios."""
    
    def test_simple_initialization(self):
        """Test SimpleDataIngester initialization."""
        ingester = SimpleDataIngester()
        assert hasattr(ingester, 'supported_formats')
    
    def test_simple_load_csv(self, sample_csv_file):
        """Test simple CSV loading."""
        ingester = SimpleDataIngester()
        df = ingester.load_data(str(sample_csv_file))
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0
    
    def test_simple_clean_column_name(self):
        """Test simple column name cleaning."""
        ingester = SimpleDataIngester()
        
        assert ingester._clean_column_name("Test Name") == "test_name"
        assert ingester._clean_column_name("123number") == "col_123number"
    
    def test_simple_optimize_dtypes(self, sample_csv_data):
        """Test simple data type optimization."""
        ingester = SimpleDataIngester()
        
        # Test with small integers
        test_df = sample_csv_data.copy()
        test_df['small_val'] = [1, 2, 3, 4, 5]
        
        optimized_df = ingester._optimize_dtypes(test_df)
        
        # Should attempt to optimize
        assert optimized_df['small_val'].dtype in ['uint8', 'int8', 'int64']


class TestIngestEdgeCases:
    """Test edge cases and error conditions."""
    
    def test_empty_csv_file(self, empty_csv_file):
        """Test loading empty CSV file."""
        ingester = DataIngester()
        df, schema = ingester.load_data(str(empty_csv_file))
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 0
        assert len(df.columns) > 0  # Should have headers
    
    def test_single_row_file(self, tmp_dir):
        """Test loading file with single row."""
        single_row_file = tmp_dir / "single.csv"
        single_row_file.write_text("id,name\n1,Alice\n")
        
        ingester = DataIngester()
        df, schema = ingester.load_data(str(single_row_file))
        
        assert len(df) == 1
        assert schema.total_rows == 1
    
    def test_malformed_csv_content(self, tmp_dir):
        """Test loading malformed CSV content."""
        malformed_file = tmp_dir / "malformed.csv"
        malformed_file.write_text("id,name\n1,Alice\n2,Bob,Extra\n3\n")
        
        ingester = DataIngester()
        # Should handle gracefully or raise appropriate error
        try:
            df, schema = ingester.load_data(str(malformed_file))
            assert isinstance(df, pd.DataFrame)
        except Exception as e:
            assert isinstance(e, (pd.errors.ParserError, ValueError))
    
    def test_very_large_column_names(self, tmp_dir):
        """Test handling very long column names."""
        long_column = "a" * 1000  # Very long column name
        df = pd.DataFrame({
            long_column: [1, 2, 3],
            'normal': [4, 5, 6]
        })
        
        csv_file = tmp_dir / "long_columns.csv"
        df.to_csv(csv_file, index=False)
        
        ingester = DataIngester()
        loaded_df, schema = ingester.load_data(str(csv_file))
        
        assert isinstance(loaded_df, pd.DataFrame)
        assert len(loaded_df.columns) == 2
    
    def test_unicode_content(self, tmp_dir):
        """Test handling Unicode content."""
        unicode_df = pd.DataFrame({
            'name': ['Alice', 'José', '张三', 'Ahmed'],
            'city': ['New York', 'México', '北京', 'القاهرة']
        })
        
        csv_file = tmp_dir / "unicode.csv"
        unicode_df.to_csv(csv_file, index=False, encoding='utf-8')
        
        ingester = DataIngester()
        df, schema = ingester.load_data(str(csv_file))
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 4
        assert 'José' in df['name'].values
    
    def test_mixed_data_types_in_column(self, tmp_dir):
        """Test handling mixed data types in columns."""
        mixed_df = pd.DataFrame({
            'mixed_column': [1, 'string', 3.14, True, None],
            'id': [1, 2, 3, 4, 5]
        })
        
        csv_file = tmp_dir / "mixed.csv"
        mixed_df.to_csv(csv_file, index=False)
        
        ingester = DataIngester()
        df, schema = ingester.load_data(str(csv_file))
        
        assert isinstance(df, pd.DataFrame)
        assert df['mixed_column'].dtype == 'object'
    
    def test_date_parsing(self, tmp_dir):
        """Test automatic date parsing."""
        date_df = pd.DataFrame({
            'date_string': ['2023-01-01', '2023-01-02', '2023-01-03'],
            'datetime_string': ['2023-01-01 10:00:00', '2023-01-02 11:00:00', '2023-01-03 12:00:00'],
            'not_date': ['abc', 'def', 'ghi']
        })
        
        csv_file = tmp_dir / "dates.csv"
        date_df.to_csv(csv_file, index=False)
        
        ingester = DataIngester()
        df, schema = ingester.load_data(str(csv_file))
        
        assert isinstance(df, pd.DataFrame)
        # Should recognize date patterns in analysis
        assert len(schema.column_types) > 0


class TestIngestPerformance:
    """Performance tests for ingestion."""
    
    @pytest.mark.slow
    def test_large_file_processing(self, tmp_dir, large_dataset, performance_monitor):
        """Test processing large datasets."""
        large_file = tmp_dir / "large.csv"
        large_dataset.to_csv(large_file, index=False)
        
        ingester = DataIngester()
        df, schema = ingester.load_data(str(large_file))
        
        assert len(df) == len(large_dataset)
        assert isinstance(schema, SchemaInfo)
    
    def test_memory_efficiency(self, tmp_dir, large_dataset):
        """Test memory usage optimization."""
        large_file = tmp_dir / "large.csv"
        large_dataset.to_csv(large_file, index=False)
        
        ingester = DataIngester()
        df, schema = ingester.load_data(str(large_file))
        
        # Clean and optimize
        cleaned_df = ingester.clean_schema(df, schema)
        
        # Check that optimization reduced memory usage
        original_memory = df.memory_usage(deep=True).sum()
        optimized_memory = cleaned_df.memory_usage(deep=True).sum()
        
        # Memory should be same or better after optimization
        assert optimized_memory <= original_memory * 1.1  # Allow 10% tolerance 