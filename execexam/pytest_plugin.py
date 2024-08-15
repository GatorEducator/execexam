"""This module contains the pytest plugin for the execexam package."""

from typing import Any, List

# create the report list of
# dictionaries that are organized by nodeid
reports: List[dict[str, Any]] = []


def pytest_runtest_protocol(item, nextitem):
    """Track when a test case is run."""
    global reports
    # create a new dictionary for the report
    # and add it to the report list
    reports.append({"nodeid": item.nodeid})


# def pytest_assertrepr_compare(config, op, left, right):
#     """Prints out the values of the left and right sides of an assertion."""
#     print(
#         f"NICE pytest_assertrepr_compare! Assertion is {op} with {left} and {right}"
#     )
#     return [f"{left} {op} {right}"]


def pytest_exception_interact(node, call, report):
    """Interacts with exceptions."""
    global reports  # noqa: PLW0602
    # there was an assertion error and thus
    # the plugin must extract details about what failed
    if isinstance(call.excinfo.value, AssertionError):
        # create an empty dictionary for the test report
        current_test_report = {}
        # find the test report for this specific test that
        # has a passing assertion
        for current_report in reports:
            # found the test report for this specific test
            # based on what matches according to the nodeid
            if current_report["nodeid"] == node.nodeid:
                current_test_report = current_report
        # one of the test reports was found
        # and thus we can store information about this assertion
        if current_test_report is not {}:
            # extract the data to the values we can store
            # --> extract the line number
            last_traceback_entry = call.excinfo.traceback[-1]
            lineno = last_traceback_entry.lineno + 1
            # --> extract the error message and the exact
            # assertion from data that looks like this:
            # "Minimum negative value in matrix assert (-4 == 1)"
            # extract the part before 'assert'
            assertion_output = str(call.excinfo.value)
            orig = assertion_output.split("assert")[0].strip()
            # extract the part inside the parentheses
            expl = assertion_output.split("(")[1].split(")")[0]
            # there is no data about assertions for this test
            if current_test_report.get("assertions") is None:
                # create an empty dictionary for the data about
                # this assertion and then add the needed fields
                current_assertion_dict = {}
                current_assertion_dict["Line"] = lineno
                current_assertion_dict["Exact"] = expl
                current_assertion_dict["Error"] = orig
                # create a new list and add the dictionary with
                # the details about this assertion to the new list
                assertions_dictionary_list = [current_assertion_dict]
                current_test_report["assertions"] = assertions_dictionary_list
            # there is already data about assertions for this test
            else:
                # create an empty dictionary for the data about
                # this assertion and then add the needed fields
                current_assertion_dict = {}
                current_assertion_dict["Line"] = lineno
                current_assertion_dict["Exact"] = expl
                current_assertion_dict["Error"] = orig
                # there is an existing list of assertion dictionaries
                # for this test case and thus we must add a new one to it
                current_test_report["assertions"].append(current_assertion_dict)
        print(
            f"NICE pytest_exception_interact! AssertionError in {node.nodeid}: **{call.excinfo.value}**"
        )
        print(
            f"NICE pytest_exception_interact! AssertionError extrac **{dir(call.excinfo.value)}**"
        )
        # repr = call.excinfo.getrepr(showlocals=True, style="short")
        # print(
        #     f"HIYA AssertionError occurred at line {repr.reprtraceback.reprentries[-1].lines} in {node.nodeid}: {call.excinfo.value}"
        # )
        # print(f"NICE, here is the type data for node: {dir(node)}")
        # print(
        #     f"NICE, showing details about the report --> lineno: {report.location[1]}"
        # )
        # print(f"NICE, here is the type data for call: {dir(call.excinfo)}")
        # print(f"NICE, here is the call traceback: {call.excinfo.traceback}")
        # last_traceback_entry = call.excinfo.traceback[-1]
        # print(
        #     f"COOL, AssertionError occurred at line {last_traceback_entry.lineno} in {node.nodeid}: {call.excinfo.value}"
        # )


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
        # there is no data about assertions for this test
        if current_test_report.get("assertions") is None:
            # create an empty dictionary for the data about
            # this assertion and then add the needed fields
            current_assertion_dict = {}
            current_assertion_dict["Line"] = lineno
            current_assertion_dict["Code"] = orig
            current_assertion_dict["Exact"] = expl
            # create a new list and add the dictionary with
            # the details about this assertion to the new list
            assertions_dictionary_list = [current_assertion_dict]
            current_test_report["assertions"] = assertions_dictionary_list
        # there is already data about assertions for this test
        else:
            # create an empty dictionary for the data about
            # this assertion and then add the needed fields
            current_assertion_dict = {}
            current_assertion_dict["Line"] = lineno
            current_assertion_dict["Code"] = orig
            current_assertion_dict["Exact"] = expl
            # there is an existing list of assertion dictionaries
            # for this test case and thus we must add a new one to it
            current_test_report["assertions"].append(current_assertion_dict)
