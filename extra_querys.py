import sqlite3
from db import connect_db

conn = connect_db()
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS sales (
    sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER,
    sale_time DATETIME,
    total_amount REAL,
    payment_method TEXT,
    FOREIGN KEY(order_id) REFERENCES orders(id)
)
''')

conn.commit()
conn.close()

