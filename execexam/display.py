"""Display results from running the execexam tool."""

from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.text import Text


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
