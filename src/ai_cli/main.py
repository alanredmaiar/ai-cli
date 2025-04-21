import typer

from ai_cli.settings import settings as st
from ai_cli.utils import register_commands, register_callbacks
from ai_cli.options import version
from ai_cli.commands import filterlog


def main():
    """Entry point for the application."""

    app = typer.Typer(
        name=st.PYPROJECT["project"]["name"],
        help=st.PYPROJECT["project"]["description"],
        add_completion=True,
    )

    options = [version]
    commands = [filterlog]  

    register_commands(app, commands)
    register_callbacks(app, options)
    
    
    app()


if __name__ == "__main__":
    main()