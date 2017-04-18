import sqlite3
t = 1
t = int(t)
connection = sqlite3.connect("test.db")
cursor = connection.cursor()
cursor.execute("""SELECT * FROM memory WHERE drive=1""")
print(cursor.fetchone())
