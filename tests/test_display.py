"""Test cases for the display.py file."""

from typing import List
from unittest.mock import Mock

import typer
from rich.console import Console
from typer.testing import CliRunner

from execexam.display import (
    display_advice,
    get_display_return_code,
    make_colon_separated_string,
)
from execexam.display import (
    display_content as display_content_function,
)
from execexam.enumerations import ReportType

runner = CliRunner()
app = typer.Typer()


@app.command()
def display_content(  # noqa: PLR0913
    report_type: ReportType,
    report_types: List[ReportType],
    content: str,
    label: str,
    richtext: bool,
    syntax: bool,
    syntax_theme: str,
    syntax_language: str,
    newline: bool,
):
    console = Mock(spec=Console)
    display_content_function(
        console,
        report_type,
        report_types,
        content,
        label,
        richtext,
        syntax,
        syntax_theme,
        syntax_language,
        newline,
    )


def test_make_colon_separated_string():
    """Function tests the make colon separated string section."""
    arguments = {"key1": "value1", "key2": "value2"}
    result = make_colon_separated_string(arguments)
    assert result == "\n- key1: value1\n- key2: value2\n"


def test_get_display_return_code():
    """Function tests the return code display."""
    assert (
        get_display_return_code(0, True) == "\n[green]✔ All checks passed.\n"
    )
    assert (
        get_display_return_code(1, True)
        == "\n[red]✘ One or more checks failed.\n"
    )
    assert get_display_return_code(0, False) == "\n[green]✔ All checks passed."
    assert (
        get_display_return_code(1, False)
        == "\n[red]✘ One or more checks failed."
    )


def test_display_advice():
    """Function tests the display advice."""
    assert (
        display_advice(0)
        == "\n[green]✔ Advise requested, but none is needed!\n"
    )
    assert (
        display_advice(1)
        == "\n[red]✘ Advise requested, and will be provided!\n"
    )


def test_display_content():
    """Function tests the display content."""
    content = "print('Hello, World!')"
    label = "Test Label"

    result = runner.invoke(
        app,
        [
            ReportType.all.name,
            ReportType.all.name,
            content,
            label,
            "True",
            "True",
            "ansi_dark",
            "python",
            "True",
        ],
    )

    assert result.exit_code == 0


def test_display_content_plain_text():
    """Function tests the display content with plain text."""
    content = "print('Hello, World!')"
    label = "Test Label"

    result = runner.invoke(
        app,
        [
            ReportType.all.name,
            ReportType.all.name,
            content,
            label,
            "False",
            "False",
            "ansi_dark",
            "python",
            "False",
        ],
    )

    assert result.exit_code == 0


def test_display_content_no_newline():
    """Function tests the display content without newline."""
    content = "print('Hello, World!')"
    label = "Test Label"

    result = runner.invoke(
        app,
        [
            ReportType.all.name,
            ReportType.all.name,
            content,
            label,
            "True",
            "True",
            "ansi_dark",
            "python",
            "False",
        ],
    )

    assert result.exit_code == 0
