from pathlib import Path

from rich import print as rprint
import tomli
import typer

from src.ai_cli.commands.filterlog import filterlog

pyproject = tomli.load((Path(__file__).parents[3] / "pyproject.toml").read_text())


app = typer.Typer(
    name=pyproject["project"]["name"],
    help=pyproject["project"]["description"],
    add_completion=True,
)


app.add_command(filterlog)


def get_commands_help() -> str:
    """Generate dynamic help text based on registered commands."""
    commands = []
    for command_name, command in app.registered_commands:
        commands.append(f"  • {command_name}: {command.help}")

    if commands:
        return "\nAvailable commands:\n" + "\n".join(commands)
    return ""


@app.callback()
def callback(
    version: bool | None = typer.Option(None, "--version", "-v", help="Show the application version and exit.", is_flag=True),
) -> None:
    """
    AI-CLI: Advanced command-line tools powered by AI for Ubuntu systems.
    """
    if version:
        rprint(f"[bold green]{pyproject['project']['name']}[/] version: [bold]{pyproject['project']['version']}[/]")
        raise typer.Exit()


if __name__ == "__main__":
    app()
