"""Command-line interface for execexam."""

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
        ..., help="Project directory for an executable examination"
    ),
    tests: Path = typer.Argument(
        ..., help="Test file or test directory for an executable examination"
    ),
) -> None:
    """Run an executable exam."""
    # tests = "/home/gkapfham/working/teaching/github-classroom/algorithmology/executable-examinations/solutions/algorithm-analysis-midterm-examination-solution/exam"
    sys.path.append(str(project))
    # construct the path to the tests/ directory
    # tests_dir = os.path.join(tests, "tests")
    # create the plugin
    plugin = JSONReport()
    # run pytest for the test_question_one.py file
    pytest.main(
        [
            "-q",
            "--json-report-file=none",
            "-p",
            "no:logging",
            "-p",
            "no:warnings",
            "--tb=no",
            # os.path.join(tests_dir, "test_question_one.py"),
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
    # print(process.stdout)
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
