import rich_click as click
from rich import print as rprint

from ai_cli.settings import settings as st


def version_callback(ctx, param, value):
    """Callback function to handle version display."""
    if not value or ctx.resilient_parsing:
        return
    rprint(f"[bold green]{st.PYPROJECT['project']['name']}[/] version: [bold]{st.PYPROJECT['project']['version']}[/]")
    ctx.exit()


def version(function=None):
    """Show the application version and exit."""
    if function is None:
        return click.option(
            "--version",
            "-v",
            help="Show the application version and exit.",
            is_flag=True,
            callback=version_callback,
            is_eager=True,
            expose_value=False,
        )
    return version()(function)