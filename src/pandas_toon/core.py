"""
Core functionality for pandas-toon, including DataFrame accessor registration.
"""

from pathlib import Path
from typing import Optional, Union

import pandas as pd

from pandas_toon.parser import serialize_toon


def to_toon(
    df: pd.DataFrame,
    path_or_buf: Optional[Union[str, Path]] = None,
    table_name: Optional[str] = None,
) -> Optional[str]:
    """
    Write a DataFrame to TOON format.

    Parameters
    ----------
    df : DataFrame
        The DataFrame to serialize.
    path_or_buf : str, Path, or None, optional
        File path or buffer to write to. If None, returns the TOON string.
    table_name : str, optional
        Optional table name to include in the TOON output.

    Returns
    -------
    str or None
        If path_or_buf is None, returns the TOON-formatted string.
        Otherwise, writes to the file and returns None.

    Examples
    --------
    >>> import pandas as pd
    >>> df = pd.DataFrame({'name': ['Alice', 'Bob'], 'age': [30, 25]})
    >>> toon_str = df.to_toon()
    >>> print(toon_str)
    name|age
    ---
    Alice|30
    Bob|25

    >>> df.to_toon('output.toon')
    """
    # Get column names and data
    columns = df.columns.tolist()
    data = df.values.tolist()

    # Serialize to TOON format
    toon_content = serialize_toon(columns, data, table_name=table_name)

    # Write to file or return string
    if path_or_buf is None:
        return toon_content
    path = (
        Path(path_or_buf) if isinstance(path_or_buf, str) else path_or_buf
    )
    with path.open("w", encoding="utf-8") as f:
        f.write(toon_content)
    return None


def register_dataframe_accessor() -> None:
    """
    Register the to_toon method on pandas DataFrame and read_toon on pandas module.

    This function is called automatically when pandas_toon is imported.
    """
    from pandas_toon.io import read_toon as _read_toon  # noqa: PLC0415

    # Add to_toon as a method to DataFrame
    pd.DataFrame.to_toon = to_toon

    # Add read_toon as a function to pandas module
    pd.read_toon = _read_toon
