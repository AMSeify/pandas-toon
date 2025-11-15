# Quick Reference Guide

Quick commands and workflows for common tasks.

## Development

### Setup Development Environment
```bash
# Clone repository
git clone https://github.com/AMSeify/pandas-toon.git
cd pandas-toon

# Install in development mode
pip install -e ".[dev]"
```

### Running Tests
```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=pandas_toon tests/

# Run specific test file
pytest tests/test_pandas_toon.py

# Run specific test
pytest tests/test_pandas_toon.py::TestToonParser::test_parse_simple_toon
```

### Code Quality
```bash
# Lint code
ruff check src/

# Auto-fix linting issues
ruff check --fix src/

# Format code
ruff format src/

# Type check
mypy src/pandas_toon
```

### Building the Package
```bash
# Install build tool
pip install build

# Build distributions
python -m build

# Check built distributions
pip install twine
twine check dist/*
```

### Testing Installation Locally
```bash
# Create test environment
python -m venv test_env
source test_env/bin/activate  # Windows: test_env\Scripts\activate

# Install from local build
pip install dist/pandas_toon-0.1.0-py3-none-any.whl

# Test it works
python -c "import pandas as pd; import pandas_toon; print('Success!')"

# Clean up
deactivate
rm -rf test_env
```

## Git Workflows

### Create Feature Branch
```bash
git checkout develop
git pull
git checkout -b feature/my-new-feature
# Make changes...
git add .
git commit -m "Add new feature"
git push origin feature/my-new-feature
# Create pull request to develop
```

### Prepare Release
```bash
# Switch to develop and ensure it's up to date
git checkout develop
git pull

# Update version in pyproject.toml (e.g., 0.1.0 -> 0.2.0)
# Update CHANGELOG.md

# Commit changes
git add pyproject.toml CHANGELOG.md
git commit -m "Bump version to 0.2.0"
git push

# Merge to main (via PR)
# Then tag the release
git checkout main
git pull
git tag -a v0.2.0 -m "Release version 0.2.0"
git push origin v0.2.0
```

## GitHub Actions

### Trigger Test Workflow Manually
1. Go to: https://github.com/AMSeify/pandas-toon/actions
2. Select "Tests" workflow
3. Click "Run workflow"
4. Select branch and run

### Publish to Test PyPI
1. Go to: https://github.com/AMSeify/pandas-toon/actions
2. Select "Publish to PyPI" workflow
3. Click "Run workflow"
4. Check "Publish to Test PyPI instead of PyPI"
5. Run workflow

### Publish to PyPI (Production)
1. Create GitHub Release with tag (e.g., v0.2.0)
2. Workflow runs automatically
3. Package published to PyPI

## PyPI Configuration

### Configure Trusted Publishing on PyPI
1. Go to: https://pypi.org/manage/account/publishing/
2. Add pending publisher:
   - **Project**: pandas-toon
   - **Owner**: AMSeify
   - **Repository**: pandas-toon
   - **Workflow**: publish.yml
   - **Environment**: pypi

### Configure Test PyPI (Optional)
1. Go to: https://test.pypi.org/manage/account/publishing/
2. Add same configuration with environment: testpypi

## Installation Testing

### Install from PyPI
```bash
pip install pandas-toon
```

### Install from Test PyPI
```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple pandas-toon
```

### Install from Source
```bash
git clone https://github.com/AMSeify/pandas-toon.git
cd pandas-toon
pip install -e .
```

### Install with Development Dependencies
```bash
pip install pandas-toon[dev]
```

## Quick Tests

### Test Basic Functionality
```python
import pandas as pd
import pandas_toon

# Create DataFrame
df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [30, 25, 35],
    'city': ['New York', 'London', 'Paris']
})

# Convert to TOON
toon_str = df.to_toon(table_name='users')
print(toon_str)

# Parse back
from io import StringIO
df2 = pd.read_toon(StringIO(toon_str))
print(df2)
```

### Test File I/O
```python
import pandas as pd
import pandas_toon

# Create sample data
df = pd.DataFrame({'a': [1, 2, 3], 'b': ['x', 'y', 'z']})

# Write to file
df.to_toon('output.toon')

# Read from file
df2 = pd.read_toon('output.toon')
print(df2)
```

## Troubleshooting

### Tests Fail
```bash
# Update dependencies
pip install -e ".[dev]" --upgrade

# Clear cache
pytest --cache-clear tests/

# Run with verbose output
pytest -v tests/
```

### Build Fails
```bash
# Clean previous builds
rm -rf build/ dist/ *.egg-info src/*.egg-info

# Reinstall build tools
pip install --upgrade build setuptools wheel

# Try building again
python -m build
```

### Import Error
```bash
# Check installation
pip list | grep pandas-toon

# Reinstall
pip uninstall pandas-toon
pip install -e .

# Check Python path
python -c "import sys; print('\n'.join(sys.path))"
```

## Useful Links

- **GitHub Repo**: https://github.com/AMSeify/pandas-toon
- **PyPI Package**: https://pypi.org/project/pandas-toon/
- **Test PyPI**: https://test.pypi.org/project/pandas-toon/
- **GitHub Actions**: https://github.com/AMSeify/pandas-toon/actions
- **Issues**: https://github.com/AMSeify/pandas-toon/issues

## Documentation Files

- **PUBLISHING.md**: Complete publishing guide
- **RELEASE_CHECKLIST.md**: First release checklist
- **WORKFLOWS.md**: GitHub Actions documentation
- **SETUP_SUMMARY.md**: Overview of all configurations
- **CONTRIBUTING.md**: Contribution guidelines
- **CHANGELOG.md**: Version history

## Version Information

Current version: **0.1.0**

Supported Python versions: **3.8, 3.9, 3.10, 3.11, 3.12**

Supported platforms: **Linux, macOS, Windows**

## Common Issues

### "Module not found" after installation
```bash
# Ensure you're in the right environment
which python
which pip

# Reinstall
pip install --force-reinstall pandas-toon
```

### GitHub Actions workflow fails
- Check workflow logs in Actions tab
- Verify trusted publishing configuration
- Ensure version number was incremented
- Check that all tests pass

### PyPI upload fails
- Verify you've configured trusted publishing
- Check environment names match exactly
- Ensure version doesn't already exist
- Review PyPI project settings

## Getting Help

- Check existing documentation in the repo
- Search GitHub Issues: https://github.com/AMSeify/pandas-toon/issues
- Create new issue with details about your problem
- Include Python version, OS, and error messages
