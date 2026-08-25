from pathlib import Path
import pandas as pd
DATA_DIR = Path("data/raw")
for file in sorted(DATA_DIR.glob("*.xlsx")):
    print("\n"+"="*80)
    print(f"FILE:{file.name}")
    print("="*80)
    try: 
        excel_file = pd.ExcelFile(file)
        print(f"sheet:{excel_file.sheet_names}")
        for sheet in excel_file.sheet_names:
            print(f"\n-----Sheet:{sheet}-----")

            df = pd.read_excel(file,sheet_name = sheet)
            print(f"Rows:{len(df)}")
            print(f"Columns:{len(df.columns)}")

            print("\n columns names")
            print(list(df.columns))
            print("\n first 3 rows")
            print(df.head(3).to_string(index=False))
    except Exception as e:
        print(f"Erorr:{e}")
