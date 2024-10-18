"""Test cases for the display.py file."""

from typing import Any, Dict
from execexam.display import make_colon_separated_string, get_display_return_code
from rich.console import Console
from execexam.enumerations import ReportType


"""Test cases for the display.py file."""

from execexam.display import (
    make_colon_separated_string,
    get_display_return_code,
    display_advice,
    display_content,
)


def test_make_colon_separated_string():
    """Function tests colon separated string outputs with different dictionaries."""
    # Basic dictionary test
    input_dictionary = {"key1": "value1", "key2": "value2"}
    expected_output = "\n- key1: value1\n- key2: value2\n"  # Include trailing newline
    assert make_colon_separated_string(input_dictionary) == expected_output
    # Test with an empty dictionary
    input_dictionary = {}
    expected_output = "\n"
    assert make_colon_separated_string(input_dictionary) == expected_output
    # Test with numbers
    input_dictionary = {"key1": 123, "key2": 25.5}
    expected_output = "\n- key1: 123\n- key2: 25.5\n"  # Include trailing newline
    assert make_colon_separated_string(input_dictionary) == expected_output
    # Test with mixed types
    input_dictionary = {"key1": "value1", "key2": 25.5, "key3": None}
    expected_output = "\n- key1: value1\n- key2: 25.5\n- key3: None\n"  # Include trailing newline
    assert make_colon_separated_string(input_dictionary) == expected_output


def test_get_display_return_code():
    """Function tests the return code display."""
    # Test with fancy display
    assert get_display_return_code(0, True) == "Success"
    assert get_display_return_code(1, True) == "Failure"
    # Test without fancy display
    assert get_display_return_code(0, False) == "0"
    assert get_display_return_code(1, False) == "1"


def test_display_advice():
    """Function tests the display advice."""
    # Test with no errors
    assert display_advice(0) == "\n[green]\u2714 Advise requested, but none is needed!\n"
    # Test with errors
    assert display_advice(1) == "\n[red]\u2718 Advise requested, and will be provided!\n"


def test_display_content():
    """Function tests the display content."""
    console = Console()
    content = "print('Hello, World!')"
    label = "Test Label"

    # Test with rich text and syntax highlighting
    display_content(
        console,
        ReportType.all,
        [ReportType.all],
        content,
        label,
        richtext=True,
        syntax=True,
        syntax_theme="ansi_dark",
        syntax_language="python",
        newline=True,
    )

    # Test with rich text without syntax highlighting
    display_content(
        console,
        ReportType.all,
        [ReportType.all],
        content,
        label,
        richtext=True,
        syntax=False,
        syntax_theme="ansi_dark",
        syntax_language="python",
        newline=True,
    )

    # Test without rich text but with syntax highlighting
    display_content(
        console,
        ReportType.all,
        [ReportType.all],
        content,
        label,
        richtext=False,
        syntax=True,
        syntax_theme="ansi_dark",
        syntax_language="python",
        newline=False,
    )

    # Test without rich text and without syntax highlighting
    display_content(
        console,
        ReportType.all,
        [ReportType.all],
        content,
        label,
        richtext=False,
        syntax=False,
        syntax_theme="ansi_dark",
        syntax_language="python",
        newline=False,
    )


def test_get_display_return_code():
    """Function tests the return code display."""
    # Test with fancy display
    assert get_display_return_code(0, True) == "\n[green]\u2714 All checks passed.\n"
    assert get_display_return_code(1, True) == "\n[red]\u2718 One or more checks failed.\n"
    # Test without fancy display
    assert get_display_return_code(0, False) == "\n[green]\u2714 All checks passed."
    assert get_display_return_code(1, False) == "\n[red]\u2718 One or more checks failed."
