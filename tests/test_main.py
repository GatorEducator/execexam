"""Test cases for the command-line interface provided by main."""

from typer.testing import CliRunner

from execexam import main

runner = CliRunner()


def test_run_use_help():
    """Test the run command with the --help."""
    result = runner.invoke(main.cli, ["run", "--help"])
    assert result.exit_code == 0
    assert "Arguments" in result.output
    assert "Options" in result.output


def test_run_valid_argument_no_action():
    """Test the run command with valid required arguments."""
    result = runner.invoke(main.cli, ["run", ". tests/"])
    assert result.exit_code != 0


def test_run_invalid_report_argument():
    """Test the run command with invalid report argument."""
    result = runner.invoke(main.cli, ["run", ". tests/", "--report invalid"])
    assert result.exit_code != 0
