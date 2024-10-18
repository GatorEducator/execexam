"""Utility functions for the execexam package."""

import pytest


def determine_execexam_return_code(pytest_return_code: int) -> int:
    """Determine the return code for the execexam command by pytest code."""
    execexam_return_code = 0
    # see if the pytest exit code is one of the designated
    # codes and then assign it to the appropriate value
    if pytest_return_code == pytest.ExitCode.TESTS_FAILED:
        execexam_return_code = 1
    elif pytest_return_code == pytest.ExitCode.INTERRUPTED:
        execexam_return_code = 2
    elif pytest_return_code == pytest.ExitCode.INTERNAL_ERROR:
        execexam_return_code = 3
    elif pytest_return_code == pytest.ExitCode.USAGE_ERROR:
        execexam_return_code = 4
    elif pytest_return_code == pytest.ExitCode.NO_TESTS_COLLECTED:
        execexam_return_code = 5
    return execexam_return_code
