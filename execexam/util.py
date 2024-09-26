"""Utility functions for the execexam package."""

import pytest


def determine_execexam_return_code(pytest_return_code: int) -> str:
    """Determine the return code for the execexam command by pytest code."""
    # see if the pytest exit code is one of the designated codes
    # and then assign it to the appropriate string message
    if pytest_return_code == pytest.ExitCode.TESTS_FAILED:
        return "Tests Failed"
    elif pytest_return_code == pytest.ExitCode.INTERRUPTED:
        return "Interrupted"
    elif pytest_return_code == pytest.ExitCode.INTERNAL_ERROR:
        return "Internal Error"
    elif pytest_return_code == pytest.ExitCode.USAGE_ERROR:
        return "Usage Error"
    elif pytest_return_code == pytest.ExitCode.NO_TESTS_COLLECTED:
        return "No Tests Collected"
    else:
        return "Success"  # Default to success if no errors
