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
    # Create a temporary directory
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
                "./tests/test_question_one.py",
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
                # "--advice-method", "apiserver",
                # "--advice-model", "anthropic/claude-3-haiku-20240307",
                # "--advice-server", "https://execexamadviser.fly.dev/",
                # "--report", "advice",
                "--fancy",
                "--debug",
            ],
            cwd=cwd,  # Change working directory to the root of the project
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )

        assert (
            result.returncode == EXPECTED_EXIT_CODE_FILE_NOT_FOUND
        )  # confirms that the file was not found
