"""Test cases for the main.py file."""

import os
import subprocess
import tempfile
from pathlib import Path

import pytest
from typer.testing import CliRunner

runner = CliRunner()

EXPECTED_EXIT_CODE_FILE_NOT_FOUND = 4


@pytest.fixture
def cwd():
    """Define a test fixture for the current working directory."""
    return os.getcwd()


def test_run_with_missing_test(cwd):
    """Test the run command with default options."""
    with tempfile.TemporaryDirectory() as temp_dir:
        test_one = Path(temp_dir) / "test_one"
        test_one.mkdir()

        # Run the CLI command in a subprocess
        result = subprocess.run(
            [
                "poetry",
                "run",
                "execexam",
                ".",
                os.path.join(".", "tests", "test_question_one.py"),
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
            encoding="utf-8",  # Ensure correct handling of Unicode characters
            check=False,
        )

        # Check the return code
        assert result.returncode == EXPECTED_EXIT_CODE_FILE_NOT_FOUND
