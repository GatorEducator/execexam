from socket import timeout as SocketTimeout
from unittest.mock import Mock, patch

import pytest

from execexam.advise import check_internet_connection


def test_check_internet_connection_success():
    """Test that check_internet_connection returns True when connection is successful."""
    with patch("socket.create_connection") as mock_create_connection:
        mock_create_connection.return_value = Mock()
        assert check_internet_connection() is True
        mock_create_connection.assert_called_once_with(
            ("8.8.8.8", 53), timeout=5
        )


def test_check_internet_connection_failure():
    """Test that check_internet_connection returns False when connection fails."""
    with patch(
        "socket.create_connection",
        side_effect=OSError("Network is unreachable"),
    ):
        assert check_internet_connection() is False


def test_check_internet_connection_timeout():
    """Test that check_internet_connection handles timeout correctly."""
    with patch(
        "socket.create_connection",
        side_effect=SocketTimeout("Connection timed out"),
    ):
        assert check_internet_connection() is False


@pytest.mark.parametrize("timeout", [1, 5, 10])
def test_check_internet_connection_custom_timeout(timeout):
    """Test that check_internet_connection respects custom timeout values."""
    with patch("socket.create_connection") as mock_create_connection:
        mock_create_connection.return_value = Mock()
        assert check_internet_connection(timeout=timeout) is True
        mock_create_connection.assert_called_once_with(
            ("8.8.8.8", 53), timeout=timeout
        )
