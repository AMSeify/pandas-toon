"""
TOON (Token-Oriented Object Notation) parser and serializer.

TOON is a data format optimized for LLMs with minimal token usage.
It uses a structured but compact syntax for representing tabular data.
"""

import re
from typing import Any, Dict, List, Union
import io


class ToonParseError(Exception):
    """Exception raised when parsing TOON format fails."""
    pass


def parse_toon(content: str) -> Dict[str, Any]:
    """
    Parse TOON format string into a dictionary structure.
    
    TOON format example:
    @table_name
    col1|col2|col3
    ---
    val1|val2|val3
    val4|val5|val6
    
    Args:
        content: String content in TOON format
        
    Returns:
        Dictionary with 'columns' and 'data' keys
    """
    lines = content.strip().split('\n')
    
    if not lines or (len(lines) == 1 and not lines[0].strip()):
        raise ToonParseError("Empty TOON content")
    
    # Parse table name (optional)
    table_name = None
    start_idx = 0
    if lines[0].startswith('@'):
        table_name = lines[0][1:].strip()
        start_idx = 1
    
    if len(lines) <= start_idx:
        raise ToonParseError("Missing column headers")
    
    # Parse column headers
    header_line = lines[start_idx]
    columns = [col.strip() for col in header_line.split('|')]
    
    # Find data separator (---)
    sep_idx = start_idx + 1
    if sep_idx >= len(lines) or not lines[sep_idx].strip().startswith('---'):
        # No separator, assume data starts immediately
        sep_idx = start_idx
    
    # Parse data rows
    data = []
    for i in range(sep_idx + 1, len(lines)):
        line = lines[i].strip()
        if not line:
            continue
        
        values = [val.strip() for val in line.split('|')]
        
        # Handle different value types
        parsed_values = []
        for val in values:
            parsed_values.append(_parse_value(val))
        
        data.append(parsed_values)
    
    return {
        'table_name': table_name,
        'columns': columns,
        'data': data
    }


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
    if val == '' or val.lower() in ('null', 'none', 'na', 'nan'):
        return None
    
    # Handle booleans
    if val.lower() == 'true':
        return True
    if val.lower() == 'false':
        return False
    
    # Try parsing as number
    try:
        # Try int first
        if '.' not in val and 'e' not in val.lower():
            return int(val)
        # Try float
        return float(val)
    except ValueError:
        pass
    
    # Return as string
    return val


def serialize_toon(columns: List[str], data: List[List[Any]], 
                  table_name: str = None) -> str:
    """
    Serialize data to TOON format.
    
    Args:
        columns: List of column names
        data: List of rows (each row is a list of values)
        table_name: Optional table name
        
    Returns:
        String in TOON format
    """
    lines = []
    
    # Add table name if provided
    if table_name:
        lines.append(f"@{table_name}")
    
    # Add column headers
    lines.append('|'.join(columns))
    
    # Add separator
    lines.append('---')
    
    # Add data rows
    for row in data:
        serialized_row = []
        for val in row:
            serialized_row.append(_serialize_value(val))
        lines.append('|'.join(serialized_row))
    
    return '\n'.join(lines)


def _serialize_value(val: Any) -> str:
    """
    Serialize a single value to TOON format string.
    """
    if val is None or (isinstance(val, float) and str(val) == 'nan'):
        return ''
    
    if isinstance(val, bool):
        return 'true' if val else 'false'
    
    if isinstance(val, (int, float)):
        return str(val)
    
    # Convert to string and handle special characters
    s = str(val)
    # For now, keep it simple - just convert to string
    return s
