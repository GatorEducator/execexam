"""Testing for the advise module"""

from socket import timeout as SocketTimeout
from unittest.mock import Mock, patch

import pytest

from execexam.advise import (
    check_internet_connection,
    validate_url,
)


# Test for validate_url function
def test_validate_url():
    """Validates proper URL invalidates improper URL."""
    # Test with an invalid URL
    result = validate_url("invalid-url")
    assert not result

    # Test with an empty string
    result = validate_url("")
    assert not result

    # Test with a URL that includes spaces
    result = validate_url("https://example .com")
    assert not result

    # Test with valid URL
    result = validate_url("https://developerdevelopment.com/")
    assert result

    # Test with another valid URL
    result = validate_url("https://developerdevelopment.com/schedule/")
    assert result


def test_check_internet_connection_success():
    """Test that check_internet_connection returns True when connection is successful."""
    with patch("socket.create_connection") as mock_create_connection:
        # Mock random.choice to always return the first DNS server
        with patch("random.choice", return_value=("8.8.8.8", 53)):
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


@pytest.mark.parametrize(
    "dns_server",
    [
        ("8.8.8.8", 53),  # Google DNS
        ("1.1.1.1", 53),  # Cloudflare DNS
        ("9.9.9.9", 53),  # Quad9 DNS
        ("208.67.222.222", 53),  # OpenDNS
    ],
)
def test_check_internet_connection_different_dns(dns_server):
    """Test that check_internet_connection works with different DNS servers."""
    with patch("socket.create_connection") as mock_create_connection:
        with patch("random.choice", return_value=dns_server):
            mock_create_connection.return_value = Mock()
            assert check_internet_connection() is True
            mock_create_connection.assert_called_once_with(
                dns_server, timeout=5
            )
