"""URL to filesystem path resolution."""

from pathlib import Path
from urllib.parse import unquote, urlparse

from ..filesystem.sanitizer import sanitize_path_component


def url_to_local_path(url: str, output_dir: Path) -> Path:
    """Convert a URL to a local file path preserving directory structure.

    Args:
        url: Full URL of the resource.
        output_dir: Base output directory.

    Returns:
        Local path where the resource should be saved.
    """
    parsed = urlparse(url)

    # Get host (strip port for directory name)
    host = parsed.netloc.split(":")[0]
    host = sanitize_path_component(host)

    # Get path and decode URL encoding
    url_path = unquote(parsed.path)

    # Handle root path
    if not url_path or url_path == "/":
        url_path = "/index.html"

    # Handle paths ending with / (directory index)
    if url_path.endswith("/"):
        url_path = url_path + "index.html"

    # Split into components and sanitize each
    path_parts = url_path.strip("/").split("/")
    sanitized_parts = [sanitize_path_component(part) for part in path_parts]

    # Build full local path
    local_path = output_dir / host / Path(*sanitized_parts)

    return local_path
