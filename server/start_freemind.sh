#!/bin/bash

# This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit creativecommons.org/licenses/by-nc-sa/4.0/
# or send a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.
# created 2016 by Daniel Körsten aka TechnikAmateur

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
