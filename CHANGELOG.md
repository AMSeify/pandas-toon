# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-11-15

### Added
- Initial release of pandas-toon library
- `pd.read_toon()` function to read TOON format files into pandas DataFrames
- `DataFrame.to_toon()` method to export DataFrames to TOON format
- Support for common data types: strings, integers, floats, booleans, and null values
- Optional table name support in TOON format
- Comprehensive test suite with 97% code coverage
- Example usage scripts and sample data files
- Full documentation in README
- Type hints support with py.typed marker

### Features
- File and StringIO input support for reading TOON files
- File path and in-memory string output for writing TOON
- Automatic type inference for TOON data
- Round-trip conversion support (DataFrame → TOON → DataFrame)
- Compatible with pandas 1.3.0 and later
- Python 3.8+ support

[0.1.0]: https://github.com/AMSeify/pandas-toon/releases/tag/v0.1.0
