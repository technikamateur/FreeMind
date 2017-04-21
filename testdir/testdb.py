import sqlite3
connection = sqlite3.connect("fmweb.db")
cursor = connection.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS memory(
                  drive INTEGER PRIMARY KEY,
                  name TEXT,
                  percent INTEGER,
                  smart TEXT);""")
connection.commit()
connection.close()
connection = sqlite3.connect("fmweb.db")
cursor = connection.cursor()
cursor.execute("""INSERT INTO memory(drive, name, percent, smart)
                              VALUES(1,"Testdrive",58,"green")""")
cursor.execute("""INSERT INTO memory(drive, name, percent, smart)
                              VALUES(2,"Testdrive2",59,"green")""")
cursor.execute("""INSERT INTO memory(drive, name, percent, smart)
                              VALUES(3,"Testdrive3",57,"dark")""")
cursor.execute("""INSERT INTO memory(drive, name, percent, smart)
                              VALUES(4,"Testdrive4",56,"orange")""")
connection.commit()
connection.close()
