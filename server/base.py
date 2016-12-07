#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
To view a copy of this license, visit creativecommons.org/licenses/by-nc-sa/4.0/
or send a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.
created 2016 by Daniel Körsten aka TechnikAmateur
"""
import os, sys, time, sqlite3
# checking database
if not os.path.isfile("freemind.db"):
    connection = sqlite3.connect("freemind.db")
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS errorlog(
                      id INTEGER PRIMARY KEY,
                      error INTEGER,
                      details TEXT,
                      date TEXT,
                      time TEXT);""")
    connection.close()
# functions
def inserterror():
    x = 0
    dberror = 1
    dbdetails = int(sys.argv[2])
    dbdate = str(strftime("%Y-%m-%d", gmtime()))
    dbtime = str(strftime("%H-%M", gmtime()))
    connection = sqlite3.connect("freemind.db")
    cursor = connection.cursor()
    for i in range(1,9999):
        try:
            cursor.execute("""INSERT INTO errorlog(id, error, details, date, time)
                              VALUES(?,?,?,?,?)""", (i, dberror, dbdetails, dbdate, dbtime))
            connection.commit()
        except:
            x = x + 1 # only that something is happening
        else:
            break
    connection.close()
    if i == 9998:
        os.remove("freemind.db")
        connection = sqlite3.connect("freemind.db")
        cursor = connection.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS errorlog(
                          id INTEGER PRIMARY KEY,
                          error INTEGER,
                          details TEXT,
                          date TEXT,
                          time TEXT);""")
        connection.close()
        x = 0
        connection = sqlite3.connect("freemind.db")
        cursor = connection.cursor()
        for i in range(1,9999):
            try:
                cursor.execute("""INSERT INTO errorlog(id, error, details, date, time)
                                  VALUES(?,?,?,?,?)""", (i, dberror, dbdetails, dbdate, dbtime))
                connection.commit()
            except:
                x = x + 1 # only that something is happening
            else:
                break
        connection.close()

# getting sys arguments
if sys.argv[1] == "off":
    insertoff()
elif sys.argv[1] == "updatereq":
    bpla
