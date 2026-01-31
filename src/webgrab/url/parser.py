"""URL parsing and validation utilities."""

from urllib.parse import ParseResult, urlparse

from ..errors import ConfigurationError


def parse_url(url: str) -> ParseResult:
    """Validate and parse a URL.

    Args:
        url: The URL string to parse.

    Returns:
        Parsed URL components.

    Raises:
        ConfigurationError: If URL is invalid or missing scheme/host.
    """
    # Add scheme if missing
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    parsed = urlparse(url)

    if not parsed.netloc:
        raise ConfigurationError(f"Invalid URL: missing host in '{url}'")

    if parsed.scheme not in ("http", "https"):
        raise ConfigurationError(
            f"Invalid URL scheme: '{parsed.scheme}' (must be http or https)"
        )

    return parsed


def is_same_origin(url: str, base_url: str) -> bool:
    """Check if a URL is same-origin as the base URL.

    Args:
        url: URL to check.
        base_url: Base URL to compare against.

    Returns:
        True if both URLs have the same origin (scheme + host).
    """
    parsed_url = urlparse(url)
    parsed_base = urlparse(base_url)
    return parsed_url.netloc == parsed_base.netloc


def should_skip_url(url: str) -> bool:
    """Check if a URL should be skipped (data:, blob:, etc.).

    Args:
        url: URL to check.

    Returns:
        True if URL should be skipped.
    """
    skip_prefixes = (
        "data:",
        "blob:",
        "about:",
        "javascript:",
        "chrome:",
        "chrome-extension:",
    )
    return url.startswith(skip_prefixes)
