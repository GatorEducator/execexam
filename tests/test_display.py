"""Testing for display module."""

from typing import Any, Dict


def make_colon_separated_string(arguments: Dict[str, Any]) -> str:
    """Make a colon separated string from a dictionary."""
    return "\n" + "\n".join(
        f"- {key}: {value}" for key, value in arguments.items()
    )


# Tests
def test_make_colon_separated_string():
    """Function tests colon separated string outputs with different dictionaries."""
    # Basic dictionary test
    input_dictionary = {"key1": "value1", "key2": "value2"}
    expected_output = "\n- key1: value1\n- key2: value2"
    assert make_colon_separated_string(input_dictionary) == expected_output

    # Test with an empty dictionary
    input_dictionary = {}
    expected_output = "\n"
    assert make_colon_separated_string(input_dictionary) == expected_output

    # Test with numbers
    input_dictionary = {"key1": 123, "key2": 25.5}
    expected_output = "\n- key1: 123\n- key2: 25.5"
    assert make_colon_separated_string(input_dictionary) == expected_output

    # Test with mixed types
    input_dictionary = {"key1": "value1", "key2": None, "key3": [1, 2, 3]}
    expected_output = "\n- key1: value1\n- key2: None\n- key3: [1, 2, 3]"
    assert make_colon_separated_string(input_dictionary) == expected_output

    # Test special characters
    input_dictionary = {"key1": "!@#$%", "key2": "value2/*&"}
    expected_output = "\n- key1: !@#$%\n- key2: value2/*&"
    assert make_colon_separated_string(input_dictionary) == expected_output
