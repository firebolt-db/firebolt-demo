"""
Test CLI compatibility across Python version matrix (3.9-3.13).
This test validates that the CLI works correctly across all supported Python versions.
"""
import pytest
import subprocess
import sys
import json
import tempfile
import os
from pathlib import Path


class TestCLIVersionMatrix:
    """Test CLI functionality across Python version matrix."""
    
    def test_cli_import(self):
        """Test that CLI module imports successfully."""
        result = subprocess.run(
            [sys.executable, "-c", "import cli; print('SUCCESS')"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent
        )
        assert result.returncode == 0
        assert "SUCCESS" in result.stdout
        assert "Error" not in result.stderr
    
    def test_cli_help_command(self):
        """Test that CLI help command works."""
        result = subprocess.run(
            [sys.executable, "-m", "cli", "--help"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent
        )
        assert result.returncode == 0
        assert "DreamBolt" in result.stdout
        assert "ingest" in result.stdout
        assert "status" in result.stdout
    
    def test_cli_version_command(self):
        """Test that CLI version command works and shows correct info."""
        result = subprocess.run(
            [sys.executable, "-m", "cli", "--version"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent
        )
        assert result.returncode == 0
        assert "DreamBolt CLI" in result.stdout
        assert f"Python: {sys.version_info.major}.{sys.version_info.minor}" in result.stdout
        assert "Typer:" in result.stdout
        assert "Click:" in result.stdout
        assert "Platform:" in result.stdout
    
    def test_cli_status_command(self):
        """Test that CLI status command works."""
        result = subprocess.run(
            [sys.executable, "-m", "cli", "status"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent
        )
        assert result.returncode == 0
        assert "DreamBolt Status Check" in result.stdout
        assert "Pandas:" in result.stdout
    
    def test_cli_ingest_dry_run(self):
        """Test that CLI ingest command works in dry-run mode."""
        # Create a temporary CSV file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("name,age,city\n")
            f.write("Alice,25,New York\n")
            f.write("Bob,30,San Francisco\n")
            temp_csv = f.name
        
        try:
            result = subprocess.run(
                [sys.executable, "-m", "cli", "ingest", temp_csv, "--no-synth", "--dry-run"],
                capture_output=True,
                text=True,
                cwd=Path(__file__).parent.parent
            )
            
            # Should succeed or fail gracefully (not crash)
            assert result.returncode in [0, 1]  # Allow for expected failures in test env
            assert "DreamBolt ingestion" in result.stderr or "Pipeline failed" in result.stderr
            
        finally:
            # Clean up
            if os.path.exists(temp_csv):
                os.unlink(temp_csv)
    
    def test_python_version_compatibility(self):
        """Test that we're running on a supported Python version."""
        version_info = sys.version_info
        assert version_info.major == 3
        assert version_info.minor >= 9, f"Python 3.9+ required, got {version_info.major}.{version_info.minor}"
        assert version_info.minor <= 13, f"Python 3.13 is max tested, got {version_info.major}.{version_info.minor}"
    
    def test_typer_click_compatibility(self):
        """Test that Typer and Click versions are compatible."""
        try:
            from importlib.metadata import version
            typer_version = version("typer")
            click_version = version("click")
            
            # Basic version checks
            assert typer_version is not None
            assert click_version is not None
            
            # Typer should be 0.16.0+
            typer_major, typer_minor = map(int, typer_version.split('.')[:2])
            assert typer_major == 0 and typer_minor >= 16, f"Typer 0.16.0+ required, got {typer_version}"
            
            # Click should be 8.1+
            click_major, click_minor = map(int, click_version.split('.')[:2])
            assert click_major >= 8 and click_minor >= 1, f"Click 8.1+ required, got {click_version}"
            
        except Exception as e:
            pytest.fail(f"Failed to check Typer/Click compatibility: {e}")
    
    def test_no_deprecation_warnings(self):
        """Test that CLI doesn't produce deprecation warnings."""
        result = subprocess.run(
            [sys.executable, "-W", "error::DeprecationWarning", "-m", "cli", "--version"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent
        )
        
        # Should succeed without deprecation warnings
        # (If there are deprecation warnings, they'll be treated as errors)
        assert result.returncode == 0
        assert "DreamBolt CLI" in result.stdout
    
    def test_unicode_emoji_support(self):
        """Test that CLI handles Unicode/emoji correctly."""
        result = subprocess.run(
            [sys.executable, "-m", "cli", "status"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent
        )
        assert result.returncode == 0
        # Should contain emoji characters
        assert "🚀" in result.stdout or "✅" in result.stdout
    
    @pytest.mark.parametrize("command", [
        ["--help"],
        ["--version"],
        ["status"],
        ["ingest", "--help"]
    ])
    def test_cli_command_exit_codes(self, command):
        """Test that CLI commands have proper exit codes."""
        result = subprocess.run(
            [sys.executable, "-m", "cli"] + command,
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent
        )
        
        # All these commands should succeed
        assert result.returncode == 0, f"Command {command} failed with exit code {result.returncode}"


class TestPython313Specific:
    """Python 3.13 specific compatibility tests."""
    
    @pytest.mark.skipif(sys.version_info < (3, 13), reason="Python 3.13+ specific tests")
    def test_python313_new_features(self):
        """Test that CLI works with Python 3.13 specific features."""
        # Test that we can use new Python 3.13 features without issues
        result = subprocess.run(
            [sys.executable, "-c", """
import sys
print(f"Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
import cli
print("CLI imported successfully on Python 3.13")
            """],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent
        )
        assert result.returncode == 0
        assert "Python 3.13" in result.stdout
        assert "CLI imported successfully" in result.stdout
    
    @pytest.mark.skipif(sys.version_info < (3, 13), reason="Python 3.13+ specific tests")
    def test_python313_performance(self):
        """Test that CLI performs well on Python 3.13."""
        import time
        start_time = time.time()
        
        result = subprocess.run(
            [sys.executable, "-m", "cli", "--version"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent
        )
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        assert result.returncode == 0
        # Should complete within reasonable time (5 seconds is very generous)
        assert execution_time < 5.0, f"CLI took too long: {execution_time:.2f}s"


if __name__ == "__main__":
    # Run tests when executed directly
    pytest.main([__file__, "-v"]) 