"""This module contains the pytest plugin for the execexam package."""

from typing import Any, List, Tuple

import pytest
from _pytest.config import Config
from _pytest.nodes import Item

# create the report list of
# dictionaries that are organized by nodeid
reports: List[dict[str, Any]] = []

# No longer used but may be needed {{{

# internal_coverage = coverage.Coverage()

# }}}


def pytest_configure(config: Config):
    """Define the order marker that can control test order in the test suites."""
    # note that if the plugin did not define the order
    # marker then this would lead to warnings when execexam
    # runs a provided test suite that uses this marker;
    # defining the marker inside of the plugin avoids needing
    # to define it in every test suite that uses this plugin
    config.addinivalue_line(
        "markers", "order(number): Mark test to run in a specific order"
    )


def extract_single_line(text: str) -> str:
    """Extract a single line from a string."""
    # split the text into lines
    lines = text.splitlines()
    # extract the first line from the text
    # and add an ellipsis to indicate that
    # the text has been truncated if there
    # were other lines beyod the first one
    output = lines[0]
    if len(lines) > 1:
        output += " ..."
    return output


def extract_exception_details(call: pytest.CallInfo) -> Tuple[int, str, str]:
    """Process an exception into relevant details about the exact issue and a message."""
    # initialize all of the variables
    # to empty values before processing
    lineno = 0
    exact = ""
    message = ""
    # dealing with a pytest.CallInfo that is an exception and it can
    # first be processed generally and then, if possible, as an AssertionError
    if call.excinfo is not None and isinstance(call.excinfo.value, Exception):
        # extract the line number
        last_traceback_entry = call.excinfo.traceback[-1]
        lineno = last_traceback_entry.lineno + 1
        # transform the exception into a string
        exception_output = str(call.excinfo.value)
        # specifically dealing with an AssertionError and thus
        # there is specialized information that should be extracted
        if isinstance(call.excinfo.value, AssertionError):
            # extract the error message before the "assert" keyword
            message = exception_output.split("assert")[0].strip()
            # there is no message and thus we must
            # set it to a default value of "AssertionError"
            if message == "":
                message = type(call.excinfo.value).__name__
            # extract any details after the "assert" keyword that
            # corresponds to the exact assertion that failed
            exact = exception_output.split("assert")[1].strip()
        # dealing with an exception that is not an AssertionError
        else:
            # note that there is not an ideal match for the information
            # that is available to the plugin for a general purpose
            # exception and the information that the plugin can report
            # --> the message is the exception's text-based rendering
            message = exception_output
            # --> the exact message is the type of the exception
            exact = type(call.excinfo.value).__name__
    # return the details extracted from the exception
    return (lineno, exact, message)


def pytest_collection_modifyitems(items: List[Item]):
    """Reorder the tests based on the 'order' mark that has an integer value."""
    # sort the items in-place based on the 'order' mark;
    # note that this actually modifies the item list which
    # is what pytest uses to determine the order of tests
    items.sort(
        key=lambda item: item.get_closest_marker("order").args[0]  # type: ignore
        if item.get_closest_marker("order")
        else float("inf")
    )


def pytest_runtest_call(item: Item):
    """Called before the test function is called."""
    # save the name of the test
    test_name = item.nodeid
    # save the full path of the test file
    test_file_name_path = item.fspath
    _ = (test_name, test_file_name_path)
    # start the coverage collection
    # sys.settrace(trace_calls)


def pytest_runtest_protocol(item: Item, nextitem: Item):  # type: ignore
    """Track when a test case is run."""
    global reports  # noqa: PLW0602
    # reference the nextitem parameter
    # that is not used by the hook
    _ = nextitem
    # create a new dictionary for the report
    # and add it to the report list
    reports.append({"nodeid": item.nodeid})


def pytest_exception_interact(node: Item, call: pytest.CallInfo, report: Any):
    """Interacts with exceptions."""
    global reports  # noqa: PLW0602
    # reference the report parameter
    # that is not used by the hook
    _ = report
    # extract the details about the exception that was thrown
    exception_info = call.excinfo
    # set the details about the exception to be the empty string
    # and if there are more details about it, then extract them
    traceback_text = ""
    if exception_info is not None:
        traceback_text = exception_info.exconly()
    # there was an assertion error and thus
    # the plugin must extract details about what failed
    if isinstance(call.excinfo.value, Exception):  # type: ignore
        # create an empty dictionary for the test report
        current_test_report = {}
        # find the test report for this specific test that
        # has a passing assertion
        for current_report in reports:
            # found the test report for this specific test
            # based on what matches according to the nodeid
            if current_report["nodeid"] == node.nodeid:
                current_test_report = current_report
        # extract the details about the exception
        (lineno, expl, orig) = extract_exception_details(call)
        # one of the test reports was found
        # and thus we can store information about this assertion
        if current_test_report != {}:
            # create an empty dictionary for the data about
            # the assertions for this failing test
            current_assertion_dict = {}
            # indicate that the assertion failed
            current_assertion_dict["Status"] = "Failed"
            # there is no data about assertions for this test
            if current_test_report.get("assertions") is None:
                # add the needed fields about the assertion
                current_assertion_dict["Line"] = str(lineno)
                current_assertion_dict["Exact"] = extract_single_line(expl)
                current_assertion_dict["Message"] = orig
                # create a new list and add the dictionary with
                # the details about this assertion to the new list
                assertions_dictionary_list = [current_assertion_dict]
                current_test_report["assertions"] = assertions_dictionary_list
            # there is already data about assertions for this test
            else:
                # add the needed fields about the assertion
                current_assertion_dict["Line"] = str(lineno)
                current_assertion_dict["Exact"] = extract_single_line(expl)
                current_assertion_dict["Message"] = orig
                # there is an existing list of assertion dictionaries
                # for this test case and thus we must add a new dictionary
                # to the list that already exists with assertion information
                current_test_report["assertions"].append(
                    current_assertion_dict
                )
        # there was no information about this exception; this would normally
        # occur when there is an underlying problem with running this specific
        # test because otherwise a different hook would have already added
        # the name of the test into the report list. This means that we need
        # to record all of the information about this test in a new report
        else:
            # create a new dictionary for the failing test case
            new_failing_test_report = {}
            new_failing_test_report["nodeid"] = node.nodeid
            # create an empty dictionary for the data about
            # the assertions for this failing test
            current_assertion_dict = {}
            current_assertion_dict["Status"] = "Failed"
            current_assertion_dict["Message"] = traceback_text
            # store the details about this test failure's assertions
            # inside of the assertion dictionary; note that this is
            # essentially "overloading" the assertion dictionary because
            # there are actually no assertions being recorded --- it is
            # only the fact that the test failed and then the traceback
            # of the exception that was raised when running the test
            new_failing_test_report["assertions"] = [current_assertion_dict]  # type: ignore
            # add the new failing test report to the list of reports
            reports.append(new_failing_test_report)


def pytest_assertion_pass(
    item: Any, lineno: int, orig: str, expl: str
) -> None:
    """Extract and save information about a passing assertion."""
    # Important note: this function is only active in the
    # pytest plugin if the project that is using execexam
    # enables the pytest assertion_pass_hook;
    # reference: https://docs.pytest.org/en/stable/reference/reference.html
    global reports  # noqa: PLW0602
    # create an empty dictionary for the test report
    current_test_report = {}
    # find the test report for this specific test that
    # has a passing assertion
    for current_report in reports:
        # found the test report for this specific test
        # based on what matches according to the nodeid
        if current_report["nodeid"] == item.nodeid:
            current_test_report = current_report
    # one of the test reports was found
    # and thus we can store information about this assertion
    if current_test_report != {}:
        # create a dictionary to store details
        # about the passing assertion for this test
        current_assertion_dict = {}
        # indicate that the assertion passed
        current_assertion_dict["Status"] = "Passed"
        # there is no data about assertions for this test
        if current_test_report.get("assertions") is None:
            # create an empty dictionary for the data about
            current_assertion_dict["Line"] = str(lineno)
            current_assertion_dict["Code"] = orig
            current_assertion_dict["Exact"] = extract_single_line(expl)
            # create a new list and add the dictionary with
            # the details about this assertion to the new list
            assertions_dictionary_list = [current_assertion_dict]
            current_test_report["assertions"] = assertions_dictionary_list
        # there is already data about assertions for this test
        else:
            # create an empty dictionary for the data about
            # this assertion and then add the needed fields
            current_assertion_dict["Line"] = str(lineno)
            current_assertion_dict["Code"] = orig
            current_assertion_dict["Exact"] = extract_single_line(expl)
            # there is an existing list of assertion dictionaries
            # for this test case and thus we must add a new one to it
            current_test_report["assertions"].append(current_assertion_dict)


# No longer used but may be needed {{{

# def trace_calls(frame: FrameType, event: str, arg: Any):
#     """Trace function calls."""
#     if event != "call":
#         return
#     code = frame.f_code
#     func_name = code.co_name
#     func_filename = code.co_filename
#     if func_name == "write":
#         # ignore write() calls from print statements
#         return
#     # note that all of this is current hard-coded
#     target_dir = Path(
#         "/home/gkapfham/working/teaching/github-classroom/algorithmology/executable-examinations/solutions/algorithm-analysis-final-examination-solution/exam/questions/"
#     )
#     if Path(func_filename).resolve().parent == target_dir.resolve():
#         called = (func_name, func_filename)
#         _ = called

# def pytest_runtest_teardown(item: Item, nextitem: Item):
#     """Called after the test function has been called."""
# Stop the coverage collection
# Stop the trace
# sys.settrace(None)


#     internal_coverage.stop()
#     internal_coverage.save()
#     # Get the coverage data
#     cov_data = internal_coverage.get_data()
#     # Analyze the coverage data
#     for filename in cov_data.measured_files():
#         # Get the analysis for the file
#         analysis = internal_coverage._analyze(filename)
#         # Get the list of executed lines
#         executed_lines = analysis.executed
#         # Get the list of statements (lines that could have been executed)
#         statements = analysis.statements
#         # Get the list of missing lines (statements that were not executed)
#         missing_lines = analysis.missing
#         print(f"Test: {item.nodeid}")
#         print(f"File: {filename}")
#         print(f"Executed lines: {executed_lines}")
#         print(f"Statements: {statements}")
#         print(f"Missing lines: {missing_lines}")
#     # Clear the coverage data for the next test
#     internal_coverage.erase()

#     }}}
