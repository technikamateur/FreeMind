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
if [[ $EUID != 0 ]]; then
  echo "Please run script as root!"
  exit 1
fi
# starting update procedure...
if [[ $1 == "backup" ]]; then
  backup=$($varcurl -s --request GET "192.168.0.111/bridge.php?action=4")
  if [[ $backup == "true" ]]; then
    mount | grep /dev/sda1 > /dev/null # prüfen, ob HDD angeschlossen
    if [[ $? == 0 ]]; then
      rsync --rsync-path="sudo rsync" --delete -aze 'ssh -i /root/.ssh/id_rsa' rsyncuser@192.168.0.111:/media/fileraid/ /media/backupdrive/igfserverbackup --exclude='.recycle'
      if [[ $? == 0 ]]; then
        find /media/backupdrive/igfserverbackup -type d -empty -exec rmdir {} +
        chown -R igfbackup:igfbackup /media/backupdrive/igfserverbackup
        chmod -R 700 /media/backupdrive/igfserverbackup
        $varcurl -s --request GET "192.168.0.111/bridge.php?action=3" > /dev/null # Backup-done
      else
        $varcurl -s --request GET "192.168.0.111/bridge.php?action=5" > /dev/null # Backup f3hler
      fi
    else
      $varcurl -s --request GET "192.168.0.111/bridge.php?action=6" > /dev/null # Festplatte nicht online
    fi
  fi
fi
if [[ $1 == "update" ]]; then
  $varcurl -s --request GET "https://update.freemind-client.org/index.php?userProgram=2&userChannel=2&userVersion=$version" > /dev/null || $internet=false
  if [[ $internet == true ]]; then
    update=$($varcurl -s --request GET "https://update.freemind-client.org/index.php?userProgram=2&userChannel=2&userVersion=$version")
    if [[ $update != "latest-version" ]]; then
      rm -r /etc/freemind/update
      mkdir /etc/freemind/update && cd /etc/freemind/update
      wget -q $update
      tar xzf slave.tar.gz
      chmod +x update.sh
      bash /etc/freemind/update/update.sh &
      exit 0
    fi
  fi
fi
exit 0
