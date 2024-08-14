"""Run an executable examination."""

import io
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

import pytest
import typer
from pytest_jsonreport.plugin import JSONReport
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.text import Text

from . import pytest_plugin  # import the plugin

# create a Typer object to support the command-line interface
cli = typer.Typer(no_args_is_help=True)

# create a default console
console = Console()

# create the skip list for data not needed
skip = ["keywords", "setup", "teardown"]


def path_to_string(path_name: Path, levels: int = 4) -> str:
    """Convert the path to an elided version of the path as a string."""
    parts = path_name.parts
    if len(parts) > levels:
        return Path("<...>", *parts[-levels:]).as_posix()
    else:
        return path_name.as_posix()


def create_spaced_marks(marks: List[str]) -> str:
    """Create a string with spaced marks."""
    found_marks_str = ""
    found_marks = False
    for mark in marks:
        if not found_marks:
            found_marks_str = f"{mark}"
            found_marks = True
            continue
        if found_marks:
            found_marks_str += f" and {mark}"
    return found_marks_str


def extract_details(details: Dict[Any, Any]) -> str:
    """Extract the details of a dictionary and return it as a string."""
    output = []
    # iterate through the dictionary and add each key-value pair
    for key, value in details.items():
        output.append(f"{value} {key}")
    return "Details: " + ", ".join(output)


def extract_test_run_details(details: Dict[Any, Any]) -> str:
    """Extract the details of a test run."""
    # Format of the data in the dictionary:
    # 'summary': Counter({'passed': 2, 'total': 2, 'collected': 2})
    summary_details = details["summary"]
    # convert the dictionary of summary to a string
    summary_details_str = extract_details(summary_details)
    return summary_details_str


def extract_failing_test_details(
    details: dict[Any, Any]
) -> Tuple[str, List[Dict[str, Path]]]:
    """Extract the details of a failing test."""
    # extract the tests from the details
    tests = details["tests"]
    console.print(tests)
    # create an empty string that starts with a newline;
    # the goal of the for loop is to incrementally build
    # of a string that contains all deteails about failing tests
    failing_details_str = "\n"
    # create an initial path for the file containing the failing test
    failing_test_paths = []
    # incrementally build up results for all of the failing tests
    for test in tests:
        if test["outcome"] == "failed":
            current_test_failing_dict = {}
            # convert the dictionary of failing details to a string
            # and add it to the failing_details_str
            failing_details = test
            # get the nodeid of the failing test
            failing_test_nodeid = failing_details["nodeid"]
            failing_details_str += f"  Name: {failing_test_nodeid}\n"
            # get the call information of the failing test
            failing_test_call = failing_details["call"]
            # get the crash information of the failing test's call
            failing_test_crash = failing_test_call["crash"]
            # get all needed information about the test crash call
            failing_test_path = Path(failing_test_crash["path"])
            # extract the name of the function from the nodeid
            failing_test_name = failing_test_nodeid.split("::")[-1]
            current_test_failing_dict["test_name"] = failing_test_name
            current_test_failing_dict["test_path"] = failing_test_path
            failing_test_paths.append(current_test_failing_dict)
            failing_test_path_str = path_to_string(failing_test_path, 4)
            failing_test_lineno = failing_test_crash["lineno"]
            failing_test_message = failing_test_crash["message"]
            # assemble all of the failing test details into the string
            failing_details_str += f"  Path: {failing_test_path_str}\n"
            failing_details_str += f"  Line number: {failing_test_lineno}\n"
            failing_details_str += f"  Message: {failing_test_message}\n"
    # return the string that contains all of the failing test details
    return (failing_details_str, failing_test_paths)


def is_failing_test_details_empty(details: str) -> bool:
    """Determine if the string contains a newline as a hallmark of no failing tests."""
    if details == "\n":
        return True
    return False


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
    mark: str = typer.Option(
        None, help="Only run tests with the specified mark(s)"
    ),
    verbose: bool = typer.Option(False, help="Display verbose output"),
) -> None:
    """Run an executable exam."""
    return_code = 0
    # add the project directory to the system path
    sys.path.append(str(project))
    # create the plugin that will collect all data
    # about the test runs and report it as a JSON object;
    # note that this approach avoids the need to write
    # a custom pytest plugin for the executable examination
    plugin = JSONReport()
    # display basic diagnostic information about command-line
    # arguments using an emoji and the rich console
    diagnostics = f"\nProject directory: {project}\n"
    diagnostics += f"Test file or test directory: {tests}\n"
    console.print()
    console.print(
        Panel(
            Text(diagnostics, overflow="fold"),
            expand=False,
            title="Parameter Information",
        )
    )
    # run pytest for either:
    # - a single test file that was specified in tests
    # - a directory of test files that was specified in tests
    # note that this relies on pytest correctly discovering
    # all of the test files and running their test cases
    # redirect stdout and stderr to /dev/null
    captured_output = io.StringIO()
    sys.stdout = captured_output
    sys.stderr = captured_output
    # run pytest in a fashion that will not
    # produce any output to the console
    found_marks_str = mark
    if found_marks_str:
        pytest.main(
            [
                "-q",
                "-ra",
                "-s",
                "-p",
                "no:logging",
                "-p",
                "no:warnings",
                "--tb=no",
                "--json-report-file=none",
                "--maxfail=10",
                "-m",
                found_marks_str,
                os.path.join(tests),
            ],
            plugins=[plugin, pytest_plugin],
        )
    else:
        pytest.main(
            [
            "-q",
            "-ra",
            "-s",
            "-p",
            "no:logging",
            "-p",
            "no:warnings",
            "--tb=no",
            "--maxfail=10",
            "--json-report-file=none",
            os.path.join(tests),
            ],
            plugins=[plugin, pytest_plugin],
        )
    # restore stdout and stderr; this will allow
    # the execexam program to continue to produce
    # output in the console
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__
    # extract information about the test run from plugin.report
    # --> display details about the test runs
    test_run_details = extract_test_run_details(plugin.report)  # type: ignore
    console.print()
    console.print(
        Panel(
            Text(
                "\n" + captured_output.getvalue() + test_run_details + "\n",
                overflow="fold",
            ),
            expand=False,
            title="Test output",
        )
    )
    # --> display details about the failing tests,
    # if they exist. Note that there can be:
    # - zero failing tests
    # - one failing test
    # - multiple failing tests
    (
        failing_test_details,
        failing_test_path_dicts,
    ) = extract_failing_test_details(plugin.report)  # type: ignore
    # there was at least one failing test case
    if not is_failing_test_details_empty(failing_test_details):
        # there were test failures and thus the return code is non-zero
        # to indicate that at least one test case did not pass
        return_code = 1
        # there was a request for verbose output, so display additional
        # helpful information about the failing test cases
        if verbose:
            # display the details about the failing test cases
            console.print()
            console.print(
                Panel(
                    Text(failing_test_details, overflow="fold"),
                    expand=False,
                    title="Failing test details",
                )
            )
            # display the source code for the failing test cases
            for failing_test_path_dict in failing_test_path_dicts:
                test_name = failing_test_path_dict["test_name"]
                failing_test_path = failing_test_path_dict["test_path"]
                # build the command for running symbex; this tool can
                # perform static analysis of Python source code and
                # extract the code of a function inside of a file
                console.print(failing_test_path_dict)
                console.print(f"Test Name: {test_name}")
                console.print(f"Failing Test Path: {failing_test_path}")
                command = f"symbex {test_name} -f {failing_test_path}"
                # run the symbex command and collect its output
                process = subprocess.run(
                    command,
                    shell=True,
                    check=True,
                    text=True,
                    capture_output=True,
                )
                # delete an extra blank line from the end of the file
                # if there are two blank lines in a row
                sanitized_output = process.stdout.rstrip() + "\n"
                # use rich to display this source code in a formatted box
                source_code_syntax = Syntax(
                    "\n" + sanitized_output,
                    "python",
                    theme="ansi_dark",
                )
                console.print()
                console.print(
                    Panel(
                        source_code_syntax,
                        expand=False,
                        title="Failing test code",
                    )
                )
    # pretty print the JSON report using rich
    # return the code for the overall success of the program
    # to communicate to the operating system the examination's status
    sys.exit(return_code)
