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

# Dieses Script sollte nicht als root ausgeführt werden

import os
import sys
import sqlite3
import time


# No root variante - libary.py nur für root
def actionlog(client, variety):
    # sicherstellen, dass client und variety integer sind
    client = int(client)
    variety = int(variety)
    content = time.strftime("%Y-%m-%d", time.gmtime())
    content = str(content)
    connection = sqlite3.connect("freemind.db")
    cursor = connection.cursor()
    cursor.execute("""UPDATE actionlog SET content=?
                      WHERE client=? AND variety=?""", (content, client, variety))
    connection.commit()
    connection.close()


# 1=OS-Update; 2=FM-Update; 3=Backup-done; 4=Do-Backup?
try:
    para = int(sys.argv[1])
except Exception as e:
    print("Parameter not valid!")
    sys.exit(2)
if para < 4:
    if os.path.isfile("freemind.db"):
        actionlog(2, para)
    else:
        pass # Datenbank ist nicht vorhanden
elif para == 4: # Do Backup? - Wird aktuell einfach bejat
    result = "true"
    print(result)
else:
    pass # Argument Error
