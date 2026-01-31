# Publishing Guide

This guide covers how to publish webgrab to PyPI.

## Prerequisites

1. **PyPI Account**
   - Create an account at https://pypi.org
   - Create an account at https://test.pypi.org (for testing)

2. **API Tokens**
   - Generate an API token on PyPI (Account Settings → API tokens)
   - Generate an API token on Test PyPI
   - Store tokens in GitHub Secrets:
     - `PYPI_API_TOKEN` - Production PyPI token
     - `TEST_PYPI_API_TOKEN` - Test PyPI token

3. **GitHub Permissions**
   - Ensure you have permission to create releases in the repository

## Manual Publishing

### 1. Prepare for Release

Update the version in `pyproject.toml`:

```toml
[project]
name = "py-webgrab"
version = "0.1.1"  # Increment this
```

### 2. Build the Package

```bash
# Install build tools
pip install build twine

# Build the package
python -m build

# Check the build
twine check dist/*
```

### 3. Test on Test PyPI (Recommended)

```bash
# Upload to Test PyPI
twine upload --repository testpypi dist/*

# Test installation
pip install --index-url https://test.pypi.org/simple/ py-webgrab
```

### 4. Publish to PyPI

```bash
# Upload to PyPI
twine upload dist/*
```

## Automated Publishing via GitHub Actions

The recommended approach is to use GitHub Actions for automated publishing.

### Publishing to Test PyPI

Use the manual workflow dispatch:

1. Go to **Actions** → **Publish to PyPI**
2. Click **Run workflow**
3. Check **Publish to Test PyPI instead of PyPI**
4. Click **Run workflow**

### Publishing to Production PyPI

Create a GitHub Release:

1. **Update Version**
   ```bash
   # Update version in pyproject.toml
   git add pyproject.toml
   git commit -m "Bump version to 0.1.1"
   git push
   ```

2. **Create and Push Tag**
   ```bash
   git tag v0.1.1
   git push origin v0.1.1
   ```

3. **Create GitHub Release**
   - Go to **Releases** → **Draft a new release**
   - Select the tag you just created (`v0.1.1`)
   - Set the release title (e.g., `v0.1.1`)
   - Add release notes describing changes
   - Click **Publish release**

4. **Automatic Publishing**
   - GitHub Actions will automatically:
     - Build the package
     - Run quality checks
     - Publish to PyPI
     - Available at: https://pypi.org/project/py-webgrab/

## Release Checklist

Before creating a release:

- [ ] All tests pass locally (`pytest`)
- [ ] Lint checks pass (`ruff check src/webgrab tests`)
- [ ] GitHub Actions workflows are green
- [ ] Version number updated in `pyproject.toml`
- [ ] CHANGELOG.md updated (if exists)
- [ ] README.md updated if needed
- [ ] All changes committed and pushed

## Versioning

We follow [Semantic Versioning](https://semver.org/):

- **MAJOR** version (1.0.0): Incompatible API changes
- **MINOR** version (0.1.0): Add functionality (backwards compatible)
- **PATCH** version (0.0.1): Bug fixes (backwards compatible)

Examples:
- `0.1.0` → `0.1.1`: Bug fix
- `0.1.0` → `0.2.0`: New feature
- `0.9.0` → `1.0.0`: First stable release

## Troubleshooting

### "File already exists" error

PyPI doesn't allow re-uploading the same version. You must:
1. Increment the version number
2. Rebuild: `python -m build`
3. Upload again

### GitHub Actions fails to publish

Check that:
1. GitHub Secrets are set correctly (`PYPI_API_TOKEN`)
2. The API token has upload permissions
3. The version number doesn't already exist on PyPI

### Package doesn't install correctly

Verify `pyproject.toml` includes:
- Correct package name
- All dependencies
- Correct package paths in `[tool.hatch.build.targets.wheel]`

## Post-Release

After publishing:

1. **Verify Installation**
   ```bash
   pip install py-webgrab
   webgrab --version
   ```

2. **Update Documentation**
   - Update README.md badges if needed
   - Update installation instructions
   - Announce the release (Twitter, Discord, etc.)

3. **Monitor Issues**
   - Watch for issues on GitHub
   - Check PyPI download stats
   - Respond to user feedback

## Resources

- [PyPI Help](https://pypi.org/help/)
- [Python Packaging Guide](https://packaging.python.org/)
- [Semantic Versioning](https://semver.org/)
- [GitHub Releases](https://docs.github.com/en/repositories/releasing-projects-on-github)
