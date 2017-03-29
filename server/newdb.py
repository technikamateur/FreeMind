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

import os
import sqlite3


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
                          time TEXT);""") # kann wech
        cursor.execute("""CREATE TABLE IF NOT EXISTS updatelog(
                          id INTEGER PRIMARY KEY,
                          date TEXT,
                          time TEXT,
                          updatetyp INTEGER);""") # kann wech
        cursor.execute("""CREATE TABLE IF NOT EXISTS recycleready(
                          id INTEGER PRIMARY KEY,
                          ready INTEGER);""") # 0 = not ready, 1 = ready
        cursor.execute("""CREATE TABLE IF NOT EXISTS memory(
                          id INTEGER PRIMARY KEY,
                          total TEXT,
                          free TEXT,
                          drive INTEGER);""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS backupready(
                          id INTEGER PRIMARY KEY,
                          ready INTEGER);""") # 0 = not ready, 1 = ready
        cursor.execute("""CREATE TABLE IF NOT EXISTS logs(
                          id INTEGER PRIMARY KEY,
                          date TEXT,
                          time TEXT,
                          typ INTEGER);""")
        connection.close()


# function insert data in database
# v 1.0 - NOT final
def insert(dbtarget, dbdata): # dbtarget: table, dbdataarray: data for table

    if dbtarget == 1: # insert backupready
        connection = sqlite3.connect("freemind.db")
        cursor = connection.cursor()
        try:
            # yapf: disable
            cursor.execute("""UPDATE backupready SET ready=?
                              WHERE id = 1""", (ready))
            connection.commit()
            connection.close()
            # yapf: enable
        except:
            # yapf: disable
            cursor.execute("""INSERT INTO backupready(id, ready)
                              VALUES(1,?)""", (ready))
            connection.commit()
            connection.close()
            # yapf: enable
    elif dbtarget == 2: # insert recycleready
        connection = sqlite3.connect("freemind.db")
        cursor = connection.cursor()
        try:
            # yapf: disable
            cursor.execute("""UPDATE recycleready SET ready=?
                              WHERE id=1""", (ready))
            connection.commit()
            connection.close()
            # yapf: enable
        except:
            # yapf: disable
            cursor.execute("""INSERT INTO recycleready(id, redeay)
                              VALUES(1,?)""", (ready))
            connection.commit()
            connection.close()
            # yapf: enable
    #else...


# function get data from database
# v 1.0 - NOT final
def get(dbtarget):
    if dbtarget == 1: # get backupready
        try:
            connection = sqlite3.connect("freemind.db")
            cursor = connection.cursor()
            # yapf: disable
            cursor.execute("""SELECT * FROM backupready WHERE id=1""") # * should be replaced by colum
            # yapf: enable
            ready = cursor[1]
            connection.close()
        except:
            ready = "err"
        ready = str(ready)
        return ready
    elif dbtarget == 2: # get recycleready
        try:
            connection = sqlite3.connect("freemind.db")
            cursor = connection.cursor()
            # yapf: disable
            cursor.execute("""SELECT * FROM recycleready WHERE id=1""")
            # yapf: enable
            ready = cursor[1]
            connection.close()
        except:
            ready = "err"
        ready = str(ready)
        return ready
    else:
        ready = "value"
        return ready
