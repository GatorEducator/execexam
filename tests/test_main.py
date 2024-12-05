"""Test cases for the command-line interface provided by main."""

from typer.testing import CliRunner

from execexam import main

# NOTE: Unless there is a clear reason to do so, only
# write tests for the command-line interface using the
# CliRunner provided by typer.

runner = CliRunner()

# NOTE: tests that run execexam through the its CLI
# using the CliRunner can run into dependency issues
# due to the fact that the pytest plugin that
# execexam uses is going to be repeatedly loaded
# and (potentially) not unloaded

# Tests that provide valid arguments {{{


def test_run_use_help():
    """Test the run command with the --help."""
    result = runner.invoke(main.cli, ["run", "--help"])
    assert result.exit_code == 0
    assert "Arguments" in result.output
    assert "Options" in result.output


def test_run_use_tldr():
    """Test the run command with the --tldr."""
    result = runner.invoke(main.cli, ["run", "--tldr"])
    assert result.exit_code == 0
    assert "Too" in result.output
    assert "Lazy" in result.output
    assert "--help" in result.output


def test_run_use_tldr_and_help_defaults_to_help():
    """Test the run command with the --tldr and --help."""
    result = runner.invoke(main.cli, ["run", "--tldr", "--help"])
    assert result.exit_code == 0
    assert "Arguments" in result.output
    assert "Options" in result.output
    result = runner.invoke(main.cli, ["run", "--help", "--tldr"])
    assert result.exit_code == 0
    assert "Arguments" in result.output
    assert "Options" in result.output


# }}}


# Tests that provide invalid arguments {{{


def test_run_valid_argument_no_action():
    """Test the run command with valid required arguments."""
    result = runner.invoke(main.cli, ["run", ". tests/"])
    assert result.exit_code != 0


def test_run_invalid_report_argument():
    """Test the run command with invalid report argument."""
    result = runner.invoke(main.cli, ["run", ". tests/", "--report invalid"])
    assert result.exit_code != 0


def test_invalid_tldr_spelling():
    """Test the run command with invalid tldr command-line argument spelling."""
    result = runner.invoke(main.cli, ["run", ". tests/", "--tldear"])
    assert result.exit_code != 0


def test_invalid_help_spelling():
    """Test the run command with invalid help command-line argument spelling."""
    result = runner.invoke(main.cli, ["run", ". tests/", "--hlp"])
    assert result.exit_code != 0


def test_run_default_report_exitcode():
    """Test the run command to check the default report is set to exitcode."""
    result = runner.invoke(main.cli, ["run", ".", "--report", "--fancy"])
    assert result.exit_code != 0


def test_run_default_mark_exitcode():
    """Test the run command to check the default mark has an output."""
    result = runner.invoke(main.cli, ["run", ".", "--mark"])
    assert result.exit_code != 0

# }}}
