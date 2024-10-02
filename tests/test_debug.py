"""Test cases for debug.py file."""

import pytest
from execexam.debug import Debug, messages, debug, has_debugging_messages, get_debugging_messages

@pytest.fixture(autouse=True)
def clear_messages():
    """Fixture to clear messages before each test."""
    messages.clear()

def test_enum_values():
    assert Debug.get_advice_with_llm.value == "[green]\u2714 Correctly requested and received advice from an LLM."
    assert Debug.parameter_check_passed.value == "[green]\u2714 Validity check passed for command-line arguments."
    assert Debug.pytest_passed_with_marks.value == "[green]\u2714 Correctly ran pytest when using marks."
    assert Debug.pytest_passed_without_marks.value == "[green]\u2714 Correctly ran pytest when not using marks."

def test_messages_list_initially_empty():
    assert messages == []

def test_add_message():
    messages.append(Debug.get_advice_with_llm.value)
    assert Debug.get_advice_with_llm.value in messages

def test_clear_messages():
    messages.append(Debug.get_advice_with_llm.value)
    messages.clear()
    assert messages == []

def test_debug_function():
    debug(True, "Test message")
    assert "Test message" in messages
    debug(False, "Another message")
    assert "Another message" not in messages

def test_has_debugging_messages():
    assert not has_debugging_messages()
    messages.append("Test message")
    assert has_debugging_messages()

def test_get_debugging_messages():
    assert get_debugging_messages() == ""
    messages.append("Test message")
    assert get_debugging_messages() == "\nTest message\n"