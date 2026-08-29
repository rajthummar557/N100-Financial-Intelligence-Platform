import sqlite3
from pathlib import Path
from src.etl.loader import load_all_files
import pandas as pd
def create_database():
    db_path = Path("nifty100.db")
    schema_path = Path("db/schema.sql")
    if db_path.exists():
        db_path.unlink()    
    conn = sqlite3.connect(db_path)

    with open(schema_path,'r',encoding="utf-8") as f:
        sql_script = f.read()
    conn.executescript(sql_script)
    conn.commit()
    conn.close()
    print("Database and tabels are created succesfully")

def show_tables():
    conn = sqlite3.connect("nifty100.db")
    tables =    conn.execute(
        """
       select name
       from sqlite_master
       where type = 'table'
       order by name
        """
    ).fetchall()
    for tabel in tables:
        print(tabel[0])
    conn.close()

def load_dataframe(conn, df, table_name,rejected_counts):
    try:
        df.to_sql(
            table_name,
            conn,
            if_exists="append",
            index=False
        )
        conn.commit()
        print(f"{table_name} loaded: {len(df)} rows")
        print(f"rejected:{rejected_counts} rows")
        return {
            "table_name":table_name,
            "rows_loaded":len(df),
            "rows_rejected":rejected_counts
        }
    except Exception as e:
        conn.rollback()
        print(f"Error loading{table_name}:{e}")
        return {
            "table_name":table_name,
            "rows_loaded":0,
            "rows_rejected":len(df)+rejected_counts
        }
TABLE_MAP = {
    "companies.xlsx": "companies",
    "profitandloss.xlsx": "profitandloss",
    "balancesheet.xlsx": "balancesheet",
    "cashflow.xlsx": "cashflow",
    "analysis.xlsx": "analysis",
    "documents.xlsx": "documents",
    "prosandcons.xlsx": "prosandcons",
    "sectors.xlsx": "sectors",
    "stock_prices.xlsx": "stock_prices",
    "financial_ratios.xlsx": "financial_ratios",
    "market_cap.xlsx": "market_cap",
    "peer_groups.xlsx": "peer_groups",
}

def load_all_data(conn,data):
    audit = []
    companies = data["companies.xlsx"]

    for filename,table_name in TABLE_MAP.items():
        df = data[filename]
        rejected = 0
        if table_name != "companies" and "company_id" in df.columns:
            valid = df["company_id"].isin(companies["id"])
            rejected =(~valid).sum()
            df = df[valid]
        result = load_dataframe(conn,df,table_name,rejected)
        audit.append(result)
    return audit

def  check_foreign_keys():
    conn = sqlite3.connect("nifty100.db")
    errors = conn.execute("PRAGMA foreign_keys_check").fetchall()
    print("FK errors",len(errors))
if __name__ == "__main__":
    create_database()
    show_tables()
    data = load_all_files()

    conn = sqlite3.connect("nifty100.db")
    conn.execute("PRAGMA foreign_keys = ON")
    audit = load_all_data(
        conn,
        data
    )
    audit_df = pd.DataFrame(audit)
    audit_df.to_csv("output/load_audit.csv",index = False)
    check_foreign_keys()
    conn.close()
   