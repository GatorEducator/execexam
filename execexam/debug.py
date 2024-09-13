"""Utility functions to record and produce debugging logs."""

from enum import Enum
from typing import List

# list of debugging messages
messages: List[str] = []


class Debug(str, Enum):
    """An enumeration of the various debugging messages."""

    get_advice_with_llm = (
        "[green]\u2714 Correctly requested and received advice from an LLM."
    )
    parameter_check_passed = (
        "[green]\u2714 Validity check passed for command-line arguments."
    )
    pytest_passed_with_marks = (
        "[green]\u2714 Correctly ran pytest when using marks."
    )
    pytest_passed_without_marks = (
        "[green]\u2714 Correctly ran pytest when not using marks."
    )
    started_litellm_thread = "[green]\u2714 Correctly started LiteLLM thread."
    stopped_litellm_thread = "[green]\u2714 Correctly stopped LiteLLM thread."
    started_capturing_output = (
        "[green]\u2714 Started to capture standard output and error."
    )
    stopped_capturing_output = (
        "[green]\u2714 Stopped capturing standard output and error."
    )


def debug(allow: bool, message: str) -> None:
    """Record a debugging message."""
    if allow:
        messages.append(message)


def has_debugging_messages() -> bool:
    """Determine if there are debugging messages."""
    return len(messages) > 0


def get_debugging_messages() -> str:
    """Retrieve a formatted version of the debugging messages."""
    # there are debugging messages; create a single
    # string with newlines at the start and the end
    # of the block of debugging messages
    if messages:
        all_messages = "\n" + "\n".join(messages)
        return all_messages + "\n"
    # there are no debugging messages and thus
    # this function must return an empty string
    return ""
