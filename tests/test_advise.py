"""Testing for the advise module"""

import pytest
from rich.console import Console

from execexam.advise import (
    check_advice_model,
    check_advice_server,
    enumerations,
    validate_url,
)


# Test for validate_url function
def test_validate_url():
    """Validates proper URL invalidates improper URL."""
    # Test with an invalid URL
    result = validate_url("invalid-url")
    assert not result

    # Test with an empty string
    result = validate_url("")
    assert not result

    # Test with a URL that includes spaces
    result = validate_url("https://example .com")
    assert not result

    # Test with valid URL
    result = validate_url("https://developerdevelopment.com/")
    assert result

    # Test with another valid URL
    result = validate_url("https://developerdevelopment.com/schedule/")
    assert result


def test_check_advice_model_exit_on_none_model():
    """Test check_advice_model function with exit code"""
    console = Console()
    report = [enumerations.ReportType.testadvice]
    advice_model = None

    # Expect a SystemExit to be raised
    with pytest.raises(SystemExit) as exc_info:
        check_advice_model(console, report, advice_model)

    # Assert exit code
    assert exc_info.value.code == 1


def test_check_advice_server_invalid_url():
    """Test that the function runs when server URL is invalid"""
    console = Console()
    report = [
        enumerations.ReportType.testadvice
    ]  # report indicating advice needed
    advice_method = enumerations.AdviceMethod.api_server  # set advice to API
    advice_server = "invalid-url"  # set invalid URL to create error

    # Expect SystemExit to be raised when server is called
    with pytest.raises(SystemExit) as exc_info:
        check_advice_server(console, report, advice_method, advice_server)

    # assert exit code
    assert exc_info.value.code == 1
