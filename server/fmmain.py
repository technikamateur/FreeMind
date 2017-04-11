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

import sys

import dbase  # will be replaced by newdb
import libary
import newdb

# creating databse if not exists
dbase.create()
# getting sys arguments
if sys.argv[1] == "error":
    pass
elif sys.argv[1] == "update":
    update = sys.argv[2]
    if (update == "freemind") or (update == "system"):
        status = dbase.inserterror(update)
    elif update == "lastupdate":
        status = dbase.updatereq()
        print(status)
    else:
        sys.exit(1)
elif sys.argv[1] == "recycleready":
    recyclepara = sys.argv[2]
    status = dbase.recycleready(recyclepara)
    if (status == "1") or (status == "0"):
        print(status)
elif sys.argv[1] == 1:
    xyz = libary.spacegrabber()
elif sys.argv[1] == 2:
    if sys.argv[2] == 1:
        print("hello")
    elif sys.argv[2] == 2:
        result = newdb.get(1) # -> should be 1 instead of 2!
        if result != "error":
            print(result)
        # what if not (error)
