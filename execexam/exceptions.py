"""Define exceptions for the input errors in the command line."""

import sys
from rich.console import Console

def get_litellm_traceback() -> None:
    """Print the traceback of the last exception."""
    exc_type, exc_obj, exc_tb = sys.exc_info()

    # List of litellm exception types and their explanations
    litellm_exceptions = {
        'NotFoundError': "The requested resource was not found. Please check if your model or endpoint is correct.",
        'AuthenticationError': "There was an issue with your authentication. Please verify your API key.",
        'RateLimitError': "You've hit the rate limit. Please try again later or adjust your usage. This error can also be caused by the ",
        'InvalidRequestError': "Your request was malformed. Please check the parameters you've sent.",
        'APIError': "An internal API error occurred. Please try again later.",
        'ConnectionError': "There was a connection issue. Please ensure your internet connection is stable."
    }

    if exc_type.__name__ in litellm_exceptions:
        print(f"[bold red]Exception Type: {exc_type.__name__}[/bold red]")
        print(f"Explanation: {litellm_exceptions[exc_type.__name__]}")
    else:
        # Default behavior for non-litellm exceptions
        print(f"[bold red]Exception Type: {exc_type.__name__}[/bold red]")
        print(f"Error Message: {str(exc_obj)}")

class GeneralLiteLLMException(Exception):
    """Exception raised for general lite llm issues."""
    def __init__(self, console: Console):
        console.print("\n[bold red]If your issue persists, ensure the model you entered is listed below:[/bold red]")
        console.print("anthropic/claude-3-haiku-20240307")
        console.print("anthropic/claude-3-opus-20240229")
        console.print("groq/llama3-8b-8192")
        console.print("openrouter/meta-llama/llama-3.1-8b-instruct:free")
        console.print("openrouter/google/gemma-2-9b-it:free")
        super().__init__()
