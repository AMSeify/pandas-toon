"""
Test script to convert CSV to TOON format and read it back.

This script demonstrates the full workflow:
1. Read a sample CSV file
2. Convert it to TOON format
3. Save the TOON file
4. Read the TOON file back
5. Verify the data matches
"""

import pandas as pd
import pandas_toon
from pathlib import Path


def main():
    print("=" * 70)
    print("pandas-toon: CSV to TOON Conversion Test")
    print("=" * 70)
    print()
    
    # Step 1: Read the sample CSV file
    print("Step 1: Reading sample CSV file...")
    print("-" * 70)
    csv_path = Path(__file__).parent / "sample_data.csv"
    df_original = pd.read_csv(csv_path)
    
    print(f"Loaded CSV from: {csv_path}")
    print(f"Shape: {df_original.shape}")
    print("\nOriginal DataFrame:")
    print(df_original)
    print(f"\nData types:\n{df_original.dtypes}")
    print()
    
    # Step 2: Convert to TOON format (string)
    print("Step 2: Converting to TOON format...")
    print("-" * 70)
    toon_string = df_original.to_toon(table_name="employees")
    
    print("TOON format (string):")
    print(toon_string)
    print()
    
    # Step 3: Save to TOON file
    print("Step 3: Saving to TOON file...")
    print("-" * 70)
    toon_path = Path(__file__).parent / "sample_data.toon"
    df_original.to_toon(toon_path, table_name="employees")
    
    print(f"Saved TOON file to: {toon_path}")
    print(f"File size: {toon_path.stat().st_size} bytes")
    print()
    
    # Step 4: Read the TOON file back
    print("Step 4: Reading TOON file back...")
    print("-" * 70)
    df_loaded = pd.read_toon(toon_path)
    
    print(f"Loaded TOON from: {toon_path}")
    print(f"Shape: {df_loaded.shape}")
    print("\nLoaded DataFrame:")
    print(df_loaded)
    print(f"\nData types:\n{df_loaded.dtypes}")
    print()
    
    # Step 5: Verify the data matches
    print("Step 5: Verification")
    print("-" * 70)
    
    # Check shape
    shape_match = df_original.shape == df_loaded.shape
    print(f"Shape matches: {shape_match}")
    
    # Check column names
    columns_match = list(df_original.columns) == list(df_loaded.columns)
    print(f"Columns match: {columns_match}")
    
    # Check data equality (convert to same types for comparison)
    df_original_str = df_original.astype(str)
    df_loaded_str = df_loaded.astype(str)
    data_match = df_original_str.equals(df_loaded_str)
    print(f"Data matches: {data_match}")
    
    print()
    if shape_match and columns_match and data_match:
        print("✓ SUCCESS: All data verified correctly!")
        print("  The CSV → TOON → DataFrame round-trip worked perfectly!")
    else:
        print("✗ WARNING: Some data mismatch detected")
        print("\nDifferences:")
        if not shape_match:
            print(f"  - Shape: {df_original.shape} vs {df_loaded.shape}")
        if not columns_match:
            print(f"  - Columns: {list(df_original.columns)} vs {list(df_loaded.columns)}")
        if not data_match:
            print("  - Data values differ")
    
    print()
    print("=" * 70)
    print("Test Complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()
