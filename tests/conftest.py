"""Pytest configuration and shared fixtures."""

import tempfile
from pathlib import Path

import pytest


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_html():
    """Sample HTML content for testing."""
    return b"""<!DOCTYPE html>
<html>
<head>
    <title>Test Page</title>
    <link rel="stylesheet" href="/styles.css">
</head>
<body>
    <h1>Hello World</h1>
    <script src="/script.js"></script>
</body>
</html>"""


@pytest.fixture
def sample_css():
    """Sample CSS content for testing."""
    return b"body { margin: 0; }"


@pytest.fixture
def sample_js():
    """Sample JavaScript content for testing."""
    return b"console.log('hello');"
