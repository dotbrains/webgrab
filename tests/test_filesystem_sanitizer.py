"""Tests for filesystem path sanitization."""

import pytest

from webgrab.filesystem.sanitizer import sanitize_path_component


class TestSanitizePathComponent:
    """Tests for sanitize_path_component function."""

    def test_sanitize_normal_name(self):
        """Test sanitizing a normal filename."""
        assert sanitize_path_component("file.html") == "file.html"

    def test_sanitize_empty_string(self):
        """Test sanitizing empty string."""
        assert sanitize_path_component("") == "_"

    def test_sanitize_invalid_chars(self):
        """Test sanitizing invalid characters."""
        assert sanitize_path_component("file<>:name") == "file___name"
        assert sanitize_path_component("file|name") == "file_name"
        assert sanitize_path_component('file"name') == "file_name"

    def test_sanitize_windows_reserved_names(self):
        """Test sanitizing Windows reserved names."""
        assert sanitize_path_component("CON") == "_CON"
        assert sanitize_path_component("PRN.txt") == "_PRN.txt"
        assert sanitize_path_component("AUX") == "_AUX"
        assert sanitize_path_component("NUL.log") == "_NUL.log"
        assert sanitize_path_component("COM1") == "_COM1"
        assert sanitize_path_component("LPT1") == "_LPT1"

    def test_sanitize_dot_names(self):
        """Test sanitizing dot-only names."""
        assert sanitize_path_component(".") == "_"
        assert sanitize_path_component("..") == "_"

    def test_sanitize_preserves_extension(self):
        """Test that file extensions are preserved."""
        assert sanitize_path_component("file.min.js") == "file.min.js"

    def test_sanitize_long_name(self):
        """Test sanitizing overly long names."""
        long_name = "a" * 200 + ".txt"
        result = sanitize_path_component(long_name)
        assert len(result) <= 104  # MAX_PATH_COMPONENT (100) + extension
        assert result.endswith(".txt")

    def test_sanitize_unicode_preserved(self):
        """Test that unicode characters are preserved."""
        assert sanitize_path_component("файл.txt") == "файл.txt"
        assert sanitize_path_component("文件.html") == "文件.html"

    def test_sanitize_spaces_preserved(self):
        """Test that spaces are preserved."""
        assert sanitize_path_component("my file.txt") == "my file.txt"

    def test_sanitize_mixed_case_reserved(self):
        """Test that mixed case reserved names are handled."""
        assert sanitize_path_component("con") == "_con"
        assert sanitize_path_component("Con") == "_Con"
        assert sanitize_path_component("CON") == "_CON"
