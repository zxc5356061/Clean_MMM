# Data Transformation and Validation Process

## Overview
This repository contains scripts and utilities designed to automate the transformation and validation of marketing data. The project cleans raw files for merging later. All data will be resampled as weekly data starting from Monday.

The project contains several major sections.

- **main.py**: The main script to clean, transform, and validate the data.
  - If a file only contains monthly data, then it will be required to transform the raw data by specifying the 'special_case' and 'special_case_col' in the script. 
- **Transformer.py**: A utility script to handle date transformations and resampling of data from daily to weekly intervals.
- **Validator.py**: A utility script to validate the date format, column types, and column values (e.g., handling missing values or incorrect formats).
- **Region**:
  - CSV files contains column 'DATE', dependent and independent variables.

Files included are mock data and anonymised.

```text
    ├── Region/
        ├── 2024_xxxx_Region_company_MMM_Deliverables_Marketing_batch1 - Sample1.csv
        └── 2024_xxxx_Region_company_MMM_Deliverables_Marketing_batch1 - Sample2.csv
    ├── Output/
        ├── 2024_10_14_Region_CLIENT_Sample1.csv
        └── 2024_10_14_Region_CLIENT_Sample2.csv
    ├── main.py
    ├── Transformer.py
    └── Validator.py
```

## Expected outcome
1. The processed data will be saved as CSV files with the format: {date}_{region}_{name}_{media_name}.csv
2. Sum of each column will also to calculated for manual validation.
```text
 Channel:  Region Sample1
Columns:  ['DATE', 'Sample1_S']
Sum of Sample1_S:  60701.05

 Channel:  Region Sample2
Columns:  ['DATE', 'Sample2_S', 'Sample2_I', 'Sample2_C']
Sum of Sample2_S:  6110.95
Sum of Sample2_I:  4723394
Sum of Sample2_C:  29652
```
