"""
Generic CSV parser for factor data.
"""
import pandas as pd
from datetime import datetime
from typing import Dict
from .base_parser import BaseParser


class GenericCSVParser(BaseParser):
    """
    Generic parser for CSV files with factor returns.

    Assumes:
    - One date column
    - Multiple factor columns
    - Returns as decimals or percentages (configurable)
    """

    def parse(self, file_path: str, config: Dict) -> pd.DataFrame:
        """
        Parse a generic CSV file.

        Args:
            file_path: Path to the CSV file
            config: Configuration dict with:
                - skip_rows: Number of rows to skip
                - date_column: Name of date column
                - date_format: strptime format for dates
                - factor_mappings: Dict mapping raw column names to canonical codes
                - returns_in_pct: Whether returns are in percentage points (default: False)

        Returns:
            DataFrame with columns: date, factor_code, return_value
        """
        skip_rows = config.get('skip_rows', 0)
        date_column = config.get('date_column', 'date')
        date_format = config.get('date_format', '%Y-%m-%d')
        returns_in_pct = config.get('returns_in_pct', False)

        # Read CSV
        df = pd.read_csv(file_path, skiprows=skip_rows)

        # Clean column names
        df.columns = df.columns.str.strip()

        # Parse date
        if date_column in df.columns:
            df[date_column] = pd.to_datetime(df[date_column], format=date_format)
            df = df.rename(columns={date_column: 'date'})
        else:
            raise ValueError(f"Date column '{date_column}' not found in {file_path}")

        # Get factor columns (all except date)
        factor_columns = [col for col in df.columns if col != 'date']

        # Convert to numeric
        for col in factor_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        # Convert from percentages if needed
        if returns_in_pct:
            for col in factor_columns:
                df[col] = df[col] / 100.0

        # Melt to long format
        df_long = df.melt(id_vars=['date'], var_name='raw_factor_code', value_name='return_value')

        # Remove missing values
        df_long = df_long.dropna(subset=['return_value'])

        # Map to canonical factor codes
        factor_mappings = config.get('factor_mappings', {})
        df_long['factor_code'] = df_long['raw_factor_code'].map(factor_mappings)

        # Remove unmapped factors
        df_long = df_long[df_long['factor_code'].notna()]

        # Select final columns
        result = df_long[['date', 'factor_code', 'return_value']].copy()

        return result
