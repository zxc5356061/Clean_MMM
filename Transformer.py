import pandas as pd
from datetime import timedelta


class DataTransformer:
    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df

    def date_range_to_daily(self, start_date: str, end_date: str, *other_cols: str) -> pd.DataFrame:
        """To re-distribute data range data to dail data."""
        for i in [start_date, end_date]:
            try:
                self.df[i] = pd.to_datetime(self.df[i], format='%Y/%m/%d')
            except ValueError:
                f"Unable to convert {self.df[i]} to Y-m-d format."

        for i in [start_date, end_date]:
            assert self.df[i].dtype == 'datetime64[ns]', f"'{self.df[i]}' column is not datetime64."

        new_df = pd.DataFrame(columns=['DATE', *other_cols])

        for index, row in self.df.iterrows():
            # Generate date range for the current row
            date_range = pd.date_range(start=row[start_date], end=row[end_date])

            # Calculate daily values for each column in other_cols
            daily_values = {col: row[col] / len(date_range) for col in other_cols}

            temp_df = pd.DataFrame({
                'DATE': date_range,
                **daily_values
            })
            new_df = pd.concat([new_df, temp_df])

        new_df.reset_index(drop=True, inplace=True)
        new_df = new_df.groupby(['DATE']).sum().reset_index()

        return new_df

    def resample_daily_to_weekly(
            self, date_col: str, first_day: str = "MON"
    ) -> pd.DataFrame:
        """
        Resample a daily dataframe to weekly.

        This function is used to resample a daily dataframe to weekly.
        The dataframe must contain a date column with date as string with
        format YYYY-MM-DD.

        Parameters
        ----------
        df: DataFrame
            This dataframe must contain a date column with date as string
            with format YYYY-MM-DD.
        date_col: str
            Name of the column of df DataFrame that contains the date.
        first_day: str
            First day of the week. It can be either MON or SUN.

        Returns
        -------
        df_resampled: DataFrame
            Resampled dataframe.
        """
        if first_day == "MON":
            rule = "W"
        elif first_day == "SUN":
            rule = "W-SAT"
        else:
            raise ValueError("first_day must be either MON or SUN")

        self.df[date_col] = pd.to_datetime(self.df[date_col])
        df_resampled = (
            self.df.resample(rule, label="left", on=date_col).sum().reset_index()
        )
        # Shift the date of 1 day to get first day of the week (Monday or Sunday)
        df_resampled[date_col] = df_resampled[date_col] + timedelta(days=1)

        return df_resampled
