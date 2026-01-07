from storage.db import get_connection

def ensure_schema():
    con = get_connection()
    try:
        con.execute("""
            CREATE TABLE IF NOT EXISTS prices (
                ticker TEXT,
                date DATE,
                open DOUBLE,
                high DOUBLE,
                low DOUBLE,
                close DOUBLE,
                adj_close DOUBLE,
                volume BIGINT,
                PRIMARY KEY (ticker, date)
            )
        """)
    finally:
        con.close()
