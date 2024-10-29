"""Define exceptions for the input errors in the command line."""

import sys

from rich.console import Console

console = Console()


def get_litellm_traceback() -> None:
    """Print the traceback of the last exception."""
    exc_type, exc_obj, _ = sys.exc_info()

    if exc_type is None:
        return
    # List of litellm exception types and their explanations
    litellm_exceptions = {
        "NotFoundError": "The requested resource was not found. Please check if your model and/or endpoint is correct.",
        "AuthenticationError": "There was an issue with your authentication. Please verify your API key.",
        "RateLimitError": "You've hit the rate limit. Please try again later or adjust your usage.\nNOTE: This error can sometimes be caused by an invalid API key.",
        "InvalidRequestError": "Your request was malformed. Please check the parameters you've sent.",
        "APIError": "An internal API error occurred. Please try again later.",
        "APIConnectionError": "There was a connection issue to the server.\nNOTE: This error can sometimes be caused by an invalid server URL. Please verify the URL you're using.",
    }

    # if statements to display exceptions
    if exc_type.__name__ in litellm_exceptions:
        console.print(
            f"[bold red]Exception Type: {exc_type.__name__}[/bold red]"
        )
        console.print(f"Explanation: {litellm_exceptions[exc_type.__name__]}")
    else:
        # Default behavior for non-litellm exceptions
        console.print(
            f"[bold red]Exception Type: {exc_type.__name__}[/bold red]"
        )
        console.print(f"Error Message: {exc_obj!s}")

    # general purpose ouput as a backup
    console.print(
        "\n[bold red]If your issue persists, ensure the model you entered is correct, such as:[/bold red]"
    )
    console.print("[bold blue]- anthropic/claude-3-haiku-20240307[/bold blue]")
    console.print("[bold blue]- anthropic/claude-3-opus-20240229[/bold blue]")
    console.print("[bold blue]- groq/llama3-8b-8192[/bold blue]")
    console.print(
        "[bold blue]- openrouter/meta-llama/llama-3.1-8b-instruct:free[/bold blue]"
    )

    console.print(
        "\n[bold red]Please visit [bold blue]https://docs.litellm.ai/docs/providers [/bold blue]for more valid LiteLLM models[bold red]"
    )

    console.print(
        "\n[bold red]For server connectivity issues, please visit [bold blue]https://docs.litellm.ai/docs/simple_proxy [/bold blue]for a valid LiteLLM proxy.[/bold red]"
    )
