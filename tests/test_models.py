"""Tests for domain models."""

from pathlib import Path

import pytest

from webgrab.models import CaptureConfig, CaptureStats, Resource, SaveConfig, SaveResult


class TestResource:
    """Tests for Resource model."""

    def test_resource_creation(self):
        """Test creating a resource."""
        resource = Resource(
            url="https://example.com/test.html",
            content_type="text/html",
            body=b"<html></html>",
            headers={"content-type": "text/html"},
            status_code=200,
        )
        assert resource.url == "https://example.com/test.html"
        assert resource.size == len(b"<html></html>")

    def test_resource_immutable(self):
        """Test that resources are immutable."""
        resource = Resource(
            url="https://example.com/test.html",
            content_type="text/html",
            body=b"test",
            headers={},
            status_code=200,
        )
        with pytest.raises(AttributeError):
            resource.url = "https://new-url.com"


class TestCaptureConfig:
    """Tests for CaptureConfig model."""

    def test_capture_config_defaults(self):
        """Test capture config with defaults."""
        config = CaptureConfig(url="https://example.com")
        assert config.url == "https://example.com"
        assert config.wait_time == 0
        assert config.timeout == 60000
        assert config.headless is True

    def test_capture_config_validation_negative_wait(self):
        """Test validation for negative wait time."""
        with pytest.raises(ValueError, match="wait_time must be non-negative"):
            CaptureConfig(url="https://example.com", wait_time=-1)

    def test_capture_config_validation_zero_timeout(self):
        """Test validation for zero timeout."""
        with pytest.raises(ValueError, match="timeout must be positive"):
            CaptureConfig(url="https://example.com", timeout=0)


class TestSaveConfig:
    """Tests for SaveConfig model."""

    def test_save_config_creation(self, temp_dir):
        """Test creating a save config."""
        config = SaveConfig(
            output_dir=temp_dir,
            base_url="https://example.com",
            include_external=True,
        )
        assert config.output_dir == temp_dir
        assert config.base_url == "https://example.com"
        assert config.include_external is True


class TestCaptureStats:
    """Tests for CaptureStats model."""

    def test_capture_stats_defaults(self):
        """Test capture stats with defaults."""
        stats = CaptureStats()
        assert stats.total_requests == 0
        assert stats.successful_captures == 0
        assert stats.success_rate == 0.0

    def test_capture_stats_success_rate(self):
        """Test success rate calculation."""
        stats = CaptureStats(total_requests=10, successful_captures=8)
        assert stats.success_rate == 80.0


class TestSaveResult:
    """Tests for SaveResult model."""

    def test_save_result_defaults(self):
        """Test save result with defaults."""
        result = SaveResult()
        assert result.saved_count == 0
        assert result.skipped_count == 0
        assert result.total_failures == 0

    def test_save_result_counts(self, temp_dir):
        """Test save result counts."""
        result = SaveResult(
            saved_paths=[temp_dir / "file1.html", temp_dir / "file2.css"],
            skipped_count=3,
            failed_saves=[("https://example.com/error", Exception("test"))],
        )
        assert result.saved_count == 2
        assert result.skipped_count == 3
        assert result.total_failures == 1
