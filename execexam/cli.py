"""CLI for the execexam tool."""

import typer
from pathlib import Path
from typing import Optional, List
from .util import determine_execexam_return_code
from .display import get_display_return_code, display_advice
from .main import run as run_command
from . import enumerations

cli = typer.Typer()

@cli.command()
def run(
    project: Path = typer.Argument(..., help="Project directory containing questions and tests"),
    tests: Path = typer.Argument(..., help="Test file or test directory"),
    report: Optional[List[enumerations.ReportType]] = typer.Option(None, help="Types of reports to generate"),
    mark: str = typer.Option(None, help="Run tests with specified mark(s)"),
    maxfail: int = typer.Option(10, help="Maximum test failures before stopping"),
    advice_method: enumerations.AdviceMethod = typer.Option(enumerations.AdviceMethod.api_key, help="LLM-based method for advice"),
    advice_model: str = typer.Option(None, help="LLM model: https://docs.litellm.ai/docs/providers"),
    advice_server: str = typer.Option(None, help="URL of the LiteLLM server"),
    debug: bool = typer.Option(False, help="Collect debugging information"),
    fancy: bool = typer.Option(True, help="Display fancy output"),
    syntax_theme: enumerations.Theme = typer.Option(enumerations.Theme.ansi_dark, help="Syntax highlighting theme"),
):
    """Run the execexam tool on the specified project and tests directories."""
    run_command(
        project=project,
        tests=tests,
        report=report,
        mark=mark,
        maxfail=maxfail,
        advice_method=advice_method,
        advice_model=advice_model,
        advice_server=advice_server,
        debug=debug,
        fancy=fancy,
        syntax_theme=syntax_theme,
    )
