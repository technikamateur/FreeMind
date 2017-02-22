#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
FreeMind is a composition of software and config files. It will help you to manage your Linux fileserver.
Copyright (C) 2017  Daniel Körsten aka TechnikAmateur

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import sqlite3
import os
import sys  # remove if there are no sys args.
import time
import libary


# function create databse if not exists
# v 1.0 - final
def create():
    if not os.path.isfile("freemind.db"):
        connection = sqlite3.connect("freemind.db")
        cursor = connection.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS errorlog(
                          id INTEGER PRIMARY KEY,
                          error INTEGER,
                          date TEXT,
                          time TEXT);""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS updatelog(
                          id INTEGER PRIMARY KEY,
                          date TEXT,
                          time TEXT,
                          updatetyp INTEGER);""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS recycleready(
                          id INTEGER PRIMARY KEY,
                          ready INTEGER);""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS memory(
                          id INTEGER PRIMARY KEY,
                          total TEXT,
                          free TEXT,
                          drive INTEGER);""")
        connection.close()


# function insert error in database with current date and time stamp
# v 1.0 - final
def inserterror(dberror):
    x = 0
    dberror = int(dberror)
    dbdate = time.strftime("%Y-%m-%d", time.gmtime())
    dbtime = time.strftime("%H-%M", time.gmtime())
    connection = sqlite3.connect("freemind.db")
    cursor = connection.cursor()
    for i in range(1, 9999):
        try:
            # yapf: disable
            cursor.execute("""INSERT INTO errorlog(id, error, date, time)
                              VALUES(?,?,?,?)""", (i, dberror, dbdate, dbtime))
            # yapf: enable
            connection.commit()
        except:
            x = x + 1  # only that something is happening
        else:
            break
    connection.close()
    if i >= 9998:
        os.remove("freemind.db")
        create()
        x = 0
        connection = sqlite3.connect("freemind.db")
        cursor = connection.cursor()
        for i in range(1, 9999):
            try:
                # yapf: disable
                cursor.execute("""INSERT INTO errorlog(id, error, date, time)
                                  VALUES(?,?,?,?)""", (i, dberror, dbdate, dbtime))
                # yapf: enable
                connection.commit()
            except:
                x = x + 1  # only that something is happens
            else:
                break
        connection.close()


# function insert update in databse with current time and date stamp
# v 1.0 - final
def insertupdate(updatetyp):
    x = 0
    if updatetyp == "freemind":
        dbupdatetyp = 0
        dbupdatetyp = int(dbupdatetyp)
        dbdate = time.strftime("%Y-%m-%d", time.gmtime())
        dbtime = time.strftime("%H-%M", time.gmtime())
        connection = sqlite3.connect("freemind.db")
        cursor = connection.cursor()
        for i in range(1, 9999):
            try:
                # yapf: disable
                cursor.execute("""INSERT INTO updatelog(id, date, time, update)
                                  VALUES(?,?,?,?)""", (i, dbdate, dbtime, dbupdatetyp))
                # yapf: enable
                connection.commit()
            except:
                x = x + 1  # only that somthing happens
            else:
                break
        connection.close()
        if i >= 9998:
            os.remove("freemind.db")
            create()
            connection = sqlite3.connect("freemind.db")
            cursor = connection.cursor()
            for i in range(1, 9999):
                try:
                    # yapf: disable
                    cursor.execute("""INSERT INTO updatelog(id, date, time, update)
                                      VALUES(?,?,?,?)""", (i, dbdate, dbtime, dbupdatetyp))
                    # yapf: enable
                    connection.commit()
                except:
                    x = x + 1  # only that somthing happens
                else:
                    break
            connection.close()
    elif updatetyp == "system":
        dbupdatetyp = 1
        dbupdatetyp = int(dbupdatetyp)
        dbdate = time.strftime("%Y-%m-%d", time.gmtime())
        dbtime = time.strftime("%H-%M", time.gmtime())
        connection = sqlite3.connect("freemind.db")
        cursor = connection.cursor()
        for i in range(1, 9999):
            try:
                # yapf: disable
                cursor.execute("""INSERT INTO updatelog(id, date, time, update)
                                  VALUES(?,?,?,?)""", (i, dbdate, dbtime, dbupdatetyp))
                # yapf: enable
                connection.commit()
            except:
                x = x + 1  # only that somthing happens
            else:
                break
        connection.close()
        if i >= 9998:
            os.remove("freemind.db")
            create()
            connection = sqlite3.connect("freemind.db")
            cursor = connection.cursor()
            for i in range(1, 9999):
                try:
                    # yapf: disable
                    cursor.execute("""INSERT INTO updatelog(id, date, time, update)
                                      VALUES(?,?,?,?)""", (i, dbdate, dbtime, dbupdatetyp))
                    # yapf: enable
                    connection.commit()
                except:
                    x = x + 1  # only that somthing happens
                else:
                    break
            connection.close()
    else:
        error = False
        return error


# function get last update from database and return element
# v 1.0 - final
def updatereq():
    connection = sqlite3.connect("freemind.db")
    cursor = connection.cursor()
    lastupdate = 0
    while lastupdate == 0: #FreeMind updates got 0; OS updtes 1
        # yapf: disable
        cursor.execute("""SELECT * FROM updatelog ORDER BY id DESC LIMIT 1""")
        # yapf: enable
        dbdate = cursor[1]
        lastupdate = cursor[3]
    connection.close()
    currenttime = time.strftime("%Y-%m-%d", time.gmtime())
    timediff = libary.timediff(dbdate, currenttime)
    if timediff >= 30:
        updateit = 1
    else:
        updateit = 0
    return updateit


# function save or get recycle status and return element
# works with freemind.db, table recycleready
# v 1.0 - final
def recycleready(para):
    if (para == 0) or (para == 1):
        para = int(para)
        eid = 1
        eid = int(eid)
        connection = sqlite3.connect("freemind.db")
        cursor = connection.cursor()
        try:
            # yapf: disable
            cursor.execute("""UPDATE recycleready SET ready = ?
                              WHERE id = ?""", (para, eid))
            connection.commit()
            connection.close()
            # yapf: enable
        except sqlite3.Error as e:
            z = 1  # SQLite3 Fehler. Wird aktuell nicht verarbeitet.
        except:
            # yapf: disable
            cursor.execute("""INSERT INTO recycleready(id, ready)
                              VALUES(?,?)""", (eid, ready))
            connection.commit()
            connection.close()
            # yapf: enable
    elif para == "get":
        # Hier sollte ein try, except folgen...
        eid = 1
        eid = int(eid)
        try:
            # yapf: disable
            connection = sqlite3.connect("freemind.db")
            cursor = connection.cursor()
            cursor.execute("""SELECT * FROM recycleready WHERE id=?""", (eid))
            ready = cursor[1]
            connection.close
            # yapf: enable
        except:
            # yapf: disable
            ready = "error"
            # yapf: enable
        ready = str(ready)
        return ready
