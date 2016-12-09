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
                      date TEXT,
                      time TEXT);""")
    connection.close()
    connection =sqlite3.connect("freemind.db")
    cursor =connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS updatelog(
                      id INTEGER PRIMARY KEY,
                      date TEXT);""")
    connection.close()

# functions
# function inserterror to table errorlog in freemind.db
def inserterror():
    x = 0
    dberror = int(sys.argv[2])
    dbdate = time.strftime("%Y-%m-%d", time.gmtime())
    dbtime = time.strftime("%H-%M", time.gmtime())
    connection = sqlite3.connect("freemind.db")
    cursor = connection.cursor()
    for i in range(1,9999):
        try:
            cursor.execute("""INSERT INTO errorlog(id, error, date, time)
                              VALUES(?,?,?,?)""", (i, dberror, dbdate, dbtime))
            connection.commit()
        except:
            x = x + 1 # only that something is happening
        else:
            break
    connection.close()
    if i >= 9998:
        os.remove("freemind.db")
        connection = sqlite3.connect("freemind.db")
        cursor = connection.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS errorlog(
                          id INTEGER PRIMARY KEY,
                          error INTEGER,
                          date TEXT,
                          time TEXT);""")
        connection.close()
        x = 0
        connection = sqlite3.connect("freemind.db")
        cursor = connection.cursor()
        for i in range(1,9999):
            try:
                cursor.execute("""INSERT INTO errorlog(id, error, date, time)
                                  VALUES(?,?,?,?)""", (i, dberror, dbdate, dbtime))
                connection.commit()
            except:
                x = x + 1 # only that something is happens
            else:
                break
        connection.close()

# function read and insert update to table updatelog in freemind.db
def insertupdate():
    x = 0
    rw = sys.argv[2]
    if rw == "done":
        dbdate = time.strftime("%Y-%m-%d", time.gmtime())
        connection = sqlite3.connect("freemind.db")
        cursor = connection.cursor()
        for i in range(1,9999):
            try:
                cursor.execute("""INSERT INTO updatelog(id, date)
                                  VALUES(?,?)""", (i, dbdate))
                connection.commit()
            except:
                x = x + 1 # only that somthing happens
            else:
                break
        connection.close()
        if i >= 9998:
            os.remove("freemind.db")
            connection = sqlite3.connect("freemind.db")
            cursor = connection.cursor()
            for i in range(1,9999):
                try:
                    cursor.execute("""INSERT INTO updatelog(id, date)
                                      VALUES(?,?)""", (i, dbdate))
                    connection.commit()
                except:
                    x = x + 1 # only that somthing happens
                else:
                    break
            connection.close()
        updateit = 2
        return updateit
    else:
        connection = sqlite3.connect("freemind.db")
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM updatelog ORDER BY id DESC LIMIT 1""")
        dbdate = cursor[0][1]
        connection.close()
        currenttime = time.strftime("%Y-%m-%d", time.gmtime())
        timediff = timecalc(dbdate, currenttime)
        if timediff >= 30:
            updateit = True
        else:
            updateit = False
        return updateit

# function timecalc give two dates and get diffrence in days. Thats pretty cool!
def timecalc(olddate, newdate):
    olddate = str(olddate)
    newdate = str(newdate)
    olddatesplit = olddate.split("-")
    newdatesplit = newdate.split("-")
    olddatetuple = (int(olddatesplit[0]), int(olddatesplit[1]), int(olddatesplit[2]), 0, 0, 0, 0, 0, 0)
    newdatetuple = (int(newdatesplit[0]), int(newdatesplit[1]), int(newdatesplit[2]), 0, 0, 0, 0, 0, 0)
    olddate = time.mktime(olddatetuple)
    newdate = time.mktime(newdatetuple)
    diff = newdate - olddate
    diff = diff // 86400
    return diff

# getting sys arguments
if sys.argv[1] == "error":
    inserterror()
elif sys.argv[1] == "update":
    updatereq = insertupdate()
    if updatereq == True:
        print("required")
    elif updatereq == False:
        print("not")
