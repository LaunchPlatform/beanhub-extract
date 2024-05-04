import pathlib


def strip_base_path(base: pathlib.Path, filepath: str | pathlib.Path) -> str:
    """Strip file base path (parent folder) from given file path"""
    if isinstance(filepath, pathlib.Path):
        filepath = pathlib.Path(filepath)
    return str(filepath.relative_to(base))
