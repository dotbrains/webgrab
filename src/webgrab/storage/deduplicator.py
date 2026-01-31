"""Path deduplication for avoiding filename conflicts."""

from pathlib import Path


class PathDeduplicator:
    """Manages path deduplication with numeric suffixes."""

    def __init__(self) -> None:
        """Initialize the deduplicator."""
        self.used_paths: set[Path] = set()

    def get_unique_path(self, path: Path) -> Path:
        """Get a unique path by adding numeric suffix if needed.

        Args:
            path: Desired file path.

        Returns:
            Path that doesn't conflict with already-used paths.
        """
        if path not in self.used_paths:
            self.used_paths.add(path)
            return path

        stem = path.stem
        ext = path.suffix
        parent = path.parent
        counter = 1

        while True:
            new_path = parent / f"{stem}_{counter}{ext}"
            if new_path not in self.used_paths:
                self.used_paths.add(new_path)
                return new_path
            counter += 1

    def is_used(self, path: Path) -> bool:
        """Check if a path has been used.

        Args:
            path: Path to check.

        Returns:
            True if path has been used.
        """
        return path in self.used_paths
