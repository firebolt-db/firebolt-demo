# ❌ Feature Verification Failures

**Date:** 2025-06-20 17:01:37
**Total Failures:** 21

## Command: `python -m cli ingest s3://bucket/data.parquet --embed text-embedding-ada-002`

**Source:** README.md - Basic Usage
**Exit Code:** 1

**Error Output:**
```
17:00:51 | INFO     | 🚀 Starting DreamBolt ingestion: s3://bucket/data.parquet
17:00:51 | INFO     | Loading data from: s3://bucket/data.parquet
17:00:51 | ERROR    | ❌ Pipeline failed: S3 support temporarily disabled. Use local files.
```

**Standard Output:**
```
⠋ Loading and analyzing data...
Error: S3 support temporarily disabled. Use local files.
```

## Command: `pytest -v`

**Source:** README.md - Testing
**Exit Code:** 2

**Standard Output:**
```
============================= test session starts ==============================
platform darwin -- Python 3.13.5, pytest-8.4.1, pluggy-1.6.0 -- /Users/tosh/Desktop/Dreambolt/.audit-env/bin/python3.13
cachedir: .pytest_cache
Using --randomly-seed=2738514920
rootdir: /Users/tosh/Desktop/Dreambolt
plugins: randomly-3.16.0, cov-5.0.0, anyio-4.9.0, mock-3.14.1
collecting ... collected 80 items / 4 errors

==================================== ERRORS ====================================
____________ ERROR collecting tests/test_firebolt_comprehensive.py _____________
tests/test_firebolt_comprehensive.py:11: in <module>
    from firebolt_io import FireboltConnector, FireboltConfig
firebolt_io.py:14: in <module>
    firebolt_db = importlib.import_module('firebolt.db')
                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/opt/homebrew/Cellar/python@3.13/3.13.5/Frameworks/Python.framework/Versions/3.13/lib/python3.13/importlib/__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.audit-env/lib/python3.13/site-packages/firebolt/db/__init__.py:1: in <module>
    from firebolt.common._types import (
.audit-env/lib/python3.13/site-packages/firebolt/common/__init__.py:1: in <module>
    from firebolt.common.settings import Settings
.audit-env/lib/python3.13/site-packages/firebolt/common/settings.py:6: in <module>
    from firebolt.client.auth import Auth, UsernamePassword
.audit-env/lib/python3.13/site-packages/firebolt/client/__init__.py:1: in <module>
    from firebolt.client.auth import Auth  # backward compatibility
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.audit-env/lib/python3.13/site-packages/firebolt/client/auth/__init__.py:1: in <module>
    from firebolt.client.auth.base import Auth
.audit-env/lib/python3.13/site-packages/firebolt/client/auth/base.py:4: in <module>
    from httpx import Auth as HttpxAuth
.audit-env/lib/python3.13/site-packages/httpx/__init__.py:2: in <module>
    from ._api import delete, get, head, options, patch, post, put, request, stream
.audit-env/lib/python3.13/site-packages/httpx/_api.py:4: in <module>
    from ._client import Client
.audit-env/lib/python3.13/site-packages/httpx/_client.py:30: in <module>
    from ._transports.default import AsyncHTTPTransport, HTTPTransport
.audit-env/lib/python3.13/site-packages/httpx/_transports/default.py:30: in <module>
    import httpcore
.audit-env/lib/python3.13/site-packages/httpcore/__init__.py:1: in <module>
    from ._api import request, stream
.audit-env/lib/python3.13/site-packages/httpcore/_api.py:5: in <module>
    from ._sync.connection_pool import ConnectionPool
.audit-env/lib/python3.13/site-packages/httpcore/_sync/__init__.py:1: in <module>
    from .connection import HTTPConnection
.audit-env/lib/python3.13/site-packages/httpcore/_sync/connection.py:12: in <module>
    from .._synchronization import Lock
.audit-env/lib/python3.13/site-packages/httpcore/_synchronization.py:13: in <module>
    import trio
.audit-env/lib/python3.13/site-packages/trio/__init__.py:71: in <module>
    from ._path import Path
.audit-env/lib/python3.13/site-packages/trio/_path.py:134: in <module>
    class Path(metaclass=AsyncAutoWrapperType):
.audit-env/lib/python3.13/site-packages/trio/_path.py:85: in __init__
    type(cls).generate_forwards(cls, attrs)
.audit-env/lib/python3.13/site-packages/trio/_path.py:102: in generate_forwards
    raise TypeError(attr_name, type(attr))
E   TypeError: ('parser', <class 'module'>)
_____________ ERROR collecting tests/test_ingest_comprehensive.py ______________
tests/test_ingest_comprehensive.py:13: in <module>
    from ingest import DataIngester, SchemaInfo
ingest.py:13: in <module>
    from src.utils.s3_client import (
src/utils/s3_client.py:7: in <module>
    import s3fs
.audit-env/lib/python3.13/site-packages/s3fs/__init__.py:1: in <module>
    from .core import S3FileSystem, S3File
.audit-env/lib/python3.13/site-packages/s3fs/core.py:30: in <module>
    import aiobotocore.session
.audit-env/lib/python3.13/site-packages/aiobotocore/session.py:11: in <module>
    from .client import AioBaseClient, AioClientCreator
.audit-env/lib/python3.13/site-packages/aiobotocore/client.py:20: in <module>
    from .args import AioClientArgsCreator
.audit-env/lib/python3.13/site-packages/aiobotocore/args.py:7: in <module>
    from .config import AioConfig
.audit-env/lib/python3.13/site-packages/aiobotocore/config.py:6: in <module>
    from aiobotocore.endpoint import DEFAULT_HTTP_SESSION_CLS
.audit-env/lib/python3.13/site-packages/aiobotocore/endpoint.py:17: in <module>
    from aiobotocore.httpchecksum import handle_checksum_body
.audit-env/lib/python3.13/site-packages/aiobotocore/httpchecksum.py:19: in <module>
    import httpx
.audit-env/lib/python3.13/site-packages/httpx/__init__.py:2: in <module>
    from ._api import delete, get, head, options, patch, post, put, request, stream
.audit-env/lib/python3.13/site-packages/httpx/_api.py:4: in <module>
    from ._client import Client
.audit-env/lib/python3.13/site-packages/httpx/_client.py:30: in <module>
    from ._transports.default import AsyncHTTPTransport, HTTPTransport
.audit-env/lib/python3.13/site-packages/httpx/_transports/default.py:30: in <module>
    import httpcore
.audit-env/lib/python3.13/site-packages/httpcore/__init__.py:1: in <module>
    from ._api import request, stream
.audit-env/lib/python3.13/site-packages/httpcore/_api.py:5: in <module>
    from ._sync.connection_pool import ConnectionPool
.audit-env/lib/python3.13/site-packages/httpcore/_sync/__init__.py:1: in <module>
    from .connection import HTTPConnection
.audit-env/lib/python3.13/site-packages/httpcore/_sync/connection.py:12: in <module>
    from .._synchronization import Lock
.audit-env/lib/python3.13/site-packages/httpcore/_synchronization.py:13: in <module>
    import trio
.audit-env/lib/python3.13/site-packages/trio/__init__.py:71: in <module>
    from ._path import Path
.audit-env/lib/python3.13/site-packages/trio/_path.py:134: in <module>
    class Path(metaclass=AsyncAutoWrapperType):
.audit-env/lib/python3.13/site-packages/trio/_path.py:85: in __init__
    type(cls).generate_forwards(cls, attrs)
.audit-env/lib/python3.13/site-packages/trio/_path.py:102: in generate_forwards
    raise TypeError(attr_name, type(attr))
E   TypeError: ('parser', <class 'module'>)
_______________ ERROR collecting tests/test_s3_comprehensive.py ________________
ImportError while importing test module '/Users/tosh/Desktop/Dreambolt/tests/test_s3_comprehensive.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/opt/homebrew/Cellar/python@3.13/3.13.5/Frameworks/Python.framework/Versions/3.13/lib/python3.13/importlib/__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
tests/test_s3_comprehensive.py:14: in <module>
    from moto import mock_s3
E   ImportError: cannot import name 'mock_s3' from 'moto' (/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/moto/__init__.py). Did you mean: 'mock_aws'?
____________ ERROR collecting tests/test_synthesis_comprehensive.py ____________
tests/test_synthesis_comprehensive.py:12: in <module>
    from synth import DataSynthesizer, ModelConfig
synth.py:39: in <module>
    import openai
.audit-env/lib/python3.13/site-packages/openai/__init__.py:9: in <module>
    from . import types
.audit-env/lib/python3.13/site-packages/openai/types/__init__.py:5: in <module>
    from .batch import Batch as Batch
.audit-env/lib/python3.13/site-packages/openai/types/batch.py:6: in <module>
    from .._models import BaseModel
.audit-env/lib/python3.13/site-packages/openai/_models.py:25: in <module>
    from ._types import (
.audit-env/lib/python3.13/site-packages/openai/_types.py:21: in <module>
    import httpx
.audit-env/lib/python3.13/site-packages/httpx/__init__.py:2: in <module>
    from ._api import delete, get, head, options, patch, post, put, request, stream
.audit-env/lib/python3.13/site-packages/httpx/_api.py:4: in <module>
    from ._client import Client
.audit-env/lib/python3.13/site-packages/httpx/_client.py:30: in <module>
    from ._transports.default import AsyncHTTPTransport, HTTPTransport
.audit-env/lib/python3.13/site-packages/httpx/_transports/default.py:30: in <module>
    import httpcore
.audit-env/lib/python3.13/site-packages/httpcore/__init__.py:1: in <module>
    from ._api import request, stream
.audit-env/lib/python3.13/site-packages/httpcore/_api.py:5: in <module>
    from ._sync.connection_pool import ConnectionPool
.audit-env/lib/python3.13/site-packages/httpcore/_sync/__init__.py:1: in <module>
    from .connection import HTTPConnection
.audit-env/lib/python3.13/site-packages/httpcore/_sync/connection.py:12: in <module>
    from .._synchronization import Lock
.audit-env/lib/python3.13/site-packages/httpcore/_synchronization.py:13: in <module>
    import trio
.audit-env/lib/python3.13/site-packages/trio/__init__.py:71: in <module>
    from ._path import Path
.audit-env/lib/python3.13/site-packages/trio/_path.py:134: in <module>
    class Path(metaclass=AsyncAutoWrapperType):
.audit-env/lib/python3.13/site-packages/trio/_path.py:85: in __init__
    type(cls).generate_forwards(cls, attrs)
.audit-env/lib/python3.13/site-packages/trio/_path.py:102: in generate_forwards
    raise TypeError(attr_name, type(attr))
E   TypeError: ('parser', <class 'module'>)
------------------------------- Captured stderr --------------------------------
17:00:53 | INFO     | DataDreamer not available - synthesis features will use fallback
=============================== warnings summary ===============================
.audit-env/lib/python3.13/site-packages/pydantic/_internal/_config.py:323
  /Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/pydantic/_internal/_config.py:323: PydanticDeprecatedSince20: Support for class-based `config` is deprecated, use ConfigDict instead. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.11/migration/
    warnings.warn(DEPRECATION_MESSAGE, DeprecationWarning)

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=========================== short test summary info ============================
ERROR tests/test_firebolt_comprehensive.py - TypeError: ('parser', <class 'mo...
ERROR tests/test_ingest_comprehensive.py - TypeError: ('parser', <class 'modu...
ERROR tests/test_s3_comprehensive.py
ERROR tests/test_synthesis_comprehensive.py - TypeError: ('parser', <class 'm...
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
========================= 1 warning, 4 errors in 0.72s =========================
```

## Command: `pytest tests/test_cli_examples.py -v`

**Source:** README.md - Testing
**Exit Code:** 1

**Standard Output:**
```
============================= test session starts ==============================
platform darwin -- Python 3.13.5, pytest-8.4.1, pluggy-1.6.0 -- /Users/tosh/Desktop/Dreambolt/.audit-env/bin/python3.13
cachedir: .pytest_cache
Using --randomly-seed=2859682071
rootdir: /Users/tosh/Desktop/Dreambolt
plugins: randomly-3.16.0, cov-5.0.0, anyio-4.9.0, mock-3.14.1
collecting ... collected 7 items

tests/test_cli_examples.py::TestCLIExamples::test_ingest_command_basic FAILED [ 14%]
tests/test_cli_examples.py::TestCLIExamples::test_cli_regression_coverage FAILED [ 28%]
tests/test_cli_examples.py::TestCLIExamples::test_cli_entry_point_exists PASSED [ 42%]
tests/test_cli_examples.py::TestCLIExamples::test_status_command PASSED  [ 57%]
tests/test_cli_examples.py::TestCLIExamples::test_golden_run_commands[golden_run1] FAILED [ 71%]
tests/test_cli_examples.py::TestCLIExamples::test_golden_run_commands[golden_run0] PASSED [ 85%]
tests/test_cli_examples.py::TestCLIExamples::test_help_commands_accessible PASSED [100%]

=================================== FAILURES ===================================
__________________ TestCLIExamples.test_ingest_command_basic ___________________

self = <test_cli_examples.TestCLIExamples object at 0x11349ad70>

    def test_ingest_command_basic(self):
        """Test basic ingestion without synthesis."""
        # Only run if test data exists
        test_file = PROJECT_ROOT / "WorldCupPlayers.csv"
        if not test_file.exists():
            pytest.skip("Test data file WorldCupPlayers.csv not found")

        result = subprocess.run([
            sys.executable, "-m", "cli", "ingest",
            str(test_file), "--no-synth"
        ], cwd=PROJECT_ROOT, capture_output=True, text=True, timeout=30)

        assert result.returncode == 0, f"Ingest command failed: {result.stderr}"

        # Check for expected output messages
>       assert "Starting DreamBolt ingestion" in result.stdout
E       assert 'Starting DreamBolt ingestion' in '⠙ Loading and analyzing data...\n⠙ Cleaning schema...           \n⠙ Writing output files...      \n⠙ Loading to Firebolt...       \n✅ Ingestion completed successfully!\n'
E        +  where '⠙ Loading and analyzing data...\n⠙ Cleaning schema...           \n⠙ Writing output files...      \n⠙ Loading to Firebolt...       \n✅ Ingestion completed successfully!\n' = CompletedProcess(args=['/Users/tosh/Desktop/Dreambolt/.audit-env/bin/python3.13', '-m', 'cli', 'ingest', '/Users/tosh/Desktop/Dreambolt/WorldCupPlayers.csv', '--no-synth'], returncode=0, stdout='⠙ Loading and analyzing data...\n⠙ Cleaning schema...           \n⠙ Writing output files...      \n⠙ Loading to Firebolt...       \n✅ Ingestion completed successfully!\n', stderr="17:00:54 | INFO     | 🚀 Starting DreamBolt ingestion: /Users/tosh/Desktop/Dreambolt/WorldCupPlayers.csv\n17:00:54 | INFO     | Loading data from: /Users/tosh/Desktop/Dreambolt/WorldCupPlayers.csv\n17:00:54 | INFO     | Loaded 37784 rows, 9 columns\n17:00:54 | INFO     | 📊 Loaded 37784 rows, 9 columns\n17:00:54 | INFO     | Cleaning and standardizing schema\n17:00:54 | INFO     | Schema cleaning complete: 9 columns retained\n17:00:54 | INFO     | 🧹 Schema cleaned and validated\n17:00:54 | INFO     | 💾 Saved to: /Users/tosh/Desktop/Dreambolt/WorldCupPlayers.dreambolt.parquet\n17:00:54 | INFO     | Firebolt credentials not configured - operations will be simulated\n17:00:54 | INFO     | Firebolt not configured - running in simulation mode\n17:00:54 | INFO     | 🎭 Simulating table creation: worldcupplayers\n17:00:54 | INFO     |    - Columns: 9\n17:00:54 | INFO     |    - Schema: {'roundid': 'int64', 'matchid': 'int64', 'team_initials': 'category', 'coach_name': 'category', 'line_up': 'category', 'shirt_number': 'uint8', 'player_name': 'object', 'position': 'category', 'event': 'category'}\n17:00:54 | INFO     |    - Mode: replace\n17:00:54 | INFO     | 🎭 Simulating data copy to: worldcupplayers\n17:00:54 | INFO     |    - Source: /Users/tosh/Desktop/Dreambolt/WorldCupPlayers.dreambolt.parquet\n17:00:54 | INFO     |    - Rows: 37784 (actual count from file)\n17:00:54 | INFO     | 🔥 Data loaded to Firebolt table: worldcupplayers\n").stdout

tests/test_cli_examples.py:71: AssertionError
_________________ TestCLIExamples.test_cli_regression_coverage _________________

self = <test_cli_examples.TestCLIExamples object at 0x1136808d0>

    def test_cli_regression_coverage(self):
        """Ensure we have test coverage for critical CLI functionality."""
        critical_functions = [
            "python -m cli status",
            "python -m cli ingest --help",
        ]

        tested_commands = set()
        if GOLDEN_RUNS_FILE.exists():
            with open(GOLDEN_RUNS_FILE) as f:
                data = json.load(f)
                tested_commands = set(cmd["command"] for cmd in data.get("tested_commands", []))

        # Check that we have coverage for critical functions
        coverage_count = sum(1 for cmd in critical_functions if any(cmd in tested for tested in tested_commands))
        coverage_ratio = coverage_count / len(critical_functions)

>       assert coverage_ratio >= 0.8, (
            f"CLI test coverage too low: {coverage_ratio:.1%}\n"
            f"Critical functions: {critical_functions}\n"
            f"Tested commands: {list(tested_commands)}"
        )
E       AssertionError: CLI test coverage too low: 50.0%
E         Critical functions: ['python -m cli status', 'python -m cli ingest --help']
E         Tested commands: ['python -m cli status', 'python -m cli ingest WorldCupPlayers.csv --no-synth']
E       assert 0.5 >= 0.8

tests/test_cli_examples.py:144: AssertionError
____________ TestCLIExamples.test_golden_run_commands[golden_run1] _____________

self = <test_cli_examples.TestCLIExamples object at 0x1136807c0>
golden_run = {'command': 'python -m cli ingest WorldCupPlayers.csv --no-synth', 'execution_time_seconds': 2.1, 'exit_code': 0, 'output_files': ['WorldCupPlayers.dreambolt.parquet'], ...}

    @pytest.mark.parametrize("golden_run", [
        run for run in (
            json.load(open(GOLDEN_RUNS_FILE)) if GOLDEN_RUNS_FILE.exists()
            else {"tested_commands": []}
        ).get("tested_commands", [])
        if run.get("status") == "PASS"
    ])
    def test_golden_run_commands(self, golden_run):
        """Test each golden run command reproduces expected results."""
        cmd_parts = golden_run["command"].split()

        result = subprocess.run(
            cmd_parts, cwd=PROJECT_ROOT, capture_output=True, text=True, timeout=30
        )

        assert result.returncode == golden_run["exit_code"], (
            f"Command failed: {golden_run['command']}\n"
            f"Expected exit code: {golden_run['exit_code']}\n"
            f"Actual exit code: {result.returncode}\n"
            f"Stderr: {result.stderr}"
        )

        # Check that key output substrings are present
        expected_substrings = [
            "DreamBolt", "🚀"  # Basic branding should always appear
        ]

        for substring in expected_substrings:
>           assert substring in result.stdout, (
                f"Expected substring '{substring}' not found in output:\n{result.stdout}"
            )
E           AssertionError: Expected substring 'DreamBolt' not found in output:
E             ⠙ Loading and analyzing data...
E             ⠙ Cleaning schema...
E             ⠙ Writing output files...
E             ⠙ Loading to Firebolt...
E             ✅ Ingestion completed successfully!
E
E           assert 'DreamBolt' in '⠙ Loading and analyzing data...\n⠙ Cleaning schema...           \n⠙ Writing output files...      \n⠙ Loading to Firebolt...       \n✅ Ingestion completed successfully!\n'
E            +  where '⠙ Loading and analyzing data...\n⠙ Cleaning schema...           \n⠙ Writing output files...      \n⠙ Loading to Firebolt...       \n✅ Ingestion completed successfully!\n' = CompletedProcess(args=['python', '-m', 'cli', 'ingest', 'WorldCupPlayers.csv', '--no-synth'], returncode=0, stdout='⠙ Loading and analyzing data...\n⠙ Cleaning schema...           \n⠙ Writing output files...      \n⠙ Loading to Firebolt...       \n✅ Ingestion completed successfully!\n', stderr="17:00:55 | INFO     | 🚀 Starting DreamBolt ingestion: WorldCupPlayers.csv\n17:00:55 | INFO     | Loading data from: WorldCupPlayers.csv\n17:00:55 | INFO     | Loaded 37784 rows, 9 columns\n17:00:55 | INFO     | 📊 Loaded 37784 rows, 9 columns\n17:00:55 | INFO     | Cleaning and standardizing schema\n17:00:55 | INFO     | Schema cleaning complete: 9 columns retained\n17:00:55 | INFO     | 🧹 Schema cleaned and validated\n17:00:56 | INFO     | 💾 Saved to: WorldCupPlayers.dreambolt.parquet\n17:00:56 | INFO     | Firebolt credentials not configured - operations will be simulated\n17:00:56 | INFO     | Firebolt not configured - running in simulation mode\n17:00:56 | INFO     | 🎭 Simulating table creation: worldcupplayers\n17:00:56 | INFO     |    - Columns: 9\n17:00:56 | INFO     |    - Schema: {'roundid': 'int64', 'matchid': 'int64', 'team_initials': 'category', 'coach_name': 'category', 'line_up': 'category', 'shirt_number': 'uint8', 'player_name': 'object', 'position': 'category', 'event': 'category'}\n17:00:56 | INFO     |    - Mode: replace\n17:00:56 | INFO     | 🎭 Simulating data copy to: worldcupplayers\n17:00:56 | INFO     |    - Source: WorldCupPlayers.dreambolt.parquet\n17:00:56 | INFO     |    - Rows: 37784 (actual count from file)\n17:00:56 | INFO     | 🔥 Data loaded to Firebolt table: worldcupplayers\n").stdout

tests/test_cli_examples.py:123: AssertionError
=========================== short test summary info ============================
FAILED tests/test_cli_examples.py::TestCLIExamples::test_ingest_command_basic
FAILED tests/test_cli_examples.py::TestCLIExamples::test_cli_regression_coverage
FAILED tests/test_cli_examples.py::TestCLIExamples::test_golden_run_commands[golden_run1]
========================= 3 failed, 4 passed in 3.22s ==========================
```

## Command: `pytest tests/test_ingest.py -v`

**Source:** README.md - Testing
**Exit Code:** 1

**Standard Output:**
```
============================= test session starts ==============================
platform darwin -- Python 3.13.5, pytest-8.4.1, pluggy-1.6.0 -- /Users/tosh/Desktop/Dreambolt/.audit-env/bin/python3.13
cachedir: .pytest_cache
Using --randomly-seed=305315366
rootdir: /Users/tosh/Desktop/Dreambolt
plugins: randomly-3.16.0, cov-5.0.0, anyio-4.9.0, mock-3.14.1
collecting ... collected 9 items

tests/test_ingest.py::TestErrorHandling::test_invalid_file_path PASSED   [ 11%]
tests/test_ingest.py::TestErrorHandling::test_firebolt_connection_failure SKIPPED [ 22%]
tests/test_ingest.py::TestSynthesisIntegration::test_ingest_with_synthesis SKIPPED [ 33%]
tests/test_ingest.py::TestSynthesisIntegration::test_ingest_with_embeddings SKIPPED [ 44%]
tests/test_ingest.py::test_ingest_help PASSED                            [ 55%]
tests/test_ingest.py::test_cli_help PASSED                               [ 66%]
tests/test_ingest.py::TestBasicIngest::test_ingest_parquet_no_synth FAILED [ 77%]
tests/test_ingest.py::TestBasicIngest::test_ingest_csv_no_synth FAILED   [ 88%]
tests/test_ingest.py::TestBasicIngest::test_ingest_s3_uri SKIPPED (S...) [100%]

=================================== FAILURES ===================================
_________________ TestBasicIngest.test_ingest_parquet_no_synth _________________

self = <test_ingest.TestBasicIngest object at 0x10a605a90>
sample_csv_data =    id     name  age  salary
0   1    Alice   25   50000
1   2      Bob   30   60000
2   3  Charlie   35   70000
3   4    Diana   28   55000
4   5      Eve   32   65000
temp_output_dir = '/var/folders/z3/bjtrhnk91qqdx5ttwqn647200000gn/T/tmp151px8gv'

    def test_ingest_parquet_no_synth(self, sample_csv_data, temp_output_dir):
        """Test ingesting Parquet files."""
        input_path = Path(temp_output_dir) / "input.parquet"
        output_path = Path(temp_output_dir) / "output.parquet"

        # Create input Parquet file
        sample_csv_data.to_parquet(input_path)

>       with patch('firebolt_io.ensure_table') as _mock_table, \
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
             patch('firebolt_io.copy_data') as _mock_copy:

tests/test_ingest.py:79:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
/opt/homebrew/Cellar/python@3.13/3.13.5/Frameworks/Python.framework/Versions/3.13/lib/python3.13/unittest/mock.py:1481: in __enter__
    self.target = self.getter()
                  ^^^^^^^^^^^^^
/opt/homebrew/Cellar/python@3.13/3.13.5/Frameworks/Python.framework/Versions/3.13/lib/python3.13/pkgutil.py:513: in resolve_name
    mod = importlib.import_module(modname)
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/opt/homebrew/Cellar/python@3.13/3.13.5/Frameworks/Python.framework/Versions/3.13/lib/python3.13/importlib/__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
<frozen importlib._bootstrap>:1387: in _gcd_import
    ???
<frozen importlib._bootstrap>:1360: in _find_and_load
    ???
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

name = 'firebolt_io', import_ = <function _gcd_import at 0x1024944a0>

>   ???
E   ModuleNotFoundError: No module named 'firebolt_io'

<frozen importlib._bootstrap>:1324: ModuleNotFoundError
___________________ TestBasicIngest.test_ingest_csv_no_synth ___________________

self = <test_ingest.TestBasicIngest object at 0x10a605bd0>
sample_csv_file = '/var/folders/z3/bjtrhnk91qqdx5ttwqn647200000gn/T/tmp05bpqu8y.csv'
temp_output_dir = '/var/folders/z3/bjtrhnk91qqdx5ttwqn647200000gn/T/tmpp4y1jidc'

    def test_ingest_csv_no_synth(self, sample_csv_file, temp_output_dir):
        """Test: dreambolt ingest sample.csv --no-synth"""
        output_path = Path(temp_output_dir) / "output.parquet"

        # Mock Firebolt operations for now
>       with patch('firebolt_io.ensure_table') as _mock_table, \
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
             patch('firebolt_io.copy_data') as _mock_copy:

tests/test_ingest.py:47:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
/opt/homebrew/Cellar/python@3.13/3.13.5/Frameworks/Python.framework/Versions/3.13/lib/python3.13/unittest/mock.py:1481: in __enter__
    self.target = self.getter()
                  ^^^^^^^^^^^^^
/opt/homebrew/Cellar/python@3.13/3.13.5/Frameworks/Python.framework/Versions/3.13/lib/python3.13/pkgutil.py:513: in resolve_name
    mod = importlib.import_module(modname)
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/opt/homebrew/Cellar/python@3.13/3.13.5/Frameworks/Python.framework/Versions/3.13/lib/python3.13/importlib/__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
<frozen importlib._bootstrap>:1387: in _gcd_import
    ???
<frozen importlib._bootstrap>:1360: in _find_and_load
    ???
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

name = 'firebolt_io', import_ = <function _gcd_import at 0x1024944a0>

>   ???
E   ModuleNotFoundError: No module named 'firebolt_io'

<frozen importlib._bootstrap>:1324: ModuleNotFoundError
=========================== short test summary info ============================
FAILED tests/test_ingest.py::TestBasicIngest::test_ingest_parquet_no_synth - ...
FAILED tests/test_ingest.py::TestBasicIngest::test_ingest_csv_no_synth - Modu...
==================== 2 failed, 3 passed, 4 skipped in 1.45s ====================
```

## Command: `pytest -k "test_basic" -v`

**Source:** README.md - Testing
**Exit Code:** 2

**Standard Output:**
```
============================= test session starts ==============================
platform darwin -- Python 3.13.5, pytest-8.4.1, pluggy-1.6.0 -- /Users/tosh/Desktop/Dreambolt/.audit-env/bin/python3.13
cachedir: .pytest_cache
Using --randomly-seed=2501028555
rootdir: /Users/tosh/Desktop/Dreambolt
plugins: randomly-3.16.0, cov-5.0.0, anyio-4.9.0, mock-3.14.1
collecting ... collected 80 items / 4 errors / 80 deselected / 0 selected

==================================== ERRORS ====================================
____________ ERROR collecting tests/test_firebolt_comprehensive.py _____________
tests/test_firebolt_comprehensive.py:11: in <module>
    from firebolt_io import FireboltConnector, FireboltConfig
firebolt_io.py:14: in <module>
    firebolt_db = importlib.import_module('firebolt.db')
                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/opt/homebrew/Cellar/python@3.13/3.13.5/Frameworks/Python.framework/Versions/3.13/lib/python3.13/importlib/__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.audit-env/lib/python3.13/site-packages/firebolt/db/__init__.py:1: in <module>
    from firebolt.common._types import (
.audit-env/lib/python3.13/site-packages/firebolt/common/__init__.py:1: in <module>
    from firebolt.common.settings import Settings
.audit-env/lib/python3.13/site-packages/firebolt/common/settings.py:6: in <module>
    from firebolt.client.auth import Auth, UsernamePassword
.audit-env/lib/python3.13/site-packages/firebolt/client/__init__.py:1: in <module>
    from firebolt.client.auth import Auth  # backward compatibility
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.audit-env/lib/python3.13/site-packages/firebolt/client/auth/__init__.py:1: in <module>
    from firebolt.client.auth.base import Auth
.audit-env/lib/python3.13/site-packages/firebolt/client/auth/base.py:4: in <module>
    from httpx import Auth as HttpxAuth
.audit-env/lib/python3.13/site-packages/httpx/__init__.py:2: in <module>
    from ._api import delete, get, head, options, patch, post, put, request, stream
.audit-env/lib/python3.13/site-packages/httpx/_api.py:4: in <module>
    from ._client import Client
.audit-env/lib/python3.13/site-packages/httpx/_client.py:30: in <module>
    from ._transports.default import AsyncHTTPTransport, HTTPTransport
.audit-env/lib/python3.13/site-packages/httpx/_transports/default.py:30: in <module>
    import httpcore
.audit-env/lib/python3.13/site-packages/httpcore/__init__.py:1: in <module>
    from ._api import request, stream
.audit-env/lib/python3.13/site-packages/httpcore/_api.py:5: in <module>
    from ._sync.connection_pool import ConnectionPool
.audit-env/lib/python3.13/site-packages/httpcore/_sync/__init__.py:1: in <module>
    from .connection import HTTPConnection
.audit-env/lib/python3.13/site-packages/httpcore/_sync/connection.py:12: in <module>
    from .._synchronization import Lock
.audit-env/lib/python3.13/site-packages/httpcore/_synchronization.py:13: in <module>
    import trio
.audit-env/lib/python3.13/site-packages/trio/__init__.py:71: in <module>
    from ._path import Path
.audit-env/lib/python3.13/site-packages/trio/_path.py:134: in <module>
    class Path(metaclass=AsyncAutoWrapperType):
.audit-env/lib/python3.13/site-packages/trio/_path.py:85: in __init__
    type(cls).generate_forwards(cls, attrs)
.audit-env/lib/python3.13/site-packages/trio/_path.py:102: in generate_forwards
    raise TypeError(attr_name, type(attr))
E   TypeError: ('parser', <class 'module'>)
_____________ ERROR collecting tests/test_ingest_comprehensive.py ______________
tests/test_ingest_comprehensive.py:13: in <module>
    from ingest import DataIngester, SchemaInfo
ingest.py:13: in <module>
    from src.utils.s3_client import (
src/utils/s3_client.py:7: in <module>
    import s3fs
.audit-env/lib/python3.13/site-packages/s3fs/__init__.py:1: in <module>
    from .core import S3FileSystem, S3File
.audit-env/lib/python3.13/site-packages/s3fs/core.py:30: in <module>
    import aiobotocore.session
.audit-env/lib/python3.13/site-packages/aiobotocore/session.py:11: in <module>
    from .client import AioBaseClient, AioClientCreator
.audit-env/lib/python3.13/site-packages/aiobotocore/client.py:20: in <module>
    from .args import AioClientArgsCreator
.audit-env/lib/python3.13/site-packages/aiobotocore/args.py:7: in <module>
    from .config import AioConfig
.audit-env/lib/python3.13/site-packages/aiobotocore/config.py:6: in <module>
    from aiobotocore.endpoint import DEFAULT_HTTP_SESSION_CLS
.audit-env/lib/python3.13/site-packages/aiobotocore/endpoint.py:17: in <module>
    from aiobotocore.httpchecksum import handle_checksum_body
.audit-env/lib/python3.13/site-packages/aiobotocore/httpchecksum.py:19: in <module>
    import httpx
.audit-env/lib/python3.13/site-packages/httpx/__init__.py:2: in <module>
    from ._api import delete, get, head, options, patch, post, put, request, stream
.audit-env/lib/python3.13/site-packages/httpx/_api.py:4: in <module>
    from ._client import Client
.audit-env/lib/python3.13/site-packages/httpx/_client.py:30: in <module>
    from ._transports.default import AsyncHTTPTransport, HTTPTransport
.audit-env/lib/python3.13/site-packages/httpx/_transports/default.py:30: in <module>
    import httpcore
.audit-env/lib/python3.13/site-packages/httpcore/__init__.py:1: in <module>
    from ._api import request, stream
.audit-env/lib/python3.13/site-packages/httpcore/_api.py:5: in <module>
    from ._sync.connection_pool import ConnectionPool
.audit-env/lib/python3.13/site-packages/httpcore/_sync/__init__.py:1: in <module>
    from .connection import HTTPConnection
.audit-env/lib/python3.13/site-packages/httpcore/_sync/connection.py:12: in <module>
    from .._synchronization import Lock
.audit-env/lib/python3.13/site-packages/httpcore/_synchronization.py:13: in <module>
    import trio
.audit-env/lib/python3.13/site-packages/trio/__init__.py:71: in <module>
    from ._path import Path
.audit-env/lib/python3.13/site-packages/trio/_path.py:134: in <module>
    class Path(metaclass=AsyncAutoWrapperType):
.audit-env/lib/python3.13/site-packages/trio/_path.py:85: in __init__
    type(cls).generate_forwards(cls, attrs)
.audit-env/lib/python3.13/site-packages/trio/_path.py:102: in generate_forwards
    raise TypeError(attr_name, type(attr))
E   TypeError: ('parser', <class 'module'>)
_______________ ERROR collecting tests/test_s3_comprehensive.py ________________
ImportError while importing test module '/Users/tosh/Desktop/Dreambolt/tests/test_s3_comprehensive.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/opt/homebrew/Cellar/python@3.13/3.13.5/Frameworks/Python.framework/Versions/3.13/lib/python3.13/importlib/__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
tests/test_s3_comprehensive.py:14: in <module>
    from moto import mock_s3
E   ImportError: cannot import name 'mock_s3' from 'moto' (/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/moto/__init__.py). Did you mean: 'mock_aws'?
____________ ERROR collecting tests/test_synthesis_comprehensive.py ____________
tests/test_synthesis_comprehensive.py:12: in <module>
    from synth import DataSynthesizer, ModelConfig
synth.py:39: in <module>
    import openai
.audit-env/lib/python3.13/site-packages/openai/__init__.py:9: in <module>
    from . import types
.audit-env/lib/python3.13/site-packages/openai/types/__init__.py:5: in <module>
    from .batch import Batch as Batch
.audit-env/lib/python3.13/site-packages/openai/types/batch.py:6: in <module>
    from .._models import BaseModel
.audit-env/lib/python3.13/site-packages/openai/_models.py:25: in <module>
    from ._types import (
.audit-env/lib/python3.13/site-packages/openai/_types.py:21: in <module>
    import httpx
.audit-env/lib/python3.13/site-packages/httpx/__init__.py:2: in <module>
    from ._api import delete, get, head, options, patch, post, put, request, stream
.audit-env/lib/python3.13/site-packages/httpx/_api.py:4: in <module>
    from ._client import Client
.audit-env/lib/python3.13/site-packages/httpx/_client.py:30: in <module>
    from ._transports.default import AsyncHTTPTransport, HTTPTransport
.audit-env/lib/python3.13/site-packages/httpx/_transports/default.py:30: in <module>
    import httpcore
.audit-env/lib/python3.13/site-packages/httpcore/__init__.py:1: in <module>
    from ._api import request, stream
.audit-env/lib/python3.13/site-packages/httpcore/_api.py:5: in <module>
    from ._sync.connection_pool import ConnectionPool
.audit-env/lib/python3.13/site-packages/httpcore/_sync/__init__.py:1: in <module>
    from .connection import HTTPConnection
.audit-env/lib/python3.13/site-packages/httpcore/_sync/connection.py:12: in <module>
    from .._synchronization import Lock
.audit-env/lib/python3.13/site-packages/httpcore/_synchronization.py:13: in <module>
    import trio
.audit-env/lib/python3.13/site-packages/trio/__init__.py:71: in <module>
    from ._path import Path
.audit-env/lib/python3.13/site-packages/trio/_path.py:134: in <module>
    class Path(metaclass=AsyncAutoWrapperType):
.audit-env/lib/python3.13/site-packages/trio/_path.py:85: in __init__
    type(cls).generate_forwards(cls, attrs)
.audit-env/lib/python3.13/site-packages/trio/_path.py:102: in generate_forwards
    raise TypeError(attr_name, type(attr))
E   TypeError: ('parser', <class 'module'>)
------------------------------- Captured stderr --------------------------------
17:01:00 | INFO     | DataDreamer not available - synthesis features will use fallback
=============================== warnings summary ===============================
.audit-env/lib/python3.13/site-packages/pydantic/_internal/_config.py:323
  /Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/pydantic/_internal/_config.py:323: PydanticDeprecatedSince20: Support for class-based `config` is deprecated, use ConfigDict instead. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.11/migration/
    warnings.warn(DEPRECATION_MESSAGE, DeprecationWarning)

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=========================== short test summary info ============================
ERROR tests/test_firebolt_comprehensive.py - TypeError: ('parser', <class 'mo...
ERROR tests/test_ingest_comprehensive.py - TypeError: ('parser', <class 'modu...
ERROR tests/test_s3_comprehensive.py
ERROR tests/test_synthesis_comprehensive.py - TypeError: ('parser', <class 'm...
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
================= 80 deselected, 1 warning, 4 errors in 0.70s ==================
```

## Command: `pytest --cov=. --cov-report=html`

**Source:** README.md - Testing
**Exit Code:** 2

**Standard Output:**
```
============================= test session starts ==============================
platform darwin -- Python 3.13.5, pytest-8.4.1, pluggy-1.6.0
Using --randomly-seed=2252873134
rootdir: /Users/tosh/Desktop/Dreambolt
plugins: randomly-3.16.0, cov-5.0.0, anyio-4.9.0, mock-3.14.1
collected 80 items / 4 errors

==================================== ERRORS ====================================
____________ ERROR collecting tests/test_firebolt_comprehensive.py _____________
tests/test_firebolt_comprehensive.py:11: in <module>
    from firebolt_io import FireboltConnector, FireboltConfig
firebolt_io.py:14: in <module>
    firebolt_db = importlib.import_module('firebolt.db')
                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/opt/homebrew/Cellar/python@3.13/3.13.5/Frameworks/Python.framework/Versions/3.13/lib/python3.13/importlib/__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.audit-env/lib/python3.13/site-packages/firebolt/db/__init__.py:1: in <module>
    from firebolt.common._types import (
.audit-env/lib/python3.13/site-packages/firebolt/common/__init__.py:1: in <module>
    from firebolt.common.settings import Settings
.audit-env/lib/python3.13/site-packages/firebolt/common/settings.py:6: in <module>
    from firebolt.client.auth import Auth, UsernamePassword
.audit-env/lib/python3.13/site-packages/firebolt/client/__init__.py:1: in <module>
    from firebolt.client.auth import Auth  # backward compatibility
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.audit-env/lib/python3.13/site-packages/firebolt/client/auth/__init__.py:1: in <module>
    from firebolt.client.auth.base import Auth
.audit-env/lib/python3.13/site-packages/firebolt/client/auth/base.py:4: in <module>
    from httpx import Auth as HttpxAuth
.audit-env/lib/python3.13/site-packages/httpx/__init__.py:2: in <module>
    from ._api import delete, get, head, options, patch, post, put, request, stream
.audit-env/lib/python3.13/site-packages/httpx/_api.py:4: in <module>
    from ._client import Client
.audit-env/lib/python3.13/site-packages/httpx/_client.py:30: in <module>
    from ._transports.default import AsyncHTTPTransport, HTTPTransport
.audit-env/lib/python3.13/site-packages/httpx/_transports/default.py:30: in <module>
    import httpcore
.audit-env/lib/python3.13/site-packages/httpcore/__init__.py:1: in <module>
    from ._api import request, stream
.audit-env/lib/python3.13/site-packages/httpcore/_api.py:5: in <module>
    from ._sync.connection_pool import ConnectionPool
.audit-env/lib/python3.13/site-packages/httpcore/_sync/__init__.py:1: in <module>
    from .connection import HTTPConnection
.audit-env/lib/python3.13/site-packages/httpcore/_sync/connection.py:12: in <module>
    from .._synchronization import Lock
.audit-env/lib/python3.13/site-packages/httpcore/_synchronization.py:13: in <module>
    import trio
.audit-env/lib/python3.13/site-packages/trio/__init__.py:71: in <module>
    from ._path import Path
.audit-env/lib/python3.13/site-packages/trio/_path.py:134: in <module>
    class Path(metaclass=AsyncAutoWrapperType):
.audit-env/lib/python3.13/site-packages/trio/_path.py:85: in __init__
    type(cls).generate_forwards(cls, attrs)
.audit-env/lib/python3.13/site-packages/trio/_path.py:102: in generate_forwards
    raise TypeError(attr_name, type(attr))
E   TypeError: ('parser', <class 'module'>)
_____________ ERROR collecting tests/test_ingest_comprehensive.py ______________
tests/test_ingest_comprehensive.py:13: in <module>
    from ingest import DataIngester, SchemaInfo
ingest.py:13: in <module>
    from src.utils.s3_client import (
src/utils/s3_client.py:7: in <module>
    import s3fs
.audit-env/lib/python3.13/site-packages/s3fs/__init__.py:1: in <module>
    from .core import S3FileSystem, S3File
.audit-env/lib/python3.13/site-packages/s3fs/core.py:30: in <module>
    import aiobotocore.session
.audit-env/lib/python3.13/site-packages/aiobotocore/session.py:11: in <module>
    from .client import AioBaseClient, AioClientCreator
.audit-env/lib/python3.13/site-packages/aiobotocore/client.py:20: in <module>
    from .args import AioClientArgsCreator
.audit-env/lib/python3.13/site-packages/aiobotocore/args.py:7: in <module>
    from .config import AioConfig
.audit-env/lib/python3.13/site-packages/aiobotocore/config.py:6: in <module>
    from aiobotocore.endpoint import DEFAULT_HTTP_SESSION_CLS
.audit-env/lib/python3.13/site-packages/aiobotocore/endpoint.py:17: in <module>
    from aiobotocore.httpchecksum import handle_checksum_body
.audit-env/lib/python3.13/site-packages/aiobotocore/httpchecksum.py:19: in <module>
    import httpx
.audit-env/lib/python3.13/site-packages/httpx/__init__.py:2: in <module>
    from ._api import delete, get, head, options, patch, post, put, request, stream
.audit-env/lib/python3.13/site-packages/httpx/_api.py:4: in <module>
    from ._client import Client
.audit-env/lib/python3.13/site-packages/httpx/_client.py:30: in <module>
    from ._transports.default import AsyncHTTPTransport, HTTPTransport
.audit-env/lib/python3.13/site-packages/httpx/_transports/default.py:30: in <module>
    import httpcore
.audit-env/lib/python3.13/site-packages/httpcore/__init__.py:1: in <module>
    from ._api import request, stream
.audit-env/lib/python3.13/site-packages/httpcore/_api.py:5: in <module>
    from ._sync.connection_pool import ConnectionPool
.audit-env/lib/python3.13/site-packages/httpcore/_sync/__init__.py:1: in <module>
    from .connection import HTTPConnection
.audit-env/lib/python3.13/site-packages/httpcore/_sync/connection.py:12: in <module>
    from .._synchronization import Lock
.audit-env/lib/python3.13/site-packages/httpcore/_synchronization.py:13: in <module>
    import trio
.audit-env/lib/python3.13/site-packages/trio/__init__.py:71: in <module>
    from ._path import Path
.audit-env/lib/python3.13/site-packages/trio/_path.py:134: in <module>
    class Path(metaclass=AsyncAutoWrapperType):
.audit-env/lib/python3.13/site-packages/trio/_path.py:85: in __init__
    type(cls).generate_forwards(cls, attrs)
.audit-env/lib/python3.13/site-packages/trio/_path.py:102: in generate_forwards
    raise TypeError(attr_name, type(attr))
E   TypeError: ('parser', <class 'module'>)
_______________ ERROR collecting tests/test_s3_comprehensive.py ________________
ImportError while importing test module '/Users/tosh/Desktop/Dreambolt/tests/test_s3_comprehensive.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/opt/homebrew/Cellar/python@3.13/3.13.5/Frameworks/Python.framework/Versions/3.13/lib/python3.13/importlib/__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
tests/test_s3_comprehensive.py:14: in <module>
    from moto import mock_s3
E   ImportError: cannot import name 'mock_s3' from 'moto' (/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/moto/__init__.py). Did you mean: 'mock_aws'?
____________ ERROR collecting tests/test_synthesis_comprehensive.py ____________
tests/test_synthesis_comprehensive.py:12: in <module>
    from synth import DataSynthesizer, ModelConfig
synth.py:39: in <module>
    import openai
.audit-env/lib/python3.13/site-packages/openai/__init__.py:9: in <module>
    from . import types
.audit-env/lib/python3.13/site-packages/openai/types/__init__.py:5: in <module>
    from .batch import Batch as Batch
.audit-env/lib/python3.13/site-packages/openai/types/batch.py:6: in <module>
    from .._models import BaseModel
.audit-env/lib/python3.13/site-packages/openai/_models.py:25: in <module>
    from ._types import (
.audit-env/lib/python3.13/site-packages/openai/_types.py:21: in <module>
    import httpx
.audit-env/lib/python3.13/site-packages/httpx/__init__.py:2: in <module>
    from ._api import delete, get, head, options, patch, post, put, request, stream
.audit-env/lib/python3.13/site-packages/httpx/_api.py:4: in <module>
    from ._client import Client
.audit-env/lib/python3.13/site-packages/httpx/_client.py:30: in <module>
    from ._transports.default import AsyncHTTPTransport, HTTPTransport
.audit-env/lib/python3.13/site-packages/httpx/_transports/default.py:30: in <module>
    import httpcore
.audit-env/lib/python3.13/site-packages/httpcore/__init__.py:1: in <module>
    from ._api import request, stream
.audit-env/lib/python3.13/site-packages/httpcore/_api.py:5: in <module>
    from ._sync.connection_pool import ConnectionPool
.audit-env/lib/python3.13/site-packages/httpcore/_sync/__init__.py:1: in <module>
    from .connection import HTTPConnection
.audit-env/lib/python3.13/site-packages/httpcore/_sync/connection.py:12: in <module>
    from .._synchronization import Lock
.audit-env/lib/python3.13/site-packages/httpcore/_synchronization.py:13: in <module>
    import trio
.audit-env/lib/python3.13/site-packages/trio/__init__.py:71: in <module>
    from ._path import Path
.audit-env/lib/python3.13/site-packages/trio/_path.py:134: in <module>
    class Path(metaclass=AsyncAutoWrapperType):
.audit-env/lib/python3.13/site-packages/trio/_path.py:85: in __init__
    type(cls).generate_forwards(cls, attrs)
.audit-env/lib/python3.13/site-packages/trio/_path.py:102: in generate_forwards
    raise TypeError(attr_name, type(attr))
E   TypeError: ('parser', <class 'module'>)
------------------------------- Captured stderr --------------------------------
17:01:02 | INFO     | DataDreamer not available - synthesis features will use fallback
=============================== warnings summary ===============================
.audit-env/lib/python3.13/site-packages/pydantic/_internal/_config.py:323
  /Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/pydantic/_internal/_config.py:323: PydanticDeprecatedSince20: Support for class-based `config` is deprecated, use ConfigDict instead. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.11/migration/
    warnings.warn(DEPRECATION_MESSAGE, DeprecationWarning)

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html

---------- coverage: platform darwin, python 3.13.5-final-0 ----------
Coverage HTML written to dir htmlcov

=========================== short test summary info ============================
ERROR tests/test_firebolt_comprehensive.py - TypeError: ('parser', <class 'mo...
ERROR tests/test_ingest_comprehensive.py - TypeError: ('parser', <class 'modu...
ERROR tests/test_s3_comprehensive.py
ERROR tests/test_synthesis_comprehensive.py - TypeError: ('parser', <class 'm...
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
========================= 1 warning, 4 errors in 1.33s =========================
```

## Command: `pip install datadreamer`

**Source:** README.md - Troubleshooting
**Exit Code:** 1

**Error Output:**
```
error: subprocess-exited-with-error

  × Building wheel for pyarrow (pyproject.toml) did not run successfully.
  │ exit code: 1
  ╰─> [441 lines of output]
      <string>:34: UserWarning: pkg_resources is deprecated as an API. See https://setuptools.pypa.io/en/latest/pkg_resources.html. The pkg_resources package is slated for removal as early as 2025-11-30. Refrain from using this package or pin to Setuptools<81.
      /private/var/folders/z3/bjtrhnk91qqdx5ttwqn647200000gn/T/pip-build-env-u5otg894/overlay/lib/python3.13/site-packages/setuptools/config/_apply_pyprojecttoml.py:82: SetuptoolsDeprecationWarning: `project.license` as a TOML table is deprecated
      !!

              ********************************************************************************
              Please use a simple string containing a SPDX expression for `project.license`. You can also use `project.license-files`. (Both options available on setuptools>=77.0.0).

              By 2026-Feb-18, you need to update your project and remove deprecated calls
              or your builds will no longer be supported.

              See https://packaging.python.org/en/latest/guides/writing-pyproject-toml/#license for details.
              ********************************************************************************

      !!
        corresp(dist, value, root_dir)
      /private/var/folders/z3/bjtrhnk91qqdx5ttwqn647200000gn/T/pip-build-env-u5otg894/overlay/lib/python3.13/site-packages/setuptools/config/_apply_pyprojecttoml.py:61: SetuptoolsDeprecationWarning: License classifiers are deprecated.
      !!

              ********************************************************************************
              Please consider removing the following classifiers in favor of a SPDX license expression:

              License :: OSI Approved :: Apache Software License

              See https://packaging.python.org/en/latest/guides/writing-pyproject-toml/#license for details.
              ********************************************************************************

      !!
        dist._finalize_license_expression()
      /private/var/folders/z3/bjtrhnk91qqdx5ttwqn647200000gn/T/pip-build-env-u5otg894/overlay/lib/python3.13/site-packages/setuptools/dist.py:483: SetuptoolsDeprecationWarning: Pattern '../LICENSE.txt' cannot contain '..'
      !!

              ********************************************************************************
              Please ensure the files specified are contained by the root
              of the Python package (normally marked by `pyproject.toml`).

              By 2026-Mar-20, you need to update your project and remove deprecated calls
              or your builds will no longer be supported.

              See https://packaging.python.org/en/latest/specifications/glob-patterns/ for details.
              ********************************************************************************

      !!
        for path in sorted(cls._find_pattern(pattern, enforce_match))
      /private/var/folders/z3/bjtrhnk91qqdx5ttwqn647200000gn/T/pip-build-env-u5otg894/overlay/lib/python3.13/site-packages/setuptools/dist.py:483: SetuptoolsDeprecationWarning: Cannot find any files for the given pattern.
      !!

              ********************************************************************************
              Pattern '../LICENSE.txt' did not match any files.

              By 2026-Mar-20, you need to update your project and remove deprecated calls
              or your builds will no longer be supported.
              ********************************************************************************

      !!
        for path in sorted(cls._find_pattern(pattern, enforce_match))
      /private/var/folders/z3/bjtrhnk91qqdx5ttwqn647200000gn/T/pip-build-env-u5otg894/overlay/lib/python3.13/site-packages/setuptools/dist.py:483: SetuptoolsDeprecationWarning: Pattern '../NOTICE.txt' cannot contain '..'
      !!

              ********************************************************************************
              Please ensure the files specified are contained by the root
              of the Python package (normally marked by `pyproject.toml`).

              By 2026-Mar-20, you need to update your project and remove deprecated calls
              or your builds will no longer be supported.

              See https://packaging.python.org/en/latest/specifications/glob-patterns/ for details.
              ********************************************************************************

      !!
        for path in sorted(cls._find_pattern(pattern, enforce_match))
      /private/var/folders/z3/bjtrhnk91qqdx5ttwqn647200000gn/T/pip-build-env-u5otg894/overlay/lib/python3.13/site-packages/setuptools/dist.py:483: SetuptoolsDeprecationWarning: Cannot find any files for the given pattern.
      !!

              ********************************************************************************
              Pattern '../NOTICE.txt' did not match any files.

              By 2026-Mar-20, you need to update your project and remove deprecated calls
              or your builds will no longer be supported.
              ********************************************************************************

      !!
        for path in sorted(cls._find_pattern(pattern, enforce_match))
      /private/var/folders/z3/bjtrhnk91qqdx5ttwqn647200000gn/T/pip-build-env-u5otg894/overlay/lib/python3.13/site-packages/setuptools/dist.py:759: SetuptoolsDeprecationWarning: License classifiers are deprecated.
      !!

              ********************************************************************************
              Please consider removing the following classifiers in favor of a SPDX license expression:

              License :: OSI Approved :: Apache Software License

              See https://packaging.python.org/en/latest/guides/writing-pyproject-toml/#license for details.
              ********************************************************************************

      !!
        self._finalize_license_expression()
      running bdist_wheel
      running build
      running build_py
      creating build/lib.macosx-14.0-arm64-cpython-313/benchmarks
      copying benchmarks/array_ops.py -> build/lib.macosx-14.0-arm64-cpython-313/benchmarks
      copying benchmarks/convert_builtins.py -> build/lib.macosx-14.0-arm64-cpython-313/benchmarks
      copying benchmarks/parquet.py -> build/lib.macosx-14.0-arm64-cpython-313/benchmarks
      copying benchmarks/io.py -> build/lib.macosx-14.0-arm64-cpython-313/benchmarks
      copying benchmarks/__init__.py -> build/lib.macosx-14.0-arm64-cpython-313/benchmarks
      copying benchmarks/microbenchmarks.py -> build/lib.macosx-14.0-arm64-cpython-313/benchmarks
      copying benchmarks/convert_pandas.py -> build/lib.macosx-14.0-arm64-cpython-313/benchmarks
      copying benchmarks/common.py -> build/lib.macosx-14.0-arm64-cpython-313/benchmarks
      copying benchmarks/streaming.py -> build/lib.macosx-14.0-arm64-cpython-313/benchmarks
      creating build/lib.macosx-14.0-arm64-cpython-313/scripts
      copying scripts/test_imports.py -> build/lib.macosx-14.0-arm64-cpython-313/scripts
      copying scripts/test_leak.py -> build/lib.macosx-14.0-arm64-cpython-313/scripts
      copying scripts/run_emscripten_tests.py -> build/lib.macosx-14.0-arm64-cpython-313/scripts
      creating build/lib.macosx-14.0-arm64-cpython-313/pyarrow
      copying pyarrow/orc.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow
      copying pyarrow/conftest.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow
      copying pyarrow/_generated_version.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow
      copying pyarrow/benchmark.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow
      copying pyarrow/_compute_docstrings.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow
      copying pyarrow/ipc.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow
      copying pyarrow/util.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow
      copying pyarrow/flight.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow
      copying pyarrow/cffi.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow
      copying pyarrow/substrait.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow
      copying pyarrow/__init__.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow
      copying pyarrow/types.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow
      copying pyarrow/dataset.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow
      copying pyarrow/cuda.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow
      copying pyarrow/feather.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow
      copying pyarrow/pandas_compat.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow
      copying pyarrow/fs.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow
      copying pyarrow/acero.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow
      copying pyarrow/csv.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow
      copying pyarrow/jvm.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow
      copying pyarrow/json.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow
      copying pyarrow/compute.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow
      creating build/lib.macosx-14.0-arm64-cpython-313/examples/parquet_encryption
      copying examples/parquet_encryption/sample_vault_kms_client.py -> build/lib.macosx-14.0-arm64-cpython-313/examples/parquet_encryption
      creating build/lib.macosx-14.0-arm64-cpython-313/examples/dataset
      copying examples/dataset/write_dataset_encrypted.py -> build/lib.macosx-14.0-arm64-cpython-313/examples/dataset
      creating build/lib.macosx-14.0-arm64-cpython-313/examples/flight
      copying examples/flight/server.py -> build/lib.macosx-14.0-arm64-cpython-313/examples/flight
      copying examples/flight/client.py -> build/lib.macosx-14.0-arm64-cpython-313/examples/flight
      copying examples/flight/middleware.py -> build/lib.macosx-14.0-arm64-cpython-313/examples/flight
      creating build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests
      copying pyarrow/tests/test_tensor.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests
      copying pyarrow/tests/test_ipc.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests
      copying pyarrow/tests/test_flight_async.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests
      copying pyarrow/tests/conftest.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests
      copying pyarrow/tests/test_convert_builtin.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests
      copying pyarrow/tests/test_misc.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests
      copying pyarrow/tests/arrow_39313.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests
      copying pyarrow/tests/arrow_16597.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests
      copying pyarrow/tests/test_acero.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests
      copying pyarrow/tests/test_gandiva.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests
      copying pyarrow/tests/strategies.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests
      copying pyarrow/tests/test_adhoc_memory_leak.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests
      copying pyarrow/tests/arrow_7980.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests
      copying pyarrow/tests/util.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests
      copying pyarrow/tests/test_orc.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests
      copying pyarrow/tests/test_table.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests
      copying pyarrow/tests/test_array.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests
      copying pyarrow/tests/test_deprecations.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests
      copying pyarrow/tests/__init__.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests
      copying pyarrow/tests/test_io.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests
      copying pyarrow/tests/test_util.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests
      copying pyarrow/tests/test_cuda_numba_interop.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests
      copying pyarrow/tests/test_cpp_internals.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests
      copying pyarrow/tests/test_cffi.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests
      copying pyarrow/tests/test_schema.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests
      copying pyarrow/tests/test_jvm.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests
      copying pyarrow/tests/test_fs.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests
      copying pyarrow/tests/test_udf.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests
      copying pyarrow/tests/pandas_threaded_import.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests
      copying pyarrow/tests/pandas_examples.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests
      copying pyarrow/tests/test_cython.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests
      copying pyarrow/tests/test_sparse_tensor.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests
      copying pyarrow/tests/test_dataset.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests
      copying pyarrow/tests/test_builder.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests
      copying pyarrow/tests/test_dataset_encryption.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests
      copying pyarrow/tests/test_cuda.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests
      copying pyarrow/tests/test_extension_type.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests
      copying pyarrow/tests/test_feather.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests
      copying pyarrow/tests/test_pandas.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests
      copying pyarrow/tests/test_memory.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests
      copying pyarrow/tests/test_exec_plan.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests
      copying pyarrow/tests/test_flight.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests
      copying pyarrow/tests/test_device.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests
      copying pyarrow/tests/read_record_batch.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests
      copying pyarrow/tests/test_dlpack.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests
      copying pyarrow/tests/test_json.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests
      copying pyarrow/tests/test_compute.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests
      copying pyarrow/tests/test_strategies.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests
      copying pyarrow/tests/test_csv.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests
      copying pyarrow/tests/test_scalars.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests
      copying pyarrow/tests/test_gdb.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests
      copying pyarrow/tests/test_types.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests
      copying pyarrow/tests/test_substrait.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests
      creating build/lib.macosx-14.0-arm64-cpython-313/pyarrow/interchange
      copying pyarrow/interchange/from_dataframe.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/interchange
      copying pyarrow/interchange/dataframe.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/interchange
      copying pyarrow/interchange/__init__.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/interchange
      copying pyarrow/interchange/buffer.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/interchange
      copying pyarrow/interchange/column.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/interchange
      creating build/lib.macosx-14.0-arm64-cpython-313/pyarrow/vendored
      copying pyarrow/vendored/version.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/vendored
      copying pyarrow/vendored/__init__.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/vendored
      copying pyarrow/vendored/docscrape.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/vendored
      creating build/lib.macosx-14.0-arm64-cpython-313/pyarrow/parquet
      copying pyarrow/parquet/encryption.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/parquet
      copying pyarrow/parquet/__init__.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/parquet
      copying pyarrow/parquet/core.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/parquet
      creating build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests/interchange
      copying pyarrow/tests/interchange/__init__.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests/interchange
      copying pyarrow/tests/interchange/test_conversion.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests/interchange
      copying pyarrow/tests/interchange/test_interchange_spec.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests/interchange
      creating build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests/parquet
      copying pyarrow/tests/parquet/test_basic.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests/parquet
      copying pyarrow/tests/parquet/conftest.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests/parquet
      copying pyarrow/tests/parquet/encryption.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests/parquet
      copying pyarrow/tests/parquet/test_parquet_writer.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests/parquet
      copying pyarrow/tests/parquet/test_metadata.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests/parquet
      copying pyarrow/tests/parquet/__init__.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests/parquet
      copying pyarrow/tests/parquet/test_datetime.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests/parquet
      copying pyarrow/tests/parquet/common.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests/parquet
      copying pyarrow/tests/parquet/test_dataset.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests/parquet
      copying pyarrow/tests/parquet/test_data_types.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests/parquet
      copying pyarrow/tests/parquet/test_pandas.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests/parquet
      copying pyarrow/tests/parquet/test_parquet_file.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests/parquet
      copying pyarrow/tests/parquet/test_compliant_nested_type.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests/parquet
      copying pyarrow/tests/parquet/test_encryption.py -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests/parquet
      running egg_info
      writing pyarrow.egg-info/PKG-INFO
      writing dependency_links to pyarrow.egg-info/dependency_links.txt
      writing requirements to pyarrow.egg-info/requires.txt
      writing top-level names to pyarrow.egg-info/top_level.txt
      ERROR setuptools_scm._file_finders.git listing git files failed - pretending there aren't any
      reading manifest file 'pyarrow.egg-info/SOURCES.txt'
      reading manifest template 'MANIFEST.in'
      warning: no files found matching '../LICENSE.txt'
      warning: no files found matching '../NOTICE.txt'
      warning: no previously-included files matching '*.so' found anywhere in distribution
      warning: no previously-included files matching '*.pyc' found anywhere in distribution
      warning: no previously-included files matching '*~' found anywhere in distribution
      warning: no previously-included files matching '#*' found anywhere in distribution
      warning: no previously-included files matching '.git*' found anywhere in distribution
      warning: no previously-included files matching '.DS_Store' found anywhere in distribution
      no previously-included directories found matching '.asv'
      writing manifest file 'pyarrow.egg-info/SOURCES.txt'
      creating build/lib.macosx-14.0-arm64-cpython-313/cmake_modules
      copying cmake_modules/AWSSDKVariables.cmake -> build/lib.macosx-14.0-arm64-cpython-313/cmake_modules
      copying cmake_modules/BuildUtils.cmake -> build/lib.macosx-14.0-arm64-cpython-313/cmake_modules
      copying cmake_modules/DefineOptions.cmake -> build/lib.macosx-14.0-arm64-cpython-313/cmake_modules
      copying cmake_modules/FindAWSSDKAlt.cmake -> build/lib.macosx-14.0-arm64-cpython-313/cmake_modules
      copying cmake_modules/FindAzure.cmake -> build/lib.macosx-14.0-arm64-cpython-313/cmake_modules
      copying cmake_modules/FindBrotliAlt.cmake -> build/lib.macosx-14.0-arm64-cpython-313/cmake_modules
      copying cmake_modules/FindClangTools.cmake -> build/lib.macosx-14.0-arm64-cpython-313/cmake_modules
      copying cmake_modules/FindGTestAlt.cmake -> build/lib.macosx-14.0-arm64-cpython-313/cmake_modules
      copying cmake_modules/FindInferTools.cmake -> build/lib.macosx-14.0-arm64-cpython-313/cmake_modules
      copying cmake_modules/FindLLVMAlt.cmake -> build/lib.macosx-14.0-arm64-cpython-313/cmake_modules
      copying cmake_modules/FindOpenSSLAlt.cmake -> build/lib.macosx-14.0-arm64-cpython-313/cmake_modules
      copying cmake_modules/FindProtobufAlt.cmake -> build/lib.macosx-14.0-arm64-cpython-313/cmake_modules
      copying cmake_modules/FindPython3Alt.cmake -> build/lib.macosx-14.0-arm64-cpython-313/cmake_modules
      copying cmake_modules/FindRapidJSONAlt.cmake -> build/lib.macosx-14.0-arm64-cpython-313/cmake_modules
      copying cmake_modules/FindSQLite3Alt.cmake -> build/lib.macosx-14.0-arm64-cpython-313/cmake_modules
      copying cmake_modules/FindSnappyAlt.cmake -> build/lib.macosx-14.0-arm64-cpython-313/cmake_modules
      copying cmake_modules/FindThriftAlt.cmake -> build/lib.macosx-14.0-arm64-cpython-313/cmake_modules
      copying cmake_modules/Findc-aresAlt.cmake -> build/lib.macosx-14.0-arm64-cpython-313/cmake_modules
      copying cmake_modules/FindgRPCAlt.cmake -> build/lib.macosx-14.0-arm64-cpython-313/cmake_modules
      copying cmake_modules/FindgflagsAlt.cmake -> build/lib.macosx-14.0-arm64-cpython-313/cmake_modules
      copying cmake_modules/FindglogAlt.cmake -> build/lib.macosx-14.0-arm64-cpython-313/cmake_modules
      copying cmake_modules/FindjemallocAlt.cmake -> build/lib.macosx-14.0-arm64-cpython-313/cmake_modules
      copying cmake_modules/Findlibrados.cmake -> build/lib.macosx-14.0-arm64-cpython-313/cmake_modules
      copying cmake_modules/Findlz4Alt.cmake -> build/lib.macosx-14.0-arm64-cpython-313/cmake_modules
      copying cmake_modules/FindorcAlt.cmake -> build/lib.macosx-14.0-arm64-cpython-313/cmake_modules
      copying cmake_modules/Findre2Alt.cmake -> build/lib.macosx-14.0-arm64-cpython-313/cmake_modules
      copying cmake_modules/Findutf8proc.cmake -> build/lib.macosx-14.0-arm64-cpython-313/cmake_modules
      copying cmake_modules/FindzstdAlt.cmake -> build/lib.macosx-14.0-arm64-cpython-313/cmake_modules
      copying cmake_modules/GandivaAddBitcode.cmake -> build/lib.macosx-14.0-arm64-cpython-313/cmake_modules
      copying cmake_modules/SetupCxxFlags.cmake -> build/lib.macosx-14.0-arm64-cpython-313/cmake_modules
      copying cmake_modules/ThirdpartyToolchain.cmake -> build/lib.macosx-14.0-arm64-cpython-313/cmake_modules
      copying cmake_modules/UseCython.cmake -> build/lib.macosx-14.0-arm64-cpython-313/cmake_modules
      copying cmake_modules/Usevcpkg.cmake -> build/lib.macosx-14.0-arm64-cpython-313/cmake_modules
      copying cmake_modules/aws_sdk_cpp_generate_variables.sh -> build/lib.macosx-14.0-arm64-cpython-313/cmake_modules
      copying cmake_modules/san-config.cmake -> build/lib.macosx-14.0-arm64-cpython-313/cmake_modules
      copying cmake_modules/snappy.diff -> build/lib.macosx-14.0-arm64-cpython-313/cmake_modules
      copying pyarrow/__init__.pxd -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow
      copying pyarrow/_acero.pxd -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow
      copying pyarrow/_acero.pyx -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow
      copying pyarrow/_azurefs.pyx -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow
      copying pyarrow/_compute.pxd -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow
      copying pyarrow/_compute.pyx -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow
      copying pyarrow/_csv.pxd -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow
      copying pyarrow/_csv.pyx -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow
      copying pyarrow/_cuda.pxd -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow
      copying pyarrow/_cuda.pyx -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow
      copying pyarrow/_dataset.pxd -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow
      copying pyarrow/_dataset.pyx -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow
      copying pyarrow/_dataset_orc.pyx -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow
      copying pyarrow/_dataset_parquet.pxd -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow
      copying pyarrow/_dataset_parquet.pyx -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow
      copying pyarrow/_dataset_parquet_encryption.pyx -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow
      copying pyarrow/_dlpack.pxi -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow
      copying pyarrow/_feather.pyx -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow
      copying pyarrow/_flight.pyx -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow
      copying pyarrow/_fs.pxd -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow
      copying pyarrow/_fs.pyx -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow
      copying pyarrow/_gcsfs.pyx -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow
      copying pyarrow/_hdfs.pyx -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow
      copying pyarrow/_json.pxd -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow
      copying pyarrow/_json.pyx -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow
      copying pyarrow/_orc.pxd -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow
      copying pyarrow/_orc.pyx -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow
      copying pyarrow/_parquet.pxd -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow
      copying pyarrow/_parquet.pyx -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow
      copying pyarrow/_parquet_encryption.pxd -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow
      copying pyarrow/_parquet_encryption.pyx -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow
      copying pyarrow/_pyarrow_cpp_tests.pxd -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow
      copying pyarrow/_pyarrow_cpp_tests.pyx -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow
      copying pyarrow/_s3fs.pyx -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow
      copying pyarrow/_substrait.pyx -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow
      copying pyarrow/array.pxi -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow
      copying pyarrow/benchmark.pxi -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow
      copying pyarrow/builder.pxi -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow
      copying pyarrow/compat.pxi -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow
      copying pyarrow/config.pxi -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow
      copying pyarrow/device.pxi -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow
      copying pyarrow/error.pxi -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow
      copying pyarrow/gandiva.pyx -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow
      copying pyarrow/io.pxi -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow
      copying pyarrow/ipc.pxi -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow
      copying pyarrow/lib.pxd -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow
      copying pyarrow/lib.pyx -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow
      copying pyarrow/memory.pxi -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow
      copying pyarrow/pandas-shim.pxi -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow
      copying pyarrow/public-api.pxi -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow
      copying pyarrow/scalar.pxi -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow
      copying pyarrow/table.pxi -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow
      copying pyarrow/tensor.pxi -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow
      copying pyarrow/types.pxi -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow
      creating build/lib.macosx-14.0-arm64-cpython-313/pyarrow/includes
      copying pyarrow/includes/common.pxd -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/includes
      copying pyarrow/includes/libarrow_feather.pxd -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/includes
      copying pyarrow/includes/libarrow_acero.pxd -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/includes
      copying pyarrow/includes/libparquet_encryption.pxd -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/includes
      copying pyarrow/includes/__init__.pxd -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/includes
      copying pyarrow/includes/libgandiva.pxd -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/includes
      copying pyarrow/includes/libarrow_python.pxd -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/includes
      copying pyarrow/includes/libarrow_flight.pxd -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/includes
      copying pyarrow/includes/libarrow_dataset_parquet.pxd -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/includes
      copying pyarrow/includes/libarrow_dataset.pxd -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/includes
      copying pyarrow/includes/libarrow_substrait.pxd -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/includes
      copying pyarrow/includes/libarrow.pxd -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/includes
      copying pyarrow/includes/libarrow_cuda.pxd -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/includes
      copying pyarrow/includes/libarrow_fs.pxd -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/includes
      copying pyarrow/tests/bound_function_visit_strings.pyx -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests
      copying pyarrow/tests/extensions.pyx -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests
      copying pyarrow/tests/pyarrow_cython_example.pyx -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests
      creating build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests/data/feather
      copying pyarrow/tests/data/feather/v0.17.0.version.2-compression.lz4.feather -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests/data/feather
      creating build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests/data/orc
      copying pyarrow/tests/data/orc/README.md -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests/data/orc
      copying pyarrow/tests/data/orc/TestOrcFile.emptyFile.jsn.gz -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests/data/orc
      copying pyarrow/tests/data/orc/TestOrcFile.emptyFile.orc -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests/data/orc
      copying pyarrow/tests/data/orc/TestOrcFile.test1.jsn.gz -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests/data/orc
      copying pyarrow/tests/data/orc/TestOrcFile.test1.orc -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests/data/orc
      copying pyarrow/tests/data/orc/TestOrcFile.testDate1900.jsn.gz -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests/data/orc
      copying pyarrow/tests/data/orc/TestOrcFile.testDate1900.orc -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests/data/orc
      copying pyarrow/tests/data/orc/decimal.jsn.gz -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests/data/orc
      copying pyarrow/tests/data/orc/decimal.orc -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests/data/orc
      creating build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests/data/parquet
      copying pyarrow/tests/data/parquet/v0.7.1.all-named-index.parquet -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests/data/parquet
      copying pyarrow/tests/data/parquet/v0.7.1.column-metadata-handling.parquet -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests/data/parquet
      copying pyarrow/tests/data/parquet/v0.7.1.parquet -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests/data/parquet
      copying pyarrow/tests/data/parquet/v0.7.1.some-named-index.parquet -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/tests/data/parquet
      creating build/lib.macosx-14.0-arm64-cpython-313/pyarrow/src/arrow/python
      copying pyarrow/src/arrow/python/CMakeLists.txt -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/src/arrow/python
      copying pyarrow/src/arrow/python/api.h -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/src/arrow/python
      copying pyarrow/src/arrow/python/arrow_to_pandas.cc -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/src/arrow/python
      copying pyarrow/src/arrow/python/arrow_to_pandas.h -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/src/arrow/python
      copying pyarrow/src/arrow/python/arrow_to_python_internal.h -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/src/arrow/python
      copying pyarrow/src/arrow/python/async.h -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/src/arrow/python
      copying pyarrow/src/arrow/python/benchmark.cc -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/src/arrow/python
      copying pyarrow/src/arrow/python/benchmark.h -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/src/arrow/python
      copying pyarrow/src/arrow/python/common.cc -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/src/arrow/python
      copying pyarrow/src/arrow/python/common.h -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/src/arrow/python
      copying pyarrow/src/arrow/python/csv.cc -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/src/arrow/python
      copying pyarrow/src/arrow/python/csv.h -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/src/arrow/python
      copying pyarrow/src/arrow/python/datetime.cc -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/src/arrow/python
      copying pyarrow/src/arrow/python/datetime.h -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/src/arrow/python
      copying pyarrow/src/arrow/python/decimal.cc -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/src/arrow/python
      copying pyarrow/src/arrow/python/decimal.h -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/src/arrow/python
      copying pyarrow/src/arrow/python/deserialize.cc -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/src/arrow/python
      copying pyarrow/src/arrow/python/deserialize.h -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/src/arrow/python
      copying pyarrow/src/arrow/python/extension_type.cc -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/src/arrow/python
      copying pyarrow/src/arrow/python/extension_type.h -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/src/arrow/python
      copying pyarrow/src/arrow/python/filesystem.cc -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/src/arrow/python
      copying pyarrow/src/arrow/python/filesystem.h -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/src/arrow/python
      copying pyarrow/src/arrow/python/flight.cc -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/src/arrow/python
      copying pyarrow/src/arrow/python/flight.h -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/src/arrow/python
      copying pyarrow/src/arrow/python/gdb.cc -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/src/arrow/python
      copying pyarrow/src/arrow/python/gdb.h -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/src/arrow/python
      copying pyarrow/src/arrow/python/helpers.cc -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/src/arrow/python
      copying pyarrow/src/arrow/python/helpers.h -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/src/arrow/python
      copying pyarrow/src/arrow/python/inference.cc -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/src/arrow/python
      copying pyarrow/src/arrow/python/inference.h -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/src/arrow/python
      copying pyarrow/src/arrow/python/init.cc -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/src/arrow/python
      copying pyarrow/src/arrow/python/init.h -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/src/arrow/python
      copying pyarrow/src/arrow/python/io.cc -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/src/arrow/python
      copying pyarrow/src/arrow/python/io.h -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/src/arrow/python
      copying pyarrow/src/arrow/python/ipc.cc -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/src/arrow/python
      copying pyarrow/src/arrow/python/ipc.h -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/src/arrow/python
      copying pyarrow/src/arrow/python/iterators.h -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/src/arrow/python
      copying pyarrow/src/arrow/python/numpy_convert.cc -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/src/arrow/python
      copying pyarrow/src/arrow/python/numpy_convert.h -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/src/arrow/python
      copying pyarrow/src/arrow/python/numpy_internal.h -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/src/arrow/python
      copying pyarrow/src/arrow/python/numpy_interop.h -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/src/arrow/python
      copying pyarrow/src/arrow/python/numpy_to_arrow.cc -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/src/arrow/python
      copying pyarrow/src/arrow/python/numpy_to_arrow.h -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/src/arrow/python
      copying pyarrow/src/arrow/python/parquet_encryption.cc -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/src/arrow/python
      copying pyarrow/src/arrow/python/parquet_encryption.h -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/src/arrow/python
      copying pyarrow/src/arrow/python/pch.h -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/src/arrow/python
      copying pyarrow/src/arrow/python/platform.h -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/src/arrow/python
      copying pyarrow/src/arrow/python/pyarrow.cc -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/src/arrow/python
      copying pyarrow/src/arrow/python/pyarrow.h -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/src/arrow/python
      copying pyarrow/src/arrow/python/pyarrow_api.h -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/src/arrow/python
      copying pyarrow/src/arrow/python/pyarrow_lib.h -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/src/arrow/python
      copying pyarrow/src/arrow/python/python_test.cc -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/src/arrow/python
      copying pyarrow/src/arrow/python/python_test.h -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/src/arrow/python
      copying pyarrow/src/arrow/python/python_to_arrow.cc -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/src/arrow/python
      copying pyarrow/src/arrow/python/python_to_arrow.h -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/src/arrow/python
      copying pyarrow/src/arrow/python/serialize.cc -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/src/arrow/python
      copying pyarrow/src/arrow/python/serialize.h -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/src/arrow/python
      copying pyarrow/src/arrow/python/type_traits.h -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/src/arrow/python
      copying pyarrow/src/arrow/python/udf.cc -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/src/arrow/python
      copying pyarrow/src/arrow/python/udf.h -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/src/arrow/python
      copying pyarrow/src/arrow/python/visibility.h -> build/lib.macosx-14.0-arm64-cpython-313/pyarrow/src/arrow/python
      running build_ext
      creating /private/var/folders/z3/bjtrhnk91qqdx5ttwqn647200000gn/T/pip-install-ds6wdvvq/pyarrow_250a63b2e290475eb6f879d2d26b4c47/build/temp.macosx-14.0-arm64-cpython-313
      -- Running cmake for PyArrow
      cmake -DCMAKE_INSTALL_PREFIX=/private/var/folders/z3/bjtrhnk91qqdx5ttwqn647200000gn/T/pip-install-ds6wdvvq/pyarrow_250a63b2e290475eb6f879d2d26b4c47/build/lib.macosx-14.0-arm64-cpython-313/pyarrow -DPYTHON_EXECUTABLE=/Users/tosh/Desktop/Dreambolt/.audit-env/bin/python3.13 -DPython3_EXECUTABLE=/Users/tosh/Desktop/Dreambolt/.audit-env/bin/python3.13 -DPYARROW_CXXFLAGS= -DPYARROW_BUNDLE_ARROW_CPP=off -DPYARROW_BUNDLE_CYTHON_CPP=off -DPYARROW_GENERATE_COVERAGE=off -DCMAKE_BUILD_TYPE=release /private/var/folders/z3/bjtrhnk91qqdx5ttwqn647200000gn/T/pip-install-ds6wdvvq/pyarrow_250a63b2e290475eb6f879d2d26b4c47
      error: command 'cmake' failed: No such file or directory
      [end of output]

  note: This error originates from a subprocess, and is likely not a problem with pip.
  ERROR: Failed building wheel for pyarrow
ERROR: Failed to build installable wheels for some pyproject.toml based projects (pyarrow)
```

**Standard Output:**
```
Collecting datadreamer
  Using cached datadreamer-0.2.1-py3-none-any.whl.metadata (32 kB)
INFO: pip is looking at multiple versions of datadreamer to determine which version is compatible with other requirements. This could take a while.
  Using cached datadreamer-0.2.0-py3-none-any.whl.metadata (30 kB)
Requirement already satisfied: torch>=2.0.0 in ./.audit-env/lib/python3.13/site-packages (from datadreamer) (2.7.1)
Collecting torchvision>=0.16.0 (from datadreamer)
  Using cached torchvision-0.22.1-cp313-cp313-macosx_11_0_arm64.whl.metadata (6.1 kB)
Requirement already satisfied: transformers>=4.45.2 in ./.audit-env/lib/python3.13/site-packages (from datadreamer) (4.52.4)
Collecting diffusers>=0.31.0 (from datadreamer)
  Using cached diffusers-0.33.1-py3-none-any.whl.metadata (19 kB)
Collecting compel>=2.0.0 (from datadreamer)
  Using cached compel-2.1.1-py3-none-any.whl.metadata (13 kB)
Requirement already satisfied: tqdm>=4.0.0 in ./.audit-env/lib/python3.13/site-packages (from datadreamer) (4.67.1)
Collecting Pillow>=9.0.0 (from datadreamer)
  Using cached pillow-11.2.1-cp313-cp313-macosx_11_0_arm64.whl.metadata (8.9 kB)
Requirement already satisfied: numpy>=1.22.0 in ./.audit-env/lib/python3.13/site-packages (from datadreamer) (2.3.0)
Collecting matplotlib>=3.6.0 (from datadreamer)
  Using cached matplotlib-3.10.3-cp313-cp313-macosx_11_0_arm64.whl.metadata (11 kB)
Collecting opencv-python>=4.7.0 (from datadreamer)
  Using cached opencv_python-4.11.0.86-cp37-abi3-macosx_13_0_arm64.whl.metadata (20 kB)
Requirement already satisfied: accelerate>=0.25.0 in ./.audit-env/lib/python3.13/site-packages (from datadreamer) (1.8.1)
Collecting scipy>=1.10.0 (from datadreamer)
  Using cached scipy-1.15.3-cp313-cp313-macosx_14_0_arm64.whl.metadata (61 kB)
Collecting bitsandbytes>=0.42.0 (from datadreamer)
  Using cached bitsandbytes-0.42.0-py3-none-any.whl.metadata (9.9 kB)
Collecting nltk>=3.8.1 (from datadreamer)
  Using cached nltk-3.9.1-py3-none-any.whl.metadata (2.9 kB)
Collecting luxonis-ml>=0.5.0 (from luxonis-ml[all]>=0.5.0->datadreamer)
  Using cached luxonis_ml-0.7.1-py3-none-any.whl.metadata (26 kB)
Collecting python-box>=7.1.1 (from datadreamer)
  Using cached python_box-7.3.2-cp313-cp313-macosx_10_13_universal2.whl.metadata (8.0 kB)
Collecting gcsfs>=2023.1.0 (from datadreamer)
  Using cached gcsfs-2025.5.1-py2.py3-none-any.whl.metadata (1.9 kB)
Requirement already satisfied: packaging>=20.0 in ./.audit-env/lib/python3.13/site-packages (from accelerate>=0.25.0->datadreamer) (25.0)
Requirement already satisfied: psutil in ./.audit-env/lib/python3.13/site-packages (from accelerate>=0.25.0->datadreamer) (7.0.0)
Requirement already satisfied: pyyaml in ./.audit-env/lib/python3.13/site-packages (from accelerate>=0.25.0->datadreamer) (6.0.2)
Requirement already satisfied: huggingface_hub>=0.21.0 in ./.audit-env/lib/python3.13/site-packages (from accelerate>=0.25.0->datadreamer) (0.33.0)
Requirement already satisfied: safetensors>=0.4.3 in ./.audit-env/lib/python3.13/site-packages (from accelerate>=0.25.0->datadreamer) (0.5.3)
Collecting pyparsing~=3.0 (from compel>=2.0.0->datadreamer)
  Using cached pyparsing-3.2.3-py3-none-any.whl.metadata (5.0 kB)
Requirement already satisfied: filelock in ./.audit-env/lib/python3.13/site-packages (from transformers>=4.45.2->datadreamer) (3.18.0)
Requirement already satisfied: regex!=2019.12.17 in ./.audit-env/lib/python3.13/site-packages (from transformers>=4.45.2->datadreamer) (2024.11.6)
Requirement already satisfied: requests in ./.audit-env/lib/python3.13/site-packages (from transformers>=4.45.2->datadreamer) (2.32.4)
Requirement already satisfied: tokenizers<0.22,>=0.21 in ./.audit-env/lib/python3.13/site-packages (from transformers>=4.45.2->datadreamer) (0.21.1)
Requirement already satisfied: fsspec>=2023.5.0 in ./.audit-env/lib/python3.13/site-packages (from huggingface_hub>=0.21.0->accelerate>=0.25.0->datadreamer) (2025.5.1)
Requirement already satisfied: typing-extensions>=3.7.4.3 in ./.audit-env/lib/python3.13/site-packages (from huggingface_hub>=0.21.0->accelerate>=0.25.0->datadreamer) (4.14.0)
Requirement already satisfied: hf-xet<2.0.0,>=1.1.2 in ./.audit-env/lib/python3.13/site-packages (from huggingface_hub>=0.21.0->accelerate>=0.25.0->datadreamer) (1.1.4)
Collecting importlib-metadata (from diffusers>=0.31.0->datadreamer)
  Using cached importlib_metadata-8.7.0-py3-none-any.whl.metadata (4.8 kB)
Requirement already satisfied: aiohttp!=4.0.0a0,!=4.0.0a1 in ./.audit-env/lib/python3.13/site-packages (from gcsfs>=2023.1.0->datadreamer) (3.12.13)
Collecting decorator>4.1.2 (from gcsfs>=2023.1.0->datadreamer)
  Using cached decorator-5.2.1-py3-none-any.whl.metadata (3.9 kB)
Collecting google-auth>=1.2 (from gcsfs>=2023.1.0->datadreamer)
  Using cached google_auth-2.40.3-py2.py3-none-any.whl.metadata (6.2 kB)
Collecting google-auth-oauthlib (from gcsfs>=2023.1.0->datadreamer)
  Using cached google_auth_oauthlib-1.2.2-py3-none-any.whl.metadata (2.7 kB)
Collecting google-cloud-storage (from gcsfs>=2023.1.0->datadreamer)
  Using cached google_cloud_storage-3.1.1-py3-none-any.whl.metadata (13 kB)
Requirement already satisfied: aiohappyeyeballs>=2.5.0 in ./.audit-env/lib/python3.13/site-packages (from aiohttp!=4.0.0a0,!=4.0.0a1->gcsfs>=2023.1.0->datadreamer) (2.6.1)
Requirement already satisfied: aiosignal>=1.1.2 in ./.audit-env/lib/python3.13/site-packages (from aiohttp!=4.0.0a0,!=4.0.0a1->gcsfs>=2023.1.0->datadreamer) (1.3.2)
Requirement already satisfied: attrs>=17.3.0 in ./.audit-env/lib/python3.13/site-packages (from aiohttp!=4.0.0a0,!=4.0.0a1->gcsfs>=2023.1.0->datadreamer) (25.3.0)
Requirement already satisfied: frozenlist>=1.1.1 in ./.audit-env/lib/python3.13/site-packages (from aiohttp!=4.0.0a0,!=4.0.0a1->gcsfs>=2023.1.0->datadreamer) (1.7.0)
Requirement already satisfied: multidict<7.0,>=4.5 in ./.audit-env/lib/python3.13/site-packages (from aiohttp!=4.0.0a0,!=4.0.0a1->gcsfs>=2023.1.0->datadreamer) (6.5.0)
Requirement already satisfied: propcache>=0.2.0 in ./.audit-env/lib/python3.13/site-packages (from aiohttp!=4.0.0a0,!=4.0.0a1->gcsfs>=2023.1.0->datadreamer) (0.3.2)
Requirement already satisfied: yarl<2.0,>=1.17.0 in ./.audit-env/lib/python3.13/site-packages (from aiohttp!=4.0.0a0,!=4.0.0a1->gcsfs>=2023.1.0->datadreamer) (1.20.1)
Requirement already satisfied: idna>=2.0 in ./.audit-env/lib/python3.13/site-packages (from yarl<2.0,>=1.17.0->aiohttp!=4.0.0a0,!=4.0.0a1->gcsfs>=2023.1.0->datadreamer) (3.10)
Collecting cachetools<6.0,>=2.0.0 (from google-auth>=1.2->gcsfs>=2023.1.0->datadreamer)
  Using cached cachetools-5.5.2-py3-none-any.whl.metadata (5.4 kB)
Collecting pyasn1-modules>=0.2.1 (from google-auth>=1.2->gcsfs>=2023.1.0->datadreamer)
  Using cached pyasn1_modules-0.4.2-py3-none-any.whl.metadata (3.5 kB)
Collecting rsa<5,>=3.1.4 (from google-auth>=1.2->gcsfs>=2023.1.0->datadreamer)
  Using cached rsa-4.9.1-py3-none-any.whl.metadata (5.6 kB)
Collecting pyasn1>=0.1.3 (from rsa<5,>=3.1.4->google-auth>=1.2->gcsfs>=2023.1.0->datadreamer)
  Using cached pyasn1-0.6.1-py3-none-any.whl.metadata (8.4 kB)
Requirement already satisfied: pydantic~=2.7 in ./.audit-env/lib/python3.13/site-packages (from luxonis-ml>=0.5.0->luxonis-ml[all]>=0.5.0->datadreamer) (2.11.7)
Collecting pydantic-settings~=2.1 (from luxonis-ml>=0.5.0->luxonis-ml[all]>=0.5.0->datadreamer)
  Using cached pydantic_settings-2.9.1-py3-none-any.whl.metadata (3.8 kB)
Requirement already satisfied: rich~=13.6 in ./.audit-env/lib/python3.13/site-packages (from luxonis-ml>=0.5.0->luxonis-ml[all]>=0.5.0->datadreamer) (13.9.4)
Requirement already satisfied: typer~=0.12 in ./.audit-env/lib/python3.13/site-packages (from luxonis-ml>=0.5.0->luxonis-ml[all]>=0.5.0->datadreamer) (0.16.0)
Collecting typeguard~=4.1 (from luxonis-ml>=0.5.0->luxonis-ml[all]>=0.5.0->datadreamer)
  Using cached typeguard-4.4.4-py3-none-any.whl.metadata (3.3 kB)
Collecting aiobotocore<2.18 (from luxonis-ml>=0.5.0->luxonis-ml[all]>=0.5.0->datadreamer)
  Using cached aiobotocore-2.17.0-py3-none-any.whl.metadata (23 kB)
Requirement already satisfied: loguru~=0.7 in ./.audit-env/lib/python3.13/site-packages (from luxonis-ml>=0.5.0->luxonis-ml[all]>=0.5.0->datadreamer) (0.7.3)
Requirement already satisfied: aioitertools<1.0.0,>=0.5.1 in ./.audit-env/lib/python3.13/site-packages (from aiobotocore<2.18->luxonis-ml>=0.5.0->luxonis-ml[all]>=0.5.0->datadreamer) (0.12.0)
Collecting botocore<1.35.94,>=1.35.74 (from aiobotocore<2.18->luxonis-ml>=0.5.0->luxonis-ml[all]>=0.5.0->datadreamer)
  Downloading botocore-1.35.93-py3-none-any.whl.metadata (5.7 kB)
Requirement already satisfied: python-dateutil<3.0.0,>=2.1 in ./.audit-env/lib/python3.13/site-packages (from aiobotocore<2.18->luxonis-ml>=0.5.0->luxonis-ml[all]>=0.5.0->datadreamer) (2.9.0.post0)
Requirement already satisfied: jmespath<2.0.0,>=0.7.1 in ./.audit-env/lib/python3.13/site-packages (from aiobotocore<2.18->luxonis-ml>=0.5.0->luxonis-ml[all]>=0.5.0->datadreamer) (1.0.1)
Requirement already satisfied: urllib3!=2.2.0,<3,>=1.25.4 in ./.audit-env/lib/python3.13/site-packages (from aiobotocore<2.18->luxonis-ml>=0.5.0->luxonis-ml[all]>=0.5.0->datadreamer) (2.5.0)
Requirement already satisfied: wrapt<2.0.0,>=1.10.10 in ./.audit-env/lib/python3.13/site-packages (from aiobotocore<2.18->luxonis-ml>=0.5.0->luxonis-ml[all]>=0.5.0->datadreamer) (1.17.2)
Requirement already satisfied: annotated-types>=0.6.0 in ./.audit-env/lib/python3.13/site-packages (from pydantic~=2.7->luxonis-ml>=0.5.0->luxonis-ml[all]>=0.5.0->datadreamer) (0.7.0)
Requirement already satisfied: pydantic-core==2.33.2 in ./.audit-env/lib/python3.13/site-packages (from pydantic~=2.7->luxonis-ml>=0.5.0->luxonis-ml[all]>=0.5.0->datadreamer) (2.33.2)
Requirement already satisfied: typing-inspection>=0.4.0 in ./.audit-env/lib/python3.13/site-packages (from pydantic~=2.7->luxonis-ml>=0.5.0->luxonis-ml[all]>=0.5.0->datadreamer) (0.4.1)
Requirement already satisfied: python-dotenv>=0.21.0 in ./.audit-env/lib/python3.13/site-packages (from pydantic-settings~=2.1->luxonis-ml>=0.5.0->luxonis-ml[all]>=0.5.0->datadreamer) (1.1.0)
Requirement already satisfied: six>=1.5 in ./.audit-env/lib/python3.13/site-packages (from python-dateutil<3.0.0,>=2.1->aiobotocore<2.18->luxonis-ml>=0.5.0->luxonis-ml[all]>=0.5.0->datadreamer) (1.17.0)
Requirement already satisfied: markdown-it-py>=2.2.0 in ./.audit-env/lib/python3.13/site-packages (from rich~=13.6->luxonis-ml>=0.5.0->luxonis-ml[all]>=0.5.0->datadreamer) (3.0.0)
Requirement already satisfied: pygments<3.0.0,>=2.13.0 in ./.audit-env/lib/python3.13/site-packages (from rich~=13.6->luxonis-ml>=0.5.0->luxonis-ml[all]>=0.5.0->datadreamer) (2.19.1)
Requirement already satisfied: click>=8.0.0 in ./.audit-env/lib/python3.13/site-packages (from typer~=0.12->luxonis-ml>=0.5.0->luxonis-ml[all]>=0.5.0->datadreamer) (8.2.1)
Requirement already satisfied: shellingham>=1.3.0 in ./.audit-env/lib/python3.13/site-packages (from typer~=0.12->luxonis-ml>=0.5.0->luxonis-ml[all]>=0.5.0->datadreamer) (1.5.4)
Collecting numpy>=1.22.0 (from datadreamer)
  Using cached numpy-1.26.4-cp313-cp313-macosx_14_0_arm64.whl
Collecting albumentations>=2.0.0 (from luxonis-ml[all]>=0.5.0->datadreamer)
  Using cached albumentations-2.0.8-py3-none-any.whl.metadata (43 kB)
Collecting pyarrow~=17.0 (from luxonis-ml[all]>=0.5.0->datadreamer)
  Downloading pyarrow-17.0.0.tar.gz (1.1 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.1/1.1 MB 33.7 MB/s eta 0:00:00
  Installing build dependencies: started
  Installing build dependencies: finished with status 'done'
  Getting requirements to build wheel: started
  Getting requirements to build wheel: finished with status 'done'
  Preparing metadata (pyproject.toml): started
  Preparing metadata (pyproject.toml): finished with status 'done'
Collecting pycocotools~=2.0 (from luxonis-ml[all]>=0.5.0->datadreamer)
  Using cached pycocotools-2.0.10-cp312-abi3-macosx_10_13_universal2.whl.metadata (1.3 kB)
Collecting polars~=0.20 (from polars[timezone]~=0.20; extra == "all"->luxonis-ml[all]>=0.5.0->datadreamer)
  Downloading polars-0.20.31-cp38-abi3-macosx_11_0_arm64.whl.metadata (14 kB)
Collecting ordered-set~=4.0 (from luxonis-ml[all]>=0.5.0->datadreamer)
  Downloading ordered_set-4.1.0-py3-none-any.whl.metadata (5.3 kB)
Collecting semver~=3.0 (from luxonis-ml[all]>=0.5.0->datadreamer)
  Downloading semver-3.0.4-py3-none-any.whl.metadata (6.8 kB)
Collecting bidict~=0.21 (from luxonis-ml[all]>=0.5.0->datadreamer)
  Using cached bidict-0.23.1-py3-none-any.whl.metadata (8.7 kB)
Collecting gdown~=4.7 (from luxonis-ml[all]>=0.5.0->datadreamer)
  Downloading gdown-4.7.3-py3-none-any.whl.metadata (4.4 kB)
Collecting defusedxml~=0.7 (from luxonis-ml[all]>=0.5.0->datadreamer)
  Using cached defusedxml-0.7.1-py2.py3-none-any.whl.metadata (32 kB)
Collecting pillow-heif<0.22.0 (from luxonis-ml[all]>=0.5.0->datadreamer)
  Downloading pillow_heif-0.21.0-cp313-cp313-macosx_14_0_arm64.whl.metadata (9.8 kB)
Collecting unique-names-generator>=1.0.2 (from luxonis-ml[all]>=0.5.0->datadreamer)
  Using cached unique_names_generator-1.0.2-py2.py3-none-any.whl.metadata (2.7 kB)
Collecting docker>=6.1.3 (from luxonis-ml[all]>=0.5.0->datadreamer)
  Using cached docker-7.1.0-py3-none-any.whl.metadata (3.8 kB)
Collecting KDEpy>=1.1.5 (from luxonis-ml[all]>=0.5.0->datadreamer)
  Using cached kdepy-1.1.12-cp313-cp313-macosx_11_0_arm64.whl.metadata (7.7 kB)
Collecting kmedoids>=0.4.3 (from luxonis-ml[all]>=0.5.0->datadreamer)
  Using cached kmedoids-0.5.3.1-cp313-cp313-macosx_10_12_x86_64.macosx_11_0_arm64.macosx_10_12_universal2.whl.metadata (9.6 kB)
Collecting onnx>=1.14.0 (from luxonis-ml[all]>=0.5.0->datadreamer)
  Using cached onnx-1.18.0-cp313-cp313-macosx_12_0_universal2.whl.metadata (6.9 kB)
Collecting onnxruntime>=1.15.1 (from luxonis-ml[all]>=0.5.0->datadreamer)
  Using cached onnxruntime-1.22.0-cp313-cp313-macosx_13_0_universal2.whl.metadata (4.5 kB)
Collecting qdrant-client>=1.4.0 (from luxonis-ml[all]>=0.5.0->datadreamer)
  Using cached qdrant_client-1.14.3-py3-none-any.whl.metadata (10 kB)
Collecting weaviate-client>=4.4b2 (from luxonis-ml[all]>=0.5.0->datadreamer)
  Using cached weaviate_client-4.15.2-py3-none-any.whl.metadata (3.7 kB)
Collecting scikit-learn>=1.3.0 (from luxonis-ml[all]>=0.5.0->datadreamer)
  Using cached scikit_learn-1.7.0-cp313-cp313-macosx_12_0_arm64.whl.metadata (31 kB)
Collecting roboflow~=1.1.0 (from luxonis-ml[all]>=0.5.0->datadreamer)
  Downloading roboflow-1.1.66-py3-none-any.whl.metadata (9.7 kB)
Requirement already satisfied: s3fs>=2023.3.0 in ./.audit-env/lib/python3.13/site-packages (from luxonis-ml[all]>=0.5.0->datadreamer) (2025.5.1)
Collecting mlflow~=2.16.0 (from luxonis-ml[all]>=0.5.0->datadreamer)
  Downloading mlflow-2.16.2-py3-none-any.whl.metadata (29 kB)
Collecting beautifulsoup4 (from gdown~=4.7->luxonis-ml[all]>=0.5.0->datadreamer)
  Using cached beautifulsoup4-4.13.4-py3-none-any.whl.metadata (3.8 kB)
Collecting contourpy>=1.0.1 (from matplotlib>=3.6.0->datadreamer)
  Using cached contourpy-1.3.2-cp313-cp313-macosx_11_0_arm64.whl.metadata (5.5 kB)
Collecting cycler>=0.10 (from matplotlib>=3.6.0->datadreamer)
  Using cached cycler-0.12.1-py3-none-any.whl.metadata (3.8 kB)
Collecting fonttools>=4.22.0 (from matplotlib>=3.6.0->datadreamer)
  Using cached fonttools-4.58.4-cp313-cp313-macosx_10_13_universal2.whl.metadata (106 kB)
Collecting kiwisolver>=1.3.1 (from matplotlib>=3.6.0->datadreamer)
  Using cached kiwisolver-1.4.8-cp313-cp313-macosx_11_0_arm64.whl.metadata (6.2 kB)
Collecting mlflow-skinny==2.16.2 (from mlflow~=2.16.0->luxonis-ml[all]>=0.5.0->datadreamer)
  Downloading mlflow_skinny-2.16.2-py3-none-any.whl.metadata (30 kB)
Collecting Flask<4 (from mlflow~=2.16.0->luxonis-ml[all]>=0.5.0->datadreamer)
  Using cached flask-3.1.1-py3-none-any.whl.metadata (3.0 kB)
Collecting alembic!=1.10.0,<2 (from mlflow~=2.16.0->luxonis-ml[all]>=0.5.0->datadreamer)
  Downloading alembic-1.16.2-py3-none-any.whl.metadata (7.3 kB)
Collecting graphene<4 (from mlflow~=2.16.0->luxonis-ml[all]>=0.5.0->datadreamer)
  Downloading graphene-3.4.3-py2.py3-none-any.whl.metadata (6.9 kB)
Collecting markdown<4,>=3.3 (from mlflow~=2.16.0->luxonis-ml[all]>=0.5.0->datadreamer)
  Downloading markdown-3.8.2-py3-none-any.whl.metadata (5.1 kB)
Requirement already satisfied: pandas<3 in ./.audit-env/lib/python3.13/site-packages (from mlflow~=2.16.0->luxonis-ml[all]>=0.5.0->datadreamer) (2.3.0)
Collecting sqlalchemy<3,>=1.4.0 (from mlflow~=2.16.0->luxonis-ml[all]>=0.5.0->datadreamer)
  Downloading sqlalchemy-2.0.41-cp313-cp313-macosx_11_0_arm64.whl.metadata (9.6 kB)
Requirement already satisfied: Jinja2<4,>=2.11 in ./.audit-env/lib/python3.13/site-packages (from mlflow~=2.16.0->luxonis-ml[all]>=0.5.0->datadreamer) (3.1.6)
Collecting gunicorn<24 (from mlflow~=2.16.0->luxonis-ml[all]>=0.5.0->datadreamer)
  Downloading gunicorn-23.0.0-py3-none-any.whl.metadata (4.4 kB)
Collecting cloudpickle<4 (from mlflow-skinny==2.16.2->mlflow~=2.16.0->luxonis-ml[all]>=0.5.0->datadreamer)
  Downloading cloudpickle-3.1.1-py3-none-any.whl.metadata (7.1 kB)
Collecting databricks-sdk<1,>=0.20.0 (from mlflow-skinny==2.16.2->mlflow~=2.16.0->luxonis-ml[all]>=0.5.0->datadreamer)
  Downloading databricks_sdk-0.57.0-py3-none-any.whl.metadata (39 kB)
Collecting gitpython<4,>=3.1.9 (from mlflow-skinny==2.16.2->mlflow~=2.16.0->luxonis-ml[all]>=0.5.0->datadreamer)
  Downloading GitPython-3.1.44-py3-none-any.whl.metadata (13 kB)
Collecting opentelemetry-api<3,>=1.9.0 (from mlflow-skinny==2.16.2->mlflow~=2.16.0->luxonis-ml[all]>=0.5.0->datadreamer)
  Downloading opentelemetry_api-1.34.1-py3-none-any.whl.metadata (1.5 kB)
Collecting opentelemetry-sdk<3,>=1.9.0 (from mlflow-skinny==2.16.2->mlflow~=2.16.0->luxonis-ml[all]>=0.5.0->datadreamer)
  Downloading opentelemetry_sdk-1.34.1-py3-none-any.whl.metadata (1.6 kB)
Collecting packaging>=20.0 (from accelerate>=0.25.0->datadreamer)
  Using cached packaging-24.2-py3-none-any.whl.metadata (3.2 kB)
Collecting protobuf<6,>=3.12.0 (from mlflow-skinny==2.16.2->mlflow~=2.16.0->luxonis-ml[all]>=0.5.0->datadreamer)
  Using cached protobuf-5.29.5-cp38-abi3-macosx_10_9_universal2.whl.metadata (592 bytes)
Requirement already satisfied: sqlparse<1,>=0.4.0 in ./.audit-env/lib/python3.13/site-packages (from mlflow-skinny==2.16.2->mlflow~=2.16.0->luxonis-ml[all]>=0.5.0->datadreamer) (0.5.3)
Collecting Mako (from alembic!=1.10.0,<2->mlflow~=2.16.0->luxonis-ml[all]>=0.5.0->datadreamer)
  Downloading mako-1.3.10-py3-none-any.whl.metadata (2.9 kB)
Collecting blinker>=1.9.0 (from Flask<4->mlflow~=2.16.0->luxonis-ml[all]>=0.5.0->datadreamer)
  Using cached blinker-1.9.0-py3-none-any.whl.metadata (1.6 kB)
Collecting itsdangerous>=2.2.0 (from Flask<4->mlflow~=2.16.0->luxonis-ml[all]>=0.5.0->datadreamer)
  Using cached itsdangerous-2.2.0-py3-none-any.whl.metadata (1.9 kB)
Requirement already satisfied: markupsafe>=2.1.1 in ./.audit-env/lib/python3.13/site-packages (from Flask<4->mlflow~=2.16.0->luxonis-ml[all]>=0.5.0->datadreamer) (3.0.2)
Requirement already satisfied: werkzeug>=3.1.0 in ./.audit-env/lib/python3.13/site-packages (from Flask<4->mlflow~=2.16.0->luxonis-ml[all]>=0.5.0->datadreamer) (3.1.3)
Collecting gitdb<5,>=4.0.1 (from gitpython<4,>=3.1.9->mlflow-skinny==2.16.2->mlflow~=2.16.0->luxonis-ml[all]>=0.5.0->datadreamer)
  Downloading gitdb-4.0.12-py3-none-any.whl.metadata (1.2 kB)
Collecting smmap<6,>=3.0.1 (from gitdb<5,>=4.0.1->gitpython<4,>=3.1.9->mlflow-skinny==2.16.2->mlflow~=2.16.0->luxonis-ml[all]>=0.5.0->datadreamer)
  Downloading smmap-5.0.2-py3-none-any.whl.metadata (4.3 kB)
Collecting graphql-core<3.3,>=3.1 (from graphene<4->mlflow~=2.16.0->luxonis-ml[all]>=0.5.0->datadreamer)
  Downloading graphql_core-3.2.6-py3-none-any.whl.metadata (11 kB)
Collecting graphql-relay<3.3,>=3.1 (from graphene<4->mlflow~=2.16.0->luxonis-ml[all]>=0.5.0->datadreamer)
  Downloading graphql_relay-3.2.0-py3-none-any.whl.metadata (12 kB)
Collecting zipp>=3.20 (from importlib-metadata->diffusers>=0.31.0->datadreamer)
  Using cached zipp-3.23.0-py3-none-any.whl.metadata (3.6 kB)
Collecting opentelemetry-semantic-conventions==0.55b1 (from opentelemetry-sdk<3,>=1.9.0->mlflow-skinny==2.16.2->mlflow~=2.16.0->luxonis-ml[all]>=0.5.0->datadreamer)
  Using cached opentelemetry_semantic_conventions-0.55b1-py3-none-any.whl.metadata (2.5 kB)
Requirement already satisfied: pytz>=2020.1 in ./.audit-env/lib/python3.13/site-packages (from pandas<3->mlflow~=2.16.0->luxonis-ml[all]>=0.5.0->datadreamer) (2025.2)
Requirement already satisfied: tzdata>=2022.7 in ./.audit-env/lib/python3.13/site-packages (from pandas<3->mlflow~=2.16.0->luxonis-ml[all]>=0.5.0->datadreamer) (2025.2)
Requirement already satisfied: charset_normalizer<4,>=2 in ./.audit-env/lib/python3.13/site-packages (from requests->transformers>=4.45.2->datadreamer) (3.4.2)
Requirement already satisfied: certifi>=2017.4.17 in ./.audit-env/lib/python3.13/site-packages (from requests->transformers>=4.45.2->datadreamer) (2025.6.15)
Collecting idna>=2.0 (from yarl<2.0,>=1.17.0->aiohttp!=4.0.0a0,!=4.0.0a1->gcsfs>=2023.1.0->datadreamer)
  Downloading idna-3.7-py3-none-any.whl.metadata (9.9 kB)
Collecting opencv-python-headless==4.10.0.84 (from roboflow~=1.1.0->luxonis-ml[all]>=0.5.0->datadreamer)
  Downloading opencv_python_headless-4.10.0.84-cp37-abi3-macosx_11_0_arm64.whl.metadata (20 kB)
Collecting requests-toolbelt (from roboflow~=1.1.0->luxonis-ml[all]>=0.5.0->datadreamer)
  Downloading requests_toolbelt-1.0.0-py2.py3-none-any.whl.metadata (14 kB)
Collecting filetype (from roboflow~=1.1.0->luxonis-ml[all]>=0.5.0->datadreamer)
  Using cached filetype-1.2.0-py2.py3-none-any.whl.metadata (6.5 kB)
Collecting joblib>=1.2.0 (from scikit-learn>=1.3.0->luxonis-ml[all]>=0.5.0->datadreamer)
  Using cached joblib-1.5.1-py3-none-any.whl.metadata (5.6 kB)
Collecting threadpoolctl>=3.1.0 (from scikit-learn>=1.3.0->luxonis-ml[all]>=0.5.0->datadreamer)
  Using cached threadpoolctl-3.6.0-py3-none-any.whl.metadata (13 kB)
Collecting albucore==0.0.24 (from albumentations>=2.0.0->luxonis-ml[all]>=0.5.0->datadreamer)
  Using cached albucore-0.0.24-py3-none-any.whl.metadata (5.3 kB)
Collecting stringzilla>=3.10.4 (from albucore==0.0.24->albumentations>=2.0.0->luxonis-ml[all]>=0.5.0->datadreamer)
  Downloading stringzilla-3.12.5-cp313-cp313-macosx_11_0_arm64.whl.metadata (80 kB)
Collecting simsimd>=5.9.2 (from albucore==0.0.24->albumentations>=2.0.0->luxonis-ml[all]>=0.5.0->datadreamer)
  Downloading simsimd-6.4.9-cp313-cp313-macosx_11_0_arm64.whl.metadata (66 kB)
Requirement already satisfied: mdurl~=0.1 in ./.audit-env/lib/python3.13/site-packages (from markdown-it-py>=2.2.0->rich~=13.6->luxonis-ml>=0.5.0->luxonis-ml[all]>=0.5.0->datadreamer) (0.1.2)
Collecting coloredlogs (from onnxruntime>=1.15.1->luxonis-ml[all]>=0.5.0->datadreamer)
  Using cached coloredlogs-15.0.1-py2.py3-none-any.whl.metadata (12 kB)
Collecting flatbuffers (from onnxruntime>=1.15.1->luxonis-ml[all]>=0.5.0->datadreamer)
  Using cached flatbuffers-25.2.10-py2.py3-none-any.whl.metadata (875 bytes)
Requirement already satisfied: sympy in ./.audit-env/lib/python3.13/site-packages (from onnxruntime>=1.15.1->luxonis-ml[all]>=0.5.0->datadreamer) (1.14.0)
Collecting grpcio>=1.41.0 (from qdrant-client>=1.4.0->luxonis-ml[all]>=0.5.0->datadreamer)
  Using cached grpcio-1.73.0-cp313-cp313-macosx_11_0_universal2.whl.metadata (3.8 kB)
Requirement already satisfied: httpx>=0.20.0 in ./.audit-env/lib/python3.13/site-packages (from httpx[http2]>=0.20.0->qdrant-client>=1.4.0->luxonis-ml[all]>=0.5.0->datadreamer) (0.24.0)
INFO: pip is looking at multiple versions of qdrant-client to determine which version is compatible with other requirements. This could take a while.
Collecting qdrant-client>=1.4.0 (from luxonis-ml[all]>=0.5.0->datadreamer)
  Downloading qdrant_client-1.14.2-py3-none-any.whl.metadata (10 kB)
  Downloading qdrant_client-1.14.1-py3-none-any.whl.metadata (10 kB)
  Downloading qdrant_client-1.13.3-py3-none-any.whl.metadata (10 kB)
Collecting grpcio-tools>=1.41.0 (from qdrant-client>=1.4.0->luxonis-ml[all]>=0.5.0->datadreamer)
  Using cached grpcio_tools-1.73.0-cp313-cp313-macosx_11_0_universal2.whl.metadata (5.3 kB)
Collecting qdrant-client>=1.4.0 (from luxonis-ml[all]>=0.5.0->datadreamer)
  Downloading qdrant_client-1.13.2-py3-none-any.whl.metadata (10 kB)
  Downloading qdrant_client-1.13.1-py3-none-any.whl.metadata (10 kB)
  Downloading qdrant_client-1.13.0-py3-none-any.whl.metadata (10 kB)
  Downloading qdrant_client-1.12.2-py3-none-any.whl.metadata (10 kB)
INFO: pip is still looking at multiple versions of qdrant-client to determine which version is compatible with other requirements. This could take a while.
  Downloading qdrant_client-1.12.1-py3-none-any.whl.metadata (10 kB)
Collecting portalocker<3.0.0,>=2.7.0 (from qdrant-client>=1.4.0->luxonis-ml[all]>=0.5.0->datadreamer)
  Using cached portalocker-2.10.1-py3-none-any.whl.metadata (8.5 kB)
INFO: pip is looking at multiple versions of grpcio-tools to determine which version is compatible with other requirements. This could take a while.
Collecting grpcio-tools>=1.41.0 (from qdrant-client>=1.4.0->luxonis-ml[all]>=0.5.0->datadreamer)
  Downloading grpcio_tools-1.72.1-cp313-cp313-macosx_11_0_universal2.whl.metadata (5.3 kB)
  Downloading grpcio_tools-1.71.0-cp313-cp313-macosx_10_14_universal2.whl.metadata (5.3 kB)
Requirement already satisfied: setuptools in ./.audit-env/lib/python3.13/site-packages (from grpcio-tools>=1.41.0->qdrant-client>=1.4.0->luxonis-ml[all]>=0.5.0->datadreamer) (80.9.0)
Requirement already satisfied: httpcore<0.18.0,>=0.15.0 in ./.audit-env/lib/python3.13/site-packages (from httpx>=0.20.0->httpx[http2]>=0.20.0->qdrant-client>=1.4.0->luxonis-ml[all]>=0.5.0->datadreamer) (0.17.3)
Requirement already satisfied: sniffio in ./.audit-env/lib/python3.13/site-packages (from httpx>=0.20.0->httpx[http2]>=0.20.0->qdrant-client>=1.4.0->luxonis-ml[all]>=0.5.0->datadreamer) (1.3.1)
Requirement already satisfied: h11<0.15,>=0.13 in ./.audit-env/lib/python3.13/site-packages (from httpcore<0.18.0,>=0.15.0->httpx>=0.20.0->httpx[http2]>=0.20.0->qdrant-client>=1.4.0->luxonis-ml[all]>=0.5.0->datadreamer) (0.14.0)
Requirement already satisfied: anyio<5.0,>=3.0 in ./.audit-env/lib/python3.13/site-packages (from httpcore<0.18.0,>=0.15.0->httpx>=0.20.0->httpx[http2]>=0.20.0->qdrant-client>=1.4.0->luxonis-ml[all]>=0.5.0->datadreamer) (4.9.0)
Requirement already satisfied: h2<5,>=3 in ./.audit-env/lib/python3.13/site-packages (from httpx[http2]>=0.20.0->qdrant-client>=1.4.0->luxonis-ml[all]>=0.5.0->datadreamer) (4.2.0)
Requirement already satisfied: hyperframe<7,>=6.1 in ./.audit-env/lib/python3.13/site-packages (from h2<5,>=3->httpx[http2]>=0.20.0->qdrant-client>=1.4.0->luxonis-ml[all]>=0.5.0->datadreamer) (6.1.0)
Requirement already satisfied: hpack<5,>=4.1 in ./.audit-env/lib/python3.13/site-packages (from h2<5,>=3->httpx[http2]>=0.20.0->qdrant-client>=1.4.0->luxonis-ml[all]>=0.5.0->datadreamer) (4.1.0)
Requirement already satisfied: networkx in ./.audit-env/lib/python3.13/site-packages (from torch>=2.0.0->datadreamer) (3.5)
Requirement already satisfied: mpmath<1.4,>=1.1.0 in ./.audit-env/lib/python3.13/site-packages (from sympy->onnxruntime>=1.15.1->luxonis-ml[all]>=0.5.0->datadreamer) (1.3.0)
INFO: pip is looking at multiple versions of weaviate-client to determine which version is compatible with other requirements. This could take a while.
Collecting weaviate-client>=4.4b2 (from luxonis-ml[all]>=0.5.0->datadreamer)
  Using cached weaviate_client-4.15.1-py3-none-any.whl.metadata (3.7 kB)
  Using cached weaviate_client-4.15.0-py3-none-any.whl.metadata (3.7 kB)
  Using cached weaviate_client-4.14.4-py3-none-any.whl.metadata (3.7 kB)
  Using cached weaviate_client-4.14.3-py3-none-any.whl.metadata (3.7 kB)
  Using cached weaviate_client-4.14.1-py3-none-any.whl.metadata (3.7 kB)
  Using cached weaviate_client-4.14.0-py3-none-any.whl.metadata (3.7 kB)
  Using cached weaviate_client-4.13.2-py3-none-any.whl.metadata (3.7 kB)
INFO: pip is still looking at multiple versions of weaviate-client to determine which version is compatible with other requirements. This could take a while.
  Using cached weaviate_client-4.13.1-py3-none-any.whl.metadata (3.7 kB)
  Using cached weaviate_client-4.13.0-py3-none-any.whl.metadata (3.7 kB)
  Using cached weaviate_client-4.13.0a0-py3-none-any.whl.metadata (3.7 kB)
  Using cached weaviate_client-4.12.1-py3-none-any.whl.metadata (3.7 kB)
  Using cached weaviate_client-4.12.0-py3-none-any.whl.metadata (3.7 kB)
INFO: This is taking longer than usual. You might need to provide the dependency resolver with stricter constraints to reduce runtime. See https://pip.pypa.io/warnings/backtracking for guidance. If you want to abort this run, press Ctrl + C.
  Using cached weaviate_client-4.12.0a2-py3-none-any.whl.metadata (3.7 kB)
  Using cached weaviate_client-4.12.0a1-py3-none-any.whl.metadata (3.7 kB)
  Using cached weaviate_client-4.12.0a0-py3-none-any.whl.metadata (3.7 kB)
  Using cached weaviate_client-4.11.3-py3-none-any.whl.metadata (3.7 kB)
  Using cached weaviate_client-4.11.2-py3-none-any.whl.metadata (3.6 kB)
  Using cached weaviate_client-4.11.1-py3-none-any.whl.metadata (3.6 kB)
  Using cached weaviate_client-4.11.0-py3-none-any.whl.metadata (3.6 kB)
  Using cached weaviate_client-4.11.0b2-py3-none-any.whl.metadata (3.6 kB)
  Using cached weaviate_client-4.11.0b1-py3-none-any.whl.metadata (3.6 kB)
  Using cached weaviate_client-4.11.0b0-py3-none-any.whl.metadata (3.6 kB)
  Using cached weaviate_client-4.10.4-py3-none-any.whl.metadata (3.6 kB)
  Using cached weaviate_client-4.10.3-py3-none-any.whl.metadata (3.6 kB)
  Using cached weaviate_client-4.10.2-py3-none-any.whl.metadata (3.6 kB)
  Using cached weaviate_client-4.10.1-py3-none-any.whl.metadata (3.6 kB)
  Using cached weaviate_client-4.10.0-py3-none-any.whl.metadata (3.6 kB)
  Using cached weaviate_client-4.10.0b3-py3-none-any.whl.metadata (3.6 kB)
  Using cached weaviate_client-4.10.0b2-py3-none-any.whl.metadata (3.6 kB)
  Using cached weaviate_client-4.10.0b1-py3-none-any.whl.metadata (3.6 kB)
  Using cached weaviate_client-4.10.0b0-py3-none-any.whl.metadata (3.6 kB)
  Using cached weaviate_client-4.9.6-py3-none-any.whl.metadata (3.6 kB)
  Using cached weaviate_client-4.9.5-py3-none-any.whl.metadata (3.6 kB)
  Using cached weaviate_client-4.9.4-py3-none-any.whl.metadata (3.6 kB)
  Using cached weaviate_client-4.9.3-py3-none-any.whl.metadata (3.6 kB)
  Using cached weaviate_client-4.9.2-py3-none-any.whl.metadata (3.6 kB)
  Using cached weaviate_client-4.9.1-py3-none-any.whl.metadata (3.6 kB)
  Using cached weaviate_client-4.9.0-py3-none-any.whl.metadata (3.6 kB)
  Using cached weaviate_client-4.9.0b1-py3-none-any.whl.metadata (3.6 kB)
  Using cached weaviate_client-4.9.0b0-py3-none-any.whl.metadata (3.6 kB)
  Using cached weaviate_client-4.8.1-py3-none-any.whl.metadata (3.6 kB)
  Using cached weaviate_client-4.8.0-py3-none-any.whl.metadata (3.6 kB)
  Using cached weaviate_client-4.7.1-py3-none-any.whl.metadata (3.3 kB)
  Using cached weaviate_client-4.7.0-py3-none-any.whl.metadata (3.3 kB)
  Using cached weaviate_client-4.7.0rc3-py3-none-any.whl.metadata (3.3 kB)
  Using cached weaviate_client-4.7.0rc2-py3-none-any.whl.metadata (3.3 kB)
  Using cached weaviate_client-4.7.0rc1-py3-none-any.whl.metadata (3.3 kB)
  Using cached weaviate_client-4.7.0rc0-py3-none-any.whl.metadata (3.3 kB)
  Using cached weaviate_client-4.7.0b4-py3-none-any.whl.metadata (3.3 kB)
  Using cached weaviate_client-4.7.0b3-py3-none-any.whl.metadata (3.3 kB)
  Using cached weaviate_client-4.7.0b2-py3-none-any.whl.metadata (3.3 kB)
  Using cached weaviate_client-4.7.0b1-py3-none-any.whl.metadata (3.3 kB)
  Using cached weaviate_client-4.7.0b0-py3-none-any.whl.metadata (3.3 kB)
  Using cached weaviate_client-4.7.0a0-py3-none-any.whl.metadata (3.3 kB)
  Using cached weaviate_client-4.6.7-py3-none-any.whl.metadata (3.3 kB)
  Using cached weaviate_client-4.6.5-py3-none-any.whl.metadata (3.3 kB)
  Using cached weaviate_client-4.6.4-py3-none-any.whl.metadata (3.3 kB)
  Using cached weaviate_client-4.6.3-py3-none-any.whl.metadata (3.3 kB)
  Using cached weaviate_client-4.6.2-py3-none-any.whl.metadata (3.3 kB)
  Using cached weaviate_client-4.6.1-py3-none-any.whl.metadata (3.3 kB)
  Using cached weaviate_client-4.6.0-py3-none-any.whl.metadata (3.3 kB)
  Using cached weaviate_client-4.6.0b3-py3-none-any.whl.metadata (3.3 kB)
  Using cached weaviate_client-4.6.0b1-py3-none-any.whl.metadata (3.3 kB)
  Using cached weaviate_client-4.6.0b0-py3-none-any.whl.metadata (3.3 kB)
  Using cached weaviate_client-4.5.7-py3-none-any.whl.metadata (3.3 kB)
  Using cached weaviate_client-4.5.6-py3-none-any.whl.metadata (3.3 kB)
  Using cached weaviate_client-4.5.5-py3-none-any.whl.metadata (3.3 kB)
  Using cached weaviate_client-4.5.4-py3-none-any.whl.metadata (3.3 kB)
  Using cached weaviate_client-4.5.3-py3-none-any.whl.metadata (3.3 kB)
  Using cached weaviate_client-4.5.2-py3-none-any.whl.metadata (3.3 kB)
  Using cached weaviate_client-4.5.1-py3-none-any.whl.metadata (3.3 kB)
  Using cached weaviate_client-4.5.0-py3-none-any.whl.metadata (3.3 kB)
  Using cached weaviate_client-4.5rc0-py3-none-any.whl.metadata (3.3 kB)
  Using cached weaviate_client-4.4.4-py3-none-any.whl.metadata (3.5 kB)
  Using cached weaviate_client-4.4.3-py3-none-any.whl.metadata (3.5 kB)
  Using cached weaviate_client-4.4.2-py3-none-any.whl.metadata (3.5 kB)
  Using cached weaviate_client-4.4.1-py3-none-any.whl.metadata (3.4 kB)
  Using cached weaviate_client-4.4.0-py3-none-any.whl.metadata (3.4 kB)
  Using cached weaviate_client-4.4rc1-py3-none-any.whl.metadata (3.4 kB)
  Using cached weaviate_client-4.4rc0-py3-none-any.whl.metadata (3.4 kB)
  Using cached weaviate_client-4.4b9-py3-none-any.whl.metadata (3.4 kB)
  Using cached weaviate_client-4.4b8-py3-none-any.whl.metadata (3.5 kB)
Collecting deprecated<2.0.0,>=1.2.14 (from weaviate-client>=4.4b2->luxonis-ml[all]>=0.5.0->datadreamer)
  Using cached Deprecated-1.2.18-py2.py3-none-any.whl.metadata (5.7 kB)
Collecting weaviate-client>=4.4b2 (from luxonis-ml[all]>=0.5.0->datadreamer)
  Using cached weaviate_client-4.4b7-py3-none-any.whl.metadata (3.5 kB)
  Using cached weaviate_client-4.4b6-py3-none-any.whl.metadata (3.4 kB)
Collecting validators<1.0.0,>=0.21.2 (from weaviate-client>=4.4b2->luxonis-ml[all]>=0.5.0->datadreamer)
  Using cached validators-0.35.0-py3-none-any.whl.metadata (3.9 kB)
Collecting authlib<2.0.0,>=1.2.1 (from weaviate-client>=4.4b2->luxonis-ml[all]>=0.5.0->datadreamer)
  Using cached authlib-1.6.0-py2.py3-none-any.whl.metadata (4.1 kB)
Collecting grpcio-health-checking<2.0.0,>=1.57.0 (from weaviate-client>=4.4b2->luxonis-ml[all]>=0.5.0->datadreamer)
  Using cached grpcio_health_checking-1.73.0-py3-none-any.whl.metadata (1.0 kB)
Requirement already satisfied: cryptography in ./.audit-env/lib/python3.13/site-packages (from authlib<2.0.0,>=1.2.1->weaviate-client>=4.4b2->luxonis-ml[all]>=0.5.0->datadreamer) (45.0.4)
INFO: pip is looking at multiple versions of grpcio-health-checking to determine which version is compatible with other requirements. This could take a while.
  Downloading grpcio_health_checking-1.72.1-py3-none-any.whl.metadata (1.0 kB)
  Downloading grpcio_health_checking-1.71.0-py3-none-any.whl.metadata (1.0 kB)
Collecting soupsieve>1.2 (from beautifulsoup4->gdown~=4.7->luxonis-ml[all]>=0.5.0->datadreamer)
  Using cached soupsieve-2.7-py3-none-any.whl.metadata (4.6 kB)
Collecting humanfriendly>=9.1 (from coloredlogs->onnxruntime>=1.15.1->luxonis-ml[all]>=0.5.0->datadreamer)
  Using cached humanfriendly-10.0-py2.py3-none-any.whl.metadata (9.2 kB)
Requirement already satisfied: cffi>=1.14 in ./.audit-env/lib/python3.13/site-packages (from cryptography->authlib<2.0.0,>=1.2.1->weaviate-client>=4.4b2->luxonis-ml[all]>=0.5.0->datadreamer) (1.17.1)
Requirement already satisfied: pycparser in ./.audit-env/lib/python3.13/site-packages (from cffi>=1.14->cryptography->authlib<2.0.0,>=1.2.1->weaviate-client>=4.4b2->luxonis-ml[all]>=0.5.0->datadreamer) (2.22)
Collecting requests-oauthlib>=0.7.0 (from google-auth-oauthlib->gcsfs>=2023.1.0->datadreamer)
  Downloading requests_oauthlib-2.0.0-py2.py3-none-any.whl.metadata (11 kB)
Collecting oauthlib>=3.0.0 (from requests-oauthlib>=0.7.0->google-auth-oauthlib->gcsfs>=2023.1.0->datadreamer)
  Downloading oauthlib-3.3.1-py3-none-any.whl.metadata (7.9 kB)
Collecting google-api-core<3.0.0,>=2.15.0 (from google-cloud-storage->gcsfs>=2023.1.0->datadreamer)
  Downloading google_api_core-2.25.1-py3-none-any.whl.metadata (3.0 kB)
Collecting google-cloud-core<3.0.0,>=2.4.2 (from google-cloud-storage->gcsfs>=2023.1.0->datadreamer)
  Downloading google_cloud_core-2.4.3-py2.py3-none-any.whl.metadata (2.7 kB)
Collecting google-resumable-media<3.0.0,>=2.7.2 (from google-cloud-storage->gcsfs>=2023.1.0->datadreamer)
  Using cached google_resumable_media-2.7.2-py2.py3-none-any.whl.metadata (2.2 kB)
Collecting google-crc32c<2.0.0,>=1.1.3 (from google-cloud-storage->gcsfs>=2023.1.0->datadreamer)
  Downloading google_crc32c-1.7.1-cp313-cp313-macosx_12_0_arm64.whl.metadata (2.3 kB)
Collecting googleapis-common-protos<2.0.0,>=1.56.2 (from google-api-core<3.0.0,>=2.15.0->google-cloud-storage->gcsfs>=2023.1.0->datadreamer)
  Using cached googleapis_common_protos-1.70.0-py3-none-any.whl.metadata (9.3 kB)
Collecting proto-plus<2.0.0,>=1.22.3 (from google-api-core<3.0.0,>=2.15.0->google-cloud-storage->gcsfs>=2023.1.0->datadreamer)
  Downloading proto_plus-1.26.1-py3-none-any.whl.metadata (2.2 kB)
Collecting PySocks!=1.5.7,>=1.5.6 (from requests[socks]->gdown~=4.7->luxonis-ml[all]>=0.5.0->datadreamer)
  Downloading PySocks-1.7.1-py3-none-any.whl.metadata (13 kB)
Downloading datadreamer-0.2.0-py3-none-any.whl (99 kB)
Using cached bitsandbytes-0.42.0-py3-none-any.whl (105.0 MB)
Using cached compel-2.1.1-py3-none-any.whl (31 kB)
Using cached pyparsing-3.2.3-py3-none-any.whl (111 kB)
Using cached diffusers-0.33.1-py3-none-any.whl (3.6 MB)
Downloading gcsfs-2025.5.1-py2.py3-none-any.whl (36 kB)
Using cached decorator-5.2.1-py3-none-any.whl (9.2 kB)
Downloading google_auth-2.40.3-py2.py3-none-any.whl (216 kB)
Downloading cachetools-5.5.2-py3-none-any.whl (10 kB)
Downloading rsa-4.9.1-py3-none-any.whl (34 kB)
Downloading luxonis_ml-0.7.1-py3-none-any.whl (228 kB)
Downloading aiobotocore-2.17.0-py3-none-any.whl (77 kB)
Downloading botocore-1.35.93-py3-none-any.whl (13.3 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 13.3/13.3 MB 61.6 MB/s eta 0:00:00
Using cached pydantic_settings-2.9.1-py3-none-any.whl (44 kB)
Using cached typeguard-4.4.4-py3-none-any.whl (34 kB)
Using cached bidict-0.23.1-py3-none-any.whl (32 kB)
Using cached defusedxml-0.7.1-py2.py3-none-any.whl (25 kB)
Downloading gdown-4.7.3-py3-none-any.whl (16 kB)
Using cached matplotlib-3.10.3-cp313-cp313-macosx_11_0_arm64.whl (8.1 MB)
Downloading mlflow-2.16.2-py3-none-any.whl (26.7 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 26.7/26.7 MB 66.1 MB/s eta 0:00:00
Downloading mlflow_skinny-2.16.2-py3-none-any.whl (5.6 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 5.6/5.6 MB 66.9 MB/s eta 0:00:00
Downloading alembic-1.16.2-py3-none-any.whl (242 kB)
Downloading cloudpickle-3.1.1-py3-none-any.whl (20 kB)
Downloading databricks_sdk-0.57.0-py3-none-any.whl (733 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 733.8/733.8 kB 42.6 MB/s eta 0:00:00
Using cached docker-7.1.0-py3-none-any.whl (147 kB)
Using cached flask-3.1.1-py3-none-any.whl (103 kB)
Downloading GitPython-3.1.44-py3-none-any.whl (207 kB)
Downloading gitdb-4.0.12-py3-none-any.whl (62 kB)
Downloading graphene-3.4.3-py2.py3-none-any.whl (114 kB)
Downloading graphql_core-3.2.6-py3-none-any.whl (203 kB)
Downloading graphql_relay-3.2.0-py3-none-any.whl (16 kB)
Downloading gunicorn-23.0.0-py3-none-any.whl (85 kB)
Using cached importlib_metadata-8.7.0-py3-none-any.whl (27 kB)
Downloading markdown-3.8.2-py3-none-any.whl (106 kB)
Downloading opencv_python-4.11.0.86-cp37-abi3-macosx_13_0_arm64.whl (37.3 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 37.3/37.3 MB 61.1 MB/s eta 0:00:00
Downloading opentelemetry_api-1.34.1-py3-none-any.whl (65 kB)
Downloading opentelemetry_sdk-1.34.1-py3-none-any.whl (118 kB)
Downloading opentelemetry_semantic_conventions-0.55b1-py3-none-any.whl (196 kB)
Downloading ordered_set-4.1.0-py3-none-any.whl (7.6 kB)
Using cached packaging-24.2-py3-none-any.whl (65 kB)
Downloading pillow_heif-0.21.0-cp313-cp313-macosx_14_0_arm64.whl (4.0 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 4.0/4.0 MB 47.5 MB/s eta 0:00:00
Downloading polars-0.20.31-cp38-abi3-macosx_11_0_arm64.whl (24.8 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 24.8/24.8 MB 32.0 MB/s eta 0:00:00
Using cached protobuf-5.29.5-cp38-abi3-macosx_10_9_universal2.whl (418 kB)
Using cached pycocotools-2.0.10-cp312-abi3-macosx_10_13_universal2.whl (142 kB)
Downloading roboflow-1.1.66-py3-none-any.whl (86 kB)
Downloading idna-3.7-py3-none-any.whl (66 kB)
Downloading opencv_python_headless-4.10.0.84-cp37-abi3-macosx_11_0_arm64.whl (54.8 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 54.8/54.8 MB 64.8 MB/s eta 0:00:00
Using cached scikit_learn-1.7.0-cp313-cp313-macosx_12_0_arm64.whl (10.6 MB)
Using cached scipy-1.15.3-cp313-cp313-macosx_14_0_arm64.whl (22.4 MB)
Downloading semver-3.0.4-py3-none-any.whl (17 kB)
Downloading smmap-5.0.2-py3-none-any.whl (24 kB)
Downloading sqlalchemy-2.0.41-cp313-cp313-macosx_11_0_arm64.whl (2.1 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.1/2.1 MB 51.6 MB/s eta 0:00:00
Downloading albumentations-2.0.8-py3-none-any.whl (369 kB)
Downloading albucore-0.0.24-py3-none-any.whl (15 kB)
Using cached blinker-1.9.0-py3-none-any.whl (8.5 kB)
Using cached contourpy-1.3.2-cp313-cp313-macosx_11_0_arm64.whl (255 kB)
Using cached cycler-0.12.1-py3-none-any.whl (8.3 kB)
Using cached fonttools-4.58.4-cp313-cp313-macosx_10_13_universal2.whl (2.7 MB)
Using cached itsdangerous-2.2.0-py3-none-any.whl (16 kB)
Using cached joblib-1.5.1-py3-none-any.whl (307 kB)
Using cached kdepy-1.1.12-cp313-cp313-macosx_11_0_arm64.whl (265 kB)
Using cached kiwisolver-1.4.8-cp313-cp313-macosx_11_0_arm64.whl (65 kB)
Using cached kmedoids-0.5.3.1-cp313-cp313-macosx_10_12_x86_64.macosx_11_0_arm64.macosx_10_12_universal2.whl (915 kB)
Using cached nltk-3.9.1-py3-none-any.whl (1.5 MB)
Using cached onnx-1.18.0-cp313-cp313-macosx_12_0_universal2.whl (18.3 MB)
Using cached onnxruntime-1.22.0-cp313-cp313-macosx_13_0_universal2.whl (34.3 MB)
Using cached pillow-11.2.1-cp313-cp313-macosx_11_0_arm64.whl (3.0 MB)
Using cached pyasn1-0.6.1-py3-none-any.whl (83 kB)
Downloading pyasn1_modules-0.4.2-py3-none-any.whl (181 kB)
Using cached python_box-7.3.2-cp313-cp313-macosx_10_13_universal2.whl (1.8 MB)
Downloading qdrant_client-1.12.1-py3-none-any.whl (267 kB)
Using cached portalocker-2.10.1-py3-none-any.whl (18 kB)
Using cached grpcio-1.73.0-cp313-cp313-macosx_11_0_universal2.whl (10.6 MB)
Downloading grpcio_tools-1.71.0-cp313-cp313-macosx_10_14_universal2.whl (6.0 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 6.0/6.0 MB 54.9 MB/s eta 0:00:00
Downloading simsimd-6.4.9-cp313-cp313-macosx_11_0_arm64.whl (132 kB)
Downloading stringzilla-3.12.5-cp313-cp313-macosx_11_0_arm64.whl (79 kB)
Using cached threadpoolctl-3.6.0-py3-none-any.whl (18 kB)
Using cached torchvision-0.22.1-cp313-cp313-macosx_11_0_arm64.whl (1.9 MB)
Using cached unique_names_generator-1.0.2-py2.py3-none-any.whl (27 kB)
Using cached weaviate_client-4.4b6-py3-none-any.whl (249 kB)
Using cached authlib-1.6.0-py2.py3-none-any.whl (239 kB)
Downloading grpcio_health_checking-1.71.0-py3-none-any.whl (18 kB)
Using cached validators-0.35.0-py3-none-any.whl (44 kB)
Using cached zipp-3.23.0-py3-none-any.whl (10 kB)
Using cached beautifulsoup4-4.13.4-py3-none-any.whl (187 kB)
Using cached soupsieve-2.7-py3-none-any.whl (36 kB)
Using cached coloredlogs-15.0.1-py2.py3-none-any.whl (46 kB)
Using cached humanfriendly-10.0-py2.py3-none-any.whl (86 kB)
Using cached filetype-1.2.0-py2.py3-none-any.whl (19 kB)
Using cached flatbuffers-25.2.10-py2.py3-none-any.whl (30 kB)
Downloading google_auth_oauthlib-1.2.2-py3-none-any.whl (19 kB)
Downloading requests_oauthlib-2.0.0-py2.py3-none-any.whl (24 kB)
Downloading oauthlib-3.3.1-py3-none-any.whl (160 kB)
Downloading google_cloud_storage-3.1.1-py3-none-any.whl (175 kB)
Downloading google_api_core-2.25.1-py3-none-any.whl (160 kB)
Downloading google_cloud_core-2.4.3-py2.py3-none-any.whl (29 kB)
Downloading google_crc32c-1.7.1-cp313-cp313-macosx_12_0_arm64.whl (30 kB)
Using cached google_resumable_media-2.7.2-py2.py3-none-any.whl (81 kB)
Using cached googleapis_common_protos-1.70.0-py3-none-any.whl (294 kB)
Downloading proto_plus-1.26.1-py3-none-any.whl (50 kB)
Downloading mako-1.3.10-py3-none-any.whl (78 kB)
Downloading requests_toolbelt-1.0.0-py2.py3-none-any.whl (54 kB)
Downloading PySocks-1.7.1-py3-none-any.whl (16 kB)
Building wheels for collected packages: pyarrow
  Building wheel for pyarrow (pyproject.toml): started
  Building wheel for pyarrow (pyproject.toml): finished with status 'error'
Failed to build pyarrow
```

## Command: `python -m cli ingest s3://my-bucket/WorldCupPlayers.csv`

**Source:** README.md - S3 Usage
**Exit Code:** 1

**Error Output:**
```
17:01:20 | INFO     | 🚀 Starting DreamBolt ingestion: s3://my-bucket/WorldCupPlayers.csv
17:01:20 | INFO     | Loading data from: s3://my-bucket/WorldCupPlayers.csv
17:01:20 | ERROR    | ❌ Pipeline failed: S3 support temporarily disabled. Use local files.
```

**Standard Output:**
```
⠋ Loading and analyzing data...
Error: S3 support temporarily disabled. Use local files.
```

## Command: `python -m cli ingest s3://my-bucket/data.parquet --embed text-embedding-ada-002`

**Source:** README.md - S3 Usage
**Exit Code:** 1

**Error Output:**
```
17:01:20 | INFO     | 🚀 Starting DreamBolt ingestion: s3://my-bucket/data.parquet
17:01:20 | INFO     | Loading data from: s3://my-bucket/data.parquet
17:01:20 | ERROR    | ❌ Pipeline failed: S3 support temporarily disabled. Use local files.
```

**Standard Output:**
```
⠋ Loading and analyzing data...
Error: S3 support temporarily disabled. Use local files.
```

## Command: `python -m cli ingest s3://my-bucket/data.parquet --table my_table --database analytics`

**Source:** README.md - S3 Usage
**Exit Code:** 2

**Error Output:**
```
Usage: cli.py ingest [OPTIONS] PATH
Try 'cli.py ingest --help' for help.
╭─ Error ──────────────────────────────────────────────────────────────────────────────────────────────────╮
│ No such option: --database Did you mean --table?                                                         │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## Command: `python -c "from synth import ModelConfig; print(ModelConfig.SUPPORTED_MODELS)"`

**Source:** README.md - Troubleshooting
**Exit Code:** 1

**Error Output:**
```
2025-06-20 17:01:21.669 | INFO     | synth:<module>:18 - DataDreamer not available - synthesis features will use fallback
Error in sys.excepthook:
Traceback (most recent call last):
  File "/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/trio/_core/_multierror.py", line 447, in trio_excepthook
    for chunk in traceback.format_exception(etype, value, tb):
  File "/opt/homebrew/Cellar/python@3.13/3.13.5/Frameworks/Python.framework/Versions/3.13/lib/python3.13/traceback.py", line 155, in format_exception
    return list(te.format(chain=chain, colorize=colorize))
TypeError: traceback_exception_format() got an unexpected keyword argument 'colorize'

Original exception was:
Traceback (most recent call last):
  File "<string>", line 1, in <module>
  File "/Users/tosh/Desktop/Dreambolt/synth.py", line 39, in <module>
    import openai
  File "/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/openai/__init__.py", line 9, in <module>
    from . import types
  File "/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/openai/types/__init__.py", line 5, in <module>
    from .batch import Batch as Batch
  File "/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/openai/types/batch.py", line 6, in <module>
    from .._models import BaseModel
  File "/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/openai/_models.py", line 25, in <module>
    from ._types import (
  File "/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/openai/_types.py", line 21, in <module>
    import httpx
  File "/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/httpx/__init__.py", line 2, in <module>
    from ._api import delete, get, head, options, patch, post, put, request, stream
  File "/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/httpx/_api.py", line 4, in <module>
    from ._client import Client
  File "/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/httpx/_client.py", line 30, in <module>
    from ._transports.default import AsyncHTTPTransport, HTTPTransport
  File "/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/httpx/_transports/default.py", line 30, in <module>
    import httpcore
  File "/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/httpcore/__init__.py", line 1, in <module>
    from ._api import request, stream
  File "/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/httpcore/_api.py", line 5, in <module>
    from ._sync.connection_pool import ConnectionPool
  File "/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/httpcore/_sync/__init__.py", line 1, in <module>
    from .connection import HTTPConnection
  File "/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/httpcore/_sync/connection.py", line 12, in <module>
    from .._synchronization import Lock
  File "/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/httpcore/_synchronization.py", line 13, in <module>
    import trio
  File "/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/trio/__init__.py", line 71, in <module>
    from ._path import Path
  File "/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/trio/_path.py", line 134, in <module>
    class Path(metaclass=AsyncAutoWrapperType):
  File "/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/trio/_path.py", line 85, in __init__
    type(cls).generate_forwards(cls, attrs)
  File "/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/trio/_path.py", line 102, in generate_forwards
    raise TypeError(attr_name, type(attr))
TypeError: ('parser', <class 'module'>)
```

## Command: `python ingest.py`

**Source:** README.md - Development Setup
**Exit Code:** 1

**Error Output:**
```
Error in sys.excepthook:
Traceback (most recent call last):
  File "/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/trio/_core/_multierror.py", line 447, in trio_excepthook
    for chunk in traceback.format_exception(etype, value, tb):
  File "/opt/homebrew/Cellar/python@3.13/3.13.5/Frameworks/Python.framework/Versions/3.13/lib/python3.13/traceback.py", line 155, in format_exception
    return list(te.format(chain=chain, colorize=colorize))
TypeError: traceback_exception_format() got an unexpected keyword argument 'colorize'

Original exception was:
Traceback (most recent call last):
  File "/Users/tosh/Desktop/Dreambolt/ingest.py", line 13, in <module>
    from src.utils.s3_client import (
  File "/Users/tosh/Desktop/Dreambolt/src/utils/s3_client.py", line 7, in <module>
    import s3fs
  File "/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/s3fs/__init__.py", line 1, in <module>
    from .core import S3FileSystem, S3File
  File "/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/s3fs/core.py", line 30, in <module>
    import aiobotocore.session
  File "/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/aiobotocore/session.py", line 11, in <module>
    from .client import AioBaseClient, AioClientCreator
  File "/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/aiobotocore/client.py", line 20, in <module>
    from .args import AioClientArgsCreator
  File "/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/aiobotocore/args.py", line 7, in <module>
    from .config import AioConfig
  File "/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/aiobotocore/config.py", line 6, in <module>
    from aiobotocore.endpoint import DEFAULT_HTTP_SESSION_CLS
  File "/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/aiobotocore/endpoint.py", line 17, in <module>
    from aiobotocore.httpchecksum import handle_checksum_body
  File "/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/aiobotocore/httpchecksum.py", line 19, in <module>
    import httpx
  File "/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/httpx/__init__.py", line 2, in <module>
    from ._api import delete, get, head, options, patch, post, put, request, stream
  File "/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/httpx/_api.py", line 4, in <module>
    from ._client import Client
  File "/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/httpx/_client.py", line 30, in <module>
    from ._transports.default import AsyncHTTPTransport, HTTPTransport
  File "/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/httpx/_transports/default.py", line 30, in <module>
    import httpcore
  File "/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/httpcore/__init__.py", line 1, in <module>
    from ._api import request, stream
  File "/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/httpcore/_api.py", line 5, in <module>
    from ._sync.connection_pool import ConnectionPool
  File "/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/httpcore/_sync/__init__.py", line 1, in <module>
    from .connection import HTTPConnection
  File "/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/httpcore/_sync/connection.py", line 12, in <module>
    from .._synchronization import Lock
  File "/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/httpcore/_synchronization.py", line 13, in <module>
    import trio
  File "/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/trio/__init__.py", line 71, in <module>
    from ._path import Path
  File "/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/trio/_path.py", line 134, in <module>
    class Path(metaclass=AsyncAutoWrapperType):
  File "/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/trio/_path.py", line 85, in __init__
    type(cls).generate_forwards(cls, attrs)
  File "/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/trio/_path.py", line 102, in generate_forwards
    raise TypeError(attr_name, type(attr))
TypeError: ('parser', <class 'module'>)
```

## Command: `python synth.py`

**Source:** README.md - Development Setup
**Exit Code:** 1

**Error Output:**
```
2025-06-20 17:01:24.686 | INFO     | __main__:<module>:18 - DataDreamer not available - synthesis features will use fallback
Error in sys.excepthook:
Traceback (most recent call last):
  File "/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/trio/_core/_multierror.py", line 447, in trio_excepthook
    for chunk in traceback.format_exception(etype, value, tb):
  File "/opt/homebrew/Cellar/python@3.13/3.13.5/Frameworks/Python.framework/Versions/3.13/lib/python3.13/traceback.py", line 155, in format_exception
    return list(te.format(chain=chain, colorize=colorize))
TypeError: traceback_exception_format() got an unexpected keyword argument 'colorize'

Original exception was:
Traceback (most recent call last):
  File "/Users/tosh/Desktop/Dreambolt/synth.py", line 39, in <module>
    import openai
  File "/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/openai/__init__.py", line 9, in <module>
    from . import types
  File "/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/openai/types/__init__.py", line 5, in <module>
    from .batch import Batch as Batch
  File "/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/openai/types/batch.py", line 6, in <module>
    from .._models import BaseModel
  File "/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/openai/_models.py", line 25, in <module>
    from ._types import (
  File "/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/openai/_types.py", line 21, in <module>
    import httpx
  File "/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/httpx/__init__.py", line 2, in <module>
    from ._api import delete, get, head, options, patch, post, put, request, stream
  File "/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/httpx/_api.py", line 4, in <module>
    from ._client import Client
  File "/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/httpx/_client.py", line 30, in <module>
    from ._transports.default import AsyncHTTPTransport, HTTPTransport
  File "/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/httpx/_transports/default.py", line 30, in <module>
    import httpcore
  File "/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/httpcore/__init__.py", line 1, in <module>
    from ._api import request, stream
  File "/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/httpcore/_api.py", line 5, in <module>
    from ._sync.connection_pool import ConnectionPool
  File "/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/httpcore/_sync/__init__.py", line 1, in <module>
    from .connection import HTTPConnection
  File "/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/httpcore/_sync/connection.py", line 12, in <module>
    from .._synchronization import Lock
  File "/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/httpcore/_synchronization.py", line 13, in <module>
    import trio
  File "/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/trio/__init__.py", line 71, in <module>
    from ._path import Path
  File "/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/trio/_path.py", line 134, in <module>
    class Path(metaclass=AsyncAutoWrapperType):
  File "/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/trio/_path.py", line 85, in __init__
    type(cls).generate_forwards(cls, attrs)
  File "/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/trio/_path.py", line 102, in generate_forwards
    raise TypeError(attr_name, type(attr))
TypeError: ('parser', <class 'module'>)
```

## Command: `python firebolt_io.py`

**Source:** README.md - Development Setup
**Exit Code:** 1

**Error Output:**
```
Error in sys.excepthook:
Traceback (most recent call last):
  File "/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/trio/_core/_multierror.py", line 447, in trio_excepthook
    for chunk in traceback.format_exception(etype, value, tb):
  File "/opt/homebrew/Cellar/python@3.13/3.13.5/Frameworks/Python.framework/Versions/3.13/lib/python3.13/traceback.py", line 155, in format_exception
    return list(te.format(chain=chain, colorize=colorize))
TypeError: traceback_exception_format() got an unexpected keyword argument 'colorize'

Original exception was:
Traceback (most recent call last):
  File "/Users/tosh/Desktop/Dreambolt/firebolt_io.py", line 14, in <module>
    firebolt_db = importlib.import_module('firebolt.db')
  File "/opt/homebrew/Cellar/python@3.13/3.13.5/Frameworks/Python.framework/Versions/3.13/lib/python3.13/importlib/__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 1026, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/firebolt/db/__init__.py", line 1, in <module>
    from firebolt.common._types import (
  File "/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/firebolt/common/__init__.py", line 1, in <module>
    from firebolt.common.settings import Settings
  File "/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/firebolt/common/settings.py", line 6, in <module>
    from firebolt.client.auth import Auth, UsernamePassword
  File "/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/firebolt/client/__init__.py", line 1, in <module>
    from firebolt.client.auth import Auth  # backward compatibility
  File "/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/firebolt/client/auth/__init__.py", line 1, in <module>
    from firebolt.client.auth.base import Auth
  File "/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/firebolt/client/auth/base.py", line 4, in <module>
    from httpx import Auth as HttpxAuth
  File "/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/httpx/__init__.py", line 2, in <module>
    from ._api import delete, get, head, options, patch, post, put, request, stream
  File "/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/httpx/_api.py", line 4, in <module>
    from ._client import Client
  File "/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/httpx/_client.py", line 30, in <module>
    from ._transports.default import AsyncHTTPTransport, HTTPTransport
  File "/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/httpx/_transports/default.py", line 30, in <module>
    import httpcore
  File "/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/httpcore/__init__.py", line 1, in <module>
    from ._api import request, stream
  File "/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/httpcore/_api.py", line 5, in <module>
    from ._sync.connection_pool import ConnectionPool
  File "/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/httpcore/_sync/__init__.py", line 1, in <module>
    from .connection import HTTPConnection
  File "/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/httpcore/_sync/connection.py", line 12, in <module>
    from .._synchronization import Lock
  File "/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/httpcore/_synchronization.py", line 13, in <module>
    import trio
  File "/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/trio/__init__.py", line 71, in <module>
    from ._path import Path
  File "/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/trio/_path.py", line 134, in <module>
    class Path(metaclass=AsyncAutoWrapperType):
  File "/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/trio/_path.py", line 85, in __init__
    type(cls).generate_forwards(cls, attrs)
  File "/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/trio/_path.py", line 102, in generate_forwards
    raise TypeError(attr_name, type(attr))
TypeError: ('parser', <class 'module'>)
```

## Command: `pytest --collect-only`

**Source:** testing.md - Test Suite Execution
**Exit Code:** 2

**Standard Output:**
```
============================= test session starts ==============================
platform darwin -- Python 3.13.5, pytest-8.4.1, pluggy-1.6.0
Using --randomly-seed=2744825905
rootdir: /Users/tosh/Desktop/Dreambolt
plugins: randomly-3.16.0, cov-5.0.0, anyio-4.9.0, mock-3.14.1
collected 80 items / 4 errors

<Dir Dreambolt>
  <Dir tests>
    <Module test_cli_examples.py>
      <Class TestCLIExamples>
        <Function test_golden_run_commands[golden_run1]>
        <Function test_status_command>
        <Function test_golden_run_commands[golden_run0]>
        <Function test_cli_regression_coverage>
        <Function test_help_commands_accessible>
        <Function test_ingest_command_basic>
        <Function test_cli_entry_point_exists>
    <Module test_cli_helper_functions.py>
      <Class TestCLIHelperFunctions>
        <Function test_generate_output_path[no_extension-no_extension.dreambolt.parquet]>
        <Function test_generate_output_path[file.CSV-file.dreambolt.parquet]>
        <Function test_derive_table_name[special!@#chars.csv-special!@#chars]>
        <Function test_generate_output_path[data.parquet-data.dreambolt.parquet]>
        <Function test_derive_table_name_extracts_basename>
        <Function test_generate_output_path_preserves_directory>
        <Function test_derive_table_name[data.csv-data]>
        <Function test_derive_table_name[UPPERCASE.CSV-uppercase]>
        <Function test_generate_output_path[/path/to/file.csv-/path/to/file.dreambolt.parquet]>
        <Function test_generate_output_path[data.csv-data.dreambolt.parquet]>
        <Function test_derive_table_name[/path/to/file.csv-file]>
        <Function test_derive_table_name[data-with-dashes.csv-data_with_dashes]>
        <Function test_generate_output_path[complex-file_name.csv-complex-file_name.dreambolt.parquet]>
        <Function test_derive_table_name[My Data File.csv-my data file]>
        <Function test_derive_table_name[file with spaces.parquet-file with spaces]>
        <Function test_derive_table_name[123numeric.csv-123numeric]>
    <Module test_s3_basic.py>
      <Function test_s3_uri_detection>
      <Function test_s3_error_handling_mock>
      <Function test_s3_client_initialization>
      <Function test_s3_integration_placeholder>
      <Function test_s3_unavailable_import_error>
    <Module test_cli_version_matrix.py>
      <Class TestPython313Specific>
        <Function test_python313_new_features>
        <Function test_python313_performance>
      <Class TestCLIVersionMatrix>
        <Function test_cli_command_exit_codes[command3]>
        <Function test_unicode_emoji_support>
        <Function test_cli_import>
        <Function test_cli_status_command>
        <Function test_no_deprecation_warnings>
        <Function test_cli_version_command>
        <Function test_typer_click_compatibility>
        <Function test_cli_command_exit_codes[command1]>
        <Function test_cli_ingest_dry_run>
        <Function test_cli_command_exit_codes[command2]>
        <Function test_python_version_compatibility>
        <Function test_cli_command_exit_codes[command0]>
        <Function test_cli_help_command>
    <Module test_cli_comprehensive.py>
      <Class TestArgparseCLI>
        <Function test_ingest_command_direct>
        <Function test_argparse_help>
        <Function test_status_command_direct>
      <Class TestCLIHelperFunctions>
        <Function test_derive_table_name[/path/to/file.csv-file]>
        <Function test_generate_output_path[/path/to/file.csv-/path/to/file.dreambolt.parquet]>
        <Function test_generate_output_path[no_extension-no_extension.dreambolt.parquet]>
        <Function test_generate_output_path[data.parquet-data.dreambolt.parquet]>
        <Function test_derive_table_name[UPPERCASE.CSV-uppercase]>
        <Function test_derive_table_name_argparse>
        <Function test_derive_table_name[data-with-dashes.csv-data_with_dashes]>
        <Function test_derive_table_name[data.csv-data]>
        <Function test_derive_table_name[My Data File.csv-my_data_file]>
        <Function test_generate_output_path_argparse>
        <Function test_generate_output_path[data.csv-data.dreambolt.parquet]>
      <Class TestCLIErrorHandling>
        <Function test_large_file_timeout>
        <Function test_permission_error>
        <Function test_invalid_file_extension>
        <Function test_network_error_handling>
      <Class TestCLIEnvironmentVariables>
        <Function test_cli_with_all_env_vars>
        <Function test_cli_without_env_vars>
      <Class TestCLIIntegration>
        <Function test_cli_ingest_integration>
        <Function test_cli_module_entry_point>
        <Function test_cli_status_integration>
      <Class TestCLIPerformance>
        <Function test_cli_startup_time>
        <Function test_large_dataset_processing>
      <Class TestCLICommands>
        <Function test_ingest_command_basic>
        <Function test_status_command>
        <Function test_cli_help>
    <Module test_ingest.py>
      <Function test_cli_help>
      <Function test_ingest_help>
      <Class TestBasicIngest>
        <Function test_ingest_csv_no_synth>
        <Function test_ingest_s3_uri>
        <Function test_ingest_parquet_no_synth>
      <Class TestSynthesisIntegration>
        <Function test_ingest_with_synthesis>
        <Function test_ingest_with_embeddings>
      <Class TestErrorHandling>
        <Function test_firebolt_connection_failure>
        <Function test_invalid_file_path>

==================================== ERRORS ====================================
____________ ERROR collecting tests/test_firebolt_comprehensive.py _____________
tests/test_firebolt_comprehensive.py:11: in <module>
    from firebolt_io import FireboltConnector, FireboltConfig
firebolt_io.py:14: in <module>
    firebolt_db = importlib.import_module('firebolt.db')
                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/opt/homebrew/Cellar/python@3.13/3.13.5/Frameworks/Python.framework/Versions/3.13/lib/python3.13/importlib/__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.audit-env/lib/python3.13/site-packages/firebolt/db/__init__.py:1: in <module>
    from firebolt.common._types import (
.audit-env/lib/python3.13/site-packages/firebolt/common/__init__.py:1: in <module>
    from firebolt.common.settings import Settings
.audit-env/lib/python3.13/site-packages/firebolt/common/settings.py:6: in <module>
    from firebolt.client.auth import Auth, UsernamePassword
.audit-env/lib/python3.13/site-packages/firebolt/client/__init__.py:1: in <module>
    from firebolt.client.auth import Auth  # backward compatibility
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.audit-env/lib/python3.13/site-packages/firebolt/client/auth/__init__.py:1: in <module>
    from firebolt.client.auth.base import Auth
.audit-env/lib/python3.13/site-packages/firebolt/client/auth/base.py:4: in <module>
    from httpx import Auth as HttpxAuth
.audit-env/lib/python3.13/site-packages/httpx/__init__.py:2: in <module>
    from ._api import delete, get, head, options, patch, post, put, request, stream
.audit-env/lib/python3.13/site-packages/httpx/_api.py:4: in <module>
    from ._client import Client
.audit-env/lib/python3.13/site-packages/httpx/_client.py:30: in <module>
    from ._transports.default import AsyncHTTPTransport, HTTPTransport
.audit-env/lib/python3.13/site-packages/httpx/_transports/default.py:30: in <module>
    import httpcore
.audit-env/lib/python3.13/site-packages/httpcore/__init__.py:1: in <module>
    from ._api import request, stream
.audit-env/lib/python3.13/site-packages/httpcore/_api.py:5: in <module>
    from ._sync.connection_pool import ConnectionPool
.audit-env/lib/python3.13/site-packages/httpcore/_sync/__init__.py:1: in <module>
    from .connection import HTTPConnection
.audit-env/lib/python3.13/site-packages/httpcore/_sync/connection.py:12: in <module>
    from .._synchronization import Lock
.audit-env/lib/python3.13/site-packages/httpcore/_synchronization.py:13: in <module>
    import trio
.audit-env/lib/python3.13/site-packages/trio/__init__.py:71: in <module>
    from ._path import Path
.audit-env/lib/python3.13/site-packages/trio/_path.py:134: in <module>
    class Path(metaclass=AsyncAutoWrapperType):
.audit-env/lib/python3.13/site-packages/trio/_path.py:85: in __init__
    type(cls).generate_forwards(cls, attrs)
.audit-env/lib/python3.13/site-packages/trio/_path.py:102: in generate_forwards
    raise TypeError(attr_name, type(attr))
E   TypeError: ('parser', <class 'module'>)
_____________ ERROR collecting tests/test_ingest_comprehensive.py ______________
tests/test_ingest_comprehensive.py:13: in <module>
    from ingest import DataIngester, SchemaInfo
ingest.py:13: in <module>
    from src.utils.s3_client import (
src/utils/s3_client.py:7: in <module>
    import s3fs
.audit-env/lib/python3.13/site-packages/s3fs/__init__.py:1: in <module>
    from .core import S3FileSystem, S3File
.audit-env/lib/python3.13/site-packages/s3fs/core.py:30: in <module>
    import aiobotocore.session
.audit-env/lib/python3.13/site-packages/aiobotocore/session.py:11: in <module>
    from .client import AioBaseClient, AioClientCreator
.audit-env/lib/python3.13/site-packages/aiobotocore/client.py:20: in <module>
    from .args import AioClientArgsCreator
.audit-env/lib/python3.13/site-packages/aiobotocore/args.py:7: in <module>
    from .config import AioConfig
.audit-env/lib/python3.13/site-packages/aiobotocore/config.py:6: in <module>
    from aiobotocore.endpoint import DEFAULT_HTTP_SESSION_CLS
.audit-env/lib/python3.13/site-packages/aiobotocore/endpoint.py:17: in <module>
    from aiobotocore.httpchecksum import handle_checksum_body
.audit-env/lib/python3.13/site-packages/aiobotocore/httpchecksum.py:19: in <module>
    import httpx
.audit-env/lib/python3.13/site-packages/httpx/__init__.py:2: in <module>
    from ._api import delete, get, head, options, patch, post, put, request, stream
.audit-env/lib/python3.13/site-packages/httpx/_api.py:4: in <module>
    from ._client import Client
.audit-env/lib/python3.13/site-packages/httpx/_client.py:30: in <module>
    from ._transports.default import AsyncHTTPTransport, HTTPTransport
.audit-env/lib/python3.13/site-packages/httpx/_transports/default.py:30: in <module>
    import httpcore
.audit-env/lib/python3.13/site-packages/httpcore/__init__.py:1: in <module>
    from ._api import request, stream
.audit-env/lib/python3.13/site-packages/httpcore/_api.py:5: in <module>
    from ._sync.connection_pool import ConnectionPool
.audit-env/lib/python3.13/site-packages/httpcore/_sync/__init__.py:1: in <module>
    from .connection import HTTPConnection
.audit-env/lib/python3.13/site-packages/httpcore/_sync/connection.py:12: in <module>
    from .._synchronization import Lock
.audit-env/lib/python3.13/site-packages/httpcore/_synchronization.py:13: in <module>
    import trio
.audit-env/lib/python3.13/site-packages/trio/__init__.py:71: in <module>
    from ._path import Path
.audit-env/lib/python3.13/site-packages/trio/_path.py:134: in <module>
    class Path(metaclass=AsyncAutoWrapperType):
.audit-env/lib/python3.13/site-packages/trio/_path.py:85: in __init__
    type(cls).generate_forwards(cls, attrs)
.audit-env/lib/python3.13/site-packages/trio/_path.py:102: in generate_forwards
    raise TypeError(attr_name, type(attr))
E   TypeError: ('parser', <class 'module'>)
_______________ ERROR collecting tests/test_s3_comprehensive.py ________________
ImportError while importing test module '/Users/tosh/Desktop/Dreambolt/tests/test_s3_comprehensive.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/opt/homebrew/Cellar/python@3.13/3.13.5/Frameworks/Python.framework/Versions/3.13/lib/python3.13/importlib/__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
tests/test_s3_comprehensive.py:14: in <module>
    from moto import mock_s3
E   ImportError: cannot import name 'mock_s3' from 'moto' (/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/moto/__init__.py). Did you mean: 'mock_aws'?
____________ ERROR collecting tests/test_synthesis_comprehensive.py ____________
tests/test_synthesis_comprehensive.py:12: in <module>
    from synth import DataSynthesizer, ModelConfig
synth.py:39: in <module>
    import openai
.audit-env/lib/python3.13/site-packages/openai/__init__.py:9: in <module>
    from . import types
.audit-env/lib/python3.13/site-packages/openai/types/__init__.py:5: in <module>
    from .batch import Batch as Batch
.audit-env/lib/python3.13/site-packages/openai/types/batch.py:6: in <module>
    from .._models import BaseModel
.audit-env/lib/python3.13/site-packages/openai/_models.py:25: in <module>
    from ._types import (
.audit-env/lib/python3.13/site-packages/openai/_types.py:21: in <module>
    import httpx
.audit-env/lib/python3.13/site-packages/httpx/__init__.py:2: in <module>
    from ._api import delete, get, head, options, patch, post, put, request, stream
.audit-env/lib/python3.13/site-packages/httpx/_api.py:4: in <module>
    from ._client import Client
.audit-env/lib/python3.13/site-packages/httpx/_client.py:30: in <module>
    from ._transports.default import AsyncHTTPTransport, HTTPTransport
.audit-env/lib/python3.13/site-packages/httpx/_transports/default.py:30: in <module>
    import httpcore
.audit-env/lib/python3.13/site-packages/httpcore/__init__.py:1: in <module>
    from ._api import request, stream
.audit-env/lib/python3.13/site-packages/httpcore/_api.py:5: in <module>
    from ._sync.connection_pool import ConnectionPool
.audit-env/lib/python3.13/site-packages/httpcore/_sync/__init__.py:1: in <module>
    from .connection import HTTPConnection
.audit-env/lib/python3.13/site-packages/httpcore/_sync/connection.py:12: in <module>
    from .._synchronization import Lock
.audit-env/lib/python3.13/site-packages/httpcore/_synchronization.py:13: in <module>
    import trio
.audit-env/lib/python3.13/site-packages/trio/__init__.py:71: in <module>
    from ._path import Path
.audit-env/lib/python3.13/site-packages/trio/_path.py:134: in <module>
    class Path(metaclass=AsyncAutoWrapperType):
.audit-env/lib/python3.13/site-packages/trio/_path.py:85: in __init__
    type(cls).generate_forwards(cls, attrs)
.audit-env/lib/python3.13/site-packages/trio/_path.py:102: in generate_forwards
    raise TypeError(attr_name, type(attr))
E   TypeError: ('parser', <class 'module'>)
------------------------------- Captured stderr --------------------------------
17:01:27 | INFO     | DataDreamer not available - synthesis features will use fallback
=============================== warnings summary ===============================
.audit-env/lib/python3.13/site-packages/pydantic/_internal/_config.py:323
  /Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/pydantic/_internal/_config.py:323: PydanticDeprecatedSince20: Support for class-based `config` is deprecated, use ConfigDict instead. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.11/migration/
    warnings.warn(DEPRECATION_MESSAGE, DeprecationWarning)

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=========================== short test summary info ============================
ERROR tests/test_firebolt_comprehensive.py - TypeError: ('parser', <class 'mo...
ERROR tests/test_ingest_comprehensive.py - TypeError: ('parser', <class 'modu...
ERROR tests/test_s3_comprehensive.py
ERROR tests/test_synthesis_comprehensive.py - TypeError: ('parser', <class 'm...
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
==================== 80 tests collected, 4 errors in 0.67s =====================
```

## Command: `pytest --cov=. --cov-report=term-missing`

**Source:** testing.md - Test Suite Execution
**Exit Code:** 2

**Standard Output:**
```
============================= test session starts ==============================
platform darwin -- Python 3.13.5, pytest-8.4.1, pluggy-1.6.0
Using --randomly-seed=4123217884
rootdir: /Users/tosh/Desktop/Dreambolt
plugins: randomly-3.16.0, cov-5.0.0, anyio-4.9.0, mock-3.14.1
collected 80 items / 4 errors

==================================== ERRORS ====================================
____________ ERROR collecting tests/test_firebolt_comprehensive.py _____________
tests/test_firebolt_comprehensive.py:11: in <module>
    from firebolt_io import FireboltConnector, FireboltConfig
firebolt_io.py:14: in <module>
    firebolt_db = importlib.import_module('firebolt.db')
                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/opt/homebrew/Cellar/python@3.13/3.13.5/Frameworks/Python.framework/Versions/3.13/lib/python3.13/importlib/__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.audit-env/lib/python3.13/site-packages/firebolt/db/__init__.py:1: in <module>
    from firebolt.common._types import (
.audit-env/lib/python3.13/site-packages/firebolt/common/__init__.py:1: in <module>
    from firebolt.common.settings import Settings
.audit-env/lib/python3.13/site-packages/firebolt/common/settings.py:6: in <module>
    from firebolt.client.auth import Auth, UsernamePassword
.audit-env/lib/python3.13/site-packages/firebolt/client/__init__.py:1: in <module>
    from firebolt.client.auth import Auth  # backward compatibility
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.audit-env/lib/python3.13/site-packages/firebolt/client/auth/__init__.py:1: in <module>
    from firebolt.client.auth.base import Auth
.audit-env/lib/python3.13/site-packages/firebolt/client/auth/base.py:4: in <module>
    from httpx import Auth as HttpxAuth
.audit-env/lib/python3.13/site-packages/httpx/__init__.py:2: in <module>
    from ._api import delete, get, head, options, patch, post, put, request, stream
.audit-env/lib/python3.13/site-packages/httpx/_api.py:4: in <module>
    from ._client import Client
.audit-env/lib/python3.13/site-packages/httpx/_client.py:30: in <module>
    from ._transports.default import AsyncHTTPTransport, HTTPTransport
.audit-env/lib/python3.13/site-packages/httpx/_transports/default.py:30: in <module>
    import httpcore
.audit-env/lib/python3.13/site-packages/httpcore/__init__.py:1: in <module>
    from ._api import request, stream
.audit-env/lib/python3.13/site-packages/httpcore/_api.py:5: in <module>
    from ._sync.connection_pool import ConnectionPool
.audit-env/lib/python3.13/site-packages/httpcore/_sync/__init__.py:1: in <module>
    from .connection import HTTPConnection
.audit-env/lib/python3.13/site-packages/httpcore/_sync/connection.py:12: in <module>
    from .._synchronization import Lock
.audit-env/lib/python3.13/site-packages/httpcore/_synchronization.py:13: in <module>
    import trio
.audit-env/lib/python3.13/site-packages/trio/__init__.py:71: in <module>
    from ._path import Path
.audit-env/lib/python3.13/site-packages/trio/_path.py:134: in <module>
    class Path(metaclass=AsyncAutoWrapperType):
.audit-env/lib/python3.13/site-packages/trio/_path.py:85: in __init__
    type(cls).generate_forwards(cls, attrs)
.audit-env/lib/python3.13/site-packages/trio/_path.py:102: in generate_forwards
    raise TypeError(attr_name, type(attr))
E   TypeError: ('parser', <class 'module'>)
_____________ ERROR collecting tests/test_ingest_comprehensive.py ______________
tests/test_ingest_comprehensive.py:13: in <module>
    from ingest import DataIngester, SchemaInfo
ingest.py:13: in <module>
    from src.utils.s3_client import (
src/utils/s3_client.py:7: in <module>
    import s3fs
.audit-env/lib/python3.13/site-packages/s3fs/__init__.py:1: in <module>
    from .core import S3FileSystem, S3File
.audit-env/lib/python3.13/site-packages/s3fs/core.py:30: in <module>
    import aiobotocore.session
.audit-env/lib/python3.13/site-packages/aiobotocore/session.py:11: in <module>
    from .client import AioBaseClient, AioClientCreator
.audit-env/lib/python3.13/site-packages/aiobotocore/client.py:20: in <module>
    from .args import AioClientArgsCreator
.audit-env/lib/python3.13/site-packages/aiobotocore/args.py:7: in <module>
    from .config import AioConfig
.audit-env/lib/python3.13/site-packages/aiobotocore/config.py:6: in <module>
    from aiobotocore.endpoint import DEFAULT_HTTP_SESSION_CLS
.audit-env/lib/python3.13/site-packages/aiobotocore/endpoint.py:17: in <module>
    from aiobotocore.httpchecksum import handle_checksum_body
.audit-env/lib/python3.13/site-packages/aiobotocore/httpchecksum.py:19: in <module>
    import httpx
.audit-env/lib/python3.13/site-packages/httpx/__init__.py:2: in <module>
    from ._api import delete, get, head, options, patch, post, put, request, stream
.audit-env/lib/python3.13/site-packages/httpx/_api.py:4: in <module>
    from ._client import Client
.audit-env/lib/python3.13/site-packages/httpx/_client.py:30: in <module>
    from ._transports.default import AsyncHTTPTransport, HTTPTransport
.audit-env/lib/python3.13/site-packages/httpx/_transports/default.py:30: in <module>
    import httpcore
.audit-env/lib/python3.13/site-packages/httpcore/__init__.py:1: in <module>
    from ._api import request, stream
.audit-env/lib/python3.13/site-packages/httpcore/_api.py:5: in <module>
    from ._sync.connection_pool import ConnectionPool
.audit-env/lib/python3.13/site-packages/httpcore/_sync/__init__.py:1: in <module>
    from .connection import HTTPConnection
.audit-env/lib/python3.13/site-packages/httpcore/_sync/connection.py:12: in <module>
    from .._synchronization import Lock
.audit-env/lib/python3.13/site-packages/httpcore/_synchronization.py:13: in <module>
    import trio
.audit-env/lib/python3.13/site-packages/trio/__init__.py:71: in <module>
    from ._path import Path
.audit-env/lib/python3.13/site-packages/trio/_path.py:134: in <module>
    class Path(metaclass=AsyncAutoWrapperType):
.audit-env/lib/python3.13/site-packages/trio/_path.py:85: in __init__
    type(cls).generate_forwards(cls, attrs)
.audit-env/lib/python3.13/site-packages/trio/_path.py:102: in generate_forwards
    raise TypeError(attr_name, type(attr))
E   TypeError: ('parser', <class 'module'>)
_______________ ERROR collecting tests/test_s3_comprehensive.py ________________
ImportError while importing test module '/Users/tosh/Desktop/Dreambolt/tests/test_s3_comprehensive.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/opt/homebrew/Cellar/python@3.13/3.13.5/Frameworks/Python.framework/Versions/3.13/lib/python3.13/importlib/__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
tests/test_s3_comprehensive.py:14: in <module>
    from moto import mock_s3
E   ImportError: cannot import name 'mock_s3' from 'moto' (/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/moto/__init__.py). Did you mean: 'mock_aws'?
____________ ERROR collecting tests/test_synthesis_comprehensive.py ____________
tests/test_synthesis_comprehensive.py:12: in <module>
    from synth import DataSynthesizer, ModelConfig
synth.py:39: in <module>
    import openai
.audit-env/lib/python3.13/site-packages/openai/__init__.py:9: in <module>
    from . import types
.audit-env/lib/python3.13/site-packages/openai/types/__init__.py:5: in <module>
    from .batch import Batch as Batch
.audit-env/lib/python3.13/site-packages/openai/types/batch.py:6: in <module>
    from .._models import BaseModel
.audit-env/lib/python3.13/site-packages/openai/_models.py:25: in <module>
    from ._types import (
.audit-env/lib/python3.13/site-packages/openai/_types.py:21: in <module>
    import httpx
.audit-env/lib/python3.13/site-packages/httpx/__init__.py:2: in <module>
    from ._api import delete, get, head, options, patch, post, put, request, stream
.audit-env/lib/python3.13/site-packages/httpx/_api.py:4: in <module>
    from ._client import Client
.audit-env/lib/python3.13/site-packages/httpx/_client.py:30: in <module>
    from ._transports.default import AsyncHTTPTransport, HTTPTransport
.audit-env/lib/python3.13/site-packages/httpx/_transports/default.py:30: in <module>
    import httpcore
.audit-env/lib/python3.13/site-packages/httpcore/__init__.py:1: in <module>
    from ._api import request, stream
.audit-env/lib/python3.13/site-packages/httpcore/_api.py:5: in <module>
    from ._sync.connection_pool import ConnectionPool
.audit-env/lib/python3.13/site-packages/httpcore/_sync/__init__.py:1: in <module>
    from .connection import HTTPConnection
.audit-env/lib/python3.13/site-packages/httpcore/_sync/connection.py:12: in <module>
    from .._synchronization import Lock
.audit-env/lib/python3.13/site-packages/httpcore/_synchronization.py:13: in <module>
    import trio
.audit-env/lib/python3.13/site-packages/trio/__init__.py:71: in <module>
    from ._path import Path
.audit-env/lib/python3.13/site-packages/trio/_path.py:134: in <module>
    class Path(metaclass=AsyncAutoWrapperType):
.audit-env/lib/python3.13/site-packages/trio/_path.py:85: in __init__
    type(cls).generate_forwards(cls, attrs)
.audit-env/lib/python3.13/site-packages/trio/_path.py:102: in generate_forwards
    raise TypeError(attr_name, type(attr))
E   TypeError: ('parser', <class 'module'>)
------------------------------- Captured stderr --------------------------------
17:01:29 | INFO     | DataDreamer not available - synthesis features will use fallback
=============================== warnings summary ===============================
.audit-env/lib/python3.13/site-packages/pydantic/_internal/_config.py:323
  /Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/pydantic/_internal/_config.py:323: PydanticDeprecatedSince20: Support for class-based `config` is deprecated, use ConfigDict instead. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.11/migration/
    warnings.warn(DEPRECATION_MESSAGE, DeprecationWarning)

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html

---------- coverage: platform darwin, python 3.13.5-final-0 ----------
Name                                    Stmts   Miss  Cover   Missing
---------------------------------------------------------------------
__main__.py                                 9      9     0%   9-20
cli.py                                    117     93    21%   100-167, 173-198, 203-222, 237, 242-246, 251-254, 259
cli_working.py                             95     83    13%   17-42, 47-97, 102-106, 111-113, 118-148, 152
firebolt_io.py                            244    235     4%   15-21, 23-463
firebolt_io_simple.py                      83     61    27%   15-22, 26, 40-48, 60-62, 74-76, 80-85, 99-103, 117-128, 135, 138, 145, 148, 151, 156-180
ingest.py                                 169    161     5%   23-24, 26-300
ingest_simple.py                          111     88    21%   29, 41-46, 50-69, 73-105, 125-149, 154-165, 169-188, 193-208
src/__init__.py                             0      0   100%
src/utils/__init__.py                       0      0   100%
src/utils/s3_client.py                    186    183     2%   8-373
synth.py                                  183    162    11%   14-16, 23, 25, 27, 31, 35, 40, 42-376
synth_simple.py                            73     59    19%   25-33, 47-49, 62-102, 115-136, 141-147, 152-173
test_command_executor.py                  132    118    11%   51-54, 63-85, 89-101, 105-247, 250-251
tests/conftest.py                         181    110    39%   25-38, 44, 50, 65, 79, 93-95, 109-111, 117-119, 125-127, 133-135, 141, 147, 153-171, 181-196, 202-213, 219-231, 237-248, 254-255, 262-276, 282-303, 309-311, 317-334, 340-352, 357-358
tests/test_cli_comprehensive.py           171    130    24%   27-29, 33-36, 40-54, 62-68, 72-79, 83-111, 119-125, 129-135, 139-153, 167-169, 180-182, 186-188, 192-194, 202-208, 213-224, 229-241, 245-254, 262-282, 286-308, 317-321, 326-343
tests/test_cli_examples.py                 62     44    29%   27-31, 35-40, 44-54, 59-77, 81-93, 104-123, 129-144, 153-154
tests/test_cli_helper_functions.py         19     10    47%   24-25, 39-40, 44-46, 50-52
tests/test_cli_version_matrix.py           92     67    27%   19-27, 31-40, 44-55, 59-67, 72-93, 97-100, 104-122, 126-136, 140-148, 158-166, 176-189, 194-209, 214
tests/test_firebolt_comprehensive.py      262    258     2%   12-463
tests/test_ingest.py                       74     44    41%   17, 27-30, 35-36, 44-69, 73-90, 96, 105-121, 127, 135-141, 147, 153-158, 162-167, 172
tests/test_ingest_comprehensive.py        208    202     3%   14-385
tests/test_s3_basic.py                     53     44    17%   10-19, 24-34, 39-47, 55, 60-79, 84-98
tests/test_s3_comprehensive.py             87     79     9%   17-173
tests/test_synthesis_comprehensive.py     282    277     2%   13-496
---------------------------------------------------------------------
TOTAL                                    2893   2517    13%

=========================== short test summary info ============================
ERROR tests/test_firebolt_comprehensive.py - TypeError: ('parser', <class 'mo...
ERROR tests/test_ingest_comprehensive.py - TypeError: ('parser', <class 'modu...
ERROR tests/test_s3_comprehensive.py
ERROR tests/test_synthesis_comprehensive.py - TypeError: ('parser', <class 'm...
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
========================= 1 warning, 4 errors in 1.14s =========================
```

## Command: `pytest tests/test_ingest.py::TestBasicIngest -v`

**Source:** testing.md - Test Suite Execution
**Exit Code:** 1

**Standard Output:**
```
============================= test session starts ==============================
platform darwin -- Python 3.13.5, pytest-8.4.1, pluggy-1.6.0 -- /Users/tosh/Desktop/Dreambolt/.audit-env/bin/python3.13
cachedir: .pytest_cache
Using --randomly-seed=475000815
rootdir: /Users/tosh/Desktop/Dreambolt
plugins: randomly-3.16.0, cov-5.0.0, anyio-4.9.0, mock-3.14.1
collecting ... collected 3 items

tests/test_ingest.py::TestBasicIngest::test_ingest_csv_no_synth FAILED   [ 33%]
tests/test_ingest.py::TestBasicIngest::test_ingest_s3_uri SKIPPED (S...) [ 66%]
tests/test_ingest.py::TestBasicIngest::test_ingest_parquet_no_synth FAILED [100%]

=================================== FAILURES ===================================
___________________ TestBasicIngest.test_ingest_csv_no_synth ___________________

self = <test_ingest.TestBasicIngest object at 0x110c9d590>
sample_csv_file = '/var/folders/z3/bjtrhnk91qqdx5ttwqn647200000gn/T/tmpqypjv7oo.csv'
temp_output_dir = '/var/folders/z3/bjtrhnk91qqdx5ttwqn647200000gn/T/tmpq91h4ih2'

    def test_ingest_csv_no_synth(self, sample_csv_file, temp_output_dir):
        """Test: dreambolt ingest sample.csv --no-synth"""
        output_path = Path(temp_output_dir) / "output.parquet"

        # Mock Firebolt operations for now
>       with patch('firebolt_io.ensure_table') as _mock_table, \
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
             patch('firebolt_io.copy_data') as _mock_copy:

tests/test_ingest.py:47:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
/opt/homebrew/Cellar/python@3.13/3.13.5/Frameworks/Python.framework/Versions/3.13/lib/python3.13/unittest/mock.py:1481: in __enter__
    self.target = self.getter()
                  ^^^^^^^^^^^^^
/opt/homebrew/Cellar/python@3.13/3.13.5/Frameworks/Python.framework/Versions/3.13/lib/python3.13/pkgutil.py:513: in resolve_name
    mod = importlib.import_module(modname)
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/opt/homebrew/Cellar/python@3.13/3.13.5/Frameworks/Python.framework/Versions/3.13/lib/python3.13/importlib/__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
<frozen importlib._bootstrap>:1387: in _gcd_import
    ???
<frozen importlib._bootstrap>:1360: in _find_and_load
    ???
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

name = 'firebolt_io', import_ = <function _gcd_import at 0x100bf04a0>

>   ???
E   ModuleNotFoundError: No module named 'firebolt_io'

<frozen importlib._bootstrap>:1324: ModuleNotFoundError
_________________ TestBasicIngest.test_ingest_parquet_no_synth _________________

self = <test_ingest.TestBasicIngest object at 0x110c9c410>
sample_csv_data =    id     name  age  salary
0   1    Alice   25   50000
1   2      Bob   30   60000
2   3  Charlie   35   70000
3   4    Diana   28   55000
4   5      Eve   32   65000
temp_output_dir = '/var/folders/z3/bjtrhnk91qqdx5ttwqn647200000gn/T/tmp7efd7nl_'

    def test_ingest_parquet_no_synth(self, sample_csv_data, temp_output_dir):
        """Test ingesting Parquet files."""
        input_path = Path(temp_output_dir) / "input.parquet"
        output_path = Path(temp_output_dir) / "output.parquet"

        # Create input Parquet file
        sample_csv_data.to_parquet(input_path)

>       with patch('firebolt_io.ensure_table') as _mock_table, \
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
             patch('firebolt_io.copy_data') as _mock_copy:

tests/test_ingest.py:79:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
/opt/homebrew/Cellar/python@3.13/3.13.5/Frameworks/Python.framework/Versions/3.13/lib/python3.13/unittest/mock.py:1481: in __enter__
    self.target = self.getter()
                  ^^^^^^^^^^^^^
/opt/homebrew/Cellar/python@3.13/3.13.5/Frameworks/Python.framework/Versions/3.13/lib/python3.13/pkgutil.py:513: in resolve_name
    mod = importlib.import_module(modname)
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/opt/homebrew/Cellar/python@3.13/3.13.5/Frameworks/Python.framework/Versions/3.13/lib/python3.13/importlib/__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
<frozen importlib._bootstrap>:1387: in _gcd_import
    ???
<frozen importlib._bootstrap>:1360: in _find_and_load
    ???
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

name = 'firebolt_io', import_ = <function _gcd_import at 0x100bf04a0>

>   ???
E   ModuleNotFoundError: No module named 'firebolt_io'

<frozen importlib._bootstrap>:1324: ModuleNotFoundError
=========================== short test summary info ============================
FAILED tests/test_ingest.py::TestBasicIngest::test_ingest_csv_no_synth - Modu...
FAILED tests/test_ingest.py::TestBasicIngest::test_ingest_parquet_no_synth - ...
========================= 2 failed, 1 skipped in 0.15s =========================
```

## Command: `pytest -m "not slow" -v`

**Source:** testing.md - Test Suite Execution
**Exit Code:** 2

**Standard Output:**
```
============================= test session starts ==============================
platform darwin -- Python 3.13.5, pytest-8.4.1, pluggy-1.6.0 -- /Users/tosh/Desktop/Dreambolt/.audit-env/bin/python3.13
cachedir: .pytest_cache
Using --randomly-seed=3225307083
rootdir: /Users/tosh/Desktop/Dreambolt
plugins: randomly-3.16.0, cov-5.0.0, anyio-4.9.0, mock-3.14.1
collecting ... collected 80 items / 4 errors / 4 deselected / 76 selected

==================================== ERRORS ====================================
____________ ERROR collecting tests/test_firebolt_comprehensive.py _____________
tests/test_firebolt_comprehensive.py:11: in <module>
    from firebolt_io import FireboltConnector, FireboltConfig
firebolt_io.py:14: in <module>
    firebolt_db = importlib.import_module('firebolt.db')
                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/opt/homebrew/Cellar/python@3.13/3.13.5/Frameworks/Python.framework/Versions/3.13/lib/python3.13/importlib/__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.audit-env/lib/python3.13/site-packages/firebolt/db/__init__.py:1: in <module>
    from firebolt.common._types import (
.audit-env/lib/python3.13/site-packages/firebolt/common/__init__.py:1: in <module>
    from firebolt.common.settings import Settings
.audit-env/lib/python3.13/site-packages/firebolt/common/settings.py:6: in <module>
    from firebolt.client.auth import Auth, UsernamePassword
.audit-env/lib/python3.13/site-packages/firebolt/client/__init__.py:1: in <module>
    from firebolt.client.auth import Auth  # backward compatibility
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.audit-env/lib/python3.13/site-packages/firebolt/client/auth/__init__.py:1: in <module>
    from firebolt.client.auth.base import Auth
.audit-env/lib/python3.13/site-packages/firebolt/client/auth/base.py:4: in <module>
    from httpx import Auth as HttpxAuth
.audit-env/lib/python3.13/site-packages/httpx/__init__.py:2: in <module>
    from ._api import delete, get, head, options, patch, post, put, request, stream
.audit-env/lib/python3.13/site-packages/httpx/_api.py:4: in <module>
    from ._client import Client
.audit-env/lib/python3.13/site-packages/httpx/_client.py:30: in <module>
    from ._transports.default import AsyncHTTPTransport, HTTPTransport
.audit-env/lib/python3.13/site-packages/httpx/_transports/default.py:30: in <module>
    import httpcore
.audit-env/lib/python3.13/site-packages/httpcore/__init__.py:1: in <module>
    from ._api import request, stream
.audit-env/lib/python3.13/site-packages/httpcore/_api.py:5: in <module>
    from ._sync.connection_pool import ConnectionPool
.audit-env/lib/python3.13/site-packages/httpcore/_sync/__init__.py:1: in <module>
    from .connection import HTTPConnection
.audit-env/lib/python3.13/site-packages/httpcore/_sync/connection.py:12: in <module>
    from .._synchronization import Lock
.audit-env/lib/python3.13/site-packages/httpcore/_synchronization.py:13: in <module>
    import trio
.audit-env/lib/python3.13/site-packages/trio/__init__.py:71: in <module>
    from ._path import Path
.audit-env/lib/python3.13/site-packages/trio/_path.py:134: in <module>
    class Path(metaclass=AsyncAutoWrapperType):
.audit-env/lib/python3.13/site-packages/trio/_path.py:85: in __init__
    type(cls).generate_forwards(cls, attrs)
.audit-env/lib/python3.13/site-packages/trio/_path.py:102: in generate_forwards
    raise TypeError(attr_name, type(attr))
E   TypeError: ('parser', <class 'module'>)
_____________ ERROR collecting tests/test_ingest_comprehensive.py ______________
tests/test_ingest_comprehensive.py:13: in <module>
    from ingest import DataIngester, SchemaInfo
ingest.py:13: in <module>
    from src.utils.s3_client import (
src/utils/s3_client.py:7: in <module>
    import s3fs
.audit-env/lib/python3.13/site-packages/s3fs/__init__.py:1: in <module>
    from .core import S3FileSystem, S3File
.audit-env/lib/python3.13/site-packages/s3fs/core.py:30: in <module>
    import aiobotocore.session
.audit-env/lib/python3.13/site-packages/aiobotocore/session.py:11: in <module>
    from .client import AioBaseClient, AioClientCreator
.audit-env/lib/python3.13/site-packages/aiobotocore/client.py:20: in <module>
    from .args import AioClientArgsCreator
.audit-env/lib/python3.13/site-packages/aiobotocore/args.py:7: in <module>
    from .config import AioConfig
.audit-env/lib/python3.13/site-packages/aiobotocore/config.py:6: in <module>
    from aiobotocore.endpoint import DEFAULT_HTTP_SESSION_CLS
.audit-env/lib/python3.13/site-packages/aiobotocore/endpoint.py:17: in <module>
    from aiobotocore.httpchecksum import handle_checksum_body
.audit-env/lib/python3.13/site-packages/aiobotocore/httpchecksum.py:19: in <module>
    import httpx
.audit-env/lib/python3.13/site-packages/httpx/__init__.py:2: in <module>
    from ._api import delete, get, head, options, patch, post, put, request, stream
.audit-env/lib/python3.13/site-packages/httpx/_api.py:4: in <module>
    from ._client import Client
.audit-env/lib/python3.13/site-packages/httpx/_client.py:30: in <module>
    from ._transports.default import AsyncHTTPTransport, HTTPTransport
.audit-env/lib/python3.13/site-packages/httpx/_transports/default.py:30: in <module>
    import httpcore
.audit-env/lib/python3.13/site-packages/httpcore/__init__.py:1: in <module>
    from ._api import request, stream
.audit-env/lib/python3.13/site-packages/httpcore/_api.py:5: in <module>
    from ._sync.connection_pool import ConnectionPool
.audit-env/lib/python3.13/site-packages/httpcore/_sync/__init__.py:1: in <module>
    from .connection import HTTPConnection
.audit-env/lib/python3.13/site-packages/httpcore/_sync/connection.py:12: in <module>
    from .._synchronization import Lock
.audit-env/lib/python3.13/site-packages/httpcore/_synchronization.py:13: in <module>
    import trio
.audit-env/lib/python3.13/site-packages/trio/__init__.py:71: in <module>
    from ._path import Path
.audit-env/lib/python3.13/site-packages/trio/_path.py:134: in <module>
    class Path(metaclass=AsyncAutoWrapperType):
.audit-env/lib/python3.13/site-packages/trio/_path.py:85: in __init__
    type(cls).generate_forwards(cls, attrs)
.audit-env/lib/python3.13/site-packages/trio/_path.py:102: in generate_forwards
    raise TypeError(attr_name, type(attr))
E   TypeError: ('parser', <class 'module'>)
_______________ ERROR collecting tests/test_s3_comprehensive.py ________________
ImportError while importing test module '/Users/tosh/Desktop/Dreambolt/tests/test_s3_comprehensive.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/opt/homebrew/Cellar/python@3.13/3.13.5/Frameworks/Python.framework/Versions/3.13/lib/python3.13/importlib/__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
tests/test_s3_comprehensive.py:14: in <module>
    from moto import mock_s3
E   ImportError: cannot import name 'mock_s3' from 'moto' (/Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/moto/__init__.py). Did you mean: 'mock_aws'?
____________ ERROR collecting tests/test_synthesis_comprehensive.py ____________
tests/test_synthesis_comprehensive.py:12: in <module>
    from synth import DataSynthesizer, ModelConfig
synth.py:39: in <module>
    import openai
.audit-env/lib/python3.13/site-packages/openai/__init__.py:9: in <module>
    from . import types
.audit-env/lib/python3.13/site-packages/openai/types/__init__.py:5: in <module>
    from .batch import Batch as Batch
.audit-env/lib/python3.13/site-packages/openai/types/batch.py:6: in <module>
    from .._models import BaseModel
.audit-env/lib/python3.13/site-packages/openai/_models.py:25: in <module>
    from ._types import (
.audit-env/lib/python3.13/site-packages/openai/_types.py:21: in <module>
    import httpx
.audit-env/lib/python3.13/site-packages/httpx/__init__.py:2: in <module>
    from ._api import delete, get, head, options, patch, post, put, request, stream
.audit-env/lib/python3.13/site-packages/httpx/_api.py:4: in <module>
    from ._client import Client
.audit-env/lib/python3.13/site-packages/httpx/_client.py:30: in <module>
    from ._transports.default import AsyncHTTPTransport, HTTPTransport
.audit-env/lib/python3.13/site-packages/httpx/_transports/default.py:30: in <module>
    import httpcore
.audit-env/lib/python3.13/site-packages/httpcore/__init__.py:1: in <module>
    from ._api import request, stream
.audit-env/lib/python3.13/site-packages/httpcore/_api.py:5: in <module>
    from ._sync.connection_pool import ConnectionPool
.audit-env/lib/python3.13/site-packages/httpcore/_sync/__init__.py:1: in <module>
    from .connection import HTTPConnection
.audit-env/lib/python3.13/site-packages/httpcore/_sync/connection.py:12: in <module>
    from .._synchronization import Lock
.audit-env/lib/python3.13/site-packages/httpcore/_synchronization.py:13: in <module>
    import trio
.audit-env/lib/python3.13/site-packages/trio/__init__.py:71: in <module>
    from ._path import Path
.audit-env/lib/python3.13/site-packages/trio/_path.py:134: in <module>
    class Path(metaclass=AsyncAutoWrapperType):
.audit-env/lib/python3.13/site-packages/trio/_path.py:85: in __init__
    type(cls).generate_forwards(cls, attrs)
.audit-env/lib/python3.13/site-packages/trio/_path.py:102: in generate_forwards
    raise TypeError(attr_name, type(attr))
E   TypeError: ('parser', <class 'module'>)
------------------------------- Captured stderr --------------------------------
17:01:31 | INFO     | DataDreamer not available - synthesis features will use fallback
=============================== warnings summary ===============================
.audit-env/lib/python3.13/site-packages/pydantic/_internal/_config.py:323
  /Users/tosh/Desktop/Dreambolt/.audit-env/lib/python3.13/site-packages/pydantic/_internal/_config.py:323: PydanticDeprecatedSince20: Support for class-based `config` is deprecated, use ConfigDict instead. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.11/migration/
    warnings.warn(DEPRECATION_MESSAGE, DeprecationWarning)

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=========================== short test summary info ============================
ERROR tests/test_firebolt_comprehensive.py - TypeError: ('parser', <class 'mo...
ERROR tests/test_ingest_comprehensive.py - TypeError: ('parser', <class 'modu...
ERROR tests/test_s3_comprehensive.py
ERROR tests/test_synthesis_comprehensive.py - TypeError: ('parser', <class 'm...
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
================== 4 deselected, 1 warning, 4 errors in 0.62s ==================
```

## Command: `python cli_working.py ingest nonexistent.csv`

**Source:** testing.md - Error Handling Testing
**Exit Code:** 1

**Error Output:**
```
2025-06-20 17:01:36.636 | INFO     | ingest_simple:load_data:41 - Loading data from: nonexistent.csv
```

**Standard Output:**
```
🚀 Starting DreamBolt ingestion: nonexistent.csv
⠋ Loading and analyzing data...
❌ Pipeline failed: File not found: nonexistent.csv
```

## Command: `python cli_working.py ingest test.txt`

**Source:** testing.md - Error Handling Testing
**Exit Code:** 1

**Error Output:**
```
2025-06-20 17:01:37.013 | INFO     | ingest_simple:load_data:41 - Loading data from: test.txt
```

**Standard Output:**
```
🚀 Starting DreamBolt ingestion: test.txt
⠋ Loading and analyzing data...
❌ Pipeline failed: Unsupported format: .txt
```

## Command: `python cli_working.py ingest s3://test-bucket/WorldCupPlayers.csv`

**Source:** testing.md - Error Handling Testing
**Exit Code:** 1

**Error Output:**
```
2025-06-20 17:01:37.381 | INFO     | ingest_simple:load_data:41 - Loading data from: s3://test-bucket/WorldCupPlayers.csv
```

**Standard Output:**
```
🚀 Starting DreamBolt ingestion: s3://test-bucket/WorldCupPlayers.csv
⠋ Loading and analyzing data...
❌ Pipeline failed: S3 support temporarily disabled. Use local files.
```

