# To define values here
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

c = "currency"

yn = "yes_no"

inputs = {
    "A": country,
    "B": nd,
    "C": d,
    "D": ns,
    "E": s,
    "F": ni,
    "G": i,
    "H": nf,
    "I": nf5,
    "J": f,
    "K": c,
    "L": yn,
    # "M": i,
    # "N": ni,
    # "O": s,
    # "P": f,
    # "Q": ns,
    # "R": nf,
    # "S": ns,
    # "T": f,
    # "U": f,
    # "V": c,
    # "W": ni,
    # "X": nf,
    # "Y": nf,
    # "Z": nf,
    # "AA": nf,
    # "AB": c,
    # "AC": c,
    # "AD": c,
    # "AE": c,
    # "AF": c,
    # "AG": c,
    # "AH": c,
    # "AI": c,
    # "AJ": c,
    # "AK": c,
    # "AL": c,
    # "AM": c,
    # "AN": c,
    # "AO": c,
    # "AP": c,
    # "AQ": c,
    # "AR": c,
    # "AS": c,
    # "AT": c,
    # "AU": c,
}

std_currencies = ("NTD", "EUR")
country_lists = ("Germany", "Italy", "USA", "UK")


# Code generators


def validate_non_mandatory_string(col: str) -> str:
    """Validate empty cell, empty string, or string"""
    # IF(OR(${col}2 = "", ISTEXT(${col}2), NOT(REGEXMATCH(TO_TEXT(${col}2), "\|"))), "OK!", "Error - " & ${col}$1 & "; ")
    return f'IF(OR(${col}2 = "", AND(ISTEXT(${col}2), NOT(REGEXMATCH(TO_TEXT(${col}2), "\|")))), "OK!", "Error - " & ${col}$1 & "; ")'


def validate_mandatory_string(col: str) -> str:
    """Validate non-empty or string"""
    # IF(AND(${col}2 <> "", ISTEXT(${col}2), NOT(REGEXMATCH(TO_TEXT(${col}2), "\|"))), "OK!", "Error - " & $E$1 & "; ")
    return f'IF(AND(${col}2 <> "", ISTEXT(${col}2), NOT(REGEXMATCH(TO_TEXT(${col}2), "\|"))), "OK!", "Error - " & ${col}$1 & "; ")'


def validate_country(col: str, countries: tuple) -> str:
    """Validate Exact Country name by list"""
    condition = [f'EXACT(${col}2,"{country}")' for country in country_lists]
    list_cur = ', '.join(condition)
    return f'IF(OR({list_cur}), "OK!", "Error - " & ${col}$1 & "; ")'


def validate_non_mandatory_date(col: str) -> str:
    """validate empty cell or yyyy-mm-dd"""
    return f'IF(OR(ISBLANK(${col}2), AND(REGEXMATCH(TO_TEXT(${col}2), "^\d{{4}}-\d{{2}}-\d{{2}}$"), ISNUMBER(DATEVALUE(${col}2)))), "OK!", "Error - " & ${col}$1 & "; ")'


def validate_date(col: str) -> str:
    """Validate yyyy-mm-dd"""
    return f'IF(AND(REGEXMATCH(TO_TEXT(${col}2), "^\d{{4}}-\d{{2}}-\d{{2}}$"), ISNUMBER(DATEVALUE(${col}2))), "OK!", "Error - " & ${col}$1 & "; ")'


def validate_non_mandatory_int(col: str) -> str:
    """Validate empty cell or int"""
    return f'IF(OR(ISBLANK(${col}2), REGEXMATCH(TO_TEXT(${col}2), "^-?\d{{1,3}}(,\d{{3}})*$")), "OK!", "Error - " & ${col}$1 & "; ")'


def validate_mandatory_int(col: str) -> str:
    """Validate int(-,+,0)"""
    return f'IF(REGEXMATCH(TO_TEXT(${col}2), "^-?\d{{1,3}}(,\d{{3}})*$"), "OK!", "Error - " & ${col}$1 & "; ")'


def validate_non_mandatory_float(col: str) -> str:
    """Validate float(-,+,0) with . sign and exact two decimal spaces, or empty cell"""
    return f'IF(OR(ISBLANK(${col}2), REGEXMATCH(TO_TEXT(${col}2), "^-?\d{{1,3}}(,\d{{3}})*\.\d{{2}}$")), "OK!", "Error - " & ${col}$1 & "; ")'


def validate_non_mandatory_float_5decimals(col: str) -> str:
    """Validate float(-,+,0) with . sign and exact two decimal spaces, or empty cell"""
    return f'IF(OR(ISBLANK(${col}2), REGEXMATCH(TO_TEXT(${col}2), "^-?\d{{1,3}}(,\d{{3}})*\.\d{{5}}$")), "OK!", "Error - " & ${col}$1 & "; ")'


def validate_mandatory_float(col: str) -> str:
    """Validate float(-,+,0) with . sign and exact two decimal spaces"""
    return f'IF(REGEXMATCH(TO_TEXT(${col}2), "^-?\d{{1,3}}(,\d{{3}})*\.\d{{2}}$"), "OK!", "Error - " & ${col}$1 & "; ")'


def validate_currency(col: str, currencies: tuple) -> str:
    """Validate exact value for currency units"""
    condition = [f'EXACT(${col}2,"{cur}")' for cur in currencies]
    list_cur = ', '.join(condition)
    return f'IF(OR({list_cur}), "OK!", "Error - " & ${col}$1 & "; ")'


def validate_yes_no(col: str) -> str:
    return f'IF(OR(LOWER(${col}2) = "yes", LOWER(${col}2) = "no"), "OK!", "Error - " & ${col}$1 & "; ")'


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
        case _:
            body.append(f'Unknown conditions -> {col}: {check_type}!')

# Get the first key under the first value
first_key = next(iter(inputs.keys()))
last_key = list(inputs.keys())[-1]

formula_body = " & \n".join(body)

result = f'=IF(LEN(CONCATENATE({first_key}2:{last_key}2))=0, "",SUBSTITUTE( \n{formula_body}, "OK!", ""))'

print(result)
