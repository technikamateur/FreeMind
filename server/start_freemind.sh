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

# setting up some basic parameters
version="1.0"
internet=true
# checking for server connection
curl -s --request GET http://46.182.19.177:8002/index.php?userversion=$version > /dev/null/temp || $internet=false
# cleaning update cache
if [ -d "/etc/freemind/update"]
then
  rm -r /etc/freemind/update
fi
# checking for updates, if connected
if [ $internet == true ]
then
  update="$(curl -s --request GET http://46.182.19.177:8002/index.php?userversion=$version)"
  if ! [ "$update" == "latest-version" ]
  then
    mkdir /etc/freemind/update
    wget -N -q -P /etc/freemid/update $update/freemind.tar.gz>/dev/null/temp
    tar -xf /etc/freemind/update/freemind.tar.gz -C /etc/freemind/update
    chmod +x /etc/freemind/update/update.sh
    bash /etc/freemind/update/update.sh &
    exit 0
  fi
fi
# start python for TCP Connection
# checking HDD online
if ! [ "$(mount | grep /dev/sdb>/dev/null/temp)" ]
then
  python3 /etc/freemind/base.py off 1
elif ! [ "$(mount | grep /dev/sdc>/dev/null/temp)" ]
then
  python3 /etc/freemind/base.py off 2
elif ! [ "$(mount | grep /dev/sdd>/dev/null/temp)" ]
then
  python3 /etc/freemind/base.py off 3
fi
