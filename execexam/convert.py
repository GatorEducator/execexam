"""Perform data conversions."""

from pathlib import Path


def path_to_string(path_name: Path, levels: int = 4) -> str:
    """Convert the path to an elided version of the path as a string."""
    # break the path into parts
    parts = path_name.parts
    # note that this uses the - 1 after len
    # because the first part is always the root
    # (for instance, on Unix-like systems, '/'
    # and on Windows, 'C:\')
    if len(parts) - 1 > levels:
        start_index = len(parts) - levels
        return Path("<...>", *parts[start_index:]).as_posix()
    else:
        return path_name.as_posix()
