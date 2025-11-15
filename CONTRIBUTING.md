# Contributing to pandas-toon

Thank you for your interest in contributing to pandas-toon! This document provides guidelines and instructions for contributing.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/pandas-toon.git
   cd pandas-toon
   ```

3. Install the package in development mode:
   ```bash
   pip install -e ".[dev]"
   ```

## Development Workflow

### Making Changes

1. Create a new branch for your feature or bugfix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes to the code

3. Add or update tests as necessary in the `tests/` directory

4. Run the test suite to ensure all tests pass:
   ```bash
   pytest tests/
   ```

5. Run tests with coverage to ensure adequate coverage:
   ```bash
   pytest --cov=pandas_toon tests/
   ```

### Code Style

- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings to all public functions and classes
- Keep functions focused and concise

### Testing

- Write tests for all new features
- Ensure existing tests pass
- Aim for high test coverage (>90%)
- Test edge cases and error conditions

### Documentation

- Update the README if you add new features
- Add docstrings following NumPy/pandas style
- Update CHANGELOG.md with your changes
- Add examples if introducing new functionality

## Submitting Changes

1. Commit your changes with clear, descriptive commit messages:
   ```bash
   git commit -m "Add feature: description of what you added"
   ```

2. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

3. Create a Pull Request on GitHub

4. In your PR description:
   - Describe what changes you made and why
   - Reference any related issues
   - Include examples of the new functionality if applicable

## Reporting Issues

When reporting issues, please include:

- A clear description of the problem
- Steps to reproduce the issue
- Expected behavior
- Actual behavior
- Your environment (Python version, pandas version, OS)
- Minimal code example that demonstrates the issue

## Questions?

If you have questions about contributing, feel free to open an issue with the "question" label.

## Code of Conduct

Please be respectful and constructive in all interactions. We aim to maintain a welcoming and inclusive community.

Thank you for contributing to pandas-toon!
