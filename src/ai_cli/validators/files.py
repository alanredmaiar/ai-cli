from pathlib import Path


def validate_dir_exists(dir: Path) -> None:
    if not dir.exists():
        raise FileNotFoundError(f"Directory {dir} does not exist")


def validate_file_parent_dir_exists(file: Path) -> None:
    if not file.parent.exists():
        raise FileNotFoundError(f"Directory {file.parent} does not exist")


def validate_file_exists(file: Path) -> None:
    if not file.exists():
        raise FileNotFoundError(f"File {file} does not exist")
