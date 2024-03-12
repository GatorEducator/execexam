"""Run an executable examination."""

import os
import subprocess
import sys
from pathlib import Path

import pytest
import typer
from pytest_jsonreport.plugin import JSONReport
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax

# create a Typer object to support the command-line interface
cli = typer.Typer(no_args_is_help=True)

# create a default console
console = Console()


@cli.command()
def run(
    project: Path = typer.Argument(
        ...,
        help="Project directory containing questions and tests",
    ),
    tests: Path = typer.Argument(
        ...,
        help="Test file or test directory",
    ),
) -> None:
    """Run an executable exam."""
    # add the project directory to the system path
    sys.path.append(str(project))
    # create the plugin that will collect all data
    # about the test runs and report it as a JSON object;
    # note that this approach avoids the need to write
    # a custom pytest plugin for the executable examination
    plugin = JSONReport()
    # display basic diagnostic information about command-line
    # arguments using an emoji and the rich console
    console.print(f"📦 Project directory: {project}")
    console.print(f"🧪 Test file or test directory: {tests}")
    # run pytest for either:
    # - a single test file that was specified in tests
    # - a directory of test files that was specified in tests
    # note that this relies on pytest correctly discovering
    # all of the test files and running their test cases
    pytest.main(
        [
            "-q",
            "--json-report-file=none",
            "-p",
            "no:logging",
            "-p",
            "no:warnings",
            "--tb=no",
            os.path.join(tests),
        ],
        plugins=[plugin],
    )
    # pretty print the JSON report using rich
    console.print(plugin.report, highlight=True)
    # define the command
    command = "symbex test_find_minimum_value -f /home/gkapfham/working/teaching/github-classroom/algorithmology/executable-examinations/solutions/algorithm-analysis-midterm-examination-solution/exam/tests/test_question_one.py"
    # run the command and collect its output
    process = subprocess.run(
        command, shell=True, check=True, text=True, capture_output=True
    )
    # print the output
    # use rich to display this soure code in a formatted box
    source_code_syntax = Syntax(
        process.stdout,
        "python",
        theme="ansi_dark",
    )
    console.print(
        Panel(
            source_code_syntax,
            expand=False,
            title="Source code file",
        )
    )
