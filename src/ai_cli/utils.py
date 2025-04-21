from typing import Callable, Any, Coroutine
import asyncio
import inspect
import functools

import typer


def register_command(app: typer.Typer, func: Callable, **kwargs):
    """Register a command with the main app."""
    if inspect.iscoroutinefunction(func):
        app.command(**kwargs)(async_to_sync(func))
    else:
        app.command(**kwargs)(func)

def register_commands(app: typer.Typer, commands: list[Callable], **kwargs):
    """Register a list of commands with the main app."""
    for command in commands:
        register_command(app, command, **kwargs)

def register_callback(app: typer.Typer, func: Callable, **kwargs):
    """Register a callback with the main app."""
    if inspect.iscoroutinefunction(func):
        app.callback(**kwargs)(async_to_sync(func))
    else:
        app.callback(**kwargs)(func)

def register_callbacks(app: typer.Typer, callbacks: list[Callable], **kwargs):
    """Register a list of callbacks with the main app."""
    for callback in callbacks:
        register_callback(app, callback, **kwargs)

def register_command_group(app: typer.Typer, group: typer.Typer, name: str = None, **kwargs):
    """Register a command group (Typer instance) with the main app."""

    process_async_commands_in_group(group)
    if name:
        app.add_typer(group, name=name, **kwargs)
    else:
        app.add_typer(group, **kwargs)

def process_async_commands_in_group(group: typer.Typer):
    """Process all commands in a Typer group to wrap async functions."""
    for command in group.registered_commands:
        if hasattr(command, "callback") and inspect.iscoroutinefunction(command.callback):
            original_callback = command.callback
            command.callback = async_to_sync(original_callback)
    
    for subgroup in group.registered_groups:
        process_async_commands_in_group(subgroup.typer_instance)

def async_to_sync(func: Callable[..., Coroutine[Any, Any, Any]]) -> Callable[..., Any]:
    """Convert an async function to a sync function by running it in an event loop."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            loop = asyncio.get_running_loop()
            is_new_loop = False
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            is_new_loop = True
        
        try:
            result = loop.run_until_complete(func(*args, **kwargs))
            return result
        finally:
            if is_new_loop and loop.is_running():
                loop.close()
    
    return wrapper