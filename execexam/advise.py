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
    """Offer advice through the use of the LLM-Based mentoring system."""
    with console.status(
        "[bold green] Getting Feedback from ExecExam's Coding Mentor"
    ):
        test_overview = (
            filtered_test_output + exec_exam_test_assertion_details,
        )
        llm_debugging_request = (
            "I am an undergraduate student completing an examination."
            + "DO NOT make suggestions to change the test cases."
            + "ALWAYS make suggestions about how to improve the Python source code of the program under test."
            + "ALWAYS give a Python code in a Markdown fenced code block shows your suggested program."
            + "ALWAYS conclude saying that you making a helpful suggestion but could be wrong."
            + "Can you please suggest in a step-by-step fashion how to fix the bug in the program?"
            + f"Here is the test overview: {test_overview}"
            + f"Here are the failing test details: {failing_test_details}"
            + f"Here is the source code for the failing test: {failing_test_code}"
        )
        if approach == "apikey":
            response = completion(  # type: ignore
                # model="groq/llama3-8b-8192",
                # model="openrouter/meta-llama/llama-3.1-8b-instruct:free",
                # model="openrouter/google/gemma-2-9b-it:free",
                # model="anthropic/claude-3-opus-20240229",
                model="anthropic/claude-3-haiku-20240307",
                messages=[{"role": "user", "content": llm_debugging_request}],
            )
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
        elif approach == "apiserver":
            # attempt with openai;
            # does not work correctly if
            # you use the standard LiteLLM
            # as done above with the extra base_url
            client = openai.OpenAI(
                api_key="anything",
                base_url="https://execexamadviser.fly.dev/",
            )
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
