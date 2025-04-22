from pathlib import Path

import pytest
from click.testing import CliRunner


@pytest.fixture
def cli_runner():
    """Return a CliRunner instance for testing CLI commands."""
    return CliRunner()


@pytest.fixture
def sample_log_path():
    """Return the path to the sample log file."""
    return Path(__file__).parent.parent / "resources" / "sample-log.log"


@pytest.fixture
def temp_output_path(tmp_path):
    """Return a temporary path for output files."""
    return tmp_path / "output.log"


@pytest.fixture
def cleanup_output():
    """Fixture to clean up any test output files."""
    yield
    # Clean up any test output files created in the current directory
    for file in Path.cwd().glob("*-filtered.log"):
        if file.is_file():
            file.unlink() 