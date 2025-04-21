from pathlib import Path
from typing import Annotated

import aiofiles
import typer

from ai_cli.validators.files import validate_file_parent_dir_exists


async def filterlog(
    file: Path = typer.Argument(..., exists=True, file_okay=True, dir_okay=False, help="Input text file to filter"),
    substrings: list[str] = typer.Argument(..., help="Substrings to filter (all must be present in line)"),
    output: Annotated[
        Path | None,
        typer.Option(
            "--output",
            "-o",
            help="Custom output file path",
            callback=validate_file_parent_dir_exists,
            rich_help_panel="Customization and Utils",
        ),
    ] = None,
):
    """Filter lines containing all substrings (case-insensitive) from a text file"""
    output = output.expanduser().resolve() if output else Path.cwd() / f"{file.stem}-filtered{file.suffix}"
    output.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        async with aiofiles.open(file, mode="r") as input_file, aiofiles.open(output, mode="w") as output_file:
            async for line in input_file:
                line_lower = line.lower()
                if all(sub.lower() in line_lower for sub in substrings):
                    await output_file.write(line)
    except UnicodeDecodeError:
        typer.echo("Error: File is not a text file", err=True)
        raise typer.Exit(code=1)

    typer.echo(f"Generated filtered file at: {output}")
