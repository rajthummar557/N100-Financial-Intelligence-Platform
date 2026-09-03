import sqlite3
import pandas as pd
from src.analytics.ratios import (
    net_profit_margin,
    operating_profit_margin,
    return_on_equity,
    debt_to_equity,
    interest_coverage,
    asset_turnover,
)
  
from src.analytics.cashflow_kpi import free_cash_flow

def load_source_data(db_path="nifty100.db"):
    conn = sqlite3.connect(db_path)

    query = """
    SELECT
        u.company_id,
        u.year,

        p.sales,
        p.operating_profit,
        p.other_income,
        p.interest,
        p.depreciation,
        p.net_profit,
        p.eps,
        p.dividend_payout,

        b.equity_capital,
        b.reserves,
        b.borrowings,
        b.investments,
        b.total_assets,

        c.operating_activity,
        c.investing_activity,
        c.financing_activity,

        comp.face_value

    FROM
    (
        SELECT company_id, year
        FROM profitandloss

        UNION

        SELECT company_id, year
        FROM balancesheet

        UNION

        SELECT company_id, year
        FROM cashflow
    ) u

    LEFT JOIN
    (
        SELECT
            company_id,
            year,
            MAX(sales) AS sales,
            MAX(operating_profit) AS operating_profit,
            MAX(other_income) AS other_income,
            MAX(interest) AS interest,
            MAX(depreciation) AS depreciation,
            MAX(net_profit) AS net_profit,
            MAX(eps) AS eps,
            MAX(dividend_payout) AS dividend_payout
        FROM profitandloss
        GROUP BY company_id, year
    ) p
        ON p.company_id = u.company_id
       AND p.year = u.year

    LEFT JOIN
    (
        SELECT
            company_id,
            year,
            MAX(equity_capital) AS equity_capital,
            MAX(reserves) AS reserves,
            MAX(borrowings) AS borrowings,
            MAX(investments) AS investments,
            MAX(total_assets) AS total_assets
        FROM balancesheet
        GROUP BY company_id, year
    ) b
        ON b.company_id = u.company_id
       AND b.year = u.year

    LEFT JOIN
    (
        SELECT
            company_id,
            year,
            MAX(operating_activity) AS operating_activity,
            MAX(investing_activity) AS investing_activity,
            MAX(financing_activity) AS financing_activity
        FROM cashflow
        GROUP BY company_id, year
    ) c
        ON c.company_id = u.company_id
       AND c.year = u.year

    LEFT JOIN companies comp
        ON comp.id = u.company_id

    ORDER BY u.company_id, u.year
    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    return df
def calculate_ratio_row(row):
    fcf = None

    if pd.notna(row["operating_activity"]) and pd.notna(row["investing_activity"]):
        fcf = free_cash_flow(
            row["operating_activity"],
            row["investing_activity"]
        )

    return {
        "company_id": row["company_id"],
        "year": row["year"],

        "net_profit_margin_pct": net_profit_margin(
            row["net_profit"],
            row["sales"]
        ) if pd.notna(row["net_profit"]) and pd.notna(row["sales"]) else None,

        "operating_profit_margin_pct": operating_profit_margin(
            row["operating_profit"],
            row["sales"]
        ) if pd.notna(row["operating_profit"]) and pd.notna(row["sales"]) else None,

        "return_on_equity_pct": return_on_equity(
            row["net_profit"],
            row["equity_capital"],
            row["reserves"]
        ) if (
            pd.notna(row["net_profit"])
            and pd.notna(row["equity_capital"])
            and pd.notna(row["reserves"])
        ) else None,

        "debt_to_equity": debt_to_equity(
            row["borrowings"],
            row["equity_capital"],
            row["reserves"]
        ) if (
            pd.notna(row["borrowings"])
            and pd.notna(row["equity_capital"])
            and pd.notna(row["reserves"])
        ) else None,

        "interest_coverage": interest_coverage(
            row["operating_profit"],
            row["other_income"],
            row["interest"]
        ) if (
            pd.notna(row["operating_profit"])
            and pd.notna(row["other_income"])
            and pd.notna(row["interest"])
        ) else None,

        "asset_turnover": asset_turnover(
            row["sales"],
            row["total_assets"]
        ) if (
            pd.notna(row["sales"])
            and pd.notna(row["total_assets"])
        ) else None,

        "free_cash_flow_cr": fcf,

        "capex_cr": abs(row["investing_activity"])
        if pd.notna(row["investing_activity"]) else None,

        "earnings_per_share": row["eps"]
        if pd.notna(row["eps"]) else None,

        "book_value_per_share": (
            (row["equity_capital"] + row["reserves"])
            / (row["equity_capital"] / row["face_value"])
        )
        if (
            pd.notna(row["equity_capital"])
            and pd.notna(row["reserves"])
            and pd.notna(row["face_value"])
            and row["face_value"] != 0
            and row["equity_capital"] != 0
        )
        else None,

        "dividend_payout_ratio_pct": row["dividend_payout"]
        if pd.notna(row["dividend_payout"]) else None,

        "total_debt_cr": row["borrowings"]
        if pd.notna(row["borrowings"]) else None,

        "cash_from_operations_cr": row["operating_activity"]
        if pd.notna(row["operating_activity"]) else None,
    }


def calculate_all_ratios(df):
    results = []

    for _, row in df.iterrows():
        result = calculate_ratio_row(row)
        results.append(result)

    return pd.DataFrame(results)

if __name__ == "__main__":
    df = load_source_data()

    ratios_df = calculate_all_ratios(df)

    print("Source rows:", len(df))
    print("Ratio rows:", len(ratios_df))
    print(ratios_df.head())
    print(ratios_df.columns.tolist())

def save_ratios_to_db(ratios_df, db_path="nifty100.db"):
    
    conn = sqlite3.connect(db_path)

    # Remove the old calculated ratio rows
    conn.execute("DELETE FROM financial_ratios")

    # Insert the newly calculated rows
    ratios_df.to_sql(
        "financial_ratios",
        conn,
        if_exists="append",
        index=False
    )

    conn.commit()
    conn.close()
if __name__ == "__main__":
    df = load_source_data()

    ratios_df = calculate_all_ratios(df)

    print("Source rows:", len(df))
    print("Ratio rows:", len(ratios_df))

    save_ratios_to_db(ratios_df)

    print("financial_ratios updated successfully")