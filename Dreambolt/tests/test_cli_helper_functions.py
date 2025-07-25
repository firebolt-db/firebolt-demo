"""
Unit Tests for CLI Helper Functions
===================================

Focused tests for utility functions in the CLI modules.
"""
import pytest
from cli import _generate_output_path, _derive_table_name


class TestCLIHelperFunctions:
    """Test CLI helper functions."""
    
    @pytest.mark.parametrize("input_path,expected", [
        ("data.csv", "data.dreambolt.parquet"),
        ("data.parquet", "data.dreambolt.parquet"),
        ("/path/to/file.csv", "/path/to/file.dreambolt.parquet"),
        ("no_extension", "no_extension.dreambolt.parquet"),
        ("file.CSV", "file.dreambolt.parquet"),
        ("complex-file_name.csv", "complex-file_name.dreambolt.parquet"),
    ])
    def test_generate_output_path(self, input_path, expected):
        """Test output path generation."""
        result = _generate_output_path(input_path)
        assert result == expected
    
    @pytest.mark.parametrize("input_path,expected", [
        ("data.csv", "data"),
        ("My Data File.csv", "my data file"),
        ("data-with-dashes.csv", "data_with_dashes"),
        ("/path/to/file.csv", "file"),
        ("UPPERCASE.CSV", "uppercase"),
        ("file with spaces.parquet", "file with spaces"),
        ("special!@#chars.csv", "special!@#chars"),
        ("123numeric.csv", "123numeric"),
    ])
    def test_derive_table_name(self, input_path, expected):
        """Test table name derivation."""
        result = _derive_table_name(input_path)
        assert result == expected
    
    def test_generate_output_path_preserves_directory(self):
        """Test that directory structure is preserved."""
        input_path = "/home/user/data/file.csv"
        result = _generate_output_path(input_path)
        assert result == "/home/user/data/file.dreambolt.parquet"
    
    def test_derive_table_name_extracts_basename(self):
        """Test that table name uses only the base filename."""
        input_path = "/very/long/path/to/my_table.csv"
        result = _derive_table_name(input_path)
        assert result == "my_table" 