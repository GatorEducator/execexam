"""Test cases for the main.py file."""

import os
import subprocess
import sys
import tempfile
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
            pytest.fail(f"Unicode decode error: {e!s}")
        except Exception as e:
            pytest.fail(f"Unexpected error: {e!s}")


@pytest.mark.no_print
def test_default_exitcode_report(cwd, poetry_env):
    """Test that the default report includes exitcode when --report is not provided."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Set up a mock project directory with proper test directory
        project_dir = Path(temp_dir) / "mock_project"
        project_dir.mkdir()

        # Create tests directory
        tests_dir = project_dir / "tests"
        tests_dir.mkdir()

        # Create test file in the tests directory
        test_file = tests_dir / "test_mock.py"
        test_file.write_text("def test_example(): assert True")

        env = os.environ.copy()
        if sys.platform == "win32":
            env["PYTHONIOENCODING"] = "utf-8"
            env["PYTHONUTF8"] = "1"
            # Use absolute paths with normalized separators
            project_dir_str = str(Path(temp_dir).resolve() / "mock_project")
            test_file_str = str(test_file.resolve())
            # Normalize path separators
            project_dir_str = project_dir_str.replace(os.sep, "/")
            test_file_str = test_file_str.replace(os.sep, "/")
        else:
            project_dir_str = str(project_dir)
            test_file_str = str(test_file)

        # Run the command without specifying the --report option
        result = subprocess.run(
            [
                poetry_env,
                "-m",
                "poetry",
                "run",
                "execexam",
                project_dir_str,
                test_file_str,
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            env=env,
            cwd=cwd,
        )

        # Validate the exit code
        assert (
            result.returncode == 0
        ), f"Expected exit code 0, got {result.returncode}"

        # Validate that the output includes either the expected 'exit code' message or equivalent status
        output_lower = result.stdout.lower()
        assert (
            "exit code" in output_lower
            or "overall status" in output_lower
            or "checks passed" in output_lower
        ), (
            "Expected 'exit code', 'overall status', or 'checks passed' in the output, but none were found. "
            f"Output: {result.stdout}"
        )
