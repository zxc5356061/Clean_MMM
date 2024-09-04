# To transform google sheet files into csv files
# after all formatting errors fixed on Google sheets

import os
from datetime import datetime, timedelta
import pandas as pd
import Validator
import Transformer


def validate_grouped_sum(filename: str, df: pd.DataFrame, column_name: str):
    if column_name in df.columns:
        assert round(df[column_name].sum(), 2) == round(df_grouped[column_name].sum(),
                                                        2), (f"{file_name}, {column_name} Grouped data not summed "
                                                             f"correctly.")


def validate_resampled_sum(df_o: pd.DataFrame, df_r: pd.DataFrame, col: str, media_name: str):
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
    "CHANNEL",
    "Operating system",
    "Campaign name",
    "Adset name (optional)",
    "adset name",
    "adset name (optional)",
    "adset name (optional)",
    "Ad group (optional)",
    "TYPE",
    "NAME",
    "YEAR",
    ""

]


for file_name in dir_list:
    # to ignore system files
    if not file_name.startswith('.') and os.path.isfile(os.path.join(path, file_name)):
        media_name = (file_name.split(' - ')[1].replace('.csv', '')
                      .replace(' ', '_')
                      .replace('(', '')
                      .replace(')', ''))

        # open file
        with open(os.path.join(path, file_name), 'r') as f:
            # print(print(f"{file_name}: Start"))
            df_raw = pd.read_csv(f)

            # Exclude error rows if there is any
            df_raw = df_raw[~df_raw['Check'].astype(str).str.lower().str.contains('error')]

            # fill na values
            df_raw = df_raw.infer_objects(copy=False).fillna(0)

            # Drop unnecessary columns
            for field in col_to_drop:
                if field in df_raw.columns:
                    df_raw = df_raw.drop(field, axis=1)

            # Validate Date format
            df_raw.rename(columns={'Date': 'DATE'}, inplace=True)
            data_validator = Validator.DataValidator(df_raw, 'DATE')
            data_validator.validate_date_column()

            if "Spends" not in df_raw.columns:
                raise ValueError(f"Error: {file_name} does not have Spends column.")

            check_list = [['Spends', 'float64', f'{media_name}_S'],
                          ['clicks', 'int', f'{media_name}_C'],
                          ['Impressions', 'int', f'{media_name}_I'],
                          ['Sends', 'int', f'{media_name}_sends'],
                          ['Reach','int', f'{media_name}_R'],
                          ['ad value', 'float64', f'{media_name}_V']]

            for check_item in check_list:
                data_validator.validate_and_rename_column(file_name, *check_item)

            # Special handle
            special_case = ['PR']
            special_case_col = [f'{media_name}_S',f'{media_name}_R',f'{media_name}_V']

            if media_name in special_case:
                df_raw['DATE'] = pd.to_datetime(df_raw['DATE'])
                df_raw['End_DATE'] = df_raw['DATE'] + pd.offsets.MonthEnd(0)

                date_transformer = Transformer.DataTransformer(df_raw)
                df = date_transformer.date_range_to_daily('DATE', 'End_DATE', *special_case_col)
            else:
                df = df_raw

            # Validate null values
            null_columns = [col for col in df.columns if df[col].isnull().any()]
            if null_columns:
                print(f"Error: Null value found in {file_name}, column(s) {null_columns}.")

            # Resample data and validation
            df_grouped = df.groupby(['DATE']).sum().reset_index()
            assert not df_grouped.isnull().values.any(), f"{file_name} Returned data contains NaN."

            variables = [f'{media_name}_S',
                         f'{media_name}_I',
                         f'{media_name}_C',
                         f'{media_name}_sends',
                         f'{media_name}_units',
                         f'{media_name}_GRP',
                         f'{media_name}_R',
                         f'{media_name}_V']

            for i in variables:
                validate_grouped_sum(file_name, df_grouped, i)

            # To resemble daily data into weekly data
            resampler = Transformer.DataTransformer(df_grouped)
            resampled_df = resampler.resample_daily_to_weekly('DATE')
            for col in variables:
                validate_resampled_sum(df_grouped, resampled_df, col, media_name)

            print("\n Channel: ", region, media_name)
            print("Columns: ", list(resampled_df.columns))
            for col in variables:
                if col in resampled_df.columns:
                    print(f"Sum of {col}: ", resampled_df[col].sum())

            count_pass += 1

            # output_file_path = os.path.join(path, f"{time}_{region}_CLIENT_{media_name}.csv")
            # resampled_df.to_csv(output_file_path, index=False)

print(f"{count_pass} file(s) Done")
