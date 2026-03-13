# create_db.py
# 创建数据库表

import sqlite3

conn = sqlite3.connect("database.db")
c = conn.cursor()

# 记录表（增加 name 字段）
c.execute("""
CREATE TABLE IF NOT EXISTS records(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
course TEXT,
base_value INTEGER,
input_value INTEGER,
result INTEGER,
time TEXT
)
""")

conn.commit()
conn.close()

print("数据库创建成功")