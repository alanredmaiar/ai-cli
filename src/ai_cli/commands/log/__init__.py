from ai_cli.asyn import async_click as click
from ai_cli.commands.log.line_filter import log_line_filter


@click.group(name="log")
def log():
    """Commands for working with log files."""
    pass


log.add_command(log_line_filter)
