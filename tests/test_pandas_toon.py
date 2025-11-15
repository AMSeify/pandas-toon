"""
Tests for pandas-toon library.
"""

import pytest
import pandas as pd
from io import StringIO
import tempfile
import os

# Import after installing the package
import pandas_toon
from pandas_toon import read_toon
from pandas_toon.parser import parse_toon, serialize_toon, ToonParseError


class TestToonParser:
    """Tests for TOON parser functions."""
    
    def test_parse_simple_toon(self):
        """Test parsing a simple TOON format."""
        content = """data[2]{name,age,city}:
  Alice,30,New York
  Bob,25,London"""
        
        result = parse_toon(content)
        
        assert result['columns'] == ['name', 'age', 'city']
        assert result['declared_length'] == 2
        assert len(result['data']) == 2
        assert result['data'][0] == ['Alice', 30, 'New York']
        assert result['data'][1] == ['Bob', 25, 'London']
    
    def test_parse_with_table_name(self):
        """Test parsing TOON with table name."""
        content = """users[2]{name,age}:
  Alice,30
  Bob,25"""
        
        result = parse_toon(content)
        
        assert result['table_name'] == 'users'
        assert result['columns'] == ['name', 'age']
        assert result['declared_length'] == 2
        assert len(result['data']) == 2
    
    def test_parse_without_separator(self):
        """Test parsing TOON with proper metadata line."""
        content = """data[2]{name,age}:
  Alice,30
  Bob,25"""
        
        result = parse_toon(content)
        
        assert result['columns'] == ['name', 'age']
        assert result['declared_length'] == 2
        assert len(result['data']) == 2
        assert result['data'][0] == ['Alice', 30]
        assert result['data'][1] == ['Bob', 25]
    
    def test_parse_null_values(self):
        """Test parsing null/empty values."""
        content = """data[2]{name,age,city}:
  Alice,,New York
  Bob,25,"""
        
        result = parse_toon(content)
        
        assert result['data'][0][1] is None
        assert result['data'][1][2] is None
    
    def test_parse_boolean_values(self):
        """Test parsing boolean values."""
        content = """data[2]{name,active}:
  Alice,true
  Bob,false"""
        
        result = parse_toon(content)
        
        assert result['data'][0][1] is True
        assert result['data'][1][1] is False
    
    def test_parse_numeric_values(self):
        """Test parsing numeric values."""
        content = """data[2]{name,age,score}:
  Alice,30,95.5
  Bob,25,88.0"""
        
        result = parse_toon(content)
        
        assert result['data'][0][1] == 30
        assert result['data'][0][2] == 95.5
        assert result['data'][1][1] == 25
    
    def test_parse_empty_content(self):
        """Test parsing empty content raises error."""
        with pytest.raises(ToonParseError):
            parse_toon("")
    
    def test_serialize_simple_toon(self):
        """Test serializing data to TOON format."""
        columns = ['name', 'age', 'city']
        data = [
            ['Alice', 30, 'New York'],
            ['Bob', 25, 'London']
        ]
        
        result = serialize_toon(columns, data)
        
        assert 'data[2]{name,age,city}:' in result
        assert 'Alice,30,New York' in result
        assert 'Bob,25,London' in result
    
    def test_serialize_with_table_name(self):
        """Test serializing with table name."""
        columns = ['name', 'age']
        data = [['Alice', 30]]
        
        result = serialize_toon(columns, data, table_name='users')
        
        assert result.startswith('users[1]{name,age}:')
        assert 'Alice,30' in result
    
    def test_serialize_null_values(self):
        """Test serializing null values."""
        columns = ['name', 'value']
        data = [['Alice', None], ['Bob', None]]
        
        result = serialize_toon(columns, data)
        
        lines = result.split('\n')
        assert 'Alice,' in result
        assert 'Bob,' in result
    
    def test_serialize_boolean_values(self):
        """Test serializing boolean values."""
        columns = ['name', 'active']
        data = [['Alice', True], ['Bob', False]]
        
        result = serialize_toon(columns, data)
        
        assert 'Alice,true' in result
        assert 'Bob,false' in result


class TestReadToon:
    """Tests for read_toon function."""
    
    def test_read_toon_from_string_io(self):
        """Test reading TOON from StringIO."""
        toon_data = """data[2]{name,age,city}:
  Alice,30,New York
  Bob,25,London"""
        
        df = read_toon(StringIO(toon_data))
        
        assert isinstance(df, pd.DataFrame)
        assert list(df.columns) == ['name', 'age', 'city']
        assert len(df) == 2
        assert df.iloc[0]['name'] == 'Alice'
        assert df.iloc[0]['age'] == 30
        assert df.iloc[1]['name'] == 'Bob'
    
    def test_read_toon_from_file(self):
        """Test reading TOON from a file."""
        toon_data = """test_data[2]{name,score}:
  Alice,95.5
  Bob,88.0"""
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.toon') as f:
            f.write(toon_data)
            temp_path = f.name
        
        try:
            df = read_toon(temp_path)
            
            assert isinstance(df, pd.DataFrame)
            assert list(df.columns) == ['name', 'score']
            assert len(df) == 2
            assert df.iloc[0]['score'] == 95.5
        finally:
            os.unlink(temp_path)
    
    def test_read_toon_with_null_values(self):
        """Test reading TOON with null values."""
        toon_data = """data[2]{name,age,city}:
  Alice,,New York
  Bob,25,"""
        
        df = read_toon(StringIO(toon_data))
        
        assert pd.isna(df.iloc[0]['age'])
        assert pd.isna(df.iloc[1]['city'])


class TestToToon:
    """Tests for DataFrame.to_toon method."""
    
    def test_to_toon_returns_string(self):
        """Test to_toon returns string when no path given."""
        df = pd.DataFrame({
            'name': ['Alice', 'Bob'],
            'age': [30, 25]
        })
        
        result = df.to_toon()
        
        assert isinstance(result, str)
        assert 'data[2]{name,age}:' in result
        assert 'Alice,30' in result
        assert 'Bob,25' in result
    
    def test_to_toon_writes_to_file(self):
        """Test to_toon writes to file."""
        df = pd.DataFrame({
            'name': ['Alice', 'Bob'],
            'age': [30, 25],
            'city': ['New York', 'London']
        })
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.toon') as f:
            temp_path = f.name
        
        try:
            result = df.to_toon(temp_path)
            
            assert result is None
            
            # Read back and verify
            with open(temp_path, 'r') as f:
                content = f.read()
            
            assert 'data[2]{name,age,city}:' in content
            assert 'Alice,30,New York' in content
            assert 'Bob,25,London' in content
        finally:
            os.unlink(temp_path)
    
    def test_to_toon_with_table_name(self):
        """Test to_toon with table name."""
        df = pd.DataFrame({
            'name': ['Alice'],
            'age': [30]
        })
        
        result = df.to_toon(table_name='users')
        
        assert result.startswith('users[1]{name,age}:')
    
    def test_to_toon_with_null_values(self):
        """Test to_toon handles null values."""
        df = pd.DataFrame({
            'name': ['Alice', 'Bob'],
            'age': [30, None]
        })
        
        result = df.to_toon()
        
        # Note: pandas converts None to NaN for numeric columns
        assert 'Alice,' in result
        assert 'Bob,' in result


class TestRoundTrip:
    """Tests for round-trip conversion (read -> write -> read)."""
    
    def test_roundtrip_basic(self):
        """Test basic round-trip conversion."""
        original_df = pd.DataFrame({
            'name': ['Alice', 'Bob', 'Charlie'],
            'age': [30, 25, 35],
            'city': ['New York', 'London', 'Paris']
        })
        
        # Convert to TOON
        toon_str = original_df.to_toon()
        
        # Read back
        df_restored = read_toon(StringIO(toon_str))
        
        # Compare
        assert list(df_restored.columns) == list(original_df.columns)
        assert len(df_restored) == len(original_df)
        
        for col in original_df.columns:
            assert list(df_restored[col]) == list(original_df[col])
    
    def test_roundtrip_with_file(self):
        """Test round-trip conversion via file."""
        original_df = pd.DataFrame({
            'name': ['Alice', 'Bob'],
            'score': [95.5, 88.0],
            'passed': [True, True]
        })
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.toon') as f:
            temp_path = f.name
        
        try:
            # Write to file
            original_df.to_toon(temp_path)
            
            # Read back
            df_restored = read_toon(temp_path)
            
            # Compare
            assert list(df_restored.columns) == list(original_df.columns)
            assert len(df_restored) == len(original_df)
        finally:
            os.unlink(temp_path)


class TestIntegration:
    """Integration tests for pandas-toon."""
    
    def test_import_pandas_toon(self):
        """Test that pandas_toon can be imported."""
        import pandas_toon
        assert hasattr(pandas_toon, 'read_toon')
        assert hasattr(pandas_toon, '__version__')
    
    def test_dataframe_has_to_toon(self):
        """Test that DataFrame has to_toon method."""
        df = pd.DataFrame({'a': [1, 2, 3]})
        assert hasattr(df, 'to_toon')
        assert callable(df.to_toon)
    
    def test_usage_example(self):
        """Test the usage example from documentation."""
        # Create a DataFrame
        df = pd.DataFrame({
            'name': ['Alice', 'Bob', 'Charlie'],
            'age': [30, 25, 35],
            'city': ['New York', 'London', 'Paris']
        })
        
        # Export to TOON
        toon_str = df.to_toon()
        assert isinstance(toon_str, str)
        
        # Read back
        df_restored = read_toon(StringIO(toon_str))
        assert isinstance(df_restored, pd.DataFrame)
        assert len(df_restored) == 3
