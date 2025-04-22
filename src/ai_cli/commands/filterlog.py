from pathlib import Path

import aiofiles
import rich_click as click

from ai_cli.validators.files import validate_file_parent_dir_exists


@click.command()
@click.argument("file", type=click.Path(exists=True, file_okay=True, dir_okay=False), help="Input text file to filter")
@click.argument("substrings", nargs=-1, required=True, help="Substrings to filter (all must be present in line)")
@click.option(
    "--output", "-o", 
    type=click.Path(), 
    help="Custom output file path",
    callback=validate_file_parent_dir_exists
)
async def filterlog(file, substrings, output):
    """Filter lines containing all substrings (case-insensitive) from a text file"""
    file = Path(file)
    output = Path(output) if output else Path.cwd() / f"{file.stem}-filtered{file.suffix}"
    output = output.expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        async with aiofiles.open(file, mode="r") as input_file, aiofiles.open(output, mode="w") as output_file:
            async for line in input_file:
                line_lower = line.lower()
                if all(sub.lower() in line_lower for sub in substrings):
                    await output_file.write(line)
    except UnicodeDecodeError:
        click.echo("Error: File is not a text file", err=True)
        ctx = click.get_current_context()
        ctx.exit(code=1)

    click.echo(f"Generated filtered file at: {output}")
