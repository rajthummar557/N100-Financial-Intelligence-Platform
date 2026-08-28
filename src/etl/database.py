import sqlite3
from pathlib import Path
def create_database():
    db_path = "nifty100.db"
    schema_path = Path("db/schema.sql")
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

if __name__ == "__main__":
    create_database()
    show_tables()