"""
TOON (Token-Oriented Object Notation) parser and serializer.

TOON is a data format optimized for LLMs with minimal token usage.
Official spec: https://github.com/toon-format/spec

TOON format example:
    employees[2]{id,name,role}:
      1,Alice,admin
      2,Bob,user
"""

import re
from typing import Any, Dict, List, Optional


class ToonParseError(Exception):
    """Exception raised when parsing TOON format fails."""


def parse_toon(content: str) -> Dict[str, Any]:
    """
    Parse TOON format string into a dictionary structure.

    TOON format follows the specification at https://github.com/toon-format/spec

    Format:
        table_name[N]{field1,field2,field3}:
          value1,value2,value3
          value4,value5,value6

    Args:
        content: String content in TOON format

    Returns:
        Dictionary with 'table_name', 'columns', 'data', and 'declared_length' keys
    """
    lines = content.strip().split("\n")

    if not lines or (len(lines) == 1 and not lines[0].strip()):
        raise ToonParseError("Empty TOON content")

    # Parse metadata line: table_name[N]{field1,field2}:
    metadata_line = lines[0].strip()
    if not metadata_line.endswith(":"):
        raise ToonParseError("Metadata line must end with ':'")

    metadata_line = metadata_line[:-1]  # Remove trailing colon

    # Parse table name, length, and fields using regex
    # Format: name[length]{field1,field2,field3}
    pattern = r"^([a-zA-Z_]\w*)\[(\d+)\]\{([^}]+)\}$"
    match = re.match(pattern, metadata_line)

    if not match:
        raise ToonParseError(
            f"Invalid TOON metadata format. Expected: name[N]{{fields}}:\n"
            f"Got: {metadata_line}",
        )

    table_name = match.group(1)
    declared_length = int(match.group(2))
    fields_str = match.group(3)

    # Parse field names
    columns = [field.strip() for field in fields_str.split(",")]

    # Parse data rows (skip first line which is metadata)
    data = []
    for i in range(1, len(lines)):
        line = lines[i].strip()
        if not line:
            continue

        # Remove leading whitespace (indentation)
        # Split by comma, but handle quoted strings
        values = _split_csv_line(line)

        if len(values) != len(columns):
            raise ToonParseError(
                f"Row {i} has {len(values)} values but {len(columns)} fields declared. "
                f"Expected {len(columns)} values.",
            )

        # Handle different value types
        parsed_values = []
        for val in values:
            parsed_values.append(_parse_value(val))

        data.append(parsed_values)

    # Validate row count
    if len(data) != declared_length:
        raise ToonParseError(
            f"Data has {len(data)} rows but declared length is {declared_length}",
        )

    return {
        "table_name": table_name,
        "columns": columns,
        "data": data,
        "declared_length": declared_length,
    }


def _split_csv_line(line: str) -> List[str]:
    """
    Split a CSV line by commas, respecting quoted strings.
    Handles double-quote escaping (e.g., "value with ""quotes"" inside")
    """
    values = []
    current = []
    in_quotes = False
    i = 0

    while i < len(line):
        char = line[i]

        if char == '"':
            if in_quotes and i + 1 < len(line) and line[i + 1] == '"':
                # Double quote escape
                current.append('"')
                i += 2
                continue
            # Toggle quote mode
            in_quotes = not in_quotes
            i += 1
            continue

        if char == "," and not in_quotes:
            # Field separator
            values.append("".join(current).strip())
            current = []
            i += 1
            continue

        current.append(char)
        i += 1

    # Add last field
    values.append("".join(current).strip())

    return values



def _parse_value(val: str) -> Any:
    """
    Parse a single value from TOON format.

    Handles:
    - null/None values
    - Numbers (int, float)
    - Booleans
    - Strings
    """
    val = val.strip()

    # Handle null/empty
    if val == "" or val.lower() in ("null", "none", "na", "nan"):
        return None

    # Handle booleans
    if val.lower() == "true":
        return True
    if val.lower() == "false":
        return False

    # Try parsing as number
    try:
        # Try int first
        if "." not in val and "e" not in val.lower():
            return int(val)
        # Try float
        return float(val)
    except ValueError:
        pass

    # Return as string
    return val


def serialize_toon(columns: List[str], data: List[List[Any]],
                  table_name: Optional[str] = None) -> str:
    """
    Serialize data to TOON format according to the official specification.

    Format: table_name[N]{field1,field2,field3}:
              value1,value2,value3
              value4,value5,value6

    Args:
        columns: List of column names
        data: List of rows (each row is a list of values)
        table_name: Optional table name (defaults to "data" if not provided)

    Returns:
        String in TOON format
    """
    if not table_name:
        table_name = "data"

    lines = []

    # Create metadata line: name[N]{fields}:
    num_rows = len(data)
    fields_str = ",".join(columns)
    metadata = f"{table_name}[{num_rows}]{{{fields_str}}}:"
    lines.append(metadata)

    # Add data rows with 2-space indentation
    for row in data:
        serialized_row = []
        for val in row:
            serialized_row.append(_serialize_value(val))
        lines.append("  " + ",".join(serialized_row))

    return "\n".join(lines)


def _serialize_value(val: Any) -> str:
    """
    Serialize a single value to TOON format.

    Handles:
    - None/null values
    - Numbers
    - Booleans
    - Strings (with comma escaping if needed)
    """
    if val is None:
        return ""

    if isinstance(val, bool):
        return "true" if val else "false"

    if isinstance(val, (int, float)):
        return str(val)

    # Convert to string
    val_str = str(val)

    # Escape commas in strings by wrapping in quotes if needed
    if "," in val_str or "\n" in val_str:
        # Escape quotes and wrap in quotes
        val_str = val_str.replace('"', '""')
        return f'"{val_str}"'

    return val_str
