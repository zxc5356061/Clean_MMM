import pandas as pd
from typing import Any
from datetime import datetime, timedelta


class DataValidator:
    def __init__(self, df: pd.DataFrame, date_column: str) -> None:
        self.df = df
        self.date_column = date_column

    def validate_date_column(self) -> None:
        """
        Validate that the date column is in the correct format (YYYY-MM-DD).
        """
        if self.date_column not in self.df.columns:
            raise ValueError(f"Date Column '{self.date_column}' Not Found")

        try:
            pd.to_datetime(self.df[self.date_column], format="%Y-%m-%d", errors='raise')
        except (TypeError, ValueError) as exc:
            raise ValueError(f"Date validation error in column '{self.date_column}': {exc}") from exc

    def _contains_comma(self, value: Any) -> bool:
        """Check if a string contains a comma."""
        return isinstance(value, str) and ',' in value

    def _validate_thousand_separator(self, series: pd.Series) -> None:
        """Check if the series contains commas as thousands separator."""
        if series.apply(self._contains_comma).any():
            raise ValueError("Error: Dataset cannot contain commas as thousands separators.")

    def validate_and_rename_column(self, file_name: str, column_name: str, expected_dtype: str, new_name: str) -> None:
        if column_name in self.df.columns:
            try:
                self.df[column_name] = self.df[column_name].astype(expected_dtype)
            except ValueError as exc:
                raise ValueError(f"{file_name}: Error converting '{column_name}' to {expected_dtype}: {exc}")

            self._validate_thousand_separator(self.df[column_name])
            self.df.rename(columns={column_name: new_name}, inplace=True)
