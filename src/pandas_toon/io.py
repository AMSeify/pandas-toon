"""
I/O operations for TOON format in pandas.
"""

import pandas as pd
from typing import Union, Optional
import io
from pathlib import Path

from pandas_toon.parser import parse_toon


def read_toon(
    filepath_or_buffer: Union[str, Path, io.StringIO],
    **kwargs
) -> pd.DataFrame:
    """
    Read a TOON format file into a DataFrame.
    
    TOON (Token-Oriented Object Notation) is a compact, LLM-optimized
    data format designed for minimal token usage.
    
    Parameters
    ----------
    filepath_or_buffer : str, Path, or file-like object
        Path to the TOON file or a file-like object containing TOON data.
    **kwargs : dict
        Additional keyword arguments (reserved for future use).
        
    Returns
    -------
    DataFrame
        A pandas DataFrame containing the parsed TOON data.
        
    Examples
    --------
    >>> import pandas as pd
    >>> df = pd.read_toon('data.toon')
    
    >>> from io import StringIO
    >>> toon_data = '''@my_table
    ... name|age|city
    ... ---
    ... Alice|30|New York
    ... Bob|25|London'''
    >>> df = pd.read_toon(StringIO(toon_data))
    """
    # Read the content
    if isinstance(filepath_or_buffer, (str, Path)):
        with open(filepath_or_buffer, 'r', encoding='utf-8') as f:
            content = f.read()
    elif hasattr(filepath_or_buffer, 'read'):
        content = filepath_or_buffer.read()
    else:
        raise ValueError(
            f"Invalid input type: {type(filepath_or_buffer)}. "
            "Expected str, Path, or file-like object."
        )
    
    # Parse the TOON content
    parsed = parse_toon(content)
    
    # Create DataFrame
    df = pd.DataFrame(parsed['data'], columns=parsed['columns'])
    
    return df
