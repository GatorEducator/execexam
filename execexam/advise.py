"""Offer advice through the use of the LLM-Based mentoring system."""

import sys
from typing import List, Optional

import openai
import validators
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
import socket

from . import enumerations
from .exceptions import InvalidAPIKeyError, MissingAPIKeyError, WrongFormatAPIKeyError


def load_litellm() -> None:
    """Load the litellm module."""
    # note that the purpose of this function is
    # to allow the loading of the litellm module
    # to take place in a separate thread, thus
    # ensuring that the main interface is not blocked
    global litellm  # noqa: PLW0602
    global completion  # noqa: PLW0603
    from litellm import completion


def validate_url(value: str) -> bool:
    """Validate a URL given as a string using the validators library."""
    if not validators.url(value):
        return False
    return True


def is_valid_api_key(api_key: str) -> bool:
    # Replace with the actual logic to validate the API key
    # For example, you might check if the API key matches a specific pattern
    return api_key.isalnum()  # Example: API key should be alphanumeric

def validate_api_key(api_key: str) -> None:
    """Validate the provided API key."""
    if not api_key:
        raise MissingAPIKeyError()
    if len(api_key) < 20:
        raise WrongFormatAPIKeyError()
    if not is_valid_api_key(api_key):
        raise InvalidAPIKeyError()


def handle_invalid_api_key(console: Console) -> None:
    """Handle invalid API key error."""
    console.print("[bold red]Error: Invalid API key provided.[/bold red]")
    console.print("Please check your API key and update it in the configuration file.")


def handle_missing_api_key(console: Console) -> None:
    """Handle missing API key error."""
    console.print("[bold red]Error: No API key provided.[/bold red]")
    console.print("Please provide an API key in the configuration file.")


def handle_wrong_format_api_key(console: Console) -> None:
    """Handle wrong format API key error."""
    console.print("[bold red]Error: API key format is incorrect.[/bold red]")
    console.print("Ensure the API key does not contain extra characters or spaces.")


def handle_generic_api_key_error(console: Console) -> None:
    """Handle generic API key error."""
    console.print("[bold red]Error: An issue occurred with the API key.[/bold red]")
    console.print("Please check your API key and configuration.")


def handle_invalid_server_url(console: Console) -> None:
    """Handle invalid server URL error."""
    console.print("[bold red]Error: Invalid server URL provided.[/bold red]")
    console.print("Please check the server URL and update it.")


def handle_missing_server_url(console: Console) -> None:
    """Handle missing server URL error."""
    console.print("[bold red]Error: No server URL provided.[/bold red]")
    console.print("Please provide a server URL. Check your configuration file.")


def handle_connection_error(console: Console) -> None:
    """Handle connection error."""
    console.print("[bold red]Error: Unable to connect to the API server.[/bold red]")
    console.print("Please check your network connection and ensure the API server is reachable.")


def check_internet_connection(timeout: int = 5) -> bool:
    """Check if the system has an active internet connection."""
    try:
        # Attempt to connect to Google's DNS server (8.8.8.8) on port 53 (DNS)
        socket.create_connection(("8.8.8.8", 53), timeout=timeout)
        return True
    except OSError:
        return False


def check_advice_model(
    console: Console,
    report: Optional[List[enumerations.ReportType]],
    advice_model: str,
) -> None:
    """Check if the advice request is valid because a model was specified."""
    if (
        report is not None
        and (
            enumerations.ReportType.testadvice in report
            or enumerations.ReportType.all in report
        )
        and advice_model is None
    ):
        return_code = 1
        console.print()
        console.print(
            "[red]The --advice-model option is required when --report includes 'advice' or 'all'"
        )
        sys.exit(return_code)


def check_advice_server(
    console: Console,
    report: Optional[List[enumerations.ReportType]],
    advice_method: str,
    advice_server: str,
) -> None:
    """Check if the advice request is valid because a server was specified."""
    if (
        report is not None
        and (
            enumerations.ReportType.testadvice in report
            or enumerations.ReportType.all in report
        )
        and advice_method == enumerations.AdviceMethod.api_server
        and advice_server is None
    ):
        return_code = 1
        console.print()
        console.print(
            "[red]The --advice-server option is required when --advice-method is 'api_server'"
        )
        sys.exit(return_code)
    elif (
        report is not None
        and (
            enumerations.ReportType.testadvice in report
            or enumerations.ReportType.all in report
        )
        and advice_method == enumerations.AdviceMethod.api_server
        and not validate_url(advice_server)
    ):
        return_code = 1
        console.print()
        console.print(
            "[red]The --advice-server option did not specify a valid URL"
        )
        sys.exit(return_code)


def fix_failures(  # noqa: PLR0913
    console: Console,
    filtered_test_output: str,
    exec_exam_test_assertion_details: str,
    test_overview: str,
    failing_test_details: str,
    failing_test_code: str,
    advice_method: enumerations.AdviceMethod,
    advice_model: str,
    advice_server: str,
    syntax_theme: enumerations.Theme,
    fancy: bool = True,
):
    """Offer advice through the use of the LLM-based mentoring system."""
    with console.status(
        "[bold green] Getting Feedback from ExecExam's Coding Mentor"
    ):
        test_overview = filtered_test_output + exec_exam_test_assertion_details
        llm_debugging_request = (
            "I am an undergraduate student completing a programming examination."
            + "You may never make suggestions to change the source code of the test cases."
            + "Always make suggestions about how to improve the Python source code of the program under test."
            + "Always give Python code in a Markdown fenced code block with your suggested program."
            + "Always start your response with a friendly greeting and overview of what you will provide."
            + "Always conclude by saying that you are making a helpful suggestion but could be wrong."
            + "Always be helpful, upbeat, friendly, encouraging, and concise when making a response."
            + "Your task is to suggest, in a step-by-step fashion, how to fix the bug(s) in the program?"
            + "What follows is all of the information you need to complete the debugging task."
            + f"Here is the test overview with test output and details about test assertions: {test_overview}"
            + f"Here is a brief overview of the test failure information: {failing_test_details}"
            + f"Here is the source code for the one or more failing test(s): {failing_test_code}"
        )

        if advice_method == enumerations.AdviceMethod.api_key:
            try:
                # attempt to validate the key
                validate_api_key(enumerations.AdviceMethod.api_key)
                # submit the debugging request to the LLM-based mentoring system
                # using the specified model and the debugging prompt
                response = completion(  # type: ignore
                    model=advice_model,
                    messages=[{"role": "user", "content": llm_debugging_request}],
                )
                if fancy:
                    console.print(
                        Panel(
                            Markdown(
                                str(
                                    response.choices[0].message.content,  # type: ignore
                                ),
                                code_theme=syntax_theme.value,
                            ),
                            expand=False,
                            title="Advice from ExecExam's Coding Mentor (API Key)",
                            padding=1,
                        )
                    )
                else:
                    console.print(
                        Markdown(
                            str(
                                response.choices[0].message.content,  # type: ignore
                            ),
                            code_theme=syntax_theme.value,
                        ),
                    )
                    console.print()
            except InvalidAPIKeyError:
                handle_invalid_api_key(console)
            except MissingAPIKeyError:
                handle_missing_api_key(console)
            except WrongFormatAPIKeyError:
                handle_wrong_format_api_key(console)
            except Exception:
                handle_generic_api_key_error(console)
        elif advice_method == enumerations.AdviceMethod.api_server:
            try:
                # debugging request to the LLM-based mentoring system
                # that is currently running on a remote LiteLLM system;
                # note that this does not seem to work correctly if
                # you use the standard LiteLLM approach as done with
                # the standard API key approach elsewhere in this file
                client = openai.OpenAI(
                    api_key="anything",
                    base_url=advice_server,
                )
                # submit the debugging request to the LLM-based mentoring system
                # using the specified model and the debugging prompt
                response = client.chat.completions.create(
                    model=advice_model,
                    messages=[{"role": "user", "content": llm_debugging_request}],
                )
                if fancy:
                    console.print(
                        Panel(
                            Markdown(
                                str(response.choices[0].message.content),
                                code_theme=syntax_theme.value,
                            ),
                            expand=False,
                            title="Advice from ExecExam's Coding Mentor (API Server)",
                            padding=1,
                        )
                    )
                else:
                    console.print(
                        Markdown(
                            str(
                                response.choices[0].message.content,  # type: ignore
                            ),
                            code_theme=syntax_theme.value,
                        ),
                    )
                    console.print()
            except InvalidAPIKeyError:
                handle_invalid_api_key(console)
            except MissingAPIKeyError:
                handle_missing_api_key(console)
            except WrongFormatAPIKeyError:
                handle_wrong_format_api_key(console)
            except Exception:
                handle_generic_api_key_error(console)
