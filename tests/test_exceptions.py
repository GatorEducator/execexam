"""Test Suite for Exceptions Module."""

from unittest.mock import patch

from rich.console import Console

from execexam.exceptions import get_litellm_traceback

# Create a console object for testing
console = Console()


def test_not_found_error():
    """Test case for NotFoundError."""
    # Mocking sys.exc_info to simulate a NotFoundError exception
    with patch(
        "sys.exc_info",
        return_value=(
            type("NotFoundError", (Exception,), {}),
            Exception("Resource not found"),
            None,
        ),
    ):
        with patch("rich.console.Console.print") as mock_print:
            # Call the function to get the traceback
            get_litellm_traceback(console)
            # Assert that the correct messages are printed for NotFoundError
            mock_print.assert_any_call(
                "[bold red]Exception Type: NotFoundError[/bold red]"
            )
            mock_print.assert_any_call(
                "Explanation: LLM resource not found. Please check your model and/or endpoint."
            )


def test_authentication_error():
    """Test case for AuthenticationError."""
    # Mocking sys.exc_info to simulate an AuthenticationError exception
    with patch(
        "sys.exc_info",
        return_value=(
            type("AuthenticationError", (Exception,), {}),
            Exception("Authentication failed"),
            None,
        ),
    ):
        with patch("rich.console.Console.print") as mock_print:
            # Call the function to get the traceback
            get_litellm_traceback(console)
            # Assert that the correct messages are printed for AuthenticationError
            mock_print.assert_any_call(
                "[bold red]Exception Type: AuthenticationError[/bold red]"
            )
            mock_print.assert_any_call(
                "Explanation: API authentication failed. Please verify your API key."
            )


def test_rate_limit_error():
    """Test case for RateLimitError."""
    # Mocking sys.exc_info to simulate a RateLimitError exception
    with patch(
        "sys.exc_info",
        return_value=(
            type("RateLimitError", (Exception,), {}),
            Exception("Rate limit exceeded"),
            None,
        ),
    ):
        with patch("rich.console.Console.print") as mock_print:
            # Call the function to get the traceback
            get_litellm_traceback(console)
            # Assert that the correct messages are printed for RateLimitError
            mock_print.assert_any_call(
                "[bold red]Exception Type: RateLimitError[/bold red]"
            )
            mock_print.assert_any_call(
                "Explanation: Rate limit exceeded. Wait and retry or check API key.\nNOTE: This error can sometimes be caused by an invalid API key."
            )
