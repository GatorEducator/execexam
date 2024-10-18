"""Test cases for the main.py file."""

from typer.testing import CliRunner
from execexam.main import cli

runner = CliRunner()

def test_run_with_default_options():
    """Test the run command with default options."""
    result = runner.invoke(cli, ["run", "path/to/project", "path/to/tests"])
    assert result.exit_code == 0
    assert "Project directory containing questions and tests" in result.output

def test_run_with_report_option():
    """Test the run command with the report option."""
    result = runner.invoke(cli, [
        "run", "path/to/project", "path/to/tests",
        "--report", "summary"
    ])
    assert result.exit_code == 0
    assert "Types of reports to generate" in result.output

def test_run_with_mark_option():
    """Test the run command with the mark option."""
    result = runner.invoke(cli, [
        "run", "path/to/project", "path/to/tests",
        "--mark", "slow"
    ])
    assert result.exit_code == 0
    assert "Run tests with specified mark(s)" in result.output

def test_run_with_maxfail_option():
    """Test the run command with the maxfail option."""
    result = runner.invoke(cli, [
        "run", "path/to/project", "path/to/tests",
        "--maxfail", "5"
    ])
    assert result.exit_code == 0
    assert "Maximum test failures before stopping" in result.output

def test_run_with_advice_method_option():
    """Test the run command with the advice method option."""
    result = runner.invoke(cli, [
        "run", "path/to/project", "path/to/tests",
        "--advice-method", "api_key"
    ])
    assert result.exit_code == 0
    assert "LLM-based method for advice" in result.output

def test_run_with_advice_model_option():
    """Test the run command with the advice model option."""
    result = runner.invoke(cli, [
        "run", "path/to/project", "path/to/tests",
        "--advice-model", "gpt-3"
    ])
    assert result.exit_code == 0
    assert "LLM model: https://docs.litellm.ai/docs/providers" in result.output

def test_run_with_advice_server_option():
    """Test the run command with the advice server option."""
    result = runner.invoke(cli, [
        "run", "path/to/project", "path/to/tests",
        "--advice-server", "http://localhost:8000"
    ])
    assert result.exit_code == 0
    assert "URL of the LiteLLM server" in result.output

def test_run_with_debug_option():
    """Test the run command with the debug option."""
    result = runner.invoke(cli, [
        "run", "path/to/project", "path/to/tests",
        "--debug"
    ])
    assert result.exit_code == 0
    assert "Collect debugging information" in result.output

def test_run_with_fancy_option():
    """Test the run command with the fancy option."""
    result = runner.invoke(cli, [
        "run", "path/to/project", "path/to/tests",
        "--fancy", "False"
    ])
    assert result.exit_code == 0
    assert "Display fancy output" in result.output

def test_run_with_syntax_theme_option():
    """Test the run command with the syntax theme option."""
    result = runner.invoke(cli, [
        "run", "path/to/project", "path/to/tests",
        "--syntax-theme", "monokai"
    ])
    assert result.exit_code == 0
    assert "Syntax highlighting theme" in result.output