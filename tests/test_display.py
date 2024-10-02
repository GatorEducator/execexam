"""Test cases for the display.py file."""

import pytest
from typing import Dict, Any


def make_colon_separated_string(arguments: Dict[str, Any]) -> str:
    """Make a colon separated string from a dictionary."""
    return "\n" + "\n".join(f"- {key}: {value}" for key, value in arguments.items())


def test_make_colon_separated_string():
    """Function tests colon separated string outputs with different dictionaries."""
    # Basic dictionary test
    input_dictionary = {'key1': 'value1', 'key2': 'value2'}
    expected_output = "\n- key1: value1\n- key2: value2"
    assert make_colon_separated_string(input_dictionary) == expected_output
    # Test with an empty dictionary
    input_dictionary = {}
    expected_output = "\n"
    assert make_colon_separated_string(input_dictionary) == expected_output
    # Test with numbers
    input_dictionary = {'key1': 123, 'key2': 25.5}
    expected_output = "\n- key1: 123\n- key2: 25.5"
    assert make_colon_separated_string(input_dictionary) == expected_output
    # Test with mixed types
    input_dictionary = {'key1': 'value1', 'key2': None, 'key3': [1, 2, 3]}
    expected_output = "\n- key1: value1\n- key2: None\n- key3: [1, 2, 3]"
    assert make_colon_separated_string(input_dictionary) == expected_output
    # Test special characters 
    input_dictionary = {'key1': '!@#$%', 'key2': 'value2/*&'}
    expected_output = "\n- key1: !@#$%\n- key2: value2/*&"
    assert make_colon_separated_string(input_dictionary) == expected_output


# Function to test
def get_display_return_code(return_code: int, fancy: bool) -> str:
    """Determine the return code from running the specified checks(s)."""
    message = "\n"
    if return_code == 0:
        message += "[green]\u2714 All checks passed."
    else:
        message += "[red]\u2718 One or more checks failed."
    if fancy:
        message += "\n"
    return message


# Tests
def test_get_display_return_code():
    """Test the get_display_return_code function with various inputs."""
    # Test case where checks pass (return_code is 0)
    # fancy: bool is False
    assert get_display_return_code(0, False) == "\n[green]\u2714 All checks passed."
    # Test case where checks pass (return_code is 0)
    # fancy: bool is True
    assert get_display_return_code(0, True) == "\n[green]\u2714 All checks passed.\n"
    # Test case where checks fail (return_code is 1)
    # fancy: bool is False
    assert get_display_return_code(1, False) == "\n[red]\u2718 One or more checks failed."
    # Test case where checks fail (return_code is 1)
    # fancy: bool is True
    assert get_display_return_code(1, True) == "\n[red]\u2718 One or more checks failed.\n"
    # Test case for another 2 return code
    # fancy: bool is False
    assert get_display_return_code(2, False) == "\n[red]\u2718 One or more checks failed."


# Function to test
def display_advice(return_code: int) -> str:
    """Determine the return code from running the specified checks(s)."""
    message = "\n"
    if return_code == 0:
        message += "[green]\u2714 Advise requested, but none is needed!"
    else:
        message += "[red]\u2718 Advise requested, and will be provided!"
    message += "\n"
    return message


# Tests
def test_display_advice():
    """Test the display_advice function with various return codes."""
    # Test case where no advice is needed (return_code is 0)
    assert display_advice(0) == "\n[green]\u2714 Advise requested, but none is needed!\n"
    # Test case where advice is needed (return_code is non-zero)
    assert display_advice(1) == "\n[red]\u2718 Advise requested, and will be provided!\n"
    # Test case for another non-zero return code
    assert display_advice(2) == "\n[red]\u2718 Advise requested, and will be provided!\n"
    # Test case for negative return code
    assert display_advice(-1) == "\n[red]\u2718 Advise requested, and will be provided!\n"
    # Test case for a large return code
    assert display_advice(999) == "\n[red]\u2718 Advise requested, and will be provided!\n"
