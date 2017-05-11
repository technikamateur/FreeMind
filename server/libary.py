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

import os #file delete, moving and chmod
import sqlite3 #support for databases
import time #calculating with the time
import subprocess #running subprocesses
import shutil #file moving


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
                          ready INTEGER);""") # 0 = not ready, 1 = ready
        cursor.execute("""CREATE TABLE IF NOT EXISTS memory(
                          drive INTEGER PRIMARY KEY,
                          total TEXT,
                          free TEXT,
                          percent INTEGER,
                          smart INTEGER);""") # id = drive
        cursor.execute("""CREATE TABLE IF NOT EXISTS backupready(
                          id INTEGER PRIMARY KEY,
                          ready INTEGER);""") # 0 = not ready, 1 = ready
        connection.close()


def buildfmweb():
    hddnames, hddmem, hddsmart = spacegrabber()
    lena = len(hddnames)
    lenb = len(hddmem)
    lenc = len(hddsmart)
    if lena == lenb and lenb == lenc:
        try:
            os.remove("fmweb.db")
        except:
            pass
        connection = sqlite3.connect("fmweb.db")
        cursor = connection.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS memory(
                          drive INTEGER PRIMARY KEY,
                          name TEXT,
                          percent INTEGER,
                          smart TEXT);""") # smart enthält Farbe
        for i in range(0, lena):
            name = str(hddnames[i])
            mem = int(hddmem[i])
            if hddsmart[i] == "passed":
                smart = "green"
            elif hddsmart[i] == "failed":
                smart = "red" # manuell in reflex.min ergänzt
            else:
                smart = "dark"
            cursor.execute("""INSERT INTO memory(drive, name, percent, smart)
                              VALUES(?,?,?,?)""", (i, name, mem, smart))
        connection.commit()
        connection.close()
        shutil.move(os.path.join("/etc/freemind/", "fmweb.db"), os.path.join("/var/www/freemind/", "fmweb.db"))
        os.chmod("/var/www/freemind/fmweb.db", 0o644)
    else:
        pass
        # Error verarbeiten: es exsistiert nicht die dieselbe anzahl von namen, mem und smart.


# function insert data in database
# v 1.0 - final
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
# v 1.0 - final
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


# function insert data for logging
# v 1.1 - final
def logging(dbtarget, dbdata):
    if dbtarget == 1: # insert error
        i = 1
        dberror = int(dbdata)
        dbdate = time.strftime("%Y-%m-%d", time.gmtime())
        dbtime = time.strftime("%H-%M", time.gmtime())
        connection = sqlite3.connect("freemind.db")
        cursor = connection.cursor()
        while True:
            try:
                # yapf: disable
                cursor.execute("""INSERT INTO errorlog(id, error, date, time)
                                  VALUES(?,?,?,?)""", (i, dberror, dbdate, dbtime))
                # yapf: enable
            except:
                i += 1
                if i >= 9999:
                    break
            else:
                connection.commit()
                break
        connection.close()
        if not i >= 9999:
            result = "okay"
        else:
            result = "dbfull"
        return result
    elif dbtarget == 2: # insert update
        dbupdatetyp = dbdata # 1=FM master; 2=FM slave; 3=OS master; 4=OS slave
        i = 1
        dbupdatetyp = int(dbupdatetyp)
        dbdate = time.strftime("%Y-%m-%d", time.gmtime())
        dbtime = time.strftime("%H-%M", time.gmtime())
        connection = sqlite3.connect("freemind.db")
        cursor = connection.cursor()
        while True:
            try:
                # yapf: disable
                cursor.execute("""INSERT INTO updatelog(id, date, time, update)
                                  VALUES(?,?,?,?)""", (i, dbdate, dbtime, dbupdatetyp))
                # yapf: enable
                connection.commit()
            except:
                i += 1
                if i >= 9999:
                    break
            else:
                break
        connection.close()
        if not i >= 9999:
            result = "okay"
        else:
            result = "dbfull"
        return result


# function read logs out of database
# v 1.0 - final
def readlogs(dbtarget, dbdata):
    if dbtarget == 1: # read errors
        connection = sqlite3.connect("freemind.db")
        cursor = connection.cursor()
        cursor.execute("""SELECT COUNT(*) FROM errorlog""") # Was ist COUNT?????
        if cursor.fetchone():
            cursor.execute("""SELECT * FROM errorlog ORDER BY id ASC""")
        else:
            cursor = "error"
        connection.close()
        result = cursor
        return cursor
    elif dbtarget == 2: # read update
        connection = sqlite3.connect("freemind.db")
        cursor = connection.cursor()
        updatetyp = int(dbdata)
        cursor.execute("""SELECT * FROM updatelog ORDER BY id DESC""")
        for element in cursor:
            if element[3] == dbdata: # is here int() necessary
                dbres == element[1] + "+" + element[2]
                break
            else:
                pass
        connection.close()
        if "+" not in dbres:
            result = "error"
        else:
            result = dbres
        return result


# give this function 2 dates and you will get timediff
# only works with dates created with time.strftime("%Y-%m-%d", time.gmtime())
def timediff(olddate, newdate):
    olddate = str(olddate)
    newdate = str(newdate)
    olddatesplit = olddate.split("-")
    newdatesplit = newdate.split("-")
    # yapf: disable
    olddatetuple = (int(olddatesplit[0]), int(olddatesplit[1]),int(olddatesplit[2]), 0, 0, 0, 0, 0, 0)
    newdatetuple = (int(newdatesplit[0]), int(newdatesplit[1]),int(newdatesplit[2]), 0, 0, 0, 0, 0, 0)
    # yapf: enable
    olddate = time.mktime(olddatetuple)
    newdate = time.mktime(newdatetuple)
    diff = newdate - olddate
    diff = diff // 86400  # ganzzahlige division durch 24h, da Ergebnis in Sekunden
    return diff


def spacegrabber():
    # gethdd.sh ausführen
    subprocess.call(["sudo", "bash", "gethdd.sh"])
    # Import Festplatteninformationen
    with open("mem.dat") as f:
        data = []
        for line in f:
            line = line.rstrip("\n")
            data.append(line)
    # Import S.M.A.R.T. Informationen
    with open("smart.dat") as f:
        smart = []
        for line in f:
            line = line.rstrip("\n")
            smart.append(line)
    # Quelle löschen
    os.remove("smart.dat")
    os.remove("mem.dat")
    # Arrays für Kategorien erzeugen
    hdd = []
    hddname = []
    memis = []
    memtotal = []
    mempercent = []
    # Schleife für Textsplitting
    for element in data:
        datasplit = element.split("+")
        hdd.append(datasplit[0])
        hddname.append(datasplit[1])
        memis.append(datasplit[2])
        memtotal.append(datasplit[3])
    # memis und memtotal verarbeiten
    # strings ersetzten (siehe unterhalb)
    for i in range(len(memis)):
        memis[i] = memis[i].replace(",", ".")
        memis[i] = memis[i].replace("TiB", "T")
        memis[i] = memis[i].replace("GiB", "G")
        memis[i] = memis[i].replace("MiB", "M")
        memtotal[i] = memtotal[i].replace(",", ".")
        memtotal[i] = memtotal[i].replace("TiB", "T")
        memtotal[i] = memtotal[i].replace("GiB", "G")
        memtotal[i] = memtotal[i].replace("MiB", "M")
        # convert everything to G
        if memis[i].endswith("G"):
            memis[i] = memis[i].replace("G", "")
        elif memis[i].endswith("T"):
            memis[i] = memis[i].replace("T", "")
            memis[i] = float(memis[i]) * 1000
        elif memis[i].endswith("M"):
            memis[i] = memis[i].replace("M", "")
            memis[i] = float(memis[i]) / 1000
        if memtotal[i].endswith("G"):
            memtotal[i] = memtotal[i].replace("G", "")
        elif memtotal[i].endswith("T"):
            memtotal[i] = memtotal[i].replace("T", "")
            memtotal[i] = float(memtotal[i]) * 1000
        elif memtotal[i].endswith("M"):
            memtotal[i] = memtotal[i].replace("M", "")
            memtotal[i] = float(memtotal[i]) / 1000
        # Speicherbelegung in Prozent berechnen
        percent = 100 * float(memis[i]) / float(memtotal[i])
        mempercent.append(int(round(percent)))
    return hddname, mempercent, smart
