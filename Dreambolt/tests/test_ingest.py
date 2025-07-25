"""
Integration tests for DreamBolt ingest functionality.
Testing guardrails: Write tests first, then implementation.
"""
import pytest
import tempfile
import pandas as pd
from pathlib import Path
import subprocess
import sys
from unittest.mock import patch

# Test data fixtures
@pytest.fixture
def sample_csv_data():
    """Create sample CSV data for testing."""
    return pd.DataFrame({
        'id': [1, 2, 3, 4, 5],
        'name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'],
        'age': [25, 30, 35, 28, 32],
        'salary': [50000, 60000, 70000, 55000, 65000]
    })

@pytest.fixture
def sample_csv_file(sample_csv_data):
    """Create temporary CSV file for testing."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        sample_csv_data.to_csv(f.name, index=False)
        yield f.name
    Path(f.name).unlink(missing_ok=True)

@pytest.fixture
def temp_output_dir():
    """Create temporary output directory."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir


class TestBasicIngest:
    """Test basic ingestion without synthesis."""
    
    def test_ingest_csv_no_synth(self, sample_csv_file, temp_output_dir):
        """Test: dreambolt ingest sample.csv --no-synth"""
        output_path = Path(temp_output_dir) / "output.parquet"
        
        # Mock Firebolt operations for now
        with patch('firebolt_io.ensure_table') as _mock_table, \
             patch('firebolt_io.copy_data') as _mock_copy:
            
            # This will fail until we implement CLI - that's the point!
            result = subprocess.run([
                sys.executable, "-m", "cli", 
                "ingest", sample_csv_file,
                "--output", str(output_path),
                "--no-synth"
            ], capture_output=True, text=True)
            
            # Assertions (will fail initially)
            assert result.returncode == 0, f"CLI failed: {result.stderr}"
            assert output_path.exists(), "Parquet file should be created"
            
            # Verify data integrity
            output_df = pd.read_parquet(output_path)
            input_df = pd.read_csv(sample_csv_file)
            assert len(output_df) == len(input_df), "Row count mismatch"
            
            # Verify Firebolt operations were called
            _mock_table.assert_called_once()
            _mock_copy.assert_called_once()

    def test_ingest_parquet_no_synth(self, sample_csv_data, temp_output_dir):
        """Test ingesting Parquet files."""
        input_path = Path(temp_output_dir) / "input.parquet"
        output_path = Path(temp_output_dir) / "output.parquet"
        
        # Create input Parquet file
        sample_csv_data.to_parquet(input_path)
        
        with patch('firebolt_io.ensure_table') as _mock_table, \
             patch('firebolt_io.copy_data') as _mock_copy:
            
            result = subprocess.run([
                sys.executable, "-m", "cli",
                "ingest", str(input_path),
                "--output", str(output_path),
                "--no-synth"
            ], capture_output=True, text=True)
            
            assert result.returncode == 0
            assert output_path.exists()

    @pytest.mark.skip(reason="S3 integration - TODO for later")
    def test_ingest_s3_uri(self):
        """Test: dreambolt ingest s3://bucket/path/data.csv"""
        # TODO: Implement S3 URI support
        pass


class TestSynthesisIntegration:
    """Test LLM synthesis functionality."""
    
    @pytest.mark.skip(reason="TODO: Implement after basic ingest works")
    def test_ingest_with_synthesis(self, sample_csv_file, temp_output_dir):
        """Test synthesis with DataDreamer."""
        output_path = Path(temp_output_dir) / "output.parquet"
        
        result = subprocess.run([
            sys.executable, "-m", "cli",
            "ingest", sample_csv_file,
            "--output", str(output_path),
            "--synthesize", "2",  # Generate 2 additional rows
            "--model", "openai:gpt-3.5-turbo"
        ], capture_output=True, text=True)
        
        assert result.returncode == 0
        assert output_path.exists()
        
        # Verify synthesis worked
        output_df = pd.read_parquet(output_path)
        input_df = pd.read_csv(sample_csv_file)
        assert len(output_df) > len(input_df), "Should have synthesized rows"

    @pytest.mark.skip(reason="TODO: Implement embedding support")
    def test_ingest_with_embeddings(self):
        """Test embedding generation and storage."""
        # TODO: Test embedding column creation
        pass


class TestErrorHandling:
    """Test error conditions and edge cases."""
    
    def test_invalid_file_path(self):
        """Test handling of non-existent files."""
        result = subprocess.run([
            sys.executable, "-m", "cli",
            "ingest", "nonexistent.csv"
        ], capture_output=True, text=True)
        
        assert result.returncode != 0
        assert "File not found" in result.stderr or "not found" in result.stderr.lower()

    @pytest.mark.skip(reason="TODO: Implement after Firebolt integration")
    def test_firebolt_connection_failure(self):
        """Test handling of Firebolt connection issues."""
        # TODO: Test connection error handling
        pass


# Integration smoke tests
def test_cli_help():
    """Verify CLI help system works."""
    result = subprocess.run([
        sys.executable, "-m", "cli", "--help"
    ], capture_output=True, text=True)
    
    assert result.returncode == 0
    assert "dreambolt" in result.stdout.lower()

def test_ingest_help():
    """Verify ingest command help."""
    result = subprocess.run([
        sys.executable, "-m", "cli", "ingest", "--help"
    ], capture_output=True, text=True)
    
    assert result.returncode == 0
    assert "ingest" in result.stdout.lower()


if __name__ == "__main__":
    # Local smoke test
    pytest.main([__file__, "-v"]) 