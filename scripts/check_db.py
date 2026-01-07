from storage.db import get_connection

con = get_connection()

# Check row counts
result = con.execute("SELECT ticker, COUNT(*) as rows FROM prices GROUP BY ticker").fetchall()
print("Row counts by ticker:")
for ticker, count in result:
    print(f"  {ticker}: {count}")

# Show recent data
print("\nRecent data:")
recent = con.execute("""
    SELECT ticker, date, close 
    FROM prices 
    ORDER BY date DESC 
    LIMIT 10
""").fetchall()

for row in recent:
    print(f"  {row[0]} {row[1]} ${row[2]:.2f}")

con.close()