"""Test suite for the util module."""

import pytest

from execexam.util import determine_execexam_return_code


def test_determine_execexam_return_code_tests_failed():
    """Confirm a correct exit code."""
    assert determine_execexam_return_code(pytest.ExitCode.TESTS_FAILED) == 1


def test_determine_execexam_return_code_interrupted():
    """Confirm a correct exit code."""
    assert determine_execexam_return_code(pytest.ExitCode.INTERRUPTED) == 2  # noqa: PLR2004


def test_determine_execexam_return_code_internal_error():
    """Confirm a correct exit code."""
    assert determine_execexam_return_code(pytest.ExitCode.INTERNAL_ERROR) == 3  # noqa: PLR2004


def test_determine_execexam_return_code_usage_error():
    """Confirm a correct exit code."""
    assert determine_execexam_return_code(pytest.ExitCode.USAGE_ERROR) == 4  # noqa: PLR2004


def test_determine_execexam_return_code_no_tests_collected():
    """Confirm a correct exit code."""
    assert (
        determine_execexam_return_code(pytest.ExitCode.NO_TESTS_COLLECTED) == 5  # noqa: PLR2004
    )


def test_determine_execexam_return_code_other():
    """Confirm a correct exit code."""
    assert determine_execexam_return_code(0) == 0
