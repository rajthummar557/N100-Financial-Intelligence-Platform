import pandas as pd
from pathlib import  Path
from normaliser import normalize_ticker,normalize_year
DATA_DIR = Path("data/raw")
def load_excel(file_path):
    
    df = pd.read_excel(file_path)
    if any(str(column).startswith("Unnamed:") for column in df.columns ):

        df = pd.read_excel(file_path,header=1)
    return df

def normalize_dataframe(df):
    if "id" in df.columns:
        df["id"] = df["id"].apply(normalize_ticker)
    if "company_id" in df.columns:
        df["company_id"] = df["company_id"].apply(normalize_ticker)
    if "year" in df.columns:
        df["year"] = df["year"].apply(normalize_year)
    return df




def load_all_files():
    data={}
    for file_path in sorted(DATA_DIR.glob("*.xlsx")):
        print(f"Loading {file_path.name}....")
        df = load_excel(file_path)
        normalize_dataframe(df)
        data[file_path.name] = df
        print("Rows:",len(df))
    return data


    