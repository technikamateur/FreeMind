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
import subprocess
import time


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
    # first, it should start the .sh
    # what happens if drive is not present?????
    subprocess.call("./spacegrabber.sh")  # if an error occurs: use(["script"])
    # check number of drives and create array size for disks
    fobj = open("mem.dat")
    countdisks = 0
    for line in fobj:
        countdisks += 1
    fobj.close()
    darray = [0] * countdisk
    # check number of names and create array size for names
    fobj = open("defhdd.conf")
    countnames = 0
    for line in fobj:
        countnames += 1
    fobj.close()
    dnames = [0] * countnames
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
    fobj.close()
    # creating array for every category
    hddname = [0] * countdisks
    hdd = [0] * countdisks
    memis = [0] * countdisks
    memtotal = [0] * countdisks
    mempercent = [0] * countdisks
    # loop for disk text splitting (mem.dat) i=0
    for i in range(len(darray)):
        hddarraysplit = darray[i].split("+")
        hdd[i] = hddarraysplit[0]
        memis[i] = hddarraysplit[1]
        memtotal[i] = hddarraysplit[2]
    # setting all hdd names to "not given"
    for i in range(len(hddname)):
        hdd[i] = "not given"
    # loop for name text splitting (defhdd.conf) i = 0; try to replace "not given" by a name
    for i in range(len(dnames)):
        try:
            hddnamesplit = dnames[i].split("=")
            if hdd[i] == hddnamesplit[0]:
                hddname[i] = hddnamesplit[1]
        # exception for statements without "=" e.g. comments: pass them!
        except:
            pass
    # processing memis and memtotal
    # replace strings below
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
        if memis[i].endswith("T"):
            memis[i] = memis[i].replace("T", "")
            memis[i] = int(memis[i]) * 1000
            #memis[i] = str(memis[i]) + "G"
        elif memtotal[i].endswith("T"):
            memtotal[i] = memtotal[i].replace("T", "")
            memtotal[i] = int(memtotal[i]) * 1000
            #memtotal[i] = str(memtotal[i]) + "G"
        elif memis[i].endswith("G"):
            memis[i] = memis[i].replace("G", "")
        elif memtotal[i].endswith("G"):
            memtotal[i] = memtotal[i].replace("G", "")
        elif memis[i].endswith("M"):
            memis[i] = memis[i].replace("M", "")
            memis[i] = int(memis[i]) / 1000
            #memis[i] = str(memis[i]) + "G"
        elif memtotal[i].endswith("M"):
            memtotal[i] = memtotal[i].replace("M", "")
            memtotal[i] = int(memtotal[i]) / 1000
            #memtotal[i] = str(memtotal[i]) + "G"
        # calculate disk usage in percent
        mempercent[i] = (100 * memis[i]) / memtotal[i]
    # return whatever
