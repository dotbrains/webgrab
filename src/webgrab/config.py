"""Configuration management for webgrab."""

from pathlib import Path

from .models import CaptureConfig, SaveConfig


def create_capture_config(
    url: str,
    wait_time: int = 0,
    timeout: int = 60000,
    headless: bool = True,
) -> CaptureConfig:
    """Create a capture configuration with defaults.

    Args:
        url: URL to capture.
        wait_time: Additional wait time in seconds.
        timeout: Navigation timeout in milliseconds.
        headless: Whether to run browser in headless mode.

    Returns:
        CaptureConfig instance.
    """
    return CaptureConfig(
        url=url,
        wait_time=wait_time,
        timeout=timeout,
        headless=headless,
    )


def create_save_config(
    output_dir: Path,
    base_url: str,
    include_external: bool = False,
) -> SaveConfig:
    """Create a save configuration with defaults.

    Args:
        output_dir: Output directory path.
        base_url: Base URL for origin checks.
        include_external: Whether to include external resources.

    Returns:
        SaveConfig instance.
    """
    return SaveConfig(
        output_dir=output_dir,
        base_url=base_url,
        include_external=include_external,
    )
