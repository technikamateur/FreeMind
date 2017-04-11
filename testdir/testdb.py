import sqlite3
connection = sqlite3.connect("test.db")
cursor = connection.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS memory(
                  drive INTEGER PRIMARY KEY,
                  total TEXT,
                  free TEXT,
                  percent INTEGER,
                  smart INTEGER);""") # id = drive
connection.close()
connection = sqlite3.connect("test.db")
cursor = connection.cursor()
cursor.execute("""INSERT INTO memory(drive, percent)
                              VALUES(1,53)""", (ready))
connection.commit()
connection.close()
