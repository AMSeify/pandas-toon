# pandas-toon

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-Apache%202.0-green.svg)](LICENSE)

TOON (Token-Oriented Object Notation) format support for pandas DataFrames.

## Overview

**pandas-toon** is a pandas plugin that brings native support for the TOON data serialization format. TOON is a compact, LLM-optimized alternative to JSON or CSV, specifically designed for scenarios such as LLM prompts, data validation, and token-efficient storage or exchange.

With pandas-toon, you can seamlessly integrate TOON into your pandas-based data workflows using familiar pandas syntax.

## Features

- **Native TOON support in pandas**: Read and write TOON just like built-in formats
- **LLM optimization**: Designed for minimal token usage and high reliability in AI/LLM pipelines
- **Easy installation**: Simple pip installation with pandas integration
- **Clean API**: Follows pandas conventions with `pd.read_toon()` and `df.to_toon()`
- **Type inference**: Automatically handles strings, numbers, booleans, and null values

## Installation

Install via pip:

```bash
pip install pandas-toon
```

Or install pandas with the toon extra (future support):

```bash
pip install pandas[toon]
```

## Quick Start

### Reading TOON files

```python
import pandas as pd
import pandas_toon

# Read a TOON file
df = pd.read_toon("data.toon")
```

### Writing TOON files

```python
import pandas as pd
import pandas_toon

# Create a DataFrame
df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [30, 25, 35],
    'city': ['New York', 'London', 'Paris']
})

# Save as TOON
df.to_toon("output.toon")

# Or get TOON string
toon_str = df.to_toon()
print(toon_str)
```

Output:
```
name|age|city
---
Alice|30|New York
Bob|25|London
Charlie|35|Paris
```

### Using table names

```python
# Write with table name
df.to_toon("data.toon", table_name="users")

# The output will include the table name:
# @users
# name|age|city
# ---
# ...
```

## TOON Format

TOON uses a simple, readable syntax optimized for token efficiency:

```
@table_name          # Optional table identifier
column1|column2|column3
---                  # Separator line
value1|value2|value3
value4|value5|value6
```

### Data Types

TOON automatically handles common data types:

- **Strings**: Plain text values
- **Numbers**: Integers and floating-point numbers (e.g., `42`, `3.14`)
- **Booleans**: `true` or `false`
- **Null values**: Empty values or `null`

Example:
```
name|age|score|active|notes
---
Alice|30|95.5|true|Great performance
Bob|25||false|
```

## Examples

### Working with different data types

```python
import pandas as pd
from io import StringIO

# Read TOON data from string
toon_data = """@employee_data
name|age|salary|active
---
Alice|30|75000.0|true
Bob|25|65000.0|true
Charlie|35||false
"""

df = pd.read_toon(StringIO(toon_data))
print(df)
#       name  age   salary  active
# 0    Alice   30  75000.0    True
# 1      Bob   25  65000.0    True
# 2  Charlie   35      NaN   False
```

### Round-trip conversion

```python
# Create DataFrame
df = pd.DataFrame({
    'product': ['Laptop', 'Mouse', 'Keyboard'],
    'price': [999.99, 29.99, 79.99],
    'in_stock': [True, True, False]
})

# Convert to TOON and back
toon_str = df.to_toon()
df_restored = pd.read_toon(StringIO(toon_str))

# Verify data integrity
assert df.equals(df_restored)
```

## Use Cases

### LLM Prompts

TOON's compact format is ideal for including data in LLM prompts while minimizing token usage:

```python
df = pd.DataFrame({
    'question': ['What is Python?', 'What is pandas?'],
    'answer': ['A programming language', 'A data analysis library']
})

# Include in prompt
prompt = f"""Here is the Q&A data:

{df.to_toon()}

Please analyze this data..."""
```

### Data Exchange

Use TOON for lightweight data exchange between systems:

```python
# Export data
df.to_toon("export.toon")

# Share file or content
# Other system reads it back
df_received = pd.read_toon("export.toon")
```

## API Reference

### `pd.read_toon(filepath_or_buffer, **kwargs)`

Read a TOON format file into a DataFrame.

**Parameters:**
- `filepath_or_buffer`: str, Path, or file-like object
  - Path to the TOON file or a file-like object containing TOON data

**Returns:**
- `DataFrame`: A pandas DataFrame containing the parsed TOON data

### `DataFrame.to_toon(path_or_buf=None, table_name=None, **kwargs)`

Write a DataFrame to TOON format.

**Parameters:**
- `path_or_buf`: str, Path, or None (optional)
  - File path to write to. If None, returns the TOON string
- `table_name`: str (optional)
  - Optional table name to include in the TOON output

**Returns:**
- `str` or `None`: If path_or_buf is None, returns the TOON-formatted string. Otherwise, writes to the file and returns None

## Development

### Setup

Clone the repository and install in development mode:

```bash
git clone https://github.com/AMSeify/pandas-toon.git
cd pandas-toon
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest tests/
```

With coverage:

```bash
pytest --cov=pandas_toon tests/
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Links

- **GitHub Repository**: https://github.com/AMSeify/pandas-toon
- **TOON Format Specification**: https://github.com/toon-format/toon
- **PyPI Package**: Coming soon

## Credits

This library builds upon:
- [pandas](https://pandas.pydata.org/) - The powerful Python data analysis library
- [TOON format](https://github.com/toon-format/toon) - Token-Oriented Object Notation specification

## About TOON

TOON (Token-Oriented Object Notation) is a data format specifically designed for Large Language Models. It aims to:

- Minimize token usage compared to JSON or CSV
- Provide clear, unambiguous structure
- Maintain human readability
- Support common data types efficiently

Learn more about TOON at the [official TOON repository](https://github.com/toon-format/toon).
