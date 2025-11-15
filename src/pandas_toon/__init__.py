"""
pandas-toon: TOON format support for pandas

This package provides read_toon() and to_toon() functions for working with
the Token-Oriented Object Notation (TOON) format in pandas DataFrames.
"""

__version__ = "0.1.0"

from pandas_toon.io import read_toon
from pandas_toon.core import register_dataframe_accessor

# Register DataFrame.to_toon() method
register_dataframe_accessor()

__all__ = ["read_toon", "__version__"]
