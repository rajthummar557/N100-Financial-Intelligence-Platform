def calculate_cagr(start, end, years, actual_years=None):
    if start == 0:
        return None,"ZERO_BASE"

    if actual_years is not None and actual_years < years:
        return None, "INSUFFICIENT"

    if start > 0 and end < 0:
        return None, "DECLINE_TO_LOSS"

    if start < 0 and end > 0:
        return None, "TURNAROUND"

    if start < 0 and end < 0:
        return None, "BOTH_NEGATIVE"

    if years<=0:
        return None,"INSUFFICIENT"
    return ((end/start)**(1/years)-1)*100,None

import pandas as pd

def matric_cagr(df,metric_column,years):
    valid_df  = df[
        df["year"].astype(str).str.match(r"^\d{4}-(0[1-9]|1[0-2])$")
    ].copy()

    if valid_df.empty:
        return None,"INSUFFICIENT",None,None
    valid_df["date"]  = pd.to_datetime(valid_df["year"],format="%Y-%m")

    valid_df = valid_df.dropna(subset = [metric_column])

    if valid_df.empty:
        return None,"INSUFFICIENT",None,None

    valid_df = valid_df.sort_values("date")
    end_rows = valid_df.iloc[-1]

    end_date = end_rows["date"]
    end_value  = end_rows[metric_column]

    target_start_date = end_date - pd.DateOffset(years=years)

    exact_start = valid_df[valid_df["date"]==target_start_date]
    if not exact_start.empty:
        start_row = exact_start.iloc[0]
    else:
        earlier_rows = valid_df[valid_df["date"]<target_start_date]
        if earlier_rows.empty:
            return None,"INSUFFICIENT",None,None
        start_row = earlier_rows.iloc[-1]

    start_date = start_row["date"]
    start_value = start_row[metric_column]
    actual_years = (end_date-start_date).days/365.25

    if actual_years<=0:
        return None,"INSUFFICIENT",start_row["year"],end_rows["year"]

    cagr,flag = calculate_cagr(
          start_value,end_value,actual_years
    )
    return (
        cagr,flag,start_row["year"],end_rows["year"]
    )


import pandas as pd

df = pd.DataFrame({
    "year": [
        "2014-03",
        "2015-03",
        "2016-03",
        "2017-03",
        "2018-03",
        "2020-03",
        "2021-03",
        "2022-03",
        "2023-03",
        "2024-03"
    ],
    "revenue": [
        100, 110, 120, 130, 145, 160,
         200, 225, 250, 300
    ],
    "pat": [
        10, 11, 13, 15, 17,
        20, 22, 25, 28, 30
    ],
    "eps": [
        5, 5.5,6.5, 7, 8,
        9, 10, 11, 12, 15
    ]
})

def calculate_all_cagrs(df, metric_column):
    results = {}

    for years in [3, 5, 10]:
        cagr, flag, start_period, end_period = matric_cagr(
            df,
            metric_column,
            years
        )

        results[f"{years}Y"] = {
            "cagr": cagr,
            "flag": flag,
            "start": start_period,
            "end": end_period
        }

    return results

revenue_results = calculate_all_cagrs(df, "revenue")
pat_results = calculate_all_cagrs(df, "pat")
eps_results = calculate_all_cagrs(df, "eps")

print("Revenue:", revenue_results)
print("PAT:", pat_results)
print("EPS:", eps_results)