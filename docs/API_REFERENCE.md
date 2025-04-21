# API Reference

This document provides detailed API reference for the AI-CLI modules and functions.

## Table of Contents

1. [Main Module](#main-module)
2. [Commands](#commands)
   - [filterlog](#filterlog)
3. [Options](#options)
   - [version](#version)
4. [Utilities](#utilities)
5. [Validators](#validators)
6. [Settings](#settings)

## Main Module

**Module:** `ai_cli.main`

### Functions

#### `main()`

The entry point for the AI-CLI application.

**Description:**
- Creates the main Typer application instance
- Registers all commands and callbacks
- Executes the application

**Usage:**
```python
from ai_cli.main import main

if __name__ == "__main__":
    main()
```

## Commands

### filterlog

**Module:** `ai_cli.commands.filterlog`

#### `filterlog(file: Path, substrings: list[str], output: Path | None = None) -> None`

Filter lines containing all specified substrings from a text file.

**Parameters:**
- `file` (Path): Input text file to filter
- `substrings` (list[str]): List of substrings to filter (all must be present in a line)
- `output` (Path, optional): Custom output file path. Default is `<original-filename>-filtered.<extension>` in the current directory

**Returns:**
- None

**Raises:**
- `UnicodeDecodeError`: If the file is not a text file
- `FileNotFoundError`: If the file or parent directory of output doesn't exist

**Implementation Details:**
- Processes files line by line to handle files of any size
- Uses asynchronous I/O for better performance
- Case-insensitive matching of substrings
- Creates parent directories for output file if they don't exist

**Example:**
```python
from pathlib import Path
from ai_cli.commands.filterlog import filterlog

await filterlog(
    file=Path("/var/log/syslog"),
    substrings=["error", "critical"],
    output=Path("~/filtered-logs/errors.log")
)
```

## Options

### version

**Module:** `ai_cli.options.version`

#### `version_callback(value: bool) -> None`

Callback function to handle version display.

**Parameters:**
- `value` (bool): Value from the CLI option

**Returns:**
- None

**Raises:**
- `typer.Exit`: To exit the application after displaying the version

**Implementation Details:**
- Displays the application name and version from the pyproject.toml file
- Uses Rich for formatted output

#### `version(_: bool | None = None) -> None`

Show the application version and exit.

**Parameters:**
- `_` (bool | None): Value from the CLI option

**Returns:**
- None

**Example:**
```python
from ai_cli.options.version import version

# Called automatically by the CLI when --version or -v is used
```

## Utilities

**Module:** `ai_cli.utils`

### Command Registration

#### `register_command(app: typer.Typer, func: Callable, **kwargs) -> None`

Register a command with the main app.

**Parameters:**
- `app` (typer.Typer): The Typer application instance
- `func` (Callable): The command function to register
- `**kwargs`: Additional arguments to pass to the Typer command decorator

**Returns:**
- None

#### `register_commands(app: typer.Typer, commands: list[Callable], **kwargs) -> None`

Register multiple commands with the main app.

**Parameters:**
- `app` (typer.Typer): The Typer application instance
- `commands` (list[Callable]): List of command functions to register
- `**kwargs`: Additional arguments to pass to the Typer command decorator

**Returns:**
- None

#### `register_callback(app: typer.Typer, func: Callable, **kwargs) -> None`

Register a callback with the main app.

**Parameters:**
- `app` (typer.Typer): The Typer application instance
- `func` (Callable): The callback function to register
- `**kwargs`: Additional arguments to pass to the Typer callback decorator

**Returns:**
- None

#### `register_callbacks(app: typer.Typer, callbacks: list[Callable], **kwargs) -> None`

Register multiple callbacks with the main app.

**Parameters:**
- `app` (typer.Typer): The Typer application instance
- `callbacks` (list[Callable]): List of callback functions to register
- `**kwargs`: Additional arguments to pass to the Typer callback decorator

**Returns:**
- None

#### `register_command_group(app: typer.Typer, group: typer.Typer, name: str = None, **kwargs) -> None`

Register a command group (Typer instance) with the main app.

**Parameters:**
- `app` (typer.Typer): The Typer application instance
- `group` (typer.Typer): The Typer group to register
- `name` (str, optional): The name for the group
- `**kwargs`: Additional arguments to pass to add_typer

**Returns:**
- None

### Async Handling

#### `process_async_commands_in_group(group: typer.Typer) -> None`

Process all commands in a Typer group to wrap async functions.

**Parameters:**
- `group` (typer.Typer): The Typer group to process

**Returns:**
- None

#### `async_to_sync(func: Callable[..., Coroutine[Any, Any, Any]]) -> Callable[..., Any]`

Convert an async function to a sync function by running it in an event loop.

**Parameters:**
- `func` (Callable): The async function to convert

**Returns:**
- Callable: A synchronous wrapper function

**Implementation Details:**
- Wraps the async function in a synchronous function
- Handles creation and management of the event loop
- Preserves function metadata using functools.wraps

## Validators

**Module:** `ai_cli.validators.files`

#### `validate_dir_exists(dir: Path) -> None`

Ensure a directory exists.

**Parameters:**
- `dir` (Path): The directory path to validate

**Returns:**
- None

**Raises:**
- `FileNotFoundError`: If the directory doesn't exist

#### `validate_file_parent_dir_exists(file: Path) -> None`

Ensure a file's parent directory exists.

**Parameters:**
- `file` (Path): The file path to validate

**Returns:**
- None

**Raises:**
- `FileNotFoundError`: If the parent directory doesn't exist

#### `validate_file_exists(file: Path) -> None`

Ensure a file exists.

**Parameters:**
- `file` (Path): The file path to validate

**Returns:**
- None

**Raises:**
- `FileNotFoundError`: If the file doesn't exist

## Settings

**Module:** `ai_cli.settings`

### Classes

#### `Settings`

A Pydantic settings class for the application.

**Attributes:**
- `PYPROJECT_PATH` (Path): Path to the pyproject.toml file
- `PYPROJECT` (dict): Parsed content of the pyproject.toml file

**Usage:**
```python
from ai_cli.settings import settings

# Access project name
project_name = settings.PYPROJECT["project"]["name"]

# Access project version
version = settings.PYPROJECT["project"]["version"]
```

**Implementation Details:**
- Uses pydantic_settings for type-safe configuration
- Automatically loads the pyproject.toml file
- Singleton instance accessible via `settings` 