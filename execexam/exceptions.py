"""Define exceptions for the input errors in the command line."""

import sys

# from rich.console import Console (ask if i need to import this?) i dont think i do because i pass it as an atg


def get_litellm_traceback(console) -> None:
    """Print the traceback of the last exception."""
    exc_type, exc_obj, _ = sys.exc_info()

    if exc_type is None:
        return
    # List of litellm exception types and their explanations
    litellm_exceptions = {
        "NotFoundError": "LLM resource not found. Please check your model and/or endpoint.",
        "AuthenticationError": "API authentication failed. Please verify your API key.",
        "RateLimitError": "Rate limit exceeded. Wait and retry or check API key.\nNOTE: This error can sometimes be caused by an invalid API key.",
        "InvalidRequestError": "Malformed API request. Please review parameters.",
        "APIError": "Internal LLM API error. Retry later.",
        "APIConnectionError": "Connection failed. \nNOTE: This error can sometimes be caused by an invalid server URL. Verify your server URL.",
    }

    # if statements to display exceptions
    if exc_type.__name__ in litellm_exceptions:
        console.print(
            f"[bold red]Exception Type: {exc_type.__name__}[/bold red]"
        )
        console.print(f"Explanation: {litellm_exceptions[exc_type.__name__]}")
    else:
        # default behavior for non-litellm exceptions
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
