"""Tests for storage modules."""

from pathlib import Path

import pytest

from webgrab.errors import FileWriteError
from webgrab.models import Resource, SaveConfig
from webgrab.storage.deduplicator import PathDeduplicator
from webgrab.storage.path_resolver import url_to_local_path
from webgrab.storage.saver import ResourceSaver
from webgrab.storage.writer import file_exists, write_file


class TestPathResolver:
    """Tests for path resolution."""

    def test_url_to_local_path_basic(self, temp_dir):
        """Test basic URL to path conversion."""
        path = url_to_local_path("https://example.com/page.html", temp_dir)
        assert path == temp_dir / "example.com" / "page.html"

    def test_url_to_local_path_nested(self, temp_dir):
        """Test nested path conversion."""
        path = url_to_local_path("https://example.com/path/to/file.js", temp_dir)
        assert path == temp_dir / "example.com" / "path" / "to" / "file.js"

    def test_url_to_local_path_root(self, temp_dir):
        """Test root path conversion."""
        path = url_to_local_path("https://example.com/", temp_dir)
        assert path == temp_dir / "example.com" / "index.html"

    def test_url_to_local_path_directory_index(self, temp_dir):
        """Test directory with trailing slash."""
        path = url_to_local_path("https://example.com/docs/", temp_dir)
        assert path == temp_dir / "example.com" / "docs" / "index.html"

    def test_url_to_local_path_with_port(self, temp_dir):
        """Test URL with port number."""
        path = url_to_local_path("https://example.com:8080/page.html", temp_dir)
        assert path == temp_dir / "example.com" / "page.html"

    def test_url_to_local_path_url_encoded(self, temp_dir):
        """Test URL encoded paths."""
        path = url_to_local_path("https://example.com/path%20with%20spaces.html", temp_dir)
        assert path == temp_dir / "example.com" / "path with spaces.html"


class TestPathDeduplicator:
    """Tests for path deduplication."""

    def test_deduplicator_unique_path(self, temp_dir):
        """Test getting unique path when no conflict."""
        dedup = PathDeduplicator()
        path = temp_dir / "file.html"
        result = dedup.get_unique_path(path)
        assert result == path

    def test_deduplicator_duplicate_path(self, temp_dir):
        """Test getting unique path with conflict."""
        dedup = PathDeduplicator()
        path = temp_dir / "file.html"
        
        first = dedup.get_unique_path(path)
        second = dedup.get_unique_path(path)
        third = dedup.get_unique_path(path)
        
        assert first == temp_dir / "file.html"
        assert second == temp_dir / "file_1.html"
        assert third == temp_dir / "file_2.html"

    def test_deduplicator_is_used(self, temp_dir):
        """Test checking if path is used."""
        dedup = PathDeduplicator()
        path = temp_dir / "file.html"
        
        assert not dedup.is_used(path)
        dedup.get_unique_path(path)
        assert dedup.is_used(path)


class TestWriter:
    """Tests for file writer."""

    def test_write_file_creates_parents(self, temp_dir):
        """Test that parent directories are created."""
        path = temp_dir / "nested" / "path" / "file.txt"
        write_file(path, b"content")
        assert path.exists()
        assert path.read_bytes() == b"content"

    def test_write_file_overwrites(self, temp_dir):
        """Test that existing files are overwritten."""
        path = temp_dir / "file.txt"
        write_file(path, b"first")
        write_file(path, b"second")
        assert path.read_bytes() == b"second"

    def test_file_exists_true(self, temp_dir):
        """Test file_exists returns true for existing file."""
        path = temp_dir / "file.txt"
        path.write_text("content")
        assert file_exists(path)

    def test_file_exists_false(self, temp_dir):
        """Test file_exists returns false for non-existing file."""
        path = temp_dir / "nonexistent.txt"
        assert not file_exists(path)

    def test_file_exists_directory(self, temp_dir):
        """Test file_exists returns false for directory."""
        subdir = temp_dir / "subdir"
        subdir.mkdir()
        assert not file_exists(subdir)


class TestResourceSaver:
    """Tests for resource saver."""

    def test_save_resource_basic(self, temp_dir, sample_html):
        """Test saving a basic resource."""
        config = SaveConfig(
            output_dir=temp_dir,
            base_url="https://example.com",
            include_external=False,
        )
        saver = ResourceSaver(config)
        
        resource = Resource(
            url="https://example.com/index.html",
            content_type="text/html",
            body=sample_html,
            headers={"content-type": "text/html"},
            status_code=200,
        )
        
        saved_path = saver.save_resource(resource)
        assert saved_path is not None
        assert saved_path.exists()
        assert saved_path.read_bytes() == sample_html

    def test_save_resource_external_excluded(self, temp_dir, sample_css):
        """Test that external resources are excluded by default."""
        config = SaveConfig(
            output_dir=temp_dir,
            base_url="https://example.com",
            include_external=False,
        )
        saver = ResourceSaver(config)
        
        resource = Resource(
            url="https://cdn.example.org/style.css",
            content_type="text/css",
            body=sample_css,
            headers={"content-type": "text/css"},
            status_code=200,
        )
        
        saved_path = saver.save_resource(resource)
        assert saved_path is None

    def test_save_resource_external_included(self, temp_dir, sample_css):
        """Test that external resources are included when configured."""
        config = SaveConfig(
            output_dir=temp_dir,
            base_url="https://example.com",
            include_external=True,
        )
        saver = ResourceSaver(config)
        
        resource = Resource(
            url="https://cdn.example.org/style.css",
            content_type="text/css",
            body=sample_css,
            headers={"content-type": "text/css"},
            status_code=200,
        )
        
        saved_path = saver.save_resource(resource)
        assert saved_path is not None
        assert saved_path.exists()

    def test_save_resources_multiple(self, temp_dir, sample_html, sample_css, sample_js):
        """Test saving multiple resources."""
        config = SaveConfig(
            output_dir=temp_dir,
            base_url="https://example.com",
            include_external=False,
        )
        saver = ResourceSaver(config)
        
        resources = [
            Resource(
                url="https://example.com/index.html",
                content_type="text/html",
                body=sample_html,
                headers={},
                status_code=200,
            ),
            Resource(
                url="https://example.com/style.css",
                content_type="text/css",
                body=sample_css,
                headers={},
                status_code=200,
            ),
            Resource(
                url="https://example.com/script.js",
                content_type="text/javascript",
                body=sample_js,
                headers={},
                status_code=200,
            ),
        ]
        
        result = saver.save_resources(resources)
        assert result.saved_count == 3
        assert result.skipped_count == 0
        assert result.total_failures == 0

    def test_save_resources_with_skipped(self, temp_dir, sample_html, sample_css):
        """Test saving resources with some skipped."""
        config = SaveConfig(
            output_dir=temp_dir,
            base_url="https://example.com",
            include_external=False,
        )
        saver = ResourceSaver(config)
        
        resources = [
            Resource(
                url="https://example.com/index.html",
                content_type="text/html",
                body=sample_html,
                headers={},
                status_code=200,
            ),
            Resource(
                url="https://cdn.example.org/style.css",
                content_type="text/css",
                body=sample_css,
                headers={},
                status_code=200,
            ),
        ]
        
        result = saver.save_resources(resources)
        assert result.saved_count == 1
        assert result.skipped_count == 1
