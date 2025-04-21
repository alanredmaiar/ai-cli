# AI-CLI User Guide

This guide provides detailed information on how to use the AI-CLI tool effectively.

## Table of Contents

1. [Installation](#installation)
2. [Basic Usage](#basic-usage)
3. [Commands](#commands)
   - [filterlog](#filterlog)
4. [Global Options](#global-options)
5. [Tips and Tricks](#tips-and-tricks)

## Installation

### Prerequisites

- Python 3.13 or higher
- Ubuntu-based system

### Using pip

```bash
pip install ai-cli
```

### Verifying Installation

After installing, verify the installation by checking the version:

```bash
ai-cli --version
```

You should see output similar to:

```
ai-cli version: 0.1.0
```

## Basic Usage

The general syntax for AI-CLI commands is:

```bash
ai-cli [OPTIONS] COMMAND [COMMAND_ARGS]
```

To get help on any command:

```bash
ai-cli COMMAND --help
```

To see a list of all available commands:

```bash
ai-cli --help
```

## Commands

### filterlog

The `filterlog` command allows you to filter lines from a text file that contain all specified substrings.

#### Syntax

```bash
ai-cli filterlog FILE SUBSTRING1 [SUBSTRING2...] [OPTIONS]
```

#### Arguments

- `FILE`: The input text file to filter (required)
- `SUBSTRING1 [SUBSTRING2...]`: One or more substrings to filter. Lines must contain ALL specified substrings to be included (required)

#### Options

- `-o, --output PATH`: Custom output file path
  - If not specified, output will be saved as `<original-filename>-filtered.<extension>` in the current directory

#### Examples

**Filter lines containing specific text:**

```bash
ai-cli filterlog /var/log/syslog error
```

This will create a file named `syslog-filtered.log` in the current directory containing only lines that include the word "error" (case-insensitive).

**Filter with multiple substrings:**

```bash
ai-cli filterlog /var/log/apache2/access.log 404 "Mozilla/5.0"
```

This will create a file with lines containing both "404" and "Mozilla/5.0".

**Specify custom output location:**

```bash
ai-cli filterlog /var/log/syslog error --output ~/logs/errors.log
```

This filters lines containing "error" and saves them to `~/logs/errors.log`.

#### How It Works

1. The command reads the input file line by line.
2. For each line, it checks if all specified substrings are present (case-insensitive).
3. If all substrings are found, the line is included in the output file.
4. The filtered results are written to the specified output file or a default location.

#### Notes

- The filtering is case-insensitive.
- The command processes text files only. Binary files will cause an error.
- Parent directories for the output file will be created if they don't exist.
- The command works with files of any size as it processes them line by line.

## Global Options

These options can be used with any command:

### Version

Display the application version and exit.

```bash
ai-cli --version
ai-cli -v
```

## Tips and Tricks

### Processing Large Files

When working with large log files, the `filterlog` command is efficient as it:

1. Processes the file line by line, avoiding loading the entire file into memory
2. Uses asynchronous I/O operations for better performance

### Chaining Commands

You can use the output of one command as input to another:

```bash
# First filter for errors, then filter again for critical errors
ai-cli filterlog /var/log/syslog error -o /tmp/errors.log
ai-cli filterlog /tmp/errors.log critical -o ~/critical-errors.log
```

### Using with System Logs

AI-CLI works well with system logs. For example, to analyze authentication failures:

```bash
sudo ai-cli filterlog /var/log/auth.log "Failed password"
```

### Advanced File Path Handling

The tool automatically handles:

- Relative and absolute paths
- Path expansion (e.g., `~` for home directory)
- Creating parent directories for output files

## Troubleshooting

### Common Issues

**Error: File is not a text file**
- This occurs when trying to process binary files
- Solution: Ensure you're working with text files only

**Error: Directory does not exist**
- This occurs when specifying an output path with a non-existent parent directory
- Solution: Ensure the parent directory exists or let the tool create it for you

### Getting Help

If you encounter issues not covered in this guide, you can:

1. Check the full help documentation:
   ```bash
   ai-cli --help
   ```

2. Check command-specific help:
   ```bash
   ai-cli filterlog --help
   ```

3. Report issues on GitHub: [https://github.com/username/ai-cli/issues](https://github.com/username/ai-cli/issues) 