"""Utility functions to record and produce debugging logs."""

from enum import Enum
from typing import List

# list of debugging messages
messages: List[str] = []


class Debug(str, Enum):
    """An enumeration of the various debugging messages."""

    parameter_check_passed = "[green]\u2714 Validity check passed for command-line arguments."


def debug(allow: bool, message: str) -> None:
    """Record a debugging message."""
    if allow:
        messages.append(message)


def has_debugging_messages() -> bool:
    """Determine if there are debugging messages."""
    return len(messages) > 0


def get_debugging_messages() -> str:
    """Retrieve the debugging messages."""
    if messages:
        return "\n".join(messages)
    return ""
