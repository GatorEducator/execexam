"""Test suite for the extract module."""

import pytest
from hypothesis import given
from hypothesis.strategies import dictionaries, text

from execexam.extract import extract_details
from execexam.extract import extract_test_run_details


def test_extract_details():
    """Confirm that extracting details from a dictionary works."""
    details = {"key1": "value1", "key2": "value2", "key3": "value3"}
    result = extract_details(details)
    assert result == "Details: value1 key1, value2 key2, value3 key3"


@given(dictionaries(keys=text(), values=text()))
@pytest.mark.fuzz
def test_extract_details_hypothesis(details):
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
