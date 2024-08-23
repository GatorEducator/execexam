"""Run an executable examination."""

import io
import os
import subprocess
import sys
import threading
import time
from enum import Enum
from pathlib import Path

import pytest
import typer
from pytest_jsonreport.plugin import JSONReport  # type: ignore
from rich.console import Console

from . import advise, display, extract
from . import pytest_plugin as exec_exam_pytest_plugin

# create a Typer object to support the command-line interface
cli = typer.Typer(no_args_is_help=True)

# create a default console
console = Console()

# create the skip list for data not needed
skip = ["keywords", "setup", "teardown"]


class Theme(str, Enum):
    """An enumeration of the themes for syntax highlighting in rich."""

    ansi_dark = "ansi_dark"
    ansi_light = "ansi_light"


@cli.command()
def run(  # noqa: PLR0913
    project: Path = typer.Argument(
        ...,
        help="Project directory containing questions and tests",
    ),
    tests: Path = typer.Argument(
        ...,
        help="Test file or test directory",
    ),
    mark: str = typer.Option(None, help="Run tests with specified mark(s)"),
    maxfail: int = typer.Option(
        10, help="Maximum test failures before stopping"
    ),
    fancy: bool = typer.Option(True, help="Display fancy output"),
    syntax_theme: Theme = typer.Option(
        Theme.ansi_dark, help="Syntax highlighting theme"
    ),
    verbose: bool = typer.Option(False, help="Display verbose output"),
) -> None:
    """Run an executable exam."""
    # load the litellm module in a separate thread
    litellm_thread = threading.Thread(target=advise.load_litellm)
    litellm_thread.start()
    # indicate that the program's exit code is zero
    # to show that the program completed successfully;
    # attempt to prove otherwise by running all the checks
    return_code = 0
    # add the project directory to the system path
    sys.path.append(str(project))
    # create the plugin that will collect all data
    # about the test runs and report it as a JSON object;
    # note that this approach avoids the need to write
    # a custom pytest plugin for the executable examination
    json_report_plugin = JSONReport()
    # display basic diagnostic information about command-line's arguments;
    # extract the local parmeters and then make a displayable string of them
    args = locals()
    colon_separated_diagnostics = display.make_colon_separated_string(args)
    syntax = False
    console.print()
    display.display_diagnostics(
        verbose,
        console,
        colon_separated_diagnostics,
        "Parameter Information",
        fancy,
        syntax,
        syntax_theme,
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
    # there were test marks on the command-line and
    # thus they should be run for the specified tests
    # (marks can control which tests are run)
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
                f"--maxfail={maxfail}",
                "-m",
                found_marks_str,
                os.path.join(tests),
            ],
            plugins=[json_report_plugin, exec_exam_pytest_plugin],
        )
    # there were no test marks specified on the command-line
    # and thus all of the tests should be run based on that specified
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
                f"--maxfail={maxfail}",
                "--json-report-file=none",
                os.path.join(tests),
            ],
            plugins=[json_report_plugin, exec_exam_pytest_plugin],
        )
    # restore stdout and stderr; this will allow
    # the execexam program to continue to produce
    # output in the console
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__
    # extract the data that was created by the internal
    # execexam pytest plugin for further diagnostic display
    execexam_report = exec_exam_pytest_plugin.reports
    # extract the details about the test assertions
    # that come from the pytest plugin that execexam uses
    exec_exam_test_assertion_details = extract.extract_test_assertions_details(
        execexam_report
    )
    # --> display details about the test runs
    _ = extract.extract_test_run_details(json_report_plugin.report)  # type: ignore
    # filter the test output and decide if an
    # extra newline is or is not needed
    filtered_test_output = extract.extract_test_output(
        "FAILED", captured_output.getvalue()
    )
    # add an extra newline to the filtered output
    # since there is a failing test case to display
    if filtered_test_output != "":
        filtered_test_output = "\n" + filtered_test_output
    # indicate that the material that will be displayed
    # is not source code and thus does not need syntax highlighting
    syntax = False
    display.display_content(
        console,
        filtered_test_output + exec_exam_test_assertion_details,
        "Test Trace",
        fancy,
        syntax,
        syntax_theme,
    )
    # display details about the failing tests,
    # if they exist. Note that there can be:
    # - zero failing tests
    # - one failing test
    # - multiple failing tests
    # note that details about the failing tests are
    # collected by the execexam pytest plugin and
    # there is no need for the developer of the
    # examination to collect and report this data
    (
        failing_test_details,
        failing_test_path_dicts,
    ) = extract.extract_failing_test_details(json_report_plugin.report)  # type: ignore
    # there was at least one failing test case
    if not extract.is_failing_test_details_empty(failing_test_details):
        # there were test failures and thus the return code is non-zero
        # to indicate that at least one test case did not pass
        return_code = 1
        # display additional helpful information about the failing
        # test cases; this is the error message that would appear
        # when standardly running the test suite with pytest
        syntax = False
        newline = True
        display.display_content(
            console,
            failing_test_details,
            "Test Failure(s)",
            fancy,
            syntax,
            syntax_theme,
            "Python",
            newline,
        )
        # display the source code for the failing test cases
        for failing_test_path_dict in failing_test_path_dicts:
            test_name = failing_test_path_dict["test_name"]
            failing_test_path = failing_test_path_dict["test_path"]
            # build the command for running symbex; this tool can
            # perform static analysis of Python source code and
            # extract the code of a function inside of a file
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
            # display the source code of the failing test
            syntax = True
            newline = True
            display.display_content(
                console,
                sanitized_output,
                "Failing Test",
                fancy,
                syntax,
                syntax_theme,
                "Python",
                newline,
            )
    # display the spinner until the litellm thread finishes
    # loading the litellm module that provides the LLM-based
    # mentoring by automatically suggesting fixes for test failures
    console.print()
    with console.status("[bold green] Loading ExecExam's Coding Mentor"):
        while litellm_thread.is_alive():
            time.sleep(0.1)
    # return control to the main thread now that the
    # litellm module has been loaded in a separate thread
    litellm_thread.join()
    # advise.fix_failures(
    #     console,
    #     filtered_test_output,
    #     exec_exam_test_assertion_details,
    #     filtered_test_output + exec_exam_test_assertion_details,
    #     failing_test_details,
    #     "apiserver",
    # )
    # display a final message about the return code;
    # this is the only output that will always appear
    # by default when no other levels are specified
    display.display_return_code(console, return_code)
    # return the code for the overall success of the program
    # to communicate to the operating system the examination's status
    sys.exit(return_code)
