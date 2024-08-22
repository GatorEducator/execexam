"""Test cases for the convert module."""

from pathlib import Path

from execexam.convert import path_to_string


def test_path_to_string():
    # path that has more than 4 parts
    path = Path("/home/user/documents/work/project/file.txt")
    result = path_to_string(path)
    assert result == "<...>/documents/work/project/file.txt"
    # path that has exactly 4 parts
    path = Path("/home/user/documents/work")
    result = path_to_string(path)
    assert result == "/home/user/documents/work"
    # path that has less than 4 parts
    path = Path("/home/user/documents")
    result = path_to_string(path)
    assert result == "/home/user/documents"
