# AI-CLI

Advanced AI-powered command-line tools for Ubuntu systems that simplify complex tasks through intelligent data parsing and AI-assisted operations.

[![Python Version](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## Overview

AI-CLI provides a collection of intelligent command-line utilities designed to streamline common tasks on Ubuntu systems. By leveraging AI-assisted operations, this tool helps with tasks like log filtering, data processing, and system monitoring.

## Installation

### Prerequisites

- Python 3.13 or higher
- Ubuntu-based system

### Using pip (recommended)

```bash
pip install ai-cli
```

### From source

```bash
git clone https://github.com/username/ai-cli.git
cd ai-cli
pip install .
```

## Commands

### filterlog

Filter lines containing specified substrings from a text file.

```bash
ai-cli filterlog INPUT_FILE SUBSTRING1 [SUBSTRING2...] [OPTIONS]
```

#### Arguments

- `INPUT_FILE`: Path to the input text file to filter (required)
- `SUBSTRING1 [SUBSTRING2...]`: One or more substrings to filter; lines must contain ALL substrings to be included (required)

#### Options

- `-o, --output PATH`: Custom output file path
  - If not specified, output will be saved as `<original-filename>-filtered.<extension>` in the current directory

#### Examples

```bash
# Filter lines containing both "error" and "critical" in a log file
ai-cli filterlog /var/log/application.log error critical

# Filter with a custom output location
ai-cli filterlog /var/log/application.log error --output ~/filtered-logs/errors.log
```

## Global Options

### Version

Display the application version and exit.

```bash
ai-cli --version
ai-cli -v
```

## Development

### Setup Development Environment

1. Clone the repository
   ```bash
   git clone https://github.com/username/ai-cli.git
   cd ai-cli
   ```

2. Create and activate a virtual environment
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows, use: .venv\Scripts\activate
   ```

3. Install development dependencies
   ```bash
   pip install -e '.[dev]'
   ```

### Project Structure

```
ai-cli/
├── src/
│   └── ai_cli/
│       ├── commands/        # Command implementations
│       ├── options/         # Global CLI options
│       ├── validators/      # Input validation utilities
│       ├── utils.py         # Utility functions
│       ├── settings.py      # Application settings
│       └── main.py          # Entry point
├── test/
│   ├── unit/               # Unit tests
│   └── resources/          # Test resources
├── pyproject.toml          # Project configuration
├── LICENSE                 # License file
└── README.md               # This documentation
```

### Running Tests

```bash
pytest
```

### Code Style and Linting

The project uses Ruff for code linting and formatting:

```bash
# Check code style
ruff check .

# Format code
ruff format .
```

### Type Checking

```bash
pyright
```

## Adding New Commands

To add a new command to the CLI:

1. Create a new Python file in the `src/ai_cli/commands/` directory
2. Implement your command function with Typer decorators for arguments/options
3. Import and export your command in `src/ai_cli/commands/__init__.py`
4. Add your command to the list in `src/ai_cli/main.py`

Example command structure:

```python
import typer

def my_command(
    arg1: str = typer.Argument(..., help="Description of argument"),
    option1: bool = typer.Option(False, "--option", "-o", help="Description of option"),
):
    """Command description that will appear in help text"""
    # Command implementation
    pass
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
