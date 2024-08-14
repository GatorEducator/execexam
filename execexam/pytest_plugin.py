"""This module contains the pytest plugin for the execexam package."""


def pytest_runtest_protocol(item, nextitem):
    """Prints out when a test case is run."""
    print(f"NICE! Running test: {item.nodeid}")


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


def pytest_assertion_pass(item, lineno, orig, expl):
    """Prints that an assertion was run and the message that went along with the assertion."""
    print(
        f"NICE pytest_assertion_pass! Assertion passed in {item.nodeid} at line {lineno} for {orig}: {expl}"
    )
