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

# This script was created for the creation of daily backups.
# It is part of FreeMind and won't work without the database!

sleep 120
backupready="$(python3 /etc/freemind/fmmain.py backupready get)"
if [[ "$backupready" == "1" ]]; then
  rsync --delete -abh /media/filedrive/ /media/backupdrive --backup-dir=/media/rescuedrive
  python3 /etc/freemind/fmmain.py backup done 1
else
  python3 /etc/freemind/fmmain.py backup done 0
fi
