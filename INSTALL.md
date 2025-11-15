# Installation Guide

## Installing from PyPI (when published)

Once published to PyPI, you can install pandas-toon with:

```bash
pip install pandas-toon
```

## Installing from source

To install from source:

```bash
git clone https://github.com/AMSeify/pandas-toon.git
cd pandas-toon
pip install -e .
```

## Development Installation

For development work, install with development dependencies:

```bash
git clone https://github.com/AMSeify/pandas-toon.git
cd pandas-toon
pip install -e ".[dev]"
```

This will install:
- pandas-toon in editable mode
- pytest for running tests
- pytest-cov for coverage reports

## Verifying Installation

After installation, verify it works:

```python
import pandas as pd
import pandas_toon

# Check version
print(pandas_toon.__version__)

# Test basic functionality
df = pd.DataFrame({'a': [1, 2], 'b': [3, 4]})
print(df.to_toon())
```

## Requirements

- Python 3.8 or later
- pandas 1.3.0 or later

## Troubleshooting

### Import Error

If you get an import error, make sure pandas is installed:

```bash
pip install pandas>=1.3.0
```

### Permission Errors

If you get permission errors during installation, try:

```bash
pip install --user pandas-toon
```

Or use a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install pandas-toon
```
