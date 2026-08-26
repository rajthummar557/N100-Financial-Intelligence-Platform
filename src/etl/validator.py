import pandas as pd


# DQ -01
def check_pk_uniqueness(df,column):
    duplicates = df[df.duplicated(subset=[column],keep = False)]
    if duplicates.empty:
        return []
    failures = []
    for _,row in duplicates.iterrows():
        failures.append(
            {
                "rule_id":"DQ-01",
                "severity":"CRITICAL",
                "column":column,
                "value":row[column],\
                "message":f"Duplicate primary key {row[column]}"
            }
        ) 
    return failures
   
#DQ-02

def check_company_year_uniqueness(df):
    duplicates = df[df.duplicated(subset=["company_id","year"],keep = False)]
    if duplicates.empty:
        return []
    failures = []
    for _,row in duplicates.iterrows():
        failures.append(
            {
                "rule_id":"DQ-02",
                "severity":"CRITICAL",
                "column":"company_id,year",
                "value":f"{row["company_id"]},{row["year"]}",
                "message":(f"Duplicate company-year combination "
                          f"{ row["company_id"]},{row["year"]}"
                           )
            }
            
        ) 
    return failures

#DQ -03

def check_foreign_key(df,column,master_df,master_column):
    invalid = df[~df[column].isin(master_df[master_column])]
    if invalid.empty:
        return []
    failures = []
    for _ , row in invalid.iterrows():
        failures.append(
            {
                "rule_id":"DQ-03",
                "severity":"critical",
                "column":column,
                "value":row[column],
                "message":f"invalid foreign key:{row[column]}"
            }

        )
        return failures

# DQ-04

def check_balance_sheet(df):
    difference = (
        abs(df["total_liabilities"]-df["total_assets"])
        /df["total_assets"].abs()
    )
    invalid = df[difference>0.01]
    if invalid.empty:
        return []
    failures = []
    for _,row in invalid.iterrows():
        failures.append({
                "rule_id":"DQ-04",
                "severity":"CRITICAL",
                "column":"total_liabilities,total_assets",
                "value":f"{row['total_assets']},{row['total_liabilities']}",
                "message" : (
                    f"Balance sheet mismatch "
                    f"total assets : {row["total_assets"]} s"
                    f"total liablities:{row["total_liabilities"]}"
                )

            }
        )
    return failures


#DQ -05
def check_opm(df):
    calculate_opm = (df["operating_profit"]/df["sales"])*100
    differnece = (calculate_opm - df["opm_percentage"]).abs()
    invalid = df[differnece>=1]
    if invalid.empty:
        return []
    failures = []
    for _,row in invalid.iterrows():

        calculate_opm = (row["operating_profit"]/row["sales"])*100
      
        failures.append(
            {

                "rule_id": "DQ-05",
            "severity": "WARNING",
            "column": "opm_percentage",
            "value": row["opm_percentage"],
            "message": (
                f"OPM mismatch: source={row['opm_percentage']:.2f}, "
                f"calculated={calculate_opm:.2f}"
            )
            }
        )
    return failures

#DQ-06
def check_sales_positive(df):
    invalid = df[df["sales"]<=0]
    if invalid.empty:
        return []
    failures = []
    for _,row in invalid.iterrows():
         failures.append({
            "rule_id": "DQ-06",
            "severity": "CRITICAL",
            "column": "sales",
            "value": row["sales"],
            "message": f"Sales must be > 0: {row['sales']}"
        })

    return failures


#DQ -07
import re


def check_year_format(df):

    valid = df["year"].astype(str).str.match(
        r"^\d{4}-(0[1-9]|1[0-2])$"
    )

    invalid = df[~valid]

    if invalid.empty:
        return []

    failures = []

    for _, row in invalid.iterrows():
        failures.append({
            "rule_id": "DQ-07",
            "severity": "WARNING",
            "column": "year",
            "value": row["year"],
            "message": f"Invalid year format: {row['year']}"
        })

    return failures

#DQ-08
def check_ticker_format(df):
    valid = df["company_id"].astype(str).str.match(
         r"^[A-Z]{2,15}$"
    )
    invalid  = df[~valid]
    if invalid.empty:
        return []
    failures = []
    for _,row in invalid.iterrows():
        failures.append(
            {
                "rule_id": "DQ-08",
                "severity": "WARNING",
                 "column": "company_id",
                "value": row['company_id'],
                "message": f"Invalid ticker format: {row['company_id']}"
            }
        )
    return failures

#DQ-09
def check_net_cash(df):

    calculated_net_cash = (
        df["operating_activity"]
        + df["investing_activity"]
        + df["financing_activity"]
    )

    difference = (
        df["net_cash_flow"] - calculated_net_cash
    ).abs()

    invalid = df[difference > 10]

    if invalid.empty:
        return []

    failures = []

    for _, row in invalid.iterrows():
        calculated = (
            row["operating_activity"]
            + row["investing_activity"]
            + row["financing_activity"]
        )

        failures.append({
            "rule_id": "DQ-09",
            "severity": "WARNING",
            "column": "net_cash_flow",
            "value": row["net_cash_flow"],
            "message": (
                f"Net cash mismatch: "
                f"source={row['net_cash_flow']}, "
                f"calculated={calculated}"
            )
        })

    return failures

#DQ-10

def check_fixed_assets(df):

    invalid = df[df["fixed_assets"] < 0]

    if invalid.empty:
        return []

    failures = []

    for _, row in invalid.iterrows():
        failures.append({
            "rule_id": "DQ-10",
            "severity": "CRITICAL",
            "column": "fixed_assets",
            "value": row["fixed_assets"],
            "message": f"Fixed assets cannot be negative: {row['fixed_assets']}"
        })

    return failures

#DQ-11
def check_tax_rate(df):

    invalid = df[
        (df["tax_rate"] < 0) |
        (df["tax_rate"] > 60)
    ]

    if invalid.empty:
        return []

    failures = []

    for _, row in invalid.iterrows():
        failures.append({
            "rule_id": "DQ-11",
            "severity": "WARNING",
            "column": "tax_rate",
            "value": row["tax_rate"],
            "message": f"Tax rate out of range: {row['tax_rate']}"
        })

    return failures

#DQ-12
def check_dividend_payout(df):

    invalid = df[df["dividend_payout"] > 200]

    if invalid.empty:
        return []

    failures = []

    for _, row in invalid.iterrows():
        failures.append({
            "rule_id": "DQ-12",
            "severity": "WARNING",
            "column": "dividend_payout",
            "value": row["dividend_payout"],
            "message": (
                f"Dividend payout exceeds 200%: "
                f"{row['dividend_payout']}"
            )
        })

    return failures

#DQ-13
import requests
def check_annual_report_urls(df):
    failures = []
    for _,row in df.iterrows():
        url = row["Annual_Report"]
        if pd.isna(url):
            continue
        try:
            response = requests.head(url,timeout=10,allow_redirects=True)
            if response.status_code != 200:
                failures.append(
                    {
                    "rule_id": "DQ-13",
                    "severity": "WARNING",
                    "column": "Annual_Report",
                    "value": url,
                    "message": (
                        f"Annual report URL returned "
                        f"status {response.status_code}")
                    }
                )
        except requests.RequestException as e:
              failures.append({
                "rule_id": "DQ-13",
                "severity": "WARNING",
                "column": "Annual_Report",
                "value": url,
                "message": f"Could not validate URL: {e}"
            })

    return failures


#DQ-14
def check_eps_sign(df):

    invalid = df[
        (
            (df["net_profit"] < 0) &
            (df["eps"] >= 0)
        )
        |
        (
            (df["net_profit"] >= 0) &
            (df["eps"] < 0)
        )
    ]

    if invalid.empty:
        return []

    failures = []

    for _, row in invalid.iterrows():
        failures.append({
            "rule_id": "DQ-14",
            "severity": "WARNING",
            "column": "eps",
            "value": row["eps"],
            "message": (
                f"EPS sign inconsistent with net profit: "
                f"net_profit={row['net_profit']}, "
                f"eps={row['eps']}"
            )
        })

    return failures
#DQ 15

def check_exact_balance(df):

    invalid = df[
        df["total_assets"] != df["total_liabilities"]
    ]

    if invalid.empty:
        return []

    failures = []

    for _, row in invalid.iterrows():
        failures.append({
            "rule_id": "DQ-15",
            "severity": "INFO",
            "column": "total_assets, total_liabilities",
            "value": (
                f"{row['total_assets']}, "
                f"{row['total_liabilities']}"
            ),
            "message": (
                f"Exact balance mismatch: "
                f"assets={row['total_assets']}, "
                f"liabilities={row['total_liabilities']}"
            )
        })

    return failures

#DQ-16
def check_historical_coverage(df):

    year_counts = (
        df.groupby("company_id")["year"]
        .nunique()
    )

    invalid = year_counts[year_counts < 5]

    if invalid.empty:
        return []

    failures = []

    for company_id, count in invalid.items():
        failures.append({
            "rule_id": "DQ-16",
            "severity": "WARNING",
            "column": "company_id, year",
            "value": company_id,
            "message": (
                f"Insufficient historical coverage: "
                f"{count} years"
            )
        })

    return failures


