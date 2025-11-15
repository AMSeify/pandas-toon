# GitHub Workflows Documentation

This document describes the GitHub Actions workflows configured for the pandas-toon project.

## Workflows Overview

### 1. Test Workflow (`.github/workflows/test.yml`)

**Trigger**: Runs on push to `main` or `develop` branches, pull requests, and manual triggers

**Purpose**: Ensures code quality and compatibility across multiple Python versions and operating systems

**Jobs**:

#### Test Job
- **Matrix Strategy**: Tests across:
  - Operating Systems: Ubuntu, macOS, Windows
  - Python Versions: 3.8, 3.9, 3.10, 3.11, 3.12
- **Steps**:
  1. Checks out code
  2. Sets up Python
  3. Installs package with dev dependencies
  4. Runs pytest with coverage
  5. Uploads coverage to Codecov (Ubuntu + Python 3.11 only)

#### Lint Job
- **Purpose**: Code quality checks
- **Steps**:
  1. Checks out code
  2. Sets up Python 3.11
  3. Installs dependencies including ruff and mypy
  4. Runs ruff linter
  5. Runs mypy type checker (non-blocking)

### 2. Publish Workflow (`.github/workflows/publish.yml`)

**Trigger**: 
- Automatically on GitHub releases
- Manually via workflow dispatch (for TestPyPI testing)

**Purpose**: Builds and publishes the package to PyPI or TestPyPI

**Jobs**:

#### Build Job
- Builds the distribution packages (wheel and sdist)
- Validates the build with twine
- Uploads artifacts for publishing jobs

#### Publish to PyPI Job
- **Trigger**: Only on release events
- **Security**: Uses OIDC trusted publishing (no API tokens needed)
- **Environment**: `pypi`
- **Steps**:
  1. Downloads built artifacts
  2. Publishes to PyPI using trusted publishing

#### Publish to TestPyPI Job
- **Trigger**: Only on manual workflow dispatch with test_pypi=true
- **Security**: Uses OIDC trusted publishing
- **Environment**: `testpypi`
- **Steps**:
  1. Downloads built artifacts
  2. Publishes to TestPyPI

## Security: Trusted Publishing

Both publishing jobs use **OIDC Trusted Publishing**, which is more secure than API tokens:

**Benefits**:
- No long-lived secrets to manage
- Automatic token rotation
- Scoped to specific workflows and environments
- Cannot be leaked or stolen

**Requirements**:
1. Configure pending publishers on PyPI/TestPyPI
2. Create GitHub environments (`pypi`, `testpypi`)
3. Grant `id-token: write` permission to workflows

See [PUBLISHING.md](PUBLISHING.md) for detailed setup instructions.

## Branch Strategy

### Main Branches

- **`main`**: Production-ready code
  - All code must pass tests
  - Direct pushes should be restricted
  - Should always be in a releasable state

- **`develop`**: Integration branch for features
  - Features are merged here first
  - Must pass all tests before merging to main
  - Can contain unreleased features

### Feature Branches

Format: `feature/<description>` or `<username>/<description>`

Example workflow:
```bash
# Create feature branch
git checkout -b feature/new-parser-feature develop

# Make changes and commit
git add .
git commit -m "Add new parser feature"

# Push to GitHub
git push origin feature/new-parser-feature

# Create pull request to develop branch
```

### Release Workflow

1. **Feature Development**
   ```bash
   feature/* → develop (via PR)
   ```

2. **Release Preparation**
   ```bash
   develop → main (via PR)
   ```

3. **Version Tagging**
   ```bash
   git checkout main
   git pull
   git tag -a v0.2.0 -m "Release v0.2.0"
   git push origin v0.2.0
   ```

4. **GitHub Release**
   - Create release from tag
   - Triggers automatic PyPI publishing

## Testing Strategy

### Unit Tests
- Located in `tests/` directory
- Run on every push and PR
- Must pass on all supported Python versions and OSes

### Integration Tests
- Verify pandas integration
- Test file I/O operations
- Validate parser correctness

### Coverage Requirements
- Aim for >80% code coverage
- Coverage reports uploaded to Codecov
- Visible in PR checks

## Manual Workflow Triggers

### Running Tests Manually
1. Go to "Actions" tab in GitHub
2. Select "Tests" workflow
3. Click "Run workflow"
4. Select branch and run

### Publishing to TestPyPI
1. Go to "Actions" tab
2. Select "Publish to PyPI" workflow
3. Click "Run workflow"
4. Check "Publish to Test PyPI instead of PyPI"
5. Run workflow

## Monitoring Workflows

### Viewing Workflow Runs
- Navigate to the "Actions" tab in GitHub
- Click on a workflow name to see all runs
- Click on a specific run to see details and logs

### Debugging Failed Workflows
1. Click on the failed workflow run
2. Expand the failed job
3. Review the step that failed
4. Check the logs for error messages
5. Fix the issue locally and push again

## Environment Variables and Secrets

### Required Secrets
None! Trusted publishing eliminates the need for API tokens.

### Optional Secrets
- `CODECOV_TOKEN`: For uploading coverage reports (optional, works without it)

### Environment Configuration

**PyPI Environment**:
- Name: `pypi`
- URL: `https://pypi.org/p/pandas-toon`
- Protection rules: (Optional) Require manual approval

**TestPyPI Environment**:
- Name: `testpypi`
- URL: `https://test.pypi.org/p/pandas-toon`
- Protection rules: None needed for testing

## Adding New Workflows

To add a new workflow:

1. Create a new file in `.github/workflows/`
2. Define the workflow in YAML format
3. Test it on a feature branch
4. Document it in this file
5. Merge via pull request

Example workflow structure:
```yaml
name: My Workflow
on: [push]
jobs:
  my-job:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Do something
        run: echo "Hello World"
```

## Best Practices

1. **Always test on feature branches** before merging
2. **Keep workflows fast** - use caching where possible
3. **Fail fast** - set `fail-fast: false` only when needed
4. **Use latest actions** - regularly update action versions
5. **Document changes** - update this file when modifying workflows
6. **Test locally first** - use `act` or similar tools to test workflows locally
7. **Monitor costs** - GitHub Actions has usage limits

## Troubleshooting Common Issues

### Workflow Won't Trigger
- Check branch names in workflow triggers
- Verify push events are reaching GitHub
- Check workflow file syntax

### Tests Fail on Specific OS
- Check OS-specific path separators
- Verify dependencies are available on all platforms
- Review OS-specific environment differences

### Publishing Fails
- Verify trusted publishing is configured
- Check environment names match exactly
- Ensure version number is incremented
- Review PyPI logs for specific errors

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [PyPI Trusted Publishing Guide](https://docs.pypi.org/trusted-publishers/)
- [Semantic Versioning](https://semver.org/)
- [pytest Documentation](https://docs.pytest.org/)
