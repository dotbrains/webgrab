"""Tests for capture filters."""

import pytest

from webgrab.capture.filters import CompositeFilter, DefaultFilter


class TestDefaultFilter:
    """Tests for DefaultFilter."""

    def test_filter_allows_success_status(self):
        """Test that successful status codes are allowed."""
        filter = DefaultFilter()
        assert filter.should_capture("https://example.com/page", "text/html", 200)
        assert filter.should_capture("https://example.com/page", "text/html", 201)
        assert filter.should_capture("https://example.com/page", "text/html", 304)

    def test_filter_rejects_error_status(self):
        """Test that error status codes are rejected."""
        filter = DefaultFilter()
        assert not filter.should_capture("https://example.com/page", "text/html", 400)
        assert not filter.should_capture("https://example.com/page", "text/html", 404)
        assert not filter.should_capture("https://example.com/page", "text/html", 500)

    def test_filter_rejects_data_urls(self):
        """Test that data URLs are rejected."""
        filter = DefaultFilter()
        assert not filter.should_capture("data:image/png;base64,iVBOR...", "image/png", 200)

    def test_filter_rejects_blob_urls(self):
        """Test that blob URLs are rejected."""
        filter = DefaultFilter()
        assert not filter.should_capture("blob:https://example.com/...", "text/plain", 200)

    def test_filter_rejects_javascript_urls(self):
        """Test that javascript URLs are rejected."""
        filter = DefaultFilter()
        assert not filter.should_capture("javascript:void(0)", "text/javascript", 200)

    def test_filter_allows_normal_urls(self):
        """Test that normal URLs are allowed."""
        filter = DefaultFilter()
        assert filter.should_capture("https://example.com/page.html", "text/html", 200)
        assert filter.should_capture("https://example.com/style.css", "text/css", 200)
        assert filter.should_capture("https://example.com/script.js", "text/javascript", 200)


class TestCompositeFilter:
    """Tests for CompositeFilter."""

    def test_composite_filter_all_pass(self):
        """Test that all filters must pass."""
        filter1 = DefaultFilter()
        filter2 = DefaultFilter()
        composite = CompositeFilter([filter1, filter2])
        
        assert composite.should_capture("https://example.com/page", "text/html", 200)

    def test_composite_filter_one_fails(self):
        """Test that if one filter fails, capture is rejected."""
        class RejectAllFilter:
            def should_capture(self, url, content_type, status_code):
                return False
        
        filter1 = DefaultFilter()
        filter2 = RejectAllFilter()
        composite = CompositeFilter([filter1, filter2])
        
        assert not composite.should_capture("https://example.com/page", "text/html", 200)

    def test_composite_filter_empty(self):
        """Test composite filter with no filters."""
        composite = CompositeFilter([])
        assert composite.should_capture("https://example.com/page", "text/html", 200)
