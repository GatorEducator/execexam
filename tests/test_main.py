"""Test cases for the main.py file."""

import os
import subprocess
import tempfile
import sys
import venv
from pathlib import Path

import pytest
from typer.testing import CliRunner

runner = CliRunner()

EXPECTED_EXIT_CODE_FILE_NOT_FOUND = 4


@pytest.fixture
def poetry_env():
    """Create a temporary virtual environment with poetry installed."""
    with tempfile.TemporaryDirectory() as temp_dir:
        venv_path = Path(temp_dir) / "venv"
        # Create a virtual environment
        venv.create(venv_path, with_pip=True)
        # Get the path to the Python executable in the virtual environment
        if sys.platform == "win32":
            python_path = venv_path / "Scripts" / "python.exe"
            pip_path = venv_path / "Scripts" / "pip.exe"
        else:
            python_path = venv_path / "bin" / "python"
            pip_path = venv_path / "bin" / "pip"
        # Install poetry in the virtual environment
        subprocess.run(
            [str(pip_path), "install", "poetry"],
            check=True,
            capture_output=True,
            text=True,
        )
        yield str(python_path)


@pytest.fixture
def cwd():
    """Define a test fixture for the current working directory."""
    return os.getcwd()


@pytest.mark.no_print
def test_run_with_missing_test(cwd, poetry_env, capfd):
    """Test the run command with default options."""
    with tempfile.TemporaryDirectory() as temp_dir:
        test_one = Path(temp_dir) / "test_one"
        test_one.mkdir()
        test_path = Path(".") / "tests" / "test_question_one.py"
        test_path_str = str(test_path)
        env = os.environ.copy()
        if sys.platform == "win32":
            env["PYTHONIOENCODING"] = "utf-8"
            env["PYTHONUTF8"] = "1"
        try:
            # Disable output capture temporarily
            with capfd.disabled():
                result = subprocess.run(
                    [
                        poetry_env,
                        "-m",
                        "poetry",
                        "run",
                        "execexam",
                        ".",
                        test_path_str,
                        "--report",
                        "trace",
                        "--report",
                        "status",
                        "--report",
                        "failure",
                        "--report",
                        "code",
                        "--report",
                        "setup",
                    ],
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                    check=False,
                    env=env,
                    cwd=cwd,
                )
            assert (
                result.returncode in [EXPECTED_EXIT_CODE_FILE_NOT_FOUND]
            ), f"Expected return code {EXPECTED_EXIT_CODE_FILE_NOT_FOUND}, got {result.returncode}"
            assert (
                "file or directory not found" in result.stdout.lower()
                or "no such file or directory" in result.stderr.lower()
            ), "Expected error message about missing file not found in output"
        except UnicodeDecodeError as e:
            pytest.fail(f"Unicode decode error: {str(e)}")
        except Exception as e:
            pytest.fail(f"Unexpected error: {str(e)}")

        except Exception as e:
            pytest.fail(f"Unexpected error: {str(e)}")
            
