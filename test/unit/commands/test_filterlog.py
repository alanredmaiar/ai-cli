import pytest
import typer
from pathlib import Path
from typer.testing import CliRunner

from ai_cli.commands.filterlog import filterlog


@pytest.fixture
def runner():
    """Return a CliRunner instance."""
    return CliRunner()


@pytest.mark.asyncio
async def test_filter_by_single_substring(sample_log_path, temp_output_path, cleanup_output):
    """Test filtering by a single substring."""
    # Call the filterlog function directly with a single substring
    await filterlog(
        file=sample_log_path,
        substrings=["error"],
        output=temp_output_path
    )
    
    # Verify the output file exists
    assert temp_output_path.exists()
    
    # Read the output and verify content
    with open(temp_output_path, "r") as f:
        lines = f.readlines()
    
    # Should have 4 lines with "ERROR"
    assert len(lines) == 4
    assert all("ERROR" in line for line in lines)


@pytest.mark.asyncio
async def test_filter_by_multiple_substrings(sample_log_path, temp_output_path, cleanup_output):
    """Test filtering by multiple substrings."""
    # Call the filterlog function with multiple substrings
    await filterlog(
        file=sample_log_path,
        substrings=["info", "success"],
        output=temp_output_path
    )
    
    # Verify the output file exists
    assert temp_output_path.exists()
    
    # Read the output and verify content
    with open(temp_output_path, "r") as f:
        lines = f.readlines()
    
    # Should have lines containing both "INFO" and "success"
    assert len(lines) > 0
    assert all("INFO" in line and "success" in line for line in lines)


@pytest.mark.asyncio
async def test_case_insensitive_filtering(sample_log_path, temp_output_path, cleanup_output):
    """Test that filtering is case-insensitive."""
    # Call with mixed case substrings
    await filterlog(
        file=sample_log_path,
        substrings=["WaRNiNg"],
        output=temp_output_path
    )
    
    # Verify the output file exists
    assert temp_output_path.exists()
    
    # Read the output and verify content
    with open(temp_output_path, "r") as f:
        lines = f.readlines()
    
    # Should have 2 lines with "WARNING"
    assert len(lines) == 2
    assert all("WARNING" in line for line in lines)


@pytest.mark.asyncio
async def test_default_output_path(sample_log_path, monkeypatch, cleanup_output):
    """Test the default output path when none is specified."""
    
    try:
        # Call without specifying an output path
        await filterlog(
            file=sample_log_path,
            substrings=["DEBUG"]
        )
        
        # Check for the default output file
        expected_output = Path.cwd() / f"{sample_log_path.stem}-filtered{sample_log_path.suffix}"
        assert expected_output.exists()
        
        # Verify content
        with open(expected_output, "r") as f:
            lines = f.readlines()
        
        # Should have 4 lines with "DEBUG"
        assert len(lines) == 4
        assert all("DEBUG" in line for line in lines)
        
    finally:
        # Clean up the created file
        expected_output = Path.cwd() / f"{sample_log_path.stem}-filtered{sample_log_path.suffix}"
        if expected_output.exists():
            expected_output.unlink()


@pytest.mark.asyncio
async def test_no_matching_lines(sample_log_path, temp_output_path, cleanup_output):
    """Test behavior when no lines match the filtering criteria."""
    # Call with a substring that doesn't exist in the log
    await filterlog(
        file=sample_log_path,
        substrings=["CRITICAL", "exception"],
        output=temp_output_path
    )
    
    # Verify the output file exists but is empty
    assert temp_output_path.exists()
    assert temp_output_path.stat().st_size == 0


@pytest.mark.asyncio
async def test_parent_directory_creation(sample_log_path, tmp_path, cleanup_output):
    """Test that parent directories are created if they don't exist."""
    # Create a deeper path that doesn't exist yet
    deep_path = tmp_path / "nested" / "dirs" / "output.log"
    
    # Call filterlog
    await filterlog(
        file=sample_log_path,
        substrings=["INFO"],
        output=deep_path
    )
    
    # Verify the output file and its parent directories were created
    assert deep_path.exists()
    
    # Verify content
    with open(deep_path, "r") as f:
        lines = f.readlines()
    
    # Should have lines with "INFO"
    assert len(lines) > 0
    assert all("INFO" in line for line in lines)


@pytest.mark.parametrize("non_text_file", [
    pytest.param(True, marks=pytest.mark.xfail(raises=typer.Exit, reason="Binary file should raise UnicodeDecodeError")),
])
@pytest.mark.asyncio
async def test_non_text_file_handling(temp_output_path, cleanup_output, non_text_file, tmp_path):
    """Test handling of non-text (binary) files."""
    if non_text_file:
        # Create a binary file
        binary_file = tmp_path / "binary.dat"
        with open(binary_file, "wb") as f:
            f.write(b'\x00\x01\x02\x03\x04\xff\xfe\xfd')
        
        # Call filterlog with the binary file
        with pytest.raises(typer.Exit):
            await filterlog(
                file=binary_file,
                substrings=["test"],
                output=temp_output_path
            ) 