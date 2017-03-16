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

import time
import os


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

def spacagrabber():
    # first, it should start the .sh
    # check number of drives and create array
    fobj = open("mem.dat")
    count = 0
    for line in fobj:
        count += 1
    fobj.close()
    darray = [0] * count
    dnames = [0] * count
    # write data from file into array
    fobj = open("mem.dat")
    i = 0
    for line in fobj:
        darray[i] = line.rstrip()
        i += 1
    fobj.close()
    # remove the source .dat
    os.remove("mem.dat")
    # read the drive names. ONLY as much as drives in mem.dat
    fobj = open("defhdd.conf")
    i = 0
    for line in fobj:
        dnames[i] = line.rstrip()
        i += 1
        if i == count:
            break
    fobj.close()
    #return dnames, darray, count
    # creating array for every category
    hddname = [0] * count
    hdd = [0] * count
    memis = [0] * count
    memtotal = [0] * count
    # count -1 because loop starts with 0 instead of 1
    count -= 1
    # loop for text splitting (mem.dat)
    for disks in darray:
        hddarraysplit = disks.split("+")
        hdd[i] = hddarraysplit[0]
        memis[i] = hddarraysplit[1]
        memtotal[i] = hddarraysplit[2]
    for names in dnames:
        hddnamesplit = names.split("=")
