"""Define exceptions for the input errors in the command line."""


class InvalidAPIKeyError(Exception):
    """Exception raised for invalid API key."""
    pass


class MissingAPIKeyError(Exception):
    """Exception raised for missing API key."""
    pass


class WrongFormatAPIKeyError(Exception):
    """Exception raised for wrong format API key."""
    pass
