import asyncio
import functools
import inspect

import rich_click as click
from rich_click.rich_command import RichMultiCommand
from rich_click.rich_help_rendering import get_rich_commands


class AsyncCommand(click.RichCommand):
    """Async-aware Command class."""

    def invoke(self, ctx):
        if inspect.iscoroutinefunction(self.callback):
            return asyncio.run(self.callback(**ctx.params))
        return super().invoke(ctx)


class AsyncGroup(click.RichGroup):
    """Group that uses AsyncCommand for subcommands and itself for nested groups."""

    command_class = AsyncCommand

    def format_commands(self, ctx, formatter):
        """Modified to show subcommands with prefix of the group."""
        commands = []

        # Collect direct commands
        for subcommand in self.list_commands(ctx):
            cmd = self.get_command(ctx, subcommand)
            if cmd is None or cmd.hidden:
                continue
            commands.append((subcommand, cmd))

        # Collect subcommands from nested groups
        for subcommand, cmd in commands.copy():
            if isinstance(cmd, click.Group):
                for sub_subcommand in cmd.list_commands(ctx):
                    sub_cmd = cmd.get_command(ctx, sub_subcommand)
                    if sub_cmd is None or sub_cmd.hidden:
                        continue
                    # Add with group prefix
                    commands.append((f"{subcommand} {sub_subcommand}", sub_cmd))

        # Create a temporary MultiCommand with our commands list
        class TempMultiCommand(RichMultiCommand):
            def list_commands(self, ctx):
                return [cmd[0] for cmd in commands]

            def get_command(self, ctx, name):
                for cmd_name, cmd_obj in commands:
                    if cmd_name == name:
                        return cmd_obj
                return None

        # Use the original get_rich_commands with our temporary command
        temp_cmd = TempMultiCommand(name=self.name)
        get_rich_commands(temp_cmd, ctx, formatter)


# Make rich_click async-aware by default
click.Command = AsyncCommand
click.Group = AsyncGroup


# Make decorators use our custom classes
click.command = functools.partial(click.command, cls=AsyncCommand)
click.group = functools.partial(click.group, cls=AsyncGroup)

command = click.command
group = click.group
async_click = click
