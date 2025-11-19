"""
Base parser class for factor data.
"""
import pandas as pd
from abc import ABC, abstractmethod
from typing import Dict


class BaseParser(ABC):
    """
    Abstract base class for factor data parsers.
    """

    @abstractmethod
    def parse(self, file_path: str, config: Dict) -> pd.DataFrame:
        """
        Parse a factor data file.

        Args:
            file_path: Path to the data file
            config: Configuration dictionary with parsing parameters

        Returns:
            DataFrame with standardized columns:
                - date: datetime
                - factor_code: str (canonical factor code)
                - return_value: float (decimal return, not percentage)
        """
        pass

    def validate_output(self, df: pd.DataFrame) -> bool:
        """
        Validate that the output DataFrame has the correct format.

        Args:
            df: DataFrame to validate

        Returns:
            True if valid

        Raises:
            ValueError if validation fails
        """
        required_columns = ['date', 'factor_code', 'return_value']

        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"Missing required column: {col}")

        if not pd.api.types.is_datetime64_any_dtype(df['date']):
            raise ValueError("'date' column must be datetime type")

        if not pd.api.types.is_numeric_dtype(df['return_value']):
            raise ValueError("'return_value' column must be numeric")

        return True
