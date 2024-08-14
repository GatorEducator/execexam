"""Supporting assertions for test suites using execexam."""


def assert_and_print(expected, actual, message):
    """Print a diagnostic message and assert that the expected and actual values are equal."""
    print(f"{message}: Expected {expected}, got {actual}")  # noqa: T201
    assert expected == actual
