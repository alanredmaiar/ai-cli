from typing import Callable, Any, Type
import inspect
import asyncio
import functools

import rich_click as click


# Async‐aware Command class
class AsyncCommand(click.RichCommand):
    def invoke(self, ctx):
        if inspect.iscoroutinefunction(self.callback):
            return asyncio.run(self.callback(**ctx.params))
        return super().invoke(ctx)


# Group that uses AsyncCommand for subcommands and itself for nested groups
class AsyncGroup(click.RichGroup):
    # all @group.command() use AsyncCommand
    command_class = AsyncCommand


# Make rich_click async-aware by default
click.Command = AsyncCommand
click.Group = AsyncGroup


# Make decorators use our custom classes
click.command = functools.partial(click.command, cls=AsyncCommand)
click.group = functools.partial(click.group, cls=AsyncGroup)


def register_command(app: click.Group, func: Callable, **kwargs):
    """Register a command with the main app."""
    # No need for async wrapping anymore as AsyncCommand handles it
    return app.command(**kwargs)(func)


def register_commands(app: click.Group, commands: list[Callable], **kwargs):
    """Register a list of commands with the main app."""
    for command in commands:
        register_command(app, command, **kwargs)


def register_callback(app: click.Group, func: Callable, **kwargs):
    """Set a callback for the command group."""
    return app.callback(**kwargs)(func)


def register_callbacks(app: click.Group, callbacks: list[Callable], **kwargs):
    """Register a list of callbacks with the main app."""
    for callback in callbacks:
        register_callback(app, callback, **kwargs)


def register_command_group(app: click.Group, group: click.Group, name: str = None, **kwargs):
    """Register a command group with the main app."""
    if name:
        kwargs['name'] = name
    app.add_command(group, **kwargs)