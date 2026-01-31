"""Low-level file I/O operations."""

from pathlib import Path

from ..errors import FileWriteError


def write_file(path: Path, content: bytes, create_parents: bool = True) -> None:
    """Write content to a file.

    Args:
        path: Path to write to.
        content: Binary content to write.
        create_parents: Whether to create parent directories.

    Raises:
        FileWriteError: If writing fails.
    """
    try:
        if create_parents:
            path.parent.mkdir(parents=True, exist_ok=True)

        path.write_bytes(content)
    except OSError as e:
        raise FileWriteError(str(path), str(e), e) from e


def file_exists(path: Path) -> bool:
    """Check if a file exists.

    Args:
        path: Path to check.

    Returns:
        True if file exists.
    """
    return path.exists() and path.is_file()
