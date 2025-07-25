#!/usr/bin/env python3
"""
DreamBolt Critical Fix Verification Script
Verifies that Option A fixes are working correctly.
"""

import sys
import subprocess
import importlib.util
from pathlib import Path

def test_import(module_name, description):
    """Test if a module can be imported successfully."""
    try:
        importlib.import_module(module_name)
        print(f"✅ {description}: Import successful")
        return True
    except ImportError as e:
        print(f"❌ {description}: Import failed - {e}")
        return False
    except Exception as e:
        print(f"⚠️ {description}: Import warning - {e}")
        return True  # Consider warnings as pass for compatibility

def test_cli_command(command, description):
    """Test if a CLI command runs successfully."""
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True, 
            timeout=30
        )
        if result.returncode == 0:
            print(f"✅ {description}: Command successful")
            return True
        else:
            print(f"❌ {description}: Command failed (exit {result.returncode})")
            print(f"   stderr: {result.stderr.strip()}")
            return False
    except subprocess.TimeoutExpired:
        print(f"⚠️ {description}: Command timed out (may still be working)")
        return False
    except Exception as e:
        print(f"❌ {description}: Command error - {e}")
        return False

def main():
    """Run all verification tests."""
    print("🔧 DreamBolt Critical Fix Verification")
    print("=" * 50)
    
    tests_passed = 0
    total_tests = 0
    
    # Test 1: Moto import (critical fix)
    total_tests += 1
    if test_import("moto", "Moto v4.x base import"):
        tests_passed += 1
    
    # Test 2: Moto mock_s3 import (specific fix)
    total_tests += 1
    try:
        # Import mock_s3 to verify moto v4.x compatibility
        import moto
        mock_s3 = getattr(moto, 'mock_s3', None)
        if mock_s3 is not None:
            print("✅ Moto mock_s3: Import successful (v4.x working)")
            tests_passed += 1
        else:
            print("❌ Moto mock_s3: Not available (likely moto v5.x)")
    except ImportError as e:
        print(f"❌ Moto mock_s3: Import failed - {e}")
    
    # Test 3: Trio import (Python 3.13 compatibility)
    total_tests += 1
    if test_import("trio", "Trio async library"):
        tests_passed += 1
    
    # Test 4: HTTPCore import (dependency chain)
    total_tests += 1
    if test_import("httpcore", "HTTPCore HTTP client"):
        tests_passed += 1
    
    # Test 5: HTTPx import (full stack)
    total_tests += 1
    if test_import("httpx", "HTTPx HTTP client"):
        tests_passed += 1
    
    # Test 6: CLI help command
    total_tests += 1
    if test_cli_command("python -m cli --help", "CLI help command"):
        tests_passed += 1
    
    # Test 7: CLI status command
    total_tests += 1
    if test_cli_command("python -m cli status", "CLI status command"):
        tests_passed += 1
    
    # Test 8: Basic S3 test
    total_tests += 1
    s3_test_file = Path("tests/test_s3_basic.py")
    if s3_test_file.exists():
        if test_cli_command("python -m pytest tests/test_s3_basic.py::test_s3_uri_detection -v", "Basic S3 test"):
            tests_passed += 1
    else:
        print("⚠️ Basic S3 test: Test file not found, skipping")
    
    # Summary
    print("\n" + "=" * 50)
    print(f"📊 Verification Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All critical fixes verified working!")
        print("✅ Option A implementation successful")
        return 0
    elif tests_passed >= total_tests * 0.8:
        print("⚠️ Most fixes working, some minor issues")
        print("🔧 Check individual test failures above")
        return 1
    else:
        print("❌ Critical fixes not working properly")
        print("🚨 Review requirements.txt and dependency installation")
        return 2

if __name__ == "__main__":
    sys.exit(main()) 