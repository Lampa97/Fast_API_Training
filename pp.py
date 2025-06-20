import sqlite3

conn = sqlite3.connect("urls.db")
cursor = conn.cursor()
cursor.execute("SELECT * FROM url")
rows = cursor.fetchall()
for row in rows:
    print(row)
conn.close()
