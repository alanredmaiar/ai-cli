from typing import Annotated

import typer
from rich import print as rprint

from ai_cli.settings import settings as st


def version_callback(value: bool):
    """Callback function to handle version display."""
    if value:
        rprint(f"[bold green]{st.PYPROJECT['project']['name']}[/] version: [bold]{st.PYPROJECT['project']['version']}[/]")
        raise typer.Exit()


def version(
    _: Annotated[bool | None, typer.Option(
        "--version",
        "-v",
        help="Show the application version and exit.",
        callback=version_callback,
        is_eager=True,
    )] = None
):
    """Show the application version and exit."""
    pass