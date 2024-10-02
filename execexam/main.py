"""Run an executable examination."""

import io
import os
import subprocess
import sys
import threading
import time
import warnings
from pathlib import Path
from typing import List, Optional

import pytest
import typer
from pytest_jsonreport.plugin import JSONReport  # type: ignore
from rich.console import Console
from typing_extensions import Annotated

from . import advise, display, enumerations, extract, util
from . import debug as debugger
from . import pytest_plugin as exec_exam_pytest_plugin

# suppress the warnings that are produced by the Pydantic library;
# note that this is needed because one of execexam's dependencies
# is not using Pydantic correctly and this produces warnings
warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")

# create a Typer object to support the command-line interface
cli = typer.Typer(no_args_is_help=True)

# create a default console
console = Console()

# create the skip list for data not needed
skip = ["keywords", "setup", "teardown"]

# create a variable of the main pytest issues
pytest_labels = ["FAILED", "ERROR", "WARNING", "COLLECTERROR"]


def tldr_callback(value: bool) -> None:
    """Display a list of example commands and their descriptions."""
    if value:
        display.display_tldr(console)
        raise typer.Exit()


@cli.command()
def run(  # noqa: PLR0913, PLR0915
    project: Path = typer.Argument(
        ...,
        help="Project directory containing questions and tests",
    ),
    tests: Path = typer.Argument(
        ...,
        help="Test file or test directory",
    ),
    tldr: Annotated[
        Optional[bool],
        typer.Option(
            "--tldr",
            callback=tldr_callback,
            help="Display summary of commands",
        ),
    ] = None,
    report: Optional[List[enumerations.ReportType]] = typer.Option(
        None,
        help="Types of reports to generate",
    ),
    mark: str = typer.Option(None, help="Run tests with specified mark(s)"),
    maxfail: int = typer.Option(
        10, help="Maximum test failures before stopping"
    ),
    advice_method: enumerations.AdviceMethod = typer.Option(
        enumerations.AdviceMethod.api_key, help="LLM-based method for advice"
    ),
    advice_model: str = typer.Option(
        None, help="LLM model: https://docs.litellm.ai/docs/providers"
    ),
    advice_server: str = typer.Option(None, help="URL of the LiteLLM server"),
    debug: bool = typer.Option(False, help="Collect debugging information"),
    fancy: bool = typer.Option(True, help="Display fancy output"),
    syntax_theme: enumerations.Theme = typer.Option(
        enumerations.Theme.ansi_dark, help="Syntax highlighting theme"
    ),
) -> None:
    """Run an executable exam and produce the requested report(s)."""
    # indicate that the program's exit code is zero
    # to show that the program completed successfully;
    # attempt to prove otherwise by running all the checks
    return_code = 0
    # confirm that the advice model is provided when
    # the report includes the advice report type or
    # when the report includes all of the report types
    advise.check_advice_model(console, report, advice_model)
    # confirm that the advice server is provided when
    # the advice method is set to the API server and
    # the report includes the advice report type or all reports
    advise.check_advice_server(console, report, advice_method, advice_server)
    # load the litellm module in a separate thread when advice
    # was requested for this run of the program
    debugger.debug(debug, debugger.Debug.parameter_check_passed.value)
    litellm_thread = threading.Thread(target=advise.load_litellm)
    # if --tldr was specified, then display the TLDR summary
    # of the commands and then exit the program
    if tldr is not None:
        return
    # if execexam was configured to produce the report for advice
    # or if it was configured to produce all of the possible reports,
    # then start the litellm thread that provides the advice
    display_report_type = enumerations.ReportType.testadvice
    if report is not None and (
        display_report_type in report or enumerations.ReportType.all in report
    ):
        litellm_thread.start()
        debugger.debug(debug, debugger.Debug.started_litellm_thread.value)
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
    # --> SETUP
    syntax = False
    newline = True
    display.display_content(
        console,
        enumerations.ReportType.setup,
        report,
        colon_separated_diagnostics,
        "Parameter Information",
        fancy,
        syntax,
        syntax_theme,
        "python",
        newline,
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
    debugger.debug(debug, debugger.Debug.started_capturing_output.value)
    # run pytest in a fashion that will not
    # produce any output to the console
    found_marks_str = mark
    # there were test marks on the command-line and
    # thus they should be run for the specified tests
    # (note that marks can control which tests are run)
    pytest_exit_code = 0
    if found_marks_str:
        pytest_exit_code = pytest.main(
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
        debugger.debug(debug, debugger.Debug.pytest_passed_with_marks.value)
    # there were no test marks specified on the command-line
    # and thus all of the tests should be run based on the specified
    # test file or test directory, which this provides to pytest
    else:
        pytest_exit_code = pytest.main(
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
        debugger.debug(debug, debugger.Debug.pytest_passed_without_marks.value)
    # restore stdout and stderr; this will allow
    # the execexam program to continue to produce
    # output in the console
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__
    debugger.debug(debug, debugger.Debug.stopped_capturing_output.value)
    # determine the return code for the execexam command
    # based on the exit code that was produced by pytest
    return_code = util.determine_execexam_return_code(pytest_exit_code)
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
    filtered_test_output = extract.extract_test_output_multiple_labels(
        pytest_labels,
        captured_output.getvalue(),
    )
    # add an extra newline to the filtered output
    # since there is a failing test case to display
    if filtered_test_output != "":
        filtered_test_output = "\n" + filtered_test_output
    # indicate that the material that will be displayed
    # is not source code and thus does not need syntax highlighting
    # --> TRACE
    syntax = False
    newline = True
    display.display_content(
        console,
        enumerations.ReportType.testtrace,
        report,
        filtered_test_output + exec_exam_test_assertion_details,
        "Test Trace",
        fancy,
        syntax,
        syntax_theme,
        "python",
        newline,
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
    failing_test_code_overall = ""
    # there was at least one failing test case
    if not extract.is_failing_test_details_empty(failing_test_details):
        # display additional helpful information about the failing
        # test cases; this is the error message that would appear
        # when standardly running the test suite with pytest
        # --> FAILURE
        syntax = False
        newline = True
        display.display_content(
            console,
            enumerations.ReportType.testfailures,
            report,
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
            failing_test_code_overall += sanitized_output
            # display the source code of the failing test
            # --> CODE
            syntax = True
            newline = True
            display.display_content(
                console,
                enumerations.ReportType.testcodes,
                report,
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
    display_report_type = enumerations.ReportType.testadvice
    if report is not None and (
        display_report_type in report or enumerations.ReportType.all in report
    ):
        # regardless of whether or not there were test failures, it is
        # appropriate to display the loading message so that the thread
        # can finish the imports and then the advice can be requested
        # (if there were test failures) or the program can stop running
        # (if there were no test failures and thus advice is not needed)
        console.print()
        with console.status("[bold green] Loading ExecExam's Coding Mentor"):
            while litellm_thread.is_alive():
                time.sleep(0.1)
        # return control to the main thread now that the
        # litellm module has been loaded in a separate thread
        litellm_thread.join()
        debugger.debug(debug, debugger.Debug.stopped_litellm_thread.value)
        # provide advice about how to fix the failing tests
        # because the non-zero return code indicates that
        # there was a test failure and that overall there
        # is at least one mistake in the examination for
        # which advice should be sought from the LLM
        if return_code != 0:
            advise.fix_failures(
                console,
                filtered_test_output,
                exec_exam_test_assertion_details,
                filtered_test_output + exec_exam_test_assertion_details,
                failing_test_details,
                failing_test_code_overall,
                advice_method,
                advice_model,
                advice_server,
                syntax_theme,
                fancy,
            )
            debugger.debug(debug, debugger.Debug.get_advice_with_llm.value)
        # there were no test failures and thus there is no need
        # to seek advice from the LLM-based mentoring system;
        # display a message to repor that even though advice
        # was requested, it was not needed and thus is not displayed
        else:
            syntax = False
            newline = False
            advice_message = display.display_advice(return_code)
            display.display_content(
                console,
                enumerations.ReportType.exitcode,
                report,
                advice_message,
                "Advice Status",
                fancy,
                syntax,
                syntax_theme,
                "Python",
                newline,
            )
    # display the debugging messages
    debugging_messages_exist = debugger.has_debugging_messages()
    if debugging_messages_exist:
        debugging_messages = debugger.get_debugging_messages()
        syntax = False
        newline = True
        display.display_content(
            console,
            enumerations.ReportType.debug,
            report,
            debugging_messages,
            "Debugging Information",
            fancy,
            syntax,
            syntax_theme,
            "Python",
            newline,
        )
    # display a final message about the return code, using
    # a human-readable message that indicates the overall status
    exit_code_message = display.get_display_return_code(return_code, fancy)
    # display the return code through a diagnostic message
    syntax = False
    newline = True
    display.display_content(
        console,
        enumerations.ReportType.exitcode,
        report,
        exit_code_message,
        "Overall Status",
        fancy,
        syntax,
        syntax_theme,
        "Python",
        newline,
    )
    # return the code for the overall success of the program
    # to communicate to the operating system the examination's status
    sys.exit(return_code)
