"""Offer advice through the use of the LLM-Based mentoring system."""

import openai
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel


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
    filtered_test_output,
    exec_exam_test_assertion_details,
    test_overview,
    failing_test_details,
    failing_test_code,
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
        test_overview = (
            filtered_test_output + exec_exam_test_assertion_details,
        )
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
            + "Please do not make suggestions to change the test cases."
            + "Always make suggestions about how to improve the Python source code of the program under test."
            + "Always give Python code in a Markdown fenced code block with your suggested program."
            + "Always conclude by saying that you are making a helpful suggestion but could be wrong."
            + "Can you please suggest in a step-by-step fashion how to fix the bug(s) in the program?"
            + f"Here is the test overview: {test_overview}"
            + f"Here are the failing test details: {failing_test_details}"
            + f"Here is the source code for the failing test(s): {failing_test_code}"
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
                            code_theme="ansi_dark",
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
                        code_theme="ansi_dark",
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
                            code_theme="ansi_dark",
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
                        code_theme="ansi_dark",
                    ),
                )
                console.print()
