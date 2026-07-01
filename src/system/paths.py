from pathlib import Path

def get_project_root() -> Path:
    file_targets = ['.git', 'pyproject.toml']
    try:
        root_dir = next(
            p for p in Path(__file__).resolve().parents
            if any((p / target).exists() for target in file_targets)
            )
    except StopIteration:
        raise FileNotFoundError(f"Top of file system reached without finding files: {' ,'.join(file_targets)}")

    return root_dir
