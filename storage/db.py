import duckdb
from pathlib import Path

DB_PATH = Path("data/etf.duckdb")

def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return duckdb.connect(DB_PATH)
