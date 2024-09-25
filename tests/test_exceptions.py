"""Test Suite for Exceptions Module."""

import pytest
from unittest.mock import patch, MagicMock
from execexam.exceptions import get_litellm_traceback


def test_not_found_error():
    """Test case for NotFoundError."""
    # Mocking sys.exc_info to simulate a NotFoundError exception
    with patch('sys.exc_info', return_value=(type('NotFoundError', (Exception,), {}), Exception("Resource not found"), None)):
        with patch('rich.console.Console.print') as mock_print:
            # Call the function to get the traceback
            get_litellm_traceback()
            # Assert that the correct messages are printed for NotFoundError
            mock_print.assert_any_call("[bold red]Exception Type: NotFoundError[/bold red]")
            mock_print.assert_any_call("Explanation: The requested resource was not found. Please check if your model or endpoint is correct.")


def test_authentication_error():
    """Test case for AuthenticationError."""
    # Mocking sys.exc_info to simulate an AuthenticationError exception
    with patch('sys.exc_info', return_value=(type('AuthenticationError', (Exception,), {}), Exception("Authentication failed"), None)):
        with patch('rich.console.Console.print') as mock_print:
            # Call the function to get the traceback
            get_litellm_traceback()
            # Assert that the correct messages are printed for AuthenticationError
            mock_print.assert_any_call("[bold red]Exception Type: AuthenticationError[/bold red]")
            mock_print.assert_any_call("Explanation: There was an issue with your authentication. Please verify your API key.")


def test_rate_limit_error():
    """Test case for RateLimitError."""
    # Mocking sys.exc_info to simulate a RateLimitError exception
    with patch('sys.exc_info', return_value=(type('RateLimitError', (Exception,), {}), Exception("Rate limit exceeded"), None)):
        with patch('rich.console.Console.print') as mock_print:
            # Call the function to get the traceback
            get_litellm_traceback()
            # Assert that the correct messages are printed for RateLimitError
            mock_print.assert_any_call("[bold red]Exception Type: RateLimitError[/bold red]")
            mock_print.assert_any_call("Explanation: You've hit the rate limit. Please try again later or adjust your usage.\nNOTE: This error can sometimes be caused by an invalid API key.")
