"""Define exceptions for the input errors in the command line."""

from rich.console import Console

# Dictionary of Error Messages
ERROR_MESSAGES = {
    429: "Error code 429: You have exceeded the allowed API requests.",
    401: "Error code 401: The API key is invalid. Please check your key configuration.",
    404: "Error code 404: The requested resource was not found. Please check the URL.",
    500: "Error code 500: Internal server error.",
    503: "Error code 503: The service is currently unavailable."
}

def error_handle(console: Console, status: int) -> None:
    """Function that checks to see if the error is among the error messages otherwise it prints 'Unknown error'."""
    if status in ERROR_MESSAGES:
        console.print(f"[bold red]{ERROR_MESSAGES[status]}[/bold red]")
    else:
        console.print("[bold red]Unknown error[/bold red]")

class InvalidAPIKeyError(Exception):
    """Exception raised for invalid API key."""
    def __init__(self, console: Console):
        error_handle(console, 401)
        super().__init__()

class MissingAPIKeyError(Exception):
    """Exception raised for missing API key."""
    def __init__(self, console: Console):
        console.print("[bold red]Error: No API key provided.[/bold red]")
        console.print("Please provide an API key in the configuration file.")
        super().__init__()

class WrongFormatAPIKeyError(Exception):
    """Exception raised for wrong format API key."""
    def __init__(self, console: Console):
        console.print("[bold red]Error: API key format is incorrect.[/bold red]")
        console.print("Ensure the API key does not contain extra characters or spaces.")
        super().__init__()

class MissingServerURLError(Exception):
    """Exception raised for missing server URL."""
    def __init__(self, console: Console):
        console.print("[bold red]Error: No server URL provided.[/bold red]")
        console.print("Please provide a server URL. Check your configuration file.")
        super().__init__()

class InvalidServerURLError(Exception):
    """Exception raised for invalid server URL."""
    def __init__(self, console: Console):
        error_handle(console, 404)
        super().__init__()

class ConnectionError(Exception):
    """Exception raised for connection error."""
    def __init__(self, console: Console):
        error_handle(console, 503)
        super().__init__()

class ExceededAPIRequestsError(Exception):
    """Exception raised for exceeding API requests."""
    def __init__(self, console: Console):
        error_handle(console, 429)
        super().__init__()

class InternalServerError(Exception):
    """Exception raised for internal server error."""
    def __init__(self, console: Console):
        error_handle(console, 500)
        super().__init__()

# checker to map error code numbers