import re
from datetime import datetime
def normalize_year(value):
    value = str(value).strip()
    if len(value) == 7 and value[4]=='-':
        return value
    if value.upper().startswith("FY"):
        year = int(value[2:])
        year = 2000 + year if year<100 else year
        return f"{year}-03"
    if value.isdigit() and len(value)==4:
        return f"{value}-03"
    clean_val = re.sub(r"[^\w\s]", " ",value).strip()
    parts = clean_val.split()
    if len(parts)==2:
        month,year=parts
        if len(year)==2 and year.isdigit():
            year = "20"+year
        clean_val=f"{month},{year}"
        for fmt in ("%b,%Y","%B,%Y"):
            try:
                return datetime.strptime(clean_val,fmt).strftime("%Y-%m")
            except ValueError:
                continue
    return "PARSE_ERROR"

def normalize_ticker(value):
    value = str(value).strip()
    return value.upper()
