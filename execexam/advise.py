"""Offer advice through the use of the LLM-Based mentoring system."""

import openai
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from . import enumerations


def load_litellm() -> None:
    """Load the litellm module."""
    # note that the purpose of this function is
    # to allow the loading of the litellm module
    # to take place in a separate thread, thus
    # ensuring that the main interface is not blocked
    global litellm  # noqa: PLW0602
    global completion  # noqa: PLW0603
    from litellm import completion


def fix_failures(  # noqa: PLR0913
    console: Console,
    filtered_test_output: str,
    exec_exam_test_assertion_details: str,
    test_overview: str,
    failing_test_details: str,
    failing_test_code: str,
    syntax_theme: enumerations.Theme,
    approach: str = "api",
    fancy: bool = True,
):
    """Offer advice through the use of the LLM-based mentoring system."""
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
        if approach == "apikey":
            # submit the debugging request to the LLM-based mentoring system
            response = completion(  # type: ignore
                # model="groq/llama3-8b-8192",
                # model="openrouter/meta-llama/llama-3.1-8b-instruct:free",
                # model="openrouter/google/gemma-2-9b-it:free",
                # model="anthropic/claude-3-opus-20240229",
                model="anthropic/claude-3-haiku-20240307",
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
        # the apiserver approach expects that the person running the execexam
        # tool will specify the URL of a remote LLM-based mentoring system
        # that is configured to provide access to an LLM system for advice
        elif approach == "apiserver":
            # use the OpenAI approach to submitting the
            # debugging request to the LLM-based mentoring system
            # that is currently running on a remote LiteLLM system;
            # note that this does not seem to work correctly if
            # you use the standard LiteLLM approach as done with
            # the standard API key approach elsewhere in this file
            client = openai.OpenAI(
                api_key="anything",
                base_url="https://execexamadviser.fly.dev/",
            )
            # submit the debugging request to the LLM-based mentoring system
            # using the specified model and the debugging prompt
            response = client.chat.completions.create(
                model="anthropic/claude-3-haiku-20240307",
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
