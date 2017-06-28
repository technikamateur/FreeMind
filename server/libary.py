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

import os # Dateien löschen/verschieben, chmod
import time # Zeitstempel - logging, etc.
import sqlite3 # Für sämtliche Datenbankoperationen
import subprocess # Subprozesse (shell) ausführen
import shutil # Dateien verschieben
import logging # Logs
from logging.handlers import SMTPHandler # Mails
import config # Config


def create():
    if not os.path.isfile("../freemind.db"):
        connection = sqlite3.connect("../freemind.db")
        cursor = connection.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS recycleready(
                          id INTEGER PRIMARY KEY,
                          ready INTEGER);""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS memory(
                          drive INTEGER PRIMARY KEY,
                          name TEXT,
                          percent INTEGER,
                          smart TEXT);""") # smart enthält Farbe; green = passed; red = failed; dark = unknown;
        cursor.execute("""CREATE TABLE IF NOT EXISTS actionlog(
                          client INTEGER,
                          variety INTEGER,
                          content TEXT);""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS clients(
                          client INTEGER PRIMARY KEY,
                          name TEXT);""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS logging(
                          timestamp REAL,
                          level INTEGER,
                          message TEXT);""")

        connection.close()
        prep_clients()
        prep_actionlog()


def prep_actionlog(): # Nicht manuell ausführen - wird über create() durchgeführt
    connection = sqlite3.connect("../freemind.db")
    cursor = connection.cursor()
    for i in range(1,3): # 1=master; 2=slave
        for k in range(1,5):# 1=OS-Update; 2=FM-Update; 3=letztes Backup; 4=Letzte Ausführung Papierkorb - nicht slave!
            cursor.execute("""INSERT INTO actionlog(client, variety, content)
                              VALUES(?,?,?)""", (i,k,"never"))
    connection.commit()
    connection.close()


def prep_clients(): # Nicht manuell ausführen - wird über create() durchgeführt
    connection = sqlite3.connect("../freemind.db")
    cursor = connection.cursor()
    cursor.execute("""INSERT INTO clients(client, name)
                      VALUES(?,?)""", (1,"Server"))
    cursor.execute("""INSERT INTO clients(client, name)
                      VALUES(?,?)""", (2,"Banana Pi"))
    connection.commit()
    connection.close()


def insert_actionlog(client, variety):
    # sicherstellen, dass client und variety integer sind
    client = int(client)
    variety = int(variety)
    content = time.strftime("%Y-%m-%d", time.gmtime())
    content = str(content)
    connection = sqlite3.connect("../freemind.db")
    cursor = connection.cursor()
    cursor.execute("""UPDATE actionlog SET content=?
                      WHERE client=? AND variety=?""", (content, client, variety))
    connection.commit()
    connection.close()


def writeSpacegrab():
    hddnames, hddmem, hddsmart = spacegrabber()
    lena = len(hddnames)
    lenb = len(hddmem)
    lenc = len(hddsmart)
    if lena == lenb and lenb == lenc:
        connection = sqlite3.connect("../freemind.db")  
        cursor = connection.cursor()

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
    else:
        pass
        # Error verarbeiten: es exsistiert nicht die dieselbe anzahl von namen, mem und smart.


def spacegrabber():
    # gethdd.sh ausführen
    subprocess.call(["sudo", "bash", "../utils/gethdd.sh"])
    # Import Festplatteninformationen
    with open("/tmp/mem.dat") as f:
        data = []
        for line in f:
            line = line.rstrip("\n")
            data.append(line)
    # Import S.M.A.R.T. Informationen
    with open("/tmp/smart.dat") as f:
        smart = []
        for line in f:
            line = line.rstrip("\n")
            smart.append(line)
    # Quelle löschen
    os.remove("/tmp/smart.dat")
    os.remove("/tmp/mem.dat")
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

###############################################################################
#                                    Logging                                  #
###############################################################################

# Patch SMTPHandler
class MySMTPHandler(SMTPHandler):
    lastMail = False;

    def getSubject(self, record):
        formatter = logging.Formatter(fmt=self.subject)
        return formatter.format(record)

    def emit(self, record):
        now = time.time()
        if not self.lastMail or (now - self.lastMail) > 10:
            super(MySMTPHandler,self).emit(record)
            self.lastMail = now;

class SQLiteHandler(logging.StreamHandler):
    def emit(self, record):
       connection = sqlite3.connect("../freemind.db")
       cursor = connection.cursor()
       cursor.execute("""insert INTO logging(timestamp, level, message) VALUES(?,?,?)""", (time.time(), record.levelno, self.format(record)))
       connection.commit()
       connection.close()

# Set up Logging and Levels
logger = logging.getLogger('SERVER');
logger.setLevel(logging.DEBUG);

# Add multiple Mail Handlers for Levels
for level in config.mail['mailAdresses']:
    if len(config.mail['mailAdresses'][level]) == 0:
        continue

    __handler = MySMTPHandler(config.mail['mailServer']['host'],
                            '<server@' + config.mail['mailServer']['host'] + '> FreeMind',
                            config.mail['mailAdresses'][level],
                            subject=config.mail['subjectLine'],
                            credentials=(config.mail['mailServer']['username'], config.mail['mailServer']['password']))

    __handler.setLevel(level)
    logger.addHandler(__handler)

__sqliteHandler = SQLiteHandler()
__sqliteHandler.setLevel(logging.DEBUG)
logger.addHandler(__sqliteHandler)


###############################################################################
#                                  Bootstrap                                  #
###############################################################################
create()
