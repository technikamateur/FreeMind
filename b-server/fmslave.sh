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

# setting up some parameters
version="1.0"
internet=true
varcurl=curl
# checking superuser
if (( $EUID != 0 ))
then
    exit 1
fi
# starting update procedure...
if [[ $1 == 1 ]]; then
  $varcurl -s --request GET "http://46.182.19.177:8002/index.php?userprogram=freemind-backup&userversion=$version" > /dev/null || $internet=false
  if [ $internet == true ]; then
    update=$($varcurl -s --request GET "http://46.182.19.177:8002/index.php?userprogram=freemind-backup&userversion=$version")
    if [ $update != "latest-version" ]; then
      mkdir /etc/freemind/update
      wget -q -O - $update/freemind-backup.tar.gz | tar xzf - -C /etc/freemind/update
      chmod +x /etc/freemind/update/update.sh
      bash /etc/freemind/update/update.sh &
      exit 0
    fi
  fi # else statement?
elif [[ $1 == 2 ]]; then
  bash fmtransfer.sh
elif [[ $1 == 3 ]]; then
  bash autobackup.sh
fi
