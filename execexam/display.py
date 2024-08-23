"""Display results from running the execexam tool."""

from typing import Any, Dict

from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax


def make_colon_separated_string(arguments: Dict[str, Any]):
    """Make a colon separated string from a dictionary."""
    return "\n" + "".join(
        [f"- {key}: {value}\n" for key, value in arguments.items()]
    )


def display_return_code(console: Console, return_code: int) -> None:
    """Display the return code from running the specified checks(s)."""
    # no errors were found in the executable examination
    if return_code == 0:
        console.print("[green]\u2714 All checks passed.")
    else:
        console.print("[red]\u2718 One or more checks failed.")


def display_diagnostics(  # noqa: PLR0913
    verbose: bool,
    console: Console,
    content: str,
    label: str,
    richtext: bool,
    syntax: bool,
    syntax_theme: str = "ansi_dark",
    syntax_language: str = "python",
) -> None:
    """Display a diagnostic message using rich or plain text."""
    if verbose:
        console.print()
        display_content(
            console,
            content,
            label,
            richtext,
            syntax,
            syntax_theme,
            syntax_language,
        )
    else:
        return None


def display_content(  # noqa: PLR0913
    console: Console,
    content: str,
    label: str,
    richtext: bool,
    syntax: bool,
    syntax_theme: str = "ansi_dark",
    syntax_language: str = "python",
    newline: bool = False,
) -> None:
    """Display a diagnostic message using rich or plain text."""
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
