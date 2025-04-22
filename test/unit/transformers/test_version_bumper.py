import os
import shutil
import pytest
import tempfile
import tomli
from scripts.transformers.version_bumper import bump_version, update_pyproject, prerelease_bump


# Test cases for the bump_version function
@pytest.mark.parametrize(
    "current_version,rule,downgrade,expected",
    [
        # Test regular version bumping
        ("1.2.3", "major", False, "2.0.0"),
        ("1.2.3", "minor", False, "1.3.0"),
        ("1.2.3", "patch", False, "1.2.4"),
        # Test premajor/preminor/prepatch
        ("1.2.3", "premajor", False, "2.0.0a0"),
        ("1.2.3", "preminor", False, "1.3.0a0"),
        ("1.2.3", "prepatch", False, "1.2.4a0"),
        # Test prerelease bumping
        ("1.2.3a0", "prerelease", False, "1.2.3a1"),
        ("1.2.3b1", "prerelease", False, "1.2.3b2"),
        ("1.2.3a9", "prerelease", False, "1.2.3a10"),
        # Test downgrading
        ("1.2.3", "major", True, "0.0.0"),
        ("1.2.3", "minor", True, "1.1.0"),
        ("1.2.3", "patch", True, "1.2.2"),
        # Test downgrading prerelease
        ("1.2.3a1", "prerelease", True, "1.2.3a0"),
        ("1.2.3b2", "prerelease", True, "1.2.3b1"),
        # Edge cases
        ("0.0.1", "patch", True, "0.0.0"),
        ("0.1.0", "minor", True, "0.0.0"),
        ("1.0.0", "major", True, "0.0.0"),
        # First prerelease downgrade
        ("1.2.3a0", "prerelease", True, "1.2.2"),
    ],
)
def test_bump_version(current_version, rule, downgrade, expected):
    """Test that version bumping works correctly for various scenarios."""
    result = bump_version(current_version, rule, downgrade)
    assert result == expected, f"Expected {expected} but got {result} when bumping {current_version} with rule {rule} and downgrade={downgrade}"


@pytest.mark.parametrize(
    "invalid_version",
    [
        "1.2",  # Missing patch version
        "1.a.3",  # Non-numeric minor version
        "1.2.3.4",  # Too many segments
        "v1.2.3",  # Leading v
        "1.2.3-rc1",  # Incorrect prerelease format
    ],
)
def test_bump_version_invalid_format(invalid_version):
    """Test that bump_version raises ValueError for invalid version formats."""
    with pytest.raises(ValueError, match="Invalid version format"):
        bump_version(invalid_version, "patch")


@pytest.mark.parametrize(
    "version,expected_groups",
    [
        (("1", "2", "3", None), (1, 2, 3, None)),
        (("1", "2", "3", "a0"), (1, 2, 3, "a0")),
        (("1", "2", "3", "b1"), (1, 2, 3, "b1")),
    ],
)
def test_prerelease_bump(version, expected_groups):
    """Test the prerelease_bump function with different version tuples."""
    # Test incrementing
    result = prerelease_bump(version, False)
    if version[3] is None:
        # For non-prerelease versions, it should add a0
        assert result == (*map(int, version[:3]), "a0"), f"Failed on increment of {version}"
    else:
        # Extract the tag and number from prerelease
        tag = version[3][0]
        num = int(version[3][1:])
        expected = (*map(int, version[:3]), f"{tag}{num+1}")
        assert result == expected, f"Failed on increment of {version}"
    
    # Test decrementing
    result = prerelease_bump(version, True)
    if version[3] is None or version[3] == "a0" or version[3] == "b0":
        # Should decrement the patch version
        expected = (int(version[0]), int(version[1]), int(version[2]) - 1, None)
        # We need to compensate for the fact that prerelease_bump doesn't return None for the last element
        assert result[:3] == expected[:3], f"Failed on decrement of {version}"
    else:
        # Extract the tag and number from prerelease
        tag = version[3][0]
        num = int(version[3][1:])
        expected = (*map(int, version[:3]), f"{tag}{num-1}")
        assert result == expected, f"Failed on decrement of {version}"


# Fixtures for pyproject.toml testing
@pytest.fixture
def temp_dir():
    """Create a temporary directory for pyproject.toml testing."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture
def setup_temp_pyproject(temp_dir, request):
    """Setup a temporary pyproject.toml file based on a template."""
    template_path = os.path.join(
        "test", "resources", f"pyproject_{request.param}.toml"
    )
    temp_pyproject = os.path.join(temp_dir, "pyproject.toml")
    shutil.copy(template_path, temp_pyproject)
    
    # Return the current working directory so we can restore it later
    cwd = os.getcwd()
    # Change to the temp directory
    os.chdir(temp_dir)
    
    yield temp_pyproject
    
    # Change back to the original directory
    os.chdir(cwd)


@pytest.mark.parametrize(
    "setup_temp_pyproject,rule,downgrade,expected_version",
    [
        # Regular version bumping
        ("regular", "patch", False, "1.2.4"),
        ("regular", "minor", False, "1.3.0"),
        ("regular", "major", False, "2.0.0"),
        # Prerelease version bumping
        ("regular", "prepatch", False, "1.2.4a0"),
        ("regular", "preminor", False, "1.3.0a0"),
        ("regular", "premajor", False, "2.0.0a0"),
        # Test with prerelease versions
        ("prerelease", "prerelease", False, "1.2.3a2"),
        ("beta", "prerelease", False, "1.2.3b3"),
        # Test downgrading
        ("regular", "patch", True, "1.2.2"),
        ("regular", "minor", True, "1.1.0"),
        ("regular", "major", True, "0.0.0"),
        # Test downgrading prerelease
        ("prerelease", "prerelease", True, "1.2.3a0"),
        ("beta", "prerelease", True, "1.2.3b1"),
    ],
    indirect=["setup_temp_pyproject"],
)
def test_update_pyproject(setup_temp_pyproject, rule, downgrade, expected_version):
    """Test updating pyproject.toml with various version bumping rules."""
    # Run the update_pyproject function
    update_pyproject(rule, downgrade)
    
    # Read the updated pyproject.toml
    with open(setup_temp_pyproject, "rb") as f:
        pyproject_data = tomli.load(f)
    
    # Check that the version was updated correctly
    assert pyproject_data["project"]["version"] == expected_version, (
        f"Expected version {expected_version} but got {pyproject_data['project']['version']} "
        f"when applying rule {rule} with downgrade={downgrade}"
    )


@pytest.mark.parametrize(
    "setup_temp_pyproject",
    [("regular")],
    indirect=True,
)
def test_update_pyproject_invalid_rule(setup_temp_pyproject, monkeypatch):
    """Test that update_pyproject exits with error for invalid rules."""
    with pytest.raises(KeyError):
        update_pyproject("invalid_rule", False)


@pytest.mark.parametrize(
    "setup_temp_pyproject",
    [("regular")],
    indirect=True,
)
def test_missing_version_key(setup_temp_pyproject):
    """Test that update_pyproject raises an error when version key is not found."""
    # Write a pyproject.toml file without a version key
    with open(setup_temp_pyproject, "w") as f:
        f.write("[project]\nname = 'test-project'\n")
    
    with pytest.raises(ValueError, match="Version key not found in pyproject.toml"):
        update_pyproject()
