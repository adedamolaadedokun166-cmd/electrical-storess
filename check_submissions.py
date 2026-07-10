import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "database.db"

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row

print("Contacts")
print("-------")
for row in conn.execute("SELECT * FROM contacts ORDER BY id DESC"):
    print(dict(row))

print("\nSubscribers")
print("----------")
for row in conn.execute("SELECT * FROM subscribers ORDER BY id DESC"):
    print(dict(row))

conn.close()
