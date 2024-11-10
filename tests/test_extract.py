"""Test cases for the extract.py file."""

from pathlib import Path

import importlib
import pytest
import os
import sys
from hypothesis import given, settings
from hypothesis.strategies import dictionaries, text

from execexam.extract import (
    extract_details,
    extract_failing_test_details,
    extract_test_assertion_details,
    extract_test_assertion_details_list,
    extract_test_assertions_details,
    extract_test_output,
    extract_test_output_multiple_labels,
    extract_test_run_details,
    is_failing_test_details_empty,
    extract_tested_functions,
    get_called_functions_from_test,
    function_exists_in_file,
    find_source_file,
    extract_tracebacks,
    extract_function_code_from_traceback,
)


def test_extract_details():
    """Confirm that extracting details from a dictionary works."""
    details = {"key1": "value1", "key2": "value2", "key3": "value3"}
    result = extract_details(details)
    assert result == "Details: value1 key1, value2 key2, value3 key3"


@settings(max_examples=2)
@given(
    dictionaries(
        keys=text(),
        values=text(),
    )
)
@pytest.mark.fuzz
def test_extract_details_hypothesis(details):
    """Test extracting details from a dictionary using hypothesis."""
    result = extract_details(details)
    # If the dictionary is empty, the expected result is an empty string
    if not details:
        expected_result = ""
    else:
        expected_result = "Details: " + ", ".join(
            f"{v} {k}" for k, v in details.items()
        )
    assert result == expected_result


def test_extract_test_run_details():
    """Test extracting details from a test run summary."""
    # check a simple example
    details = {"summary": {"passed": 2, "total": 2, "collected": 2}}
    result = extract_test_run_details(details)
    assert result == "Details: 2 passed, 2 total, 2 collected"
    # check a modified simple example
    details = {"summary": {"failed": 1, "total": 3, "collected": 3}}
    result = extract_test_run_details(details)
    assert result == "Details: 1 failed, 3 total, 3 collected"
    # check a empty example
    details = {"summary": {}}
    result = extract_test_run_details(details)
    assert result == ""


def test_extract_test_assertion_details():
    """Confirm that extract details about a test assertion works."""
    test_details = {
        "assertion1": "value1",
        "assertion2": "value2",
        "assertion3": "value3",
    }
    expected_output = (
        "  - assertion1: value1\n"
        "    assertion2: value2\n"
        "    assertion3: value3\n"
    )
    assert extract_test_assertion_details(test_details) == expected_output


def test_extract_test_assertion_details_list():
    """Confirm that extracting details about a list of test assertions works."""
    test_details_list = [
        {
            "assertion1": "value1",
            "assertion2": "value2",
        },
        {
            "assertion3": "value3",
            "assertion4": "value4",
        },
    ]
    expected_output = (
        "  - assertion1: value1\n"
        "    assertion2: value2\n"
        "  - assertion3: value3\n"
        "    assertion4: value4\n"
    )
    assert (
        extract_test_assertion_details_list(test_details_list)
        == expected_output
    )


def test_extract_test_assertions_details():
    """Confirm that extracting details about test assertions works."""
    test_reports = [
        {
            "nodeid": "/path/to/test_file.py::test_name1",
            "assertions": [
                {
                    "assertion1": "value1",
                    "assertion2": "value2",
                },
            ],
        },
        {
            "nodeid": "/path/to/test_file.py::test_name2",
            "assertions": [
                {
                    "assertion3": "value3",
                    "assertion4": "value4",
                },
            ],
        },
    ]
    expected_output = (
        "\ntest_file.py::test_name1\n"
        "  - assertion1: value1\n"
        "    assertion2: value2\n"
        "\ntest_file.py::test_name2\n"
        "  - assertion3: value3\n"
        "    assertion4: value4\n"
    )
    assert extract_test_assertions_details(test_reports) == expected_output


def test_extract_failing_test_details():
    """Confirm that extracting details about the failing tests works."""
    # define a dictionary that contains details about failing tests
    failing_test_details = {
        "root": "/home/user/project",
        "tests": [
            {
                "outcome": "failed",
                "nodeid": "test_module.py::test_function",
                "call": {"crash": {"lineno": 10, "message": "AssertionError"}},
            },
            {
                "outcome": "passed",
                "nodeid": "test_module.py::test_function2",
                "call": {"crash": {"lineno": 20, "message": "AssertionError"}},
            },
        ],
    }
    # call the function with the failing test details
    result = extract_failing_test_details(failing_test_details)
    # check the result
    assert len(result) == 2  # noqa: PLR2004
    assert (
        result[0]
        == "\n  Name: test_module.py::test_function\n  Path: /home/user/project/test_module.py\n  Line number: 10\n  Message: AssertionError\n"
    )
    assert len(result[1]) == 1
    assert result[1][0]["test_name"] == "test_function"
    assert str(result[1][0]["test_path"]) == str(
        Path("/home/user/project/test_module.py")
    )


def test_extract_test_output_with_label():
    """Confirm correct filtering out of the lines that contain the label."""
    # define a string that contains the label
    output = "This is a test\nThis is another test\nTest label: This is a test with a label\nAnother test label: This is another test with a label"
    keep_line_label = "label"
    # call the function with the output and the label
    result = extract_test_output(keep_line_label, output)
    # check the result
    assert (
        result
        == "Test label: This is a test with a label\nAnother test label: This is another test with a label\n"
    )


def test_extract_test_output_without_label():
    """Confirm correct filtering out of the lines that do not contain the label."""
    # define a string that does not contain the label
    output = "This is a test\nThis is another test\nThis is a test without a document\nThis is another test without a document"
    keep_line_label = "label"
    # call the function with the output and the label
    result = extract_test_output(keep_line_label, output)
    # check the result
    assert result == ""


def test_is_failing_test_details_empty_with_newline():
    """Confirm returns True when the input string contains only a newline."""
    # define a string that contains only a newline
    details = "\n"
    # call the function with the details
    result = is_failing_test_details_empty(details)
    # check the result
    assert result is True


def test_no_labels():
    """Confirm returns empty string when no labels are provided."""
    output = "This is a test output\nAnother line of output"
    keep_line_labels = []
    expected_output = ""
    assert (
        extract_test_output_multiple_labels(keep_line_labels, output)
        == expected_output
    )


def test_single_label():
    """Confirm returns output when a single label is provided."""
    output = "This is a test output\nAnother line of output"
    keep_line_labels = ["test"]
    expected_output = "This is a test output\n"
    assert (
        extract_test_output_multiple_labels(keep_line_labels, output)
        == expected_output
    )


def test_multiple_labels():
    """Confirm returns output when multiple labels are provided."""
    output = "This is a test output\nAnother line of output\nMore output"
    keep_line_labels = ["test", "More"]
    expected_output = "This is a test output\nMore output\n"
    assert (
        extract_test_output_multiple_labels(keep_line_labels, output)
        == expected_output
    )


def test_is_failing_test_details_empty_with_non_empty_string():
    """Confirm returns False when input contains content but not a newline."""
    # define a string that contains more than a newline
    details = "This is a test"
    # call the function with the details
    result = is_failing_test_details_empty(details)
    # check the result
    assert result is False


def test_is_failing_test_details_empty_with_empty_string():
    """Confirm returns False when the input string is empty."""
    # define an empty string
    details = ""
    # call the function with the details
    result = is_failing_test_details_empty(details)
    # check the result
    assert result is False

def test_extract_tested_functions_no_calls():
    """Test extract_tested_functions with no function calls.""" 
    failing_code = "assert 1 == 1"
    result = extract_tested_functions(failing_code)
    assert result == failing_code, "Should return the full code when no functions are called."

def test_extract_tested_functions_with_calls():
    """Test extract_tested_functions with multiple function calls."""
    failing_code = "func1()\nfunc2()\nassert test_function()"
    result = extract_tested_functions(failing_code)
    assert result == {"func1", "func2"}, "Should extract only the non-test/assert functions."

def test_get_called_functions_from_test_simple():
    """Test get_called_functions_from_test with a simple test function."""
    # Create a temporary test module to use for testing
    try:
        with open("temp_test_module.py", "w") as f:
            f.write("""
def test_sample():
    func_a()
    func_b()
""")
        # Call your function and check the result
        result = get_called_functions_from_test("temp_test_module.py::test_sample")
        assert result == ['test_sample', 'func_a', 'func_b']
    finally:
        # Delete the temporary test module after the test
        if os.path.exists("temp_test_module.py"):
            os.remove("temp_test_module.py")

def test_function_exists_in_file_exists():
    """Test function_exists_in_file when the function exists in the file."""
    # Create a temporary Python file to use for testing
    with open("temp_module.py", "w") as f:
        f.write("def existing_function(): pass")
    result = function_exists_in_file("temp_module.py", "existing_function")
    assert result, "Should return True when function exists in the file."
    os.remove("temp_module.py")

def test_function_exists_in_file_not_exists():
    """Test function_exists_in_file when the function does not exist in the file."""
    # Create a temporary Python file to use for testing
    with open("temp_module.py", "w") as f:
        f.write("def some_other_function(): pass")
    result = function_exists_in_file("temp_module.py", "non_existing_function")
    assert not result, "Should return False when function does not exist in the file."
    os.remove("temp_module.py")

def test_find_source_file_simple_import():
    """Test find_source_file with a simple import."""
    # Create a test file with an import statement
    with open("test_file.py", "w") as f:
        f.write("import module_a\n")
    with open("module_a.py", "w") as f:
        f.write("def test_func(): pass")
    result = find_source_file("test_file.py::test_func", "test_func")
    assert result == "module_a.py", "Should return the correct source file when found."
    os.remove("test_file.py")
    os.remove("module_a.py")

def test_extract_tracebacks_no_failures():
    """Test extract_tracebacks with no failures in the JSON report."""
    # Create a simple JSON report for testing that passes
    json_report = {"tests": [{"outcome": "passed", "nodeid": "test_module.py::test_function"}]}
    # Check the results are empty when the report passed
    result = extract_tracebacks(json_report, "sample failing code")
    assert result == [], "Should return an empty list when no failures are present."

def test_extract_tracebacks_with_failures():
    """Test extract_tracebacks with a failure in the JSON report."""
    # Create a test file `my_tests.py` with a failing test
    with open("my_tests.py", "w") as f:
        f.write("""
def test_sample():
    assert False, "test failed"
""")
    # Create a test JSON report with a failure
    json_report = {
        "tests": [
            {
                "outcome": "failed",
                "nodeid": "my_tests.py::test_sample",
                "call": {"longrepr": "E   AssertionError: test failed\nFile 'my_tests.py', line 3"}
            }
        ]
    }
    result = extract_tracebacks(json_report, "def func_a(): pass")
    assert isinstance(result, list), "The result should be a list of tracebacks"
    assert len(result) == 1, "There should be one traceback in the result"
    assert result[0]['error_type'] == "AssertionError", "The error_type should be 'AssertionError'"
    assert "test failed" in result[0]['full_traceback'], "The traceback should contain the error message 'test failed'"
    os.remove("my_tests.py")

def test_extract_function_code_from_traceback():
    """Test extract_function_code_from_traceback with a sample function."""
    # Create a source file with a sample function
    with open("source_file.py", "w") as f:
        f.write("""\
def sample_func():
    return True
""")
    # Prepare traceback info list for testing
    traceback_info_list = [
        {"source_file": "source_file.py", "tested_function": "sample_func"}
    ]
    # Extract the function code from the traceback
    result = extract_function_code_from_traceback(traceback_info_list)
    assert result is not None
    assert any("sample_func" in line for sublist in result for line in sublist)
    os.remove("source_file.py")