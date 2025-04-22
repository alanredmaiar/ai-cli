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

command = click.command
group = click.group
async_click = click