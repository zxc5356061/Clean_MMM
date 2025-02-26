import pandas as pd

# Set up parameters

std_currencies = ("EUR", "PLN", "GBP")
country_lists = ("Germany", "Italy", "USA", "UK")
file_path = "~/2025-02-18_Abbott_Format_Overview_Input expected - Copy of ATV_BVOD.csv"

# Read data formats
df = pd.read_csv(file_path, dtype=str)

country = "country"

nd = "non_mandatory_date"
d = "date"

ns = "non_mandatory_string"
s = "mandatory_string"

ni = "non_mandatory_int"
i = "mandatory_int"

nf = "non_mandatory_float"
nf5 = "non_mandatory_float_5decimals"
f = "mandatory_float"
f5 = "mandatory_float_5decimals"

c = "currency"

yn = "yes_no"

df = df.replace({"[Text]": ns, "[Text]M": s,
                 "[YYYY-MM-DD]": nd, "[YYYY-MM-DD]M": d,
                 "[Integer, thousand separator]": ni, "[Integer, thousand separator]M": i,
                 "[yes/no]": yn,
                 "[Float with 2 decimals, thousand separator]": nf, "[Float with 2 decimals, thousand separator]M": f,
                 "[Float with 5 decimals, thousand separator]": nf5, "[Float with 5 decimals, thousand separator]M": f5,
                 "[Currency]": c,
                 "[country]": country
                 })

inputs = df.iloc[0].to_dict()


# Generate google sheet formulas

def validate_non_mandatory_string(col: str) -> str:
    """Validate empty cell, empty string, or string"""
    return f'IF(OR(${col}2 = "", AND(ISTEXT(${col}2), NOT(REGEXMATCH(TO_TEXT(${col}2), "\\|")))), "OK!", "Error - " & ${col}$1 & "; ")'


def validate_mandatory_string(col: str) -> str:
    """Validate non-empty or string"""
    return f'IF(AND(${col}2 <> "", ISTEXT(${col}2), NOT(REGEXMATCH(TO_TEXT(${col}2), "\\|"))), "OK!", "Error - " & ${col}$1 & "; ")'


def validate_country(col: str, countries: tuple) -> str:
    """Validate Exact Country name by list"""
    condition = [f'EXACT(${col}2,"{country}")' for country in country_lists]
    list_cur = ', '.join(condition)
    return f'IF(OR({list_cur}), "OK!", "Error - " & ${col}$1 & "; ")'


def validate_non_mandatory_date(col: str) -> str:
    """validate empty cell or yyyy-mm-dd"""
    return f'IF(OR(ISBLANK(${col}2), AND(REGEXMATCH(TO_TEXT(${col}2), "^\\d{{4}}-\\d{{2}}-\\d{{2}}$"), ISNUMBER(DATEVALUE(${col}2)))), "OK!", "Error - " & ${col}$1 & "; ")'


def validate_date(col: str) -> str:
    """Validate yyyy-mm-dd"""
    return f'IF(AND(REGEXMATCH(TO_TEXT(${col}2), "^\\d{{4}}-\\d{{2}}-\\d{{2}}$"), ISNUMBER(DATEVALUE(${col}2))), "OK!", "Error - " & ${col}$1 & "; ")'


def validate_non_mandatory_int(col: str) -> str:
    """Validate empty cell or int(-,+,0), with comma as the thousand separators"""
    return f'IF(OR(ISBLANK(${col}2), REGEXMATCH(TO_TEXT(${col}2), "^-?\\d{{1,3}}(,\\d{{3}})*$")), "OK!", "Error - " & ${col}$1 & "; ")'


def validate_mandatory_int(col: str) -> str:
    """Validate int(-,+,0), with comma as the thousand separators"""
    return f'IF(REGEXMATCH(TO_TEXT(${col}2), "^-?\\d{{1,3}}(,\\d{{3}})*$"), "OK!", "Error - " & ${col}$1 & "; ")'


def validate_non_mandatory_float(col: str) -> str:
    """Validate empty cell or float(-,+,0), with comma as the thousand separators and exact two decimals"""
    return f'IF(OR(ISBLANK(${col}2), REGEXMATCH(TO_TEXT(${col}2), "^-?\\d{{1,3}}(,\\d{{3}})*\\.\\d{{2}}$")), "OK!", "Error - " & ${col}$1 & "; ")'


def validate_non_mandatory_float_5decimals(col: str) -> str:
    """Validate empty cell or float(-,+,0), with comma as the thousand separators and exact five decimals"""
    return f'IF(OR(ISBLANK(${col}2), REGEXMATCH(TO_TEXT(${col}2), "^-?\\d{{1,3}}(,\\d{{3}})*\\.\\d{{5}}$")), "OK!", "Error - " & ${col}$1 & "; ")'


def validate_mandatory_float(col: str) -> str:
    """Validate float(-,+,0), with comma as the thousand separators and exact two decimals"""
    return f'IF(REGEXMATCH(TO_TEXT(${col}2), "^-?\\d{{1,3}}(,\\d{{3}})*\\.\\d{{2}}$"), "OK!", "Error - " & ${col}$1 & "; ")'


def validate_mandatory_float_5decimals(col: str) -> str:
    """Validate float(-,+,0), with comma as the thousand separators and exact five decimals"""
    return f'IF(REGEXMATCH(TO_TEXT(${col}2), "^-?\\d{{1,3}}(,\\d{{3}})*\\.\\d{{5}}$"), "OK!", "Error - " & ${col}$1 & "; ")'


def validate_currency(col: str, currencies: tuple) -> str:
    """Validate exact value for currency units"""
    condition = [f'EXACT(${col}2,"{cur}")' for cur in currencies]
    list_cur = ', '.join(condition)
    return f'IF(OR({list_cur}), "OK!", "Error - " & ${col}$1 & "; ")'


def validate_yes_no(col: str) -> str:
    """Validate empty cell, yes, or no, not case-sensitive"""
    return f'IF(OR(ISBLANK(${col}2), LOWER(${col}2) = "yes", LOWER(${col}2) = "no"), "OK!", "Error - " & ${col}$1 & "; ")'


body = []

for col, check_type in inputs.items():
    match check_type:
        case 'country':
            body.append(validate_country(col, country_lists))
        case 'non_mandatory_date':
            body.append(validate_non_mandatory_date(col))
        case 'date':
            body.append(validate_date(col))
        case 'non_mandatory_string':
            body.append(validate_non_mandatory_string(col))
        case 'mandatory_string':
            body.append(validate_mandatory_string(col))
        case 'non_mandatory_int':
            body.append(validate_non_mandatory_int(col))
        case 'mandatory_int':
            body.append(validate_mandatory_int(col))
        case 'non_mandatory_float':
            body.append(validate_non_mandatory_float(col))
        case 'non_mandatory_float_5decimals':
            body.append(validate_non_mandatory_float_5decimals(col))
        case 'mandatory_float':
            body.append(validate_mandatory_float(col))
        case 'currency':
            body.append(validate_currency(col, std_currencies))
        case 'yes_no':
            body.append(validate_yes_no(col))
        case "mandatory_float_5decimals":
            body.append(validate_mandatory_float_5decimals(col))
        case _:
            body.append(f'Unknown conditions -> {col}: {check_type}!')


# Construct final formula
first_col = next(iter(inputs.keys())) # Get the first key under the first value
last_col = list(inputs.keys())[-1] # Get the last key

formula_body = " & \n".join(body)

result = f'=IF(LEN(CONCATENATE({first_col}2:{last_col}2))=0, "",SUBSTITUTE( \n{formula_body}, "OK!", ""))'

print(result)
