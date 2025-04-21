# Developer Documentation for AI-CLI

This document provides detailed technical information about the architecture, modules, and implementation details of the AI-CLI project.

## Architecture Overview

AI-CLI is built on a modular architecture using [Typer](https://typer.tiangolo.com/) for CLI interface and command handling. The application follows these design principles:

1. **Command-based structure**: Each CLI command is implemented as a separate function
2. **Async-friendly**: Support for both synchronous and asynchronous command handlers
3. **Modular design**: Separation of concerns across modules
4. **Type safety**: Strong typing with comprehensive validation

## Core Components

### Entry Point (`main.py`)

The `main.py` file serves as the entry point for the application. It:

- Creates the main Typer application
- Registers commands and callbacks
- Handles the application execution

```python
def main():
    app = typer.Typer(name=settings.PYPROJECT["project"]["name"], ...)
    
    options = [version]
    commands = [filterlog]
    
    register_commands(app, commands)
    register_callbacks(app, options)
    
    app()
```

### Settings (`settings.py`)

The settings module uses `pydantic_settings` to manage application configuration and reads the `pyproject.toml` file to access project metadata.

```python
class Settings(BaseSettings):
    PYPROJECT_PATH: Path = Path(__file__).parents[2] / "pyproject.toml"
    PYPROJECT: dict = tomli.load(PYPROJECT_PATH.open("rb"))

settings = Settings()
```

### Commands 

Commands are functions that implement specific CLI functionalities:

#### `filterlog.py`

The `filterlog` command:
- Takes an input text file and one or more substrings as arguments
- Filters lines that contain all the specified substrings (case-insensitive)
- Outputs the filtered content to a new file

```python
async def filterlog(
    file: Path = typer.Argument(...),
    substrings: list[str] = typer.Argument(...),
    output: Path | None = typer.Option(None, "--output", "-o"),
):
    """Filter lines containing all substrings from a text file"""
    # Implementation...
```

### Options

Options implement global CLI behaviors that apply across commands:

#### `version.py`

The `version` option displays the application version and exits:

```python
def version_callback(value: bool):
    if value:
        rprint(f"[bold green]{st.PYPROJECT['project']['name']}[/] version: [bold]{st.PYPROJECT['project']['version']}[/]")
        raise typer.Exit()

def version(_: bool | None = None):
    """Show the application version and exit."""
    pass
```

### Utilities (`utils.py`)

The utils module provides helper functions for:

1. **Command registration**:
   - `register_command()`: Register a single command
   - `register_commands()`: Register multiple commands
   - `register_callback()`: Register a callback
   - `register_callbacks()`: Register multiple callbacks
   - `register_command_group()`: Register a command group

2. **Async handling**:
   - `async_to_sync()`: Convert async functions to sync functions
   - `process_async_commands_in_group()`: Process async commands in a Typer group

### Validators

The validators module provides input validation functions:

- `validate_dir_exists()`: Ensure a directory exists
- `validate_file_parent_dir_exists()`: Ensure a file's parent directory exists
- `validate_file_exists()`: Ensure a file exists

## Adding New Commands

To add a new command:

1. Create a new Python file in `src/ai_cli/commands/` directory
2. Define your command function with Typer annotations
3. Import and add your command in `src/ai_cli/commands/__init__.py`
4. Add your command to the `commands` list in `main.py`

### Synchronous Command Example

```python
def my_sync_command(
    arg1: str = typer.Argument(..., help="Argument description"),
    flag: bool = typer.Option(False, "--flag", "-f", help="Flag description")
):
    """Command description"""
    # Implementation
```

### Asynchronous Command Example

```python
async def my_async_command(
    arg1: str = typer.Argument(..., help="Argument description"),
    flag: bool = typer.Option(False, "--flag", "-f", help="Flag description")
):
    """Command description"""
    # Async implementation
```

## Adding Options

To add a new global option:

1. Create a new file in `src/ai_cli/options/`
2. Define a function with Typer option annotations
3. Import and add your option in `src/ai_cli/options/__init__.py`
4. Add your option to the `options` list in `main.py`

## Error Handling

Error handling is managed through Typer's exception system:

- Use `typer.echo()` for user messages
- Use `typer.Exit()` to exit the application with a code
- Use validators to handle input validation

## Testing

Tests are organized under the `test` directory:

- `test/unit/`: Unit tests for individual components
- `test/unit/commands/`: Command-specific tests
- `test/resources/`: Test resources and fixtures

Testing uses pytest with pytest-asyncio for async testing support.

## Project Configuration

Project configuration is managed through `pyproject.toml`, which defines:

- Project metadata
- Dependencies
- Build configuration
- Tool settings (Ruff, Pyright)

## Advanced Features

### Async Support

The application supports both synchronous and asynchronous commands through a wrapper that converts async functions to sync functions in the Typer interface.

```python
def async_to_sync(func: Callable[..., Coroutine[Any, Any, Any]]) -> Callable[..., Any]:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Implementation to run coroutine in an event loop
    return wrapper
```

## Performance Considerations

- Async I/O operations for file handling improve performance
- Efficient command registration system
- Type-aware validation for runtime safety 