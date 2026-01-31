"""Tests for URL parsing utilities."""

import pytest

from webgrab.errors import ConfigurationError
from webgrab.url.parser import is_same_origin, parse_url, should_skip_url


class TestParseUrl:
    """Tests for parse_url function."""

    def test_parse_valid_url(self):
        """Test parsing a valid URL."""
        parsed = parse_url("https://example.com/path")
        assert parsed.scheme == "https"
        assert parsed.netloc == "example.com"
        assert parsed.path == "/path"

    def test_parse_url_adds_https(self):
        """Test that https is added to URLs without scheme."""
        parsed = parse_url("example.com")
        assert parsed.scheme == "https"
        assert parsed.netloc == "example.com"

    def test_parse_url_preserves_http(self):
        """Test that http scheme is preserved."""
        parsed = parse_url("http://example.com")
        assert parsed.scheme == "http"

    def test_parse_url_invalid_no_host(self):
        """Test parsing invalid URL without host."""
        with pytest.raises(ConfigurationError, match="missing host"):
            parse_url("https://")

    def test_parse_url_invalid_scheme(self):
        """Test parsing URL with invalid scheme."""
        with pytest.raises(ConfigurationError, match="must be http or https"):
            parse_url("ftp://example.com")


class TestIsSameOrigin:
    """Tests for is_same_origin function."""

    def test_same_origin_same_host(self):
        """Test same origin with identical hosts."""
        assert is_same_origin("https://example.com/page1", "https://example.com/page2")

    def test_same_origin_different_paths(self):
        """Test same origin with different paths."""
        assert is_same_origin(
            "https://example.com/path1", "https://example.com/path2"
        )

    def test_different_origin_different_hosts(self):
        """Test different origin with different hosts."""
        assert not is_same_origin(
            "https://example.com/page", "https://other.com/page"
        )

    def test_different_origin_subdomain(self):
        """Test different origin with subdomain."""
        assert not is_same_origin(
            "https://example.com/page", "https://sub.example.com/page"
        )

    def test_same_origin_with_port(self):
        """Test same origin with port."""
        assert is_same_origin(
            "https://example.com:8080/page1", "https://example.com:8080/page2"
        )


class TestShouldSkipUrl:
    """Tests for should_skip_url function."""

    def test_skip_data_url(self):
        """Test skipping data URLs."""
        assert should_skip_url("data:image/png;base64,iVBOR...")

    def test_skip_blob_url(self):
        """Test skipping blob URLs."""
        assert should_skip_url("blob:https://example.com/...")

    def test_skip_javascript_url(self):
        """Test skipping javascript URLs."""
        assert should_skip_url("javascript:void(0)")

    def test_skip_about_url(self):
        """Test skipping about URLs."""
        assert should_skip_url("about:blank")

    def test_skip_chrome_extension(self):
        """Test skipping chrome extension URLs."""
        assert should_skip_url("chrome-extension://...")

    def test_dont_skip_http_url(self):
        """Test not skipping normal HTTP URLs."""
        assert not should_skip_url("https://example.com/page")

    def test_dont_skip_relative_url(self):
        """Test not skipping relative URLs."""
        assert not should_skip_url("/path/to/resource")
