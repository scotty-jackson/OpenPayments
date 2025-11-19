"""
Parser for Ken French Data Library format.
"""
import pandas as pd
from datetime import datetime
from typing import Dict, List, Tuple
from .base_parser import BaseParser


class KenFrenchParser(BaseParser):
    """
    Parser for Ken French Data Library CSV files.

    Ken French files often have special formatting:
    - Date column in YYYYMM format
    - Returns in percentage points (need to divide by 100)
    - May have multiple sections in one file
    """

    def parse(self, file_path: str, config: Dict) -> pd.DataFrame:
        """
        Parse a Ken French format file.

        Args:
            file_path: Path to the CSV file
            config: Configuration dict with parsing parameters

        Returns:
            DataFrame with standardized columns: date, factor_code, return_value
        """
        skip_rows = config.get('skip_rows', 0)
        date_column = config.get('date_column', 'Date')
        date_format = config.get('date_format', '%Y%m')

        # Read the CSV file
        df = pd.read_csv(file_path, skiprows=skip_rows)

        # Clean column names
        df.columns = df.columns.str.strip()

        # Parse date column
        if date_column in df.columns:
            df[date_column] = pd.to_datetime(df[date_column].astype(str), format=date_format)
            df = df.rename(columns={date_column: 'date'})
        else:
            raise ValueError(f"Date column '{date_column}' not found in file")

        # Convert returns from percentage points to decimals
        factor_columns = [col for col in df.columns if col != 'date']
        for col in factor_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce') / 100.0

        # Melt to long format
        df_long = df.melt(id_vars=['date'], var_name='raw_factor_code', value_name='return_value')

        # Remove any rows with missing returns
        df_long = df_long.dropna(subset=['return_value'])

        # Map raw factor codes to canonical codes
        factor_mappings = config.get('factor_mappings', {})
        df_long['factor_code'] = df_long['raw_factor_code'].map(factor_mappings)

        # Remove unmapped factors
        df_long = df_long[df_long['factor_code'].notna()]

        # Select final columns
        result = df_long[['date', 'factor_code', 'return_value']].copy()

        return result
