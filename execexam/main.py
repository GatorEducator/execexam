"""Run an executable examination."""

import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict

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


def extract_details(details: Dict[Any, Any]) -> str:
    """Extract the details of a dictionary and return it as a string."""
    output = []
    emoji = ":sparkles:"
    output.append(emoji)
    for key, value in details.items():
        output.append(f"{key.capitalize()}: {value}")
    return ", ".join(output)


def extract_test_run_details(details: dict[Any, Any]) -> str:
    """Extract the details of a test run."""
    # Format of the data in the dictionary:
    # 'summary': Counter({'passed': 2, 'total': 2, 'collected': 2})
    summary_details = details["summary"]
    # convert the dictionary of summary to a string
    summary_details_str = extract_details(summary_details)
    return summary_details_str


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
    verbose: bool = typer.Option(False, help="Display verbose output"),
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
    console.print(":snake: Pytest output")
    # run pytest for either:
    # - a single test file that was specified in tests
    # - a directory of test files that was specified in tests
    # note that this relies on pytest correctly discovering
    # all of the test files and running their test cases
    # redirect stdout and stderr to /dev/null
    null_file = open(os.devnull, 'w')
    sys.stdout = null_file
    sys.stderr = null_file
    # run pytest in a fashion that will not
    # produce any output to the console
    pytest.main(
        [
            "-q",
            "-ra",
            "-s",
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
    # restore stdout and stderr; this will allow
    # the execexam program to continue to produce
    # output in the console
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__
    # extract information about the test run from plugin.report
    test_run_details = extract_test_run_details(plugin.report)  # type: ignore
    console.print(test_run_details)
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
