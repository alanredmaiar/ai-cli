from pathlib import Path


def validate_dir_exists(ctx, param, value):
    if value is None:
        return None
    
    dir_path = Path(value)
    if not dir_path.exists():
        raise FileNotFoundError(f"Directory {dir_path} does not exist")
    return dir_path


def validate_file_parent_dir_exists(ctx, param, value):
    if value is None:
        return None
    
    file_path = Path(value)
    if not file_path.parent.exists():
        raise FileNotFoundError(f"Directory {file_path.parent} does not exist")
    return file_path


def validate_file_exists(ctx, param, value):
    if value is None:
        return None
    
    file_path = Path(value)
    if not file_path.exists():
        raise FileNotFoundError(f"File {file_path} does not exist")
    return file_path