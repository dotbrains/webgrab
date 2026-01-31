"""MIME type detection and file extension mapping."""

from pathlib import Path

# MIME type to file extension mapping
CONTENT_TYPE_MAP: dict[str, str] = {
    # Text
    "text/html": ".html",
    "text/css": ".css",
    "text/javascript": ".js",
    "text/plain": ".txt",
    "text/xml": ".xml",
    # Application
    "application/javascript": ".js",
    "application/x-javascript": ".js",
    "application/json": ".json",
    "application/xml": ".xml",
    "application/pdf": ".pdf",
    "application/zip": ".zip",
    "application/gzip": ".gz",
    "application/wasm": ".wasm",
    "application/manifest+json": ".webmanifest",
    # Images
    "image/png": ".png",
    "image/jpeg": ".jpg",
    "image/gif": ".gif",
    "image/svg+xml": ".svg",
    "image/webp": ".webp",
    "image/x-icon": ".ico",
    "image/vnd.microsoft.icon": ".ico",
    "image/avif": ".avif",
    # Fonts
    "font/woff": ".woff",
    "font/woff2": ".woff2",
    "font/ttf": ".ttf",
    "font/otf": ".otf",
    "application/font-woff": ".woff",
    "application/font-woff2": ".woff2",
    "application/x-font-woff": ".woff",
    "application/x-font-ttf": ".ttf",
    "application/vnd.ms-fontobject": ".eot",
    # Audio/Video
    "audio/mpeg": ".mp3",
    "audio/wav": ".wav",
    "audio/ogg": ".ogg",
    "video/mp4": ".mp4",
    "video/webm": ".webm",
    "video/ogg": ".ogv",
}


def infer_extension(path: str, content_type: str) -> str:
    """Add file extension based on content-type if path lacks one.

    Args:
        path: URL path that may lack an extension.
        content_type: Content-Type header value.

    Returns:
        Path with extension added if needed.
    """
    filename = Path(path).name

    # Check if already has an extension
    if "." in filename:
        return path

    # Parse content-type (ignore charset, boundary, etc.)
    mime = content_type.split(";")[0].strip().lower()
    ext = CONTENT_TYPE_MAP.get(mime, "")

    return path + ext


def get_extension_for_mime(mime_type: str) -> str:
    """Get file extension for a MIME type.

    Args:
        mime_type: MIME type string.

    Returns:
        File extension (with leading dot) or empty string if unknown.
    """
    mime = mime_type.split(";")[0].strip().lower()
    return CONTENT_TYPE_MAP.get(mime, "")
