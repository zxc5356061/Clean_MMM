# To transform google sheet files into csv files
# after all formatting errors fixed on Google sheets

import os
from datetime import datetime, timedelta
from typing import Any
import pandas as pd


def validate_date_string(date_text: Any):
    """Validate that the date string is in the correct format."""
    try:
        datetime.strptime(date_text, "%Y-%m-%d")
    except TypeError as exc:
        print(exc)
    except ValueError as exc:
        print(exc)
    except KeyError as exc:
        print(exc)


def validate_date_column(df: pd.DataFrame, date_column: str):
    """Validate that the date column is in the correct format."""
    if date_column not in df.columns.to_list():
        raise print('DateColumnNotFound')

    for date in df[date_column]:
        validate_date_string(date)


def check_missing_values(df: pd.DataFrame, feature: str) -> None:
    """
    Check if the dataset contains missing values in the specified column.

    Parameters
    ----------
    df: pd.DataFrame
        The dataset to check.
    feature: str
        The name of the column to check.

    Returns
    -------
    None
    """
    if df[feature].isnull().values.any():
        raise ValueError('MissingValueError')


def validate_contains_comma(value) -> bool:
    """
    Check if the value contains a comma.

    Parameters
    ----------
    value: any value
        Values in the dataframe to be checked

    Returns
    -------
    None
    """
    # Only check str values to prevent type errors
    if isinstance(value, str) and ',' in value:
        return True
    return False


def validate_thousand_separator(series: pd.Series) -> None:
    """Check if the dataframe contains commas as thousands separator."""
    if series.map(validate_contains_comma).any():
        raise ValueError("Error: Dataset can not contain commas or thousands separators.")


def validate_and_rename_column(df, column_name, expected_dtype, new_name, file_name):
    if column_name in df.columns:
        assert df[column_name].dtype == expected_dtype, f"{file_name}: '{column_name}' column is not {expected_dtype}."
        validate_thousand_separator(df[column_name])
        df.rename(columns={column_name: new_name}, inplace=True)


def resample_daily_to_weekly(
        df: pd.DataFrame, date_col: str, first_day: str = "MON"
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

    df[date_col] = pd.to_datetime(df[date_col])
    df_resampled = (
        df.resample(rule, label="left", on=date_col).sum().reset_index()
    )
    # Shift the date of 1 day to get first day of the week (Monday or Sunday)
    df_resampled[date_col] = df_resampled[date_col] + timedelta(days=1)
    return df_resampled


def validate_grouped_sum(filename, df, column_name):
    if column_name in df.columns:
        assert round(df[column_name].sum(), 2) == round(df_grouped[column_name].sum(),
                                                        2), f"{file_name}, {column_name} Grouped data not summed correctly."


def validate_resampled_sum(df_o, df_r, col, media_name):
    if col in df_o.columns:
        assert round(df_o[col].sum(), 2) == round(df_r[col].sum(),
                                                  2), f"{media_name} {col} not resampled correctly."


# Get the list of all files and directories
path = "/Users/huangp/Documents/Data_team/DT_project/Clean_MMM/BEFR"
dir_list = os.listdir(path)

time = datetime.now().strftime("%Y_%m_%d")
region = path.split('/')[7]

count_pass = 0

col_to_drop = [
    "Check",
    "Campaign name",
    "Adset name (optional)",
    "adset name (optional)",
    "Station",
    "Length",
    "Target",
    "Regies",
    "Channel",
    "Start Time",
    "Break Code",
    "Position",
    "Position Number",
    "Program Before",
    "Program After",
    "Length",
    "GRP (000)",
    "Contacts",
    "Number of contacts 30"
]

# Radio_GRP

for file_name in dir_list:
    # to ignore system files
    if not file_name.startswith('.') and os.path.isfile(os.path.join(path, file_name)):
        media_name = file_name.split(' - ')[1].replace('.csv', '').replace(' ', '_')

        # open file
        with open(os.path.join(path, file_name), 'r') as f:
            # print(print(f"{file_name}: Start"))
            df = pd.read_csv(f)

            # Exclude error rows if there is any
            df = df[~df['Check'].astype(str).str.lower().str.contains('error')]

            # Drop unnecessary columns
            for field in col_to_drop:
                if field in df.columns:
                    df = df.drop(field, axis=1)

            # Validate Date format
            validate_date_column(df, 'Date')
            df.rename(columns={'Date': 'DATE'}, inplace=True)

            # Check 'Spends' column
            if "Spends" not in df.columns:
                raise ValueError(f"Error: {file_name} does not have Spends column.")
            validate_and_rename_column(df, 'Spends', 'float64', f'{media_name}_S', file_name)

            # Check 'Impressions' column
            validate_and_rename_column(df, 'Impressions', 'int', f'{media_name}_I', file_name)

            # Check 'clicks' column
            validate_and_rename_column(df, 'clicks', 'int', f'{media_name}_C', file_name)

            # Check 'GRP' column
            validate_and_rename_column(df, 'GRP', 'float64', f'{media_name}_GRP', file_name)

            # Validate null values
            null_columns = [col for col in df.columns if df[col].isnull().any()]
            if null_columns:
                print(f"Error: Null value found in {file_name}, column(s) {null_columns}.")

            # Resample data and validation
            df_grouped = df.groupby(['DATE']).sum().reset_index()
            assert not df_grouped.isnull().values.any(), f"{file_name} Returned data contains NaN."

            variables = [f'{media_name}_S', f'{media_name}_I', f'{media_name}_C', f'{media_name}_GRP']

            for i in variables:
                validate_grouped_sum(file_name, df_grouped, i)

            # To resemble daily data into weekly data
            resampled_df = resample_daily_to_weekly(df_grouped, 'DATE')
            for col in variables:
                validate_resampled_sum(df_grouped, resampled_df, col, media_name)

            print("\n Channel: ", region, media_name)
            print("Columns: ", list(resampled_df.columns))
            for col in variables:
                if col in resampled_df.columns:
                    print(f"Sum of {col}: ", resampled_df[col].sum())

            # print(f"{file_name}: Pass")
            count_pass += 1

            output_file_path = os.path.join(path, f"{time}_{region}_MEDIAPLUS_{media_name}.csv")
            resampled_df.to_csv(output_file_path, index=False)

print(f"{count_pass} file(s) Done")
