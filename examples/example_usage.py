"""
Example usage of pandas-toon library.

This script demonstrates how to use the pandas-toon library to read and write
TOON format files with pandas DataFrames.
"""

import pandas as pd
import pandas_toon
from io import StringIO


def main():
    print("=" * 60)
    print("pandas-toon Example Usage")
    print("=" * 60)
    print()
    
    # Example 1: Creating and exporting a DataFrame to TOON
    print("Example 1: Creating and exporting a DataFrame to TOON")
    print("-" * 60)
    
    df = pd.DataFrame({
        'name': ['Alice', 'Bob', 'Charlie'],
        'age': [30, 25, 35],
        'city': ['New York', 'London', 'Paris'],
        'active': [True, True, False]
    })
    
    print("Original DataFrame:")
    print(df)
    print()
    
    toon_str = df.to_toon()
    print("TOON format:")
    print(toon_str)
    print()
    
    # Example 2: Reading TOON format
    print("Example 2: Reading TOON format")
    print("-" * 60)
    
    toon_data = """@employees
name|department|salary|years
---
Alice|Engineering|95000.0|5
Bob|Marketing|75000.0|3
Charlie|Sales|85000.0|7
"""
    
    df_read = pd.read_toon(StringIO(toon_data))
    print("DataFrame from TOON:")
    print(df_read)
    print()
    print("Data types:")
    print(df_read.dtypes)
    print()
    
    # Example 3: Round-trip conversion
    print("Example 3: Round-trip conversion")
    print("-" * 60)
    
    original_df = pd.DataFrame({
        'product': ['Laptop', 'Mouse', 'Keyboard', 'Monitor'],
        'price': [999.99, 29.99, 79.99, 449.99],
        'stock': [15, 150, 45, 25],
        'available': [True, True, True, False]
    })
    
    print("Original DataFrame:")
    print(original_df)
    print()
    
    # Convert to TOON and back
    toon_output = original_df.to_toon(table_name='products')
    print("TOON representation:")
    print(toon_output)
    print()
    
    restored_df = pd.read_toon(StringIO(toon_output))
    print("Restored DataFrame:")
    print(restored_df)
    print()
    
    print("DataFrames are equal:", original_df.equals(restored_df))
    print()
    
    # Example 4: Handling missing values
    print("Example 4: Handling missing values")
    print("-" * 60)
    
    df_with_nulls = pd.DataFrame({
        'name': ['Alice', 'Bob', 'Charlie'],
        'email': ['alice@example.com', None, 'charlie@example.com'],
        'phone': ['123-4567', '234-5678', None]
    })
    
    print("DataFrame with null values:")
    print(df_with_nulls)
    print()
    
    toon_with_nulls = df_with_nulls.to_toon()
    print("TOON format (nulls as empty):")
    print(toon_with_nulls)
    print()
    
    # Example 5: File I/O
    print("Example 5: File I/O")
    print("-" * 60)
    
    sample_df = pd.DataFrame({
        'id': [1, 2, 3],
        'value': [10.5, 20.3, 30.1]
    })
    
    filename = '/tmp/example.toon'
    sample_df.to_toon(filename, table_name='sample_data')
    print(f"Written to {filename}")
    print()
    
    df_from_file = pd.read_toon(filename)
    print("Read from file:")
    print(df_from_file)
    print()
    
    # Clean up
    import os
    os.remove(filename)
    
    print("=" * 60)
    print("All examples completed successfully!")
    print("=" * 60)


if __name__ == '__main__':
    main()
