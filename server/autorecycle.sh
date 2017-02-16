#!/bin/bash

# FreeMind is a composition of software and config files. It will help you to manage your Linux fileserver.
# Copyright (C) 2017  Daniel Körsten aka TechnikAmateur
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# run script as sudo. Maybe a check at the beginnning would be helpful
sleep 30 # in case ist starts with OS it should wait until samba is started
if (( $EUID != 0 ))
then
    exit 1
fi
recyclepath="/media/recycledrive/sambarecycle"
fileraidpath="/media/fileraid/.recycle" # You must set the / at the end of the line.
#ready="$(python3 /etc/freemind/fmmain.py recycleready get)"
#if ! [[ "$ready" == "1" ]]; then
#  exit 1 # Es sollte vermerkt werden, ob das Script lief oder nicht. Oder ist das sinnlos? In kombi mit rsync --stats?
#fi
rsync -a $fileraidpath/ $recyclepath
find $recyclepath -type f -mtime +90 -delete
find $recyclepath -type d -empty -exec rmdir {} +
rm -r /media/fileraid/.recycle/*
