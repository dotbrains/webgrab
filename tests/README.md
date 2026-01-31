# Tests

Comprehensive test suite for webgrab using pytest.

## Setup

1. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Unix/macOS
# or
venv\Scripts\activate  # On Windows
```

2. Install the package with dev dependencies:
```bash
pip install -e ".[dev]"
```

3. Install Playwright browser:
```bash
playwright install chromium
```

## Running Tests

Run all tests:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=webgrab --cov-report=html
```

Run specific test file:
```bash
pytest tests/test_models.py
```

Run specific test:
```bash
pytest tests/test_models.py::TestResource::test_resource_creation
```

Run tests matching a pattern:
```bash
pytest -k "test_url"
```

## Test Structure

- `conftest.py` - Shared fixtures and pytest configuration
- `test_models.py` - Tests for domain models
- `test_url_parser.py` - Tests for URL parsing utilities
- `test_filesystem_sanitizer.py` - Tests for filesystem path sanitization
- `test_mime_detector.py` - Tests for MIME type detection
- `test_storage.py` - Tests for storage modules (path resolution, deduplication, file I/O, resource saving)
- `test_capture_filters.py` - Tests for resource filtering logic

## Test Coverage

Current test coverage: 80 tests covering:
- ✅ Domain models (Resource, CaptureConfig, SaveConfig, CaptureStats, SaveResult)
- ✅ URL parsing and validation
- ✅ Same-origin checking
- ✅ URL filtering (data:, blob:, javascript:, etc.)
- ✅ Filesystem path sanitization (cross-platform, Windows reserved names)
- ✅ MIME type detection and extension inference
- ✅ Path resolution (URL to filesystem)
- ✅ Path deduplication
- ✅ File I/O operations
- ✅ Resource saving with filtering
- ✅ Capture filters (default and composite)

## Writing Tests

When adding new features, ensure you add corresponding tests:

1. Place tests in the appropriate test file based on the module
2. Use descriptive test names: `test_<functionality>_<scenario>`
3. Use fixtures from `conftest.py` for common test data
4. Add docstrings to test functions explaining what they test
5. Group related tests in classes for better organization

Example:
```python
def test_my_feature_with_valid_input(temp_dir):
    \"\"\"Test that my_feature works with valid input.\"\"\"
    # Arrange
    config = MyConfig(param="value")
    
    # Act
    result = my_feature(config)
    
    # Assert
    assert result.success is True
    assert result.output == "expected"
```
