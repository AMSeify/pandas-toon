"""
I/O operations for TOON format in pandas.
"""

import io
from pathlib import Path
from typing import Union

import pandas as pd

from pandas_toon.parser import parse_toon


def read_toon(
    filepath_or_buffer: Union[str, Path, io.StringIO],
) -> pd.DataFrame:
    """
    Read a TOON format file into a DataFrame.

    TOON (Token-Oriented Object Notation) is a compact, LLM-optimized
    data format designed for minimal token usage.

    Parameters
    ----------
    filepath_or_buffer : str, Path, or file-like object
        Path to TOON file or file-like object containing TOON data.

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
        path = (
            Path(filepath_or_buffer)
            if isinstance(filepath_or_buffer, str)
            else filepath_or_buffer
        )
        with path.open(encoding="utf-8") as f:
            content = f.read()
    elif hasattr(filepath_or_buffer, "read"):
        content = filepath_or_buffer.read()
    else:
        raise ValueError(
            f"Invalid input type: {type(filepath_or_buffer)}. "
            "Expected str, Path, or file-like object.",
        )

    # Parse the TOON content
    parsed = parse_toon(content)

    # Create DataFrame
    return pd.DataFrame(parsed["data"], columns=parsed["columns"])

