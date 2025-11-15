# Publishing to PyPI

This document describes the process for publishing `pandas-toon` to PyPI.

## Prerequisites

1. **GitHub Repository Access**: Ensure you have maintainer access to the repository
2. **PyPI Trusted Publishing**: Configure trusted publishing on PyPI (recommended)
   - Or have PyPI API token (alternative method)

## Setting Up PyPI Trusted Publishing (Recommended)

Trusted publishing uses OIDC tokens and is more secure than API tokens.

### Step 1: Configure PyPI

1. Go to [PyPI](https://pypi.org/) and log in
2. If publishing for the first time, you need to create a "pending publisher":
   - Go to your PyPI account settings
   - Navigate to "Publishing" section
   - Add a new pending publisher with these details:
     - **PyPI Project Name**: `pandas-toon`
     - **Owner**: `AMSeify`
     - **Repository name**: `pandas-toon`
     - **Workflow name**: `publish.yml`
     - **Environment name**: `pypi`

### Step 2: Configure Test PyPI (Optional but Recommended)

For testing releases before publishing to the real PyPI:

1. Go to [Test PyPI](https://test.pypi.org/) and log in (separate account from PyPI)
2. Add a pending publisher with the same details:
   - **PyPI Project Name**: `pandas-toon`
   - **Owner**: `AMSeify`
   - **Repository name**: `pandas-toon`
   - **Workflow name**: `publish.yml`
   - **Environment name**: `testpypi`

### Step 3: Create GitHub Environments

1. Go to your GitHub repository settings
2. Navigate to "Environments"
3. Create two environments:
   - **pypi**: For production releases
   - **testpypi**: For test releases
4. (Optional) Add protection rules to require approval before deployment

## Release Process

### Testing on Test PyPI

Before making a real release, test your package on Test PyPI:

1. Go to the "Actions" tab in GitHub
2. Select "Publish to PyPI" workflow
3. Click "Run workflow"
4. Check "Publish to Test PyPI instead of PyPI"
5. Run the workflow

The package will be published to Test PyPI. You can then test installation:

```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple pandas-toon
```

### Publishing to PyPI

When you're ready to publish a new version:

1. **Update Version Number**
   - Edit `pyproject.toml` and update the version number
   - Follow [Semantic Versioning](https://semver.org/): MAJOR.MINOR.PATCH

2. **Update CHANGELOG.md**
   - Document all changes in the new version
   - Include breaking changes, new features, bug fixes, etc.

3. **Commit Changes**
   ```bash
   git add pyproject.toml CHANGELOG.md
   git commit -m "Bump version to X.Y.Z"
   git push
   ```

4. **Create a Git Tag**
   ```bash
   git tag -a vX.Y.Z -m "Release version X.Y.Z"
   git push origin vX.Y.Z
   ```

5. **Create a GitHub Release**
   - Go to the "Releases" page in GitHub
   - Click "Draft a new release"
   - Select the tag you just created
   - Set the release title (e.g., "v0.1.0")
   - Add release notes (can copy from CHANGELOG.md)
   - Click "Publish release"

6. **Automatic Publishing**
   - The GitHub Actions workflow will automatically trigger
   - It will build the package and publish to PyPI
   - Monitor the workflow in the "Actions" tab

## Verifying the Release

After publishing:

1. Check [PyPI](https://pypi.org/project/pandas-toon/) to see your package
2. Test installation:
   ```bash
   pip install pandas-toon
   ```
3. Verify the package works as expected

## Troubleshooting

### Workflow Fails with Permission Error

- Ensure trusted publishing is correctly configured on PyPI
- Verify the environment names match exactly
- Check that the repository and owner names are correct

### Package Already Exists Error

- You cannot re-upload the same version to PyPI
- Increment the version number in `pyproject.toml`
- Delete the tag and release, then recreate with the new version

### Tests Fail

- Fix the failing tests before publishing
- The test workflow should pass on the main branch
- You can run tests locally: `pytest tests/`

## Alternative: Using API Token

If you prefer to use an API token instead of trusted publishing:

1. Generate an API token on PyPI
2. Add it as a GitHub secret named `PYPI_API_TOKEN`
3. Modify the publish workflow to use:
   ```yaml
   - name: Publish distribution to PyPI
     uses: pypa/gh-action-pypi-publish@release/v1
     with:
       password: ${{ secrets.PYPI_API_TOKEN }}
   ```

## Future: pandas[toon] Extra

To enable installation via `pip install pandas[toon]`, you need to:

1. Contact the pandas maintainers
2. Propose adding `pandas-toon` as an optional dependency
3. Submit a pull request to the pandas repository
4. This requires community discussion and approval

Until then, users should install with:
```bash
pip install pandas-toon
```
