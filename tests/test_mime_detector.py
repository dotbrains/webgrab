"""Tests for MIME type detection."""


from webgrab.mime.detector import get_extension_for_mime, infer_extension


class TestInferExtension:
    """Tests for infer_extension function."""

    def test_infer_extension_existing(self):
        """Test that existing extensions are preserved."""
        assert infer_extension("/path/file.html", "text/html") == "/path/file.html"
        assert infer_extension("/path/style.css", "text/css") == "/path/style.css"

    def test_infer_extension_html(self):
        """Test inferring HTML extension."""
        assert infer_extension("/path/index", "text/html") == "/path/index.html"

    def test_infer_extension_css(self):
        """Test inferring CSS extension."""
        assert infer_extension("/path/style", "text/css") == "/path/style.css"

    def test_infer_extension_javascript(self):
        """Test inferring JavaScript extension."""
        assert infer_extension("/path/app", "text/javascript") == "/path/app.js"
        assert (
            infer_extension("/path/app", "application/javascript") == "/path/app.js"
        )

    def test_infer_extension_json(self):
        """Test inferring JSON extension."""
        assert infer_extension("/path/data", "application/json") == "/path/data.json"

    def test_infer_extension_images(self):
        """Test inferring image extensions."""
        assert infer_extension("/path/img", "image/png") == "/path/img.png"
        assert infer_extension("/path/img", "image/jpeg") == "/path/img.jpg"
        assert infer_extension("/path/img", "image/gif") == "/path/img.gif"
        assert infer_extension("/path/img", "image/webp") == "/path/img.webp"

    def test_infer_extension_fonts(self):
        """Test inferring font extensions."""
        assert infer_extension("/path/font", "font/woff") == "/path/font.woff"
        assert infer_extension("/path/font", "font/woff2") == "/path/font.woff2"
        assert infer_extension("/path/font", "font/ttf") == "/path/font.ttf"

    def test_infer_extension_with_charset(self):
        """Test inferring extension with charset parameter."""
        assert (
            infer_extension("/path/file", "text/html; charset=utf-8")
            == "/path/file.html"
        )

    def test_infer_extension_unknown_mime(self):
        """Test inferring extension with unknown MIME type."""
        assert infer_extension("/path/file", "application/unknown") == "/path/file"


class TestGetExtensionForMime:
    """Tests for get_extension_for_mime function."""

    def test_get_extension_html(self):
        """Test getting extension for HTML."""
        assert get_extension_for_mime("text/html") == ".html"

    def test_get_extension_css(self):
        """Test getting extension for CSS."""
        assert get_extension_for_mime("text/css") == ".css"

    def test_get_extension_javascript(self):
        """Test getting extension for JavaScript."""
        assert get_extension_for_mime("text/javascript") == ".js"
        assert get_extension_for_mime("application/javascript") == ".js"

    def test_get_extension_with_params(self):
        """Test getting extension with MIME parameters."""
        assert get_extension_for_mime("text/html; charset=utf-8") == ".html"

    def test_get_extension_unknown(self):
        """Test getting extension for unknown MIME type."""
        assert get_extension_for_mime("application/unknown") == ""

    def test_get_extension_case_insensitive(self):
        """Test that MIME type matching is case-insensitive."""
        assert get_extension_for_mime("TEXT/HTML") == ".html"
        assert get_extension_for_mime("Text/Html") == ".html"
