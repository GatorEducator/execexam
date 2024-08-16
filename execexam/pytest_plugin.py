"""This module contains the pytest plugin for the execexam package."""

from typing import Any, List, Tuple

import pytest

# create the report list of
# dictionaries that are organized by nodeid
reports: List[dict[str, Any]] = []


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
            message = exception_output
            exact = type(call.excinfo.value).__name__
    # return the details extracted from the exception
    return (lineno, exact, message)


def pytest_runtest_protocol(item, nextitem):  # type: ignore
    """Track when a test case is run."""
    global reports  # noqa: PLW0602
    # reference the nextitem parameter
    # that is not used by the hook
    _ = nextitem
    # create a new dictionary for the report
    # and add it to the report list
    reports.append({"nodeid": item.nodeid})


def pytest_exception_interact(node, call, report):
    """Interacts with exceptions."""
    global reports  # noqa: PLW0602
    # reference the report parameter
    # that is not used by the hook
    _ = report
    # there was an assertion error and thus
    # the plugin must extract details about what failed
    if isinstance(call.excinfo.value, Exception):
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
        if current_test_report is not {}:
            # create an empty dictionary for the data about
            # the assertions for this failing test
            current_assertion_dict = {}
            # indicate that the assertion failed
            current_assertion_dict["Status"] = "Failed"
            # there is no data about assertions for this test
            if current_test_report.get("assertions") is None:
                # add the needed fields about the assertion
                current_assertion_dict["Line"] = lineno
                current_assertion_dict["Exact"] = extract_single_line(expl)
                current_assertion_dict["Message"] = orig
                # create a new list and add the dictionary with
                # the details about this assertion to the new list
                assertions_dictionary_list = [current_assertion_dict]
                current_test_report["assertions"] = assertions_dictionary_list
            # there is already data about assertions for this test
            else:
                # add the needed fields about the assertion
                current_assertion_dict["Line"] = lineno
                current_assertion_dict["Exact"] = extract_single_line(expl)
                current_assertion_dict["Message"] = orig
                # there is an existing list of assertion dictionaries
                # for this test case and thus we must add a new dictionary
                # to the list that already exists with assertion information
                current_test_report["assertions"].append(
                    current_assertion_dict
                )


def pytest_assertion_pass(item, lineno, orig, expl):
    """Extract and save information about a passing assertion."""
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
    if current_test_report is not {}:
        # create a dictionary to store details
        # about the passing assertion for this test
        current_assertion_dict = {}
        print("Exact value: **", expl, "**")
        # indicate that the assertion passed
        current_assertion_dict["Status"] = "Passed"
        # there is no data about assertions for this test
        if current_test_report.get("assertions") is None:
            # create an empty dictionary for the data about
            current_assertion_dict["Line"] = lineno
            current_assertion_dict["Code"] = orig
            current_assertion_dict["Exact"] = extract_single_line(expl)
            # create a new list and add the dictionary with
            # the details about this assertion to the new list
            assertions_dictionary_list = [current_assertion_dict]
            current_test_report["assertions"] = assertions_dictionary_list
        # there is already data about assertions for this test
        else:
            print("Exact value: **", expl, "**")
            # create an empty dictionary for the data about
            # this assertion and then add the needed fields
            current_assertion_dict["Line"] = lineno
            current_assertion_dict["Code"] = orig
            current_assertion_dict["Exact"] = extract_single_line(expl)
            # there is an existing list of assertion dictionaries
            # for this test case and thus we must add a new one to it
            current_test_report["assertions"].append(current_assertion_dict)
