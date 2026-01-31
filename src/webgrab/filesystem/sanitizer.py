"""Path sanitization for cross-platform filesystem safety."""

import re

# Characters invalid in filenames (Windows-focused for cross-platform compat)
INVALID_CHARS = re.compile(r'[<>:"|?*\x00-\x1f\\]')

# Windows reserved names
WINDOWS_RESERVED = frozenset({
    "CON", "PRN", "AUX", "NUL",
    "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9",
    "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9",
})

MAX_PATH_COMPONENT = 100
MAX_FILENAME_LENGTH = 200


def sanitize_path_component(name: str) -> str:
    """Clean a path component for filesystem safety.

    Args:
        name: Raw path component from URL.

    Returns:
        Sanitized component safe for filesystem use.
    """
    if not name:
        return "_"

    # Remove invalid characters
    name = INVALID_CHARS.sub("_", name)

    # Handle Windows reserved names
    name_upper = name.upper()
    # Check both exact match and with extension (e.g., CON.txt)
    base_name = name_upper.split(".")[0]
    if base_name in WINDOWS_RESERVED:
        name = f"_{name}"

    # Handle empty or dot-only names
    if not name or name in (".", ".."):
        name = "_"

    # Truncate if too long
    if len(name) > MAX_PATH_COMPONENT:
        stem, ext = _split_extension(name)
        max_stem = MAX_PATH_COMPONENT - len(ext)
        name = stem[:max_stem] + ext

    return name


def _split_extension(filename: str) -> tuple[str, str]:
    """Split filename into stem and extension.

    Args:
        filename: The filename to split.

    Returns:
        Tuple of (stem, extension) where extension includes the dot.
    """
    if "." not in filename:
        return filename, ""

    # Handle double extensions like .min.js
    parts = filename.rsplit(".", 1)
    return parts[0], "." + parts[1]
