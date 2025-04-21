from pathlib import Path


def validate_dir_exists(dir: Path) -> Path:
    if not dir.exists():
        raise FileNotFoundError(f"Directory {dir} does not exist")
    return dir


def validate_file_parent_dir_exists(file: Path) -> Path:
    if not file.parent.exists():
        raise FileNotFoundError(f"Directory {file.parent} does not exist")
    return file


def validate_file_exists(file: Path) -> Path:
    if not file.exists():
        raise FileNotFoundError(f"File {file} does not exist")
    return file