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
from .exceptions import (
    InvalidAPIKeyError,
    MissingAPIKeyError,
    WrongFormatAPIKeyError,
    MissingServerURLError,
    InvalidServerURLError,
    ConnectionError,
    ExceededAPIRequestsError,
    InternalServerError,
)

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


def validate_api_key(console: Console, api_key: str) -> None:
    """Validate the provided API key."""
    if not api_key:
        raise MissingAPIKeyError(console)
    if len(api_key) != 32:  # Assuming the API key should be 32 characters long
        raise WrongFormatAPIKeyError(console)
    if None:  # how do we check if it is invalid
        raise InvalidAPIKeyError(console)
    if None:  # how do we check if requests were exceeded
        raise ExceededAPIRequestsError(console)


def validate_api_server(console: Console, api_server: str) -> None:
    """Validate the provided API server."""
    if not api_server:
        raise MissingServerURLError(console)
    if not validate_url(api_server):
        raise InvalidServerURLError(console)
    if None: # how do we check if there is an internal server error
        raise InternalServerError(console)


def handle_connection_error(console: Console) -> None:
    """Handle connection error."""
    # Print an error message stating there's issues with connecting to the api server.
    console.print("[bold red]Error: Unable to connect to the API server.[/bold red]")
    # Print a troubleshooting message.
    console.print("Please check your network connection and ensure the API server is reachable.")


def check_internet_connection(timeout: int = 5) -> bool:
    """Check if the system has an active internet connection."""
    try:
        # Attempt to connect to Google's DNS server (8.8.8.8) on port 53 (DNS)
        # Attempt to create a socket connection to Google's DNS server (8.8.8.8) on port 53.
        # Port 53 is used for DNS, and Google's DNS server is a commonly available address.
        # This check is used to verify if the system can connect to an external network.
        socket.create_connection(("8.8.8.8", 53), timeout=timeout)
        # If the connection is successful, return True indicating internet is available.
        return True
    # If an OSError is raised, it indicates that the connection attempt failed.
    # This could be due to no internet connection or network issues.
    except OSError:
        # Return False indicating that the internet connection is not available.
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
    # Check if there is an active internet connection before proceeding.
    if not check_internet_connection():
        # If there is no internet connection, handle the connection error.
        # Call the handle_connection_error function
        handle_connection_error(console)
        return
    with console.status(
        "[bold green] Getting Feedback from ExecExam's Coding Mentor"
    ):
        # the test overview is a string that contains both
        # the filtered test output and the details about the passing
        # and failing assertions in the test cases
        test_overview = filtered_test_output + exec_exam_test_assertion_details
        # create an LLM debugging request that contains all of the
        # information that is needed to provide advice about how
        # to fix the bug(s) in the program that are part of an
        # executable examination; note that, essentially, an
        # examination consists of Python functions that a student
        # must complete and then test cases that confirm the correctness
        # of the functions that are implemented; note also that
        # ExecExam has a Pytest plugin that collects additional details
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

        # the API key approach expects that the person running the execexam
        # tool has specified an API key for a support cloud-based LLM system
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
                # display the advice from the LLM-based mentoring system
                # in a panel that is created by using the rich library
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
            except Exception:
                console.print("[bold red]Unknown error[/bold red]")

        # the apiserver approach expects that the person running the execexam
        # tool will specify the URL of a remote LLM-based mentoring system
        # that is configured to provide access to an LLM system for advice
        elif advice_method == enumerations.AdviceMethod.api_server:
            try:
                # check to make sure the server calls the exceptions correct
                validate_api_server(enumerations.AdviceMethod.api_server)

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
                            str(response.choices[0].message.content), #type: ignore
                            code_theme=syntax_theme.value,
                        )
                    )
                    console.print()
            except Exception:
                console.print("[bold red]Unknown error[/bold red]")
