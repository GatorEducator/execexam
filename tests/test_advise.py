"""Test Suite for advice module."""
import socket
from unittest.mock import patch
from execexam.advise import check_internet_connection


def test_check_internet_connection_success():
    """Test that check_internet_connection returns True when connection is successful."""
    with patch("socket.create_connection") as mock_create_connection:
        mock_create_connection.return_value = True
        assert check_internet_connection() is True


def test_check_internet_connection_failure():
    """Test that check_internet_connection returns False when connection fails."""
    with patch("socket.create_connection", side_effect=OSError):
        assert check_internet_connection() is False


def test_check_internet_connection_timeout():
    """Test that check_internet_connection handles timeout correctly."""
    with patch("socket.create_connection", side_effect=socket.timeout):
        assert check_internet_connection() is False