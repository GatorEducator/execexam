"""This module contains the pytest plugin for the execexam package."""

from typing import Any

# create the report dictionary
report: dict[str, Any] = {}


def pytest_runtest_protocol(item, nextitem):
    """Track when a test case is run."""
    global report
    report["nodeid"] = item.nodeid


def pytest_assertrepr_compare(config, op, left, right):
    """Prints out the values of the left and right sides of an assertion."""
    print(
        f"NICE pytest_assertrepr_compare! Assertion is {op} with {left} and {right}"
    )
    return [f"{left} {op} {right}"]


def pytest_exception_interact(node, call, report):
    """Interacts with exceptions."""
    if isinstance(call.excinfo.value, AssertionError):
        print(
            f"NICE pytest_exception_interact! AssertionError in {node.nodeid}: {call.excinfo.value}"
        )

        repr = call.excinfo.getrepr(showlocals=True, style="short")
        print(
            f"HIYA AssertionError occurred at line {repr.reprtraceback.reprentries[-1].lines} in {node.nodeid}: {call.excinfo.value}"
        )

        print(f"NICE, here is the type data for node: {dir(node)}")
        print(
            f"NICE, showing details about the report --> lineno: {report.location[1]}"
        )
        print(f"NICE, here is the type data for call: {dir(call.excinfo)}")
        print(f"NICE, here is the call traceback: {call.excinfo.traceback}")
        last_traceback_entry = call.excinfo.traceback[-1]
        print(
            f"COOL, AssertionError occurred at line {last_traceback_entry.lineno} in {node.nodeid}: {call.excinfo.value}"
        )


def pytest_assertion_pass(item, lineno, orig, expl):
    """Prints that an assertion was run and the message that went along with the assertion."""
    print(
        f"NICE pytest_assertion_pass! Assertion passed in {item.nodeid} at line {lineno} for {orig}: {expl}"
    )
