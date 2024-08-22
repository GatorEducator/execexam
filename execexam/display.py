"""Display results from running the execexam tool."""

from typing import Any, Dict

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.syntax import Syntax
from rich.text import Text


def make_colon_separated_string(arguments: Dict[str, Any]):
    """Make a colon separated string from a dictionary."""
    return "\n" + "".join(
        [f"- {key}: {value}\n" for key, value in arguments.items()]
    )


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
) -> None:
    """Display a diagnostic message using rich or plain text."""
    # rich text was chosen and thus the message
    # should appear in a panel with a title
    if richtext:
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
                    Text(content, overflow="fold"),
                    expand=False,
                    title=label,
                )
            )
    # plain text was chosen and thus the message
    # should appear without any formatting
    else:
        console.print(f"{label}\n{content}")
