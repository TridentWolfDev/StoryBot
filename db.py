import sqlite3

conn = sqlite3.connect('channels.db')
cur = conn.cursor()

cur.execute("create table channels (channel_id INTEGER)")

conn.commit()