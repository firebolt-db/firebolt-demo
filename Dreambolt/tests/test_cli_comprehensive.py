"""
Comprehensive CLI Tests for DreamBolt
====================================

Tests all CLI commands, options, and error scenarios.
Uses both Typer CliRunner and subprocess for complete coverage.
"""
import pytest
import subprocess
import sys
import json
import os
from pathlib import Path
from unittest.mock import patch, Mock
from typer.testing import CliRunner

# Import CLI applications
from cli import app as typer_app
import cli_working


class TestCLICommands:
    """Test CLI commands and functionality."""
    
    def test_cli_help(self, cli_runner):
        """Test main CLI help command."""
        result = cli_runner.invoke(typer_app, ["--help"])
        assert result.exit_code == 0
        assert "DreamBolt" in result.stdout
    
    def test_status_command(self, cli_runner):
        """Test status command."""
        with patch('cli.console') as mock_console:
            result = cli_runner.invoke(typer_app, ["status"])
            assert result.exit_code == 0
            mock_console.print.assert_called()
    
    def test_ingest_command_basic(self, cli_runner, tmp_dir, sample_csv_data):
        """Test basic ingest command."""
        input_file = tmp_dir / "test.csv"
        sample_csv_data.to_csv(input_file, index=False)
        
        with patch('cli.DataIngester') as mock_ingester:
            mock_instance = Mock()
            mock_instance.load_data.return_value = (sample_csv_data, Mock())
            mock_instance.clean_schema.return_value = sample_csv_data
            mock_ingester.return_value = mock_instance
            
            result = cli_runner.invoke(typer_app, [
                "ingest", str(input_file), "--no-synth"
            ])
            
            assert result.exit_code == 0
            mock_ingester.assert_called_once()


class TestArgparseCLI:
    """Test Argparse-based CLI (cli_working.py)."""
    
    def test_argparse_help(self):
        """Test argparse CLI help."""
        result = subprocess.run([
            sys.executable, "-c", 
            "import cli_working; cli_working.main()"
        ], input="", capture_output=True, text=True)
        
        # Should show help when no arguments provided
        assert "DreamBolt" in result.stdout
    
    def test_status_command_direct(self):
        """Test status command directly."""
        with patch('cli_working.print') as mock_print:
            cli_working.status_command()
            mock_print.assert_called()
            
            # Check that status messages were printed
            call_args = [call[0][0] for call in mock_print.call_args_list]
            status_output = ' '.join(call_args)
            assert "DreamBolt Status Check" in status_output
    
    def test_ingest_command_direct(self, tmp_dir, sample_csv_data):
        """Test ingest command directly."""
        input_file = tmp_dir / "test.csv"
        sample_csv_data.to_csv(input_file, index=False)
        
        # Create mock args
        mock_args = Mock()
        mock_args.input_path = str(input_file)
        mock_args.output = None
        mock_args.table = None
        mock_args.no_synth = True
        mock_args.synthesize = None
        mock_args.model = "openai:gpt-3.5-turbo"
        mock_args.embed = None
        mock_args.engine = None
        mock_args.dry_run = False
        mock_args.verbose = False
        
        with patch('cli_working.DataIngester') as mock_ingester, \
             patch('cli_working.FireboltConnector') as mock_firebolt:
            
            # Configure mocks
            ingester_instance = Mock()
            ingester_instance.load_data.return_value = (sample_csv_data, Mock())
            ingester_instance.clean_schema.return_value = sample_csv_data
            mock_ingester.return_value = ingester_instance
            
            cli_working.ingest_command(mock_args)
            
            mock_ingester.assert_called_once()
            ingester_instance.load_data.assert_called_once()


class TestCLIIntegration:
    """Integration tests using subprocess to test actual CLI behavior."""
    
    def test_cli_module_entry_point(self):
        """Test python -m cli entry point."""
        result = subprocess.run([
            sys.executable, "-m", "cli", "--help"
        ], capture_output=True, text=True, timeout=10)
        
        # Should either work or fall back gracefully
        assert result.returncode == 0
        assert any(word in result.stdout.lower() for word in ["dreambolt", "help", "usage"])
    
    def test_cli_status_integration(self):
        """Test status command via subprocess."""
        result = subprocess.run([
            sys.executable, "-m", "cli", "status"
        ], capture_output=True, text=True, timeout=10)
        
        assert result.returncode == 0
        assert "DreamBolt Status Check" in result.stdout
        assert "Pandas:" in result.stdout
    
    def test_cli_ingest_integration(self, tmp_dir, sample_csv_data):
        """Test ingest command via subprocess."""
        input_file = tmp_dir / "test.csv"
        sample_csv_data.to_csv(input_file, index=False)
        
        result = subprocess.run([
            sys.executable, "-m", "cli", "ingest", 
            str(input_file), "--no-synth"
        ], capture_output=True, text=True, timeout=30, cwd=tmp_dir)
        
        # Should complete successfully
        assert result.returncode == 0
        assert "Starting DreamBolt ingestion" in result.stdout
        
        # Check output file was created
        expected_output = input_file.with_suffix('.dreambolt.parquet')
        assert expected_output.exists()


class TestCLIHelperFunctions:
    """Test CLI helper functions."""
    
    @pytest.mark.parametrize("input_path,expected", [
        ("data.csv", "data.dreambolt.parquet"),
        ("data.parquet", "data.dreambolt.parquet"),
        ("/path/to/file.csv", "/path/to/file.dreambolt.parquet"),
        ("no_extension", "no_extension.dreambolt.parquet"),
    ])
    def test_generate_output_path(self, input_path, expected):
        """Test output path generation."""
        from cli import _generate_output_path
        result = _generate_output_path(input_path)
        assert result == expected
    
    @pytest.mark.parametrize("input_path,expected", [
        ("data.csv", "data"),
        ("My Data File.csv", "my_data_file"),
        ("data-with-dashes.csv", "data_with_dashes"),
        ("/path/to/file.csv", "file"),
        ("UPPERCASE.CSV", "uppercase"),
    ])
    def test_derive_table_name(self, input_path, expected):
        """Test table name derivation."""
        from cli import _derive_table_name
        result = _derive_table_name(input_path)
        assert result == expected
    
    def test_generate_output_path_argparse(self):
        """Test argparse version of output path generation."""
        from cli_working import _generate_output_path
        result = _generate_output_path("test.csv")
        assert result == "test.dreambolt.parquet"
    
    def test_derive_table_name_argparse(self):
        """Test argparse version of table name derivation."""
        from cli_working import _derive_table_name
        result = _derive_table_name("test-file.csv")
        assert result == "test_file"


class TestCLIErrorHandling:
    """Test CLI error handling and edge cases."""
    
    def test_invalid_file_extension(self, cli_runner, tmp_dir):
        """Test handling of unsupported file formats."""
        invalid_file = tmp_dir / "test.txt"
        invalid_file.write_text("some content")
        
        result = cli_runner.invoke(typer_app, [
            "ingest", str(invalid_file)
        ])
        assert result.exit_code == 1
    
    def test_permission_error(self, cli_runner, tmp_dir):
        """Test handling of permission errors."""
        # Create a file without read permissions
        restricted_file = tmp_dir / "restricted.csv"
        restricted_file.write_text("id,name\n1,test\n")
        restricted_file.chmod(0o000)
        
        try:
            result = cli_runner.invoke(typer_app, [
                "ingest", str(restricted_file)
            ])
            assert result.exit_code == 1
        finally:
            # Restore permissions for cleanup
            restricted_file.chmod(0o644)
    
    def test_large_file_timeout(self, cli_runner, tmp_dir):
        """Test handling of very large files."""
        # This would be a slow test, so we'll mock it
        large_file = tmp_dir / "large.csv"
        large_file.write_text("id,name\n1,test\n")
        
        with patch('cli.DataIngester') as mock_ingester:
            # Simulate timeout
            mock_instance = Mock()
            mock_instance.load_data.side_effect = TimeoutError("File too large")
            mock_ingester.return_value = mock_instance
            
            result = cli_runner.invoke(typer_app, [
                "ingest", str(large_file)
            ])
            assert result.exit_code == 1
    
    def test_network_error_handling(self, cli_runner, sample_s3_uri):
        """Test handling of network errors for S3 files."""
        with patch('cli.DataIngester') as mock_ingester:
            # Simulate network error
            mock_instance = Mock()
            mock_instance.load_data.side_effect = ConnectionError("Network unreachable")
            mock_ingester.return_value = mock_instance
            
            result = cli_runner.invoke(typer_app, [
                "ingest", sample_s3_uri
            ])
            assert result.exit_code == 1


class TestCLIEnvironmentVariables:
    """Test CLI behavior with different environment variable configurations."""
    
    def test_cli_with_all_env_vars(self, cli_runner, tmp_dir, sample_csv_data, ingest_config):
        """Test CLI with all environment variables set."""
        input_file = tmp_dir / "test.csv"
        sample_csv_data.to_csv(input_file, index=False)
        
        # Set environment variables
        with patch.dict(os.environ, ingest_config):
            with patch('cli.DataIngester') as mock_ingester, \
                 patch('cli.FireboltConnector') as mock_firebolt:
                
                # Configure mocks
                ingester_instance = Mock()
                ingester_instance.load_data.return_value = (sample_csv_data, Mock())
                ingester_instance.clean_schema.return_value = sample_csv_data
                mock_ingester.return_value = ingester_instance
                
                result = cli_runner.invoke(typer_app, [
                    "ingest", str(input_file),
                    "--no-synth"
                ])
                
                assert result.exit_code == 0
                mock_firebolt.assert_called_once()
    
    def test_cli_without_env_vars(self, cli_runner, tmp_dir, sample_csv_data):
        """Test CLI without environment variables (should use defaults)."""
        input_file = tmp_dir / "test.csv"
        sample_csv_data.to_csv(input_file, index=False)
        
        # Clear environment variables
        env_vars_to_clear = [
            'OPENAI_API_KEY', 'FIREBOLT_USERNAME', 'FIREBOLT_PASSWORD',
            'FIREBOLT_ACCOUNT_NAME', 'FIREBOLT_DATABASE', 'FIREBOLT_ENGINE'
        ]
        
        with patch.dict(os.environ, {}, clear=True):
            with patch('cli.DataIngester') as mock_ingester:
                # Configure mocks
                ingester_instance = Mock()
                ingester_instance.load_data.return_value = (sample_csv_data, Mock())
                ingester_instance.clean_schema.return_value = sample_csv_data
                mock_ingester.return_value = ingester_instance
                
                result = cli_runner.invoke(typer_app, [
                    "ingest", str(input_file),
                    "--no-synth"
                ])
                
                assert result.exit_code == 0


@pytest.mark.slow
class TestCLIPerformance:
    """Performance tests for CLI operations."""
    
    def test_cli_startup_time(self, performance_monitor):
        """Test CLI startup time."""
        result = subprocess.run([
            sys.executable, "-m", "cli", "--help"
        ], capture_output=True, text=True, timeout=5)
        
        assert result.returncode == 0
        # Performance monitor will check duration
    
    def test_large_dataset_processing(self, cli_runner, tmp_dir, large_dataset, performance_monitor):
        """Test processing of large datasets."""
        input_file = tmp_dir / "large.csv"
        large_dataset.to_csv(input_file, index=False)
        
        with patch('cli.DataIngester') as mock_ingester, \
             patch('cli.FireboltConnector') as mock_firebolt:
            
            # Configure mocks to simulate processing
            ingester_instance = Mock()
            ingester_instance.load_data.return_value = (large_dataset, Mock())
            ingester_instance.clean_schema.return_value = large_dataset
            mock_ingester.return_value = ingester_instance
            
            result = cli_runner.invoke(typer_app, [
                "ingest", str(input_file),
                "--no-synth"
            ])
            
            assert result.exit_code == 0 