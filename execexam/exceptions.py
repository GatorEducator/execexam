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

class InvalidAPIKeyError(Exception):
    """Exception raised for invalid API key."""
    pass

class MissingAPIKeyError(Exception):
    """Exception raised for missing API key."""
    pass

class WrongFormatAPIKeyError(Exception):
    """Exception raised for wrong format API key."""
    pass

class MissingServerURLError(Exception):
    """Exception raised for missing server URL."""
    pass

class InvalidServerURLError(Exception):
    """Exception raised for invalid server URL."""
    pass

class ConnectionError(Exception):
    """Exception raised for connection error."""
    pass

class ExceededAPIRequestsError(Exception):
    """Exception raised for exceeding API requests."""
    pass

class InternalServerError(Exception):
    """Exception raised for internal server error."""
    pass

def handle_invalid_api_key(console: Console) -> None:
    """Handle invalid API key error."""
    error_handle(console, 401)

def handle_missing_api_key(console: Console) -> None:
    """Handle missing API key error."""
    console.print("[bold red]Error: No API key provided.[/bold red]")
    console.print("Please provide an API key in the configuration file.")

def handle_wrong_format_api_key(console: Console) -> None:
    """Handle wrong format API key error."""
    console.print("[bold red]Error: API key format is incorrect.[/bold red]")
    console.print("Ensure the API key does not contain extra characters or spaces.")

def handle_missing_server_url(console: Console) -> None:
    """Handle missing server URL error."""
    console.print("[bold red]Error: No server URL provided.[/bold red]")
    console.print("Please provide a server URL. Check your configuration file.")

def handle_invalid_server_url(console: Console) -> None:
    """Handle invalid server URL error."""
    error_handle(console, 404)

def handle_connection_error(console: Console) -> None:
    """Handle connection error."""
    error_handle(console, 503)

def handle_exceeded_requests(console: Console) -> None:
    """Handle exceeded API requests error."""
    error_handle(console, 429)

def handle_internal_server_error(console: Console) -> None:
    """Handle internal server error."""
    error_handle(console, 500)

def error_handle(console: Console, status: int) -> None:
    """Function that checks to see if the error is among the error messages otherwise it prints 'Unknown error'."""
    if status in ERROR_MESSAGES:
        console.print(f"[bold red]{ERROR_MESSAGES[status]}[/bold red]")
    else:
        console.print("[bold red]Unknown error[/bold red]")