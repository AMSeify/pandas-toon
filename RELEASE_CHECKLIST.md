# First Release Checklist

This checklist guides you through publishing pandas-toon to PyPI for the first time.

## Pre-Release Checklist

### Code Quality
- [ ] All tests pass locally: `pytest tests/`
- [ ] Code coverage is adequate: `pytest --cov=pandas_toon tests/`
- [ ] Linting passes: `ruff check src/`
- [ ] Type checking passes: `mypy src/pandas_toon`
- [ ] No debug code or print statements in production code
- [ ] Examples in `examples/` directory work correctly

### Documentation
- [ ] README.md is complete and accurate
- [ ] CHANGELOG.md has entry for version 0.1.0
- [ ] All docstrings are complete and accurate
- [ ] Installation instructions are correct
- [ ] Usage examples are working and clear
- [ ] API documentation is complete

### Package Configuration
- [ ] Version number is set correctly in `pyproject.toml`
- [ ] Package metadata is complete (description, authors, URLs)
- [ ] Dependencies are listed with appropriate version constraints
- [ ] Python version requirement is correct (>=3.8)
- [ ] License is set correctly (Apache-2.0)
- [ ] README.md is set as long_description
- [ ] Entry points are configured correctly

### Repository Setup
- [ ] Repository is public (or organization has appropriate access)
- [ ] LICENSE file is present
- [ ] .gitignore is configured
- [ ] All sensitive data is excluded from version control
- [ ] Branch protection rules are set for `main` branch

## PyPI Configuration

### PyPI Account Setup
- [ ] Create account on https://pypi.org/
- [ ] Verify email address
- [ ] Enable 2FA (Two-Factor Authentication) - highly recommended

### Test PyPI Account Setup (Recommended)
- [ ] Create account on https://test.pypi.org/
- [ ] Verify email address

### Trusted Publishing Setup on PyPI
- [ ] Go to PyPI account settings
- [ ] Navigate to "Publishing" section
- [ ] Click "Add a new pending publisher"
- [ ] Fill in details:
  - **PyPI Project Name**: `pandas-toon`
  - **Owner**: `AMSeify`
  - **Repository name**: `pandas-toon`
  - **Workflow name**: `publish.yml`
  - **Environment name**: `pypi`
- [ ] Save the pending publisher

### Trusted Publishing Setup on Test PyPI (Optional)
- [ ] Go to Test PyPI account settings
- [ ] Navigate to "Publishing" section
- [ ] Click "Add a new pending publisher"
- [ ] Fill in the same details as above but with environment name: `testpypi`
- [ ] Save the pending publisher

### GitHub Environment Setup
- [ ] Go to repository Settings → Environments
- [ ] Create environment named `pypi`
  - [ ] (Optional) Add deployment protection rules
  - [ ] (Optional) Add required reviewers
- [ ] Create environment named `testpypi`
  - [ ] No protection needed for test environment

## Testing the Build Locally

Before publishing, test the build process locally:

```bash
# Install build tools
pip install build twine

# Build the package
python -m build

# Check the built package
twine check dist/*

# Test installation in a clean virtual environment
python -m venv test_env
source test_env/bin/activate  # On Windows: test_env\Scripts\activate
pip install dist/pandas_toon-0.1.0-py3-none-any.whl

# Test that it works
python -c "import pandas as pd; import pandas_toon; print('Success!')"

# Clean up
deactivate
rm -rf test_env dist build src/pandas_toon.egg-info
```

## Test Release to Test PyPI

Test the entire publishing workflow:

- [ ] Go to GitHub Actions tab
- [ ] Select "Publish to PyPI" workflow
- [ ] Click "Run workflow"
- [ ] Check "Publish to Test PyPI instead of PyPI"
- [ ] Click "Run workflow" button
- [ ] Wait for workflow to complete
- [ ] Check Test PyPI: https://test.pypi.org/project/pandas-toon/

### Test Installation from Test PyPI

```bash
# Create a new virtual environment
python -m venv test_pypi_env
source test_pypi_env/bin/activate

# Install from Test PyPI
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple pandas-toon

# Test it works
python -c "import pandas as pd; import pandas_toon; df = pd.DataFrame({'a': [1,2]}); print(df.to_toon())"

# Clean up
deactivate
rm -rf test_pypi_env
```

## First Production Release

### Update Version and Changelog
- [ ] Ensure version in `pyproject.toml` is `0.1.0`
- [ ] Update CHANGELOG.md with all changes
- [ ] Commit changes:
  ```bash
  git add pyproject.toml CHANGELOG.md
  git commit -m "Prepare for v0.1.0 release"
  git push
  ```

### Create Git Tag
```bash
git tag -a v0.1.0 -m "Release version 0.1.0"
git push origin v0.1.0
```

### Create GitHub Release
- [ ] Go to https://github.com/AMSeify/pandas-toon/releases
- [ ] Click "Draft a new release"
- [ ] Click "Choose a tag" and select `v0.1.0`
- [ ] Set release title: `v0.1.0 - Initial Release`
- [ ] Add release notes (copy from CHANGELOG.md):
  ```markdown
  ## pandas-toon v0.1.0 - Initial Release
  
  First official release of pandas-toon!
  
  ### Features
  - Native TOON format support for pandas DataFrames
  - `pd.read_toon()` function for reading TOON files
  - `df.to_toon()` method for writing DataFrames to TOON format
  - Automatic type inference for strings, numbers, booleans, and null values
  - Support for table names in TOON format
  - Comprehensive test suite
  - Full documentation and examples
  
  ### Installation
  ```bash
  pip install pandas-toon
  ```
  
  ### Quick Start
  ```python
  import pandas as pd
  import pandas_toon
  
  # Read TOON file
  df = pd.read_toon("data.toon")
  
  # Write to TOON format
  df.to_toon("output.toon")
  ```
  ```
- [ ] Click "Publish release"

### Monitor the Release
- [ ] Go to Actions tab
- [ ] Watch the "Publish to PyPI" workflow
- [ ] Ensure it completes successfully
- [ ] Check PyPI: https://pypi.org/project/pandas-toon/

### Verify the Release
```bash
# Create fresh virtual environment
python -m venv verify_env
source verify_env/bin/activate

# Install from PyPI
pip install pandas-toon

# Test basic functionality
python -c "import pandas as pd; import pandas_toon; print(pd.read_toon.__doc__)"

# Run a quick test
cat > test_install.py << 'EOF'
import pandas as pd
import pandas_toon

# Create test DataFrame
df = pd.DataFrame({
    'name': ['Alice', 'Bob'],
    'age': [30, 25],
    'city': ['New York', 'London']
})

# Convert to TOON
toon_str = df.to_toon(table_name='users')
print("TOON output:")
print(toon_str)

# Parse back
from io import StringIO
df2 = pd.read_toon(StringIO(toon_str))
print("\nParsed DataFrame:")
print(df2)

print("\nSuccess! pandas-toon is working correctly.")
EOF

python test_install.py

# Clean up
deactivate
rm -rf verify_env test_install.py
```

## Post-Release

### Announce the Release
- [ ] Update README badges (they should now work)
- [ ] Tweet or post on social media (if applicable)
- [ ] Post in relevant communities (r/Python, pandas discussions, etc.)
- [ ] Update any project documentation or websites

### Monitor Issues
- [ ] Watch GitHub issues for bug reports
- [ ] Monitor PyPI download statistics
- [ ] Check for user feedback

### Plan Next Release
- [ ] Create issues for known bugs or improvements
- [ ] Update project roadmap
- [ ] Set up milestones for next version

## Troubleshooting

### Build Fails Locally
- Check that all files are committed
- Ensure `pyproject.toml` is valid
- Try cleaning: `rm -rf dist build *.egg-info`

### GitHub Workflow Fails
- Check workflow logs in Actions tab
- Verify trusted publishing is configured correctly
- Ensure environment names match exactly
- Check PyPI pending publisher configuration

### Package Not Found on PyPI
- Wait a few minutes for PyPI to index
- Check the package name spelling
- Verify the workflow completed successfully
- Check PyPI project page directly

### Installation Fails
- Check Python version compatibility
- Verify dependencies are available
- Try installing in a clean virtual environment
- Check PyPI package files are complete

## Success Criteria

You've successfully published when:
- ✅ Package appears on https://pypi.org/project/pandas-toon/
- ✅ `pip install pandas-toon` works
- ✅ Package can be imported: `import pandas_toon`
- ✅ Basic functionality works as expected
- ✅ Version number matches your release
- ✅ README and documentation display correctly on PyPI

## Next Steps

After successful first release:
1. Monitor for issues and user feedback
2. Plan version 0.2.0 with improvements
3. Consider adding more features
4. Improve documentation based on user questions
5. Build community around the project

Congratulations on your first PyPI release! 🎉
