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
startsamba=true
updatedone=true
#setting python backup "true"
python3 /etc/freemind/main.py backupready 1
# checking for server connection
curl -s --request GET http://46.182.19.177:8002/index.php?userversion=$version > /dev/null || $internet=false
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
    wget -N -q $update/freemind.tar.gz>/dev/null -P /etc/freemid/update
    tar -xf /etc/freemind/update/freemind.tar.gz
    chmod +x /etc/freemind/update/update.sh
    bash /etc/freemind/update/update.sh &
    exit 1
  fi
else
  python3 /etc/freemind/main.py error 15
fi
# checking HDD online
if ! [ "$(mount | grep /dev/sdb1>/dev/null)" ]
then
  python3 /etc/freemind/main.py error 1
  python3 startsamba=false
elif ! [ "$(mount | grep /dev/sdc1>/dev/null)" ]
then
  python3 /etc/freemind/main.py error 2
  python3 /etc/freemind/main.py backupready 0
elif ! [ "$(mount | grep /dev/sdd1>/dev/null)" ]
then
  python3 /etc/freemind/main.py error 3
  python3 /etc/freemind/main.py backupready 0
fi
done
# checking for the latest server update
internet=true
curl -s --request GET https://www.google.de/ >/dev/null || $internet=false
lastupdate="$(python3 /etc/freemind/main.py update lastupdate)"
if [ $lastupdate == 1 ] && [ $internet == true ]
then
  apt-get update >dev/null || updatedone=false
  apt-get upgrade -y >dev/null
  apt-get dist-upgrade -y >dev/null
fi
if [ $updatedone == true ]
then
  python3 /etc/freemind/main.py update system
else
  python3 /etc/freemind/main.py error 14
fi
