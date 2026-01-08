#!/usr/bin/env python3
"""Check metadata table contents."""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from storage.db import get_connection

con = get_connection()
try:
    result = con.execute("SELECT ticker, isin, description FROM etf_metadata LIMIT 10").fetchall()
    for row in result:
        print(f"{row[0]}: ISIN={row[1]}, DESC={row[2]}")
finally:
    con.close()
