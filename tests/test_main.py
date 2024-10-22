"""Test cases for the main.py file."""

from typer.testing import CliRunner
from execexam.main import cli

runner = CliRunner()

def test_run_with_default_options():
    """Test the run command with default options."""
    result = runner.invoke(cli, [
        "run", ".",
        # "--advice-model", "anthropic/claude-3-haiku-20240307",
        # "--advice-server", "https://execexamadviser.fly.dev/",
        "--report", "trace", "--report", "status", "--report", "failure",
        "--report", "code", "--report", "setup", # "--report", "advice",
        "--fancy", "--debug"
    ])
    assert result.exit_code == 0
    assert "Project directory containing questions and tests" in result.output
