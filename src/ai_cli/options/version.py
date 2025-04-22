import rich_click as click
from rich import print as rprint

from ai_cli.settings import settings as st


@click.group()
@click.version_option(st.PYPROJECT["project"]["version"])
@click.pass_context
def version(ctx):
    pass
