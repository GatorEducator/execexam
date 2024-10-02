"""Display results from running the execexam tool."""

from typing import Any, Dict, List, Optional

from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax

from . import enumerations


def make_colon_separated_string(arguments: Dict[str, Any]):
    """Make a colon separated string from a dictionary."""
    return "\n" + "".join(
        [f"- {key}: {value}\n" for key, value in arguments.items()]
    )


def get_display_return_code(return_code: int, fancy: bool) -> str:
    """Determine the return code from running the specified checks(s)."""
    message = "\n"
    # no errors were found in the executable examination
    if return_code == 0:
        message += "[green]\u2714 All checks passed."
    # there was an error in the executable examination
    else:
        message += "[red]\u2718 One or more checks failed."
    if fancy:
        message += "\n"
    return message


def display_tldr(console: Console) -> None:
    """Display a list of example commands and their descriptions."""
    console.print(
        "[bold yellow]Too Lazy; Didn't Read: Example Commands[/bold yellow]\n"
    )
    console.print(
        "[bold red]Please ensure you are in the directory with the pyproject.toml file to run these commands.[/bold red]\n"
    )

    console.print(
        "[bold cyan]poetry run execexam <path-to-project> <path-to-tests>[/bold cyan]"
    )
    console.print(
        "    Run executable exam for a project with the specified test files."
    )

    console.print(
        "[bold cyan]poetry run execexam <path-to-project> <path-to-tests> --mark <mark>[/bold cyan]"
    )
    console.print("    Run the tests with the specified mark(s).")

    console.print(
        "[bold cyan]poetry run execexam <path-to-project> <path-to-tests> --maxfail[/bold cyan]"
    )
    console.print("    Limit the number of test failures before stopping.")

    console.print(
        "[bold cyan]poetry run execexam <path-to-project> <path-to-tests> --report <report_type>/<all>[/bold cyan]"
    )
    console.print(
        "    Generate the specified type(s) of reports after the exam. Use 'all' to generate all available report types."
    )

    console.print(
        "[bold cyan]poetry run execexam <path-to-project> <path-to-tests> --advice-model <model> --advice-method <method>[/bold cyan]"
    )
    console.print(
        "    Use specified LLM model and method for providing advice on test failures."
    )

    console.print(
        "[bold cyan]poetry run execexam <path-to-project> <path-to-tests> <--debug>/<--no-debug>[/bold cyan]"
    )
    console.print("    Display or disable debugging information.")

    console.print(
        "[bold cyan]poetry run execexam <path-to-project> <path-to-tests> <--fancy>/<--no-fancy>[/bold cyan]"
    )
    console.print("    Display or disable fancy output formatting.")

    console.print(
        "\n[bold yellow]help:[/bold yellow] Use [bold yellow]--help[/bold yellow] to see more options."
    )


def display_advice(return_code: int) -> str:
    """Determine the return code from running the specified checks(s)."""
    message = "\n"
    # no errors were found in the executable examination
    # and no advice is needed, so display helpful message
    if return_code == 0:
        message += "[green]\u2714 Advise requested, but none is needed!"
    # there was an error in the executable examination;
    # note that this is not going to be normally displayed
    else:
        message += "[red]\u2718 Advise requested, and will be provided!"
    # add an extra newline to ensure suitable spacing;
    # note that this is always done and thus there is
    # no need to know whether or not fancy output needed
    message += "\n"
    return message


def display_content(  # noqa: PLR0913
    console: Console,
    display_report_type: enumerations.ReportType,
    report_types: Optional[List[enumerations.ReportType]],
    content: str,
    label: str,
    richtext: bool,
    syntax: bool,
    syntax_theme: str = "ansi_dark",
    syntax_language: str = "python",
    newline: bool = False,
) -> None:
    """Display a diagnostic message using rich or plain text."""
    if report_types is not None and (
        display_report_type in report_types
        or enumerations.ReportType.all in report_types
    ):
        # rich text was chosen and thus the message
        # should appear in a panel with a title
        if richtext:
            # add an extra newline in the output
            # to separate this block for a prior one;
            # only needed when using rich text
            if newline:
                console.print()
            # use rich to print highlighted
            # source code in a formatted box
            if syntax:
                source_code_syntax = Syntax(
                    "\n" + content,
                    syntax_language,
                    theme=syntax_theme,
                )
                console.print(
                    Panel(
                        source_code_syntax,
                        expand=False,
                        title=label,
                    )
                )
            # use rich to print sylized text since
            # the content is not source code
            # that should be syntax highlighted
            else:
                console.print(
                    Panel(
                        content,
                        expand=False,
                        title=label,
                        highlight=True,
                    )
                )
        # plain text was chosen but the content is
        # source code and thus syntax highlighting
        # is needed, even without the panel box
        elif not richtext and syntax:
            source_code_syntax = Syntax(
                "\n" + content,
                syntax_language,
                theme=syntax_theme,
            )
            console.print(f"{label}")
            console.print(source_code_syntax)
        # plain text was chosen and the content is
        # not source code and thus no syntax highlighting
        # is needed and there is no panel box either
        else:
            console.print(f"{label}\n{content}")
