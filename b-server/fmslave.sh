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
version="1.1"
channel="1" # 1 = stable; 2 = beta/dev
internet=true
varcurl=curl
host="192.168.0.111"
port="5000"
webapp="https://update.freemind-client.org/index.php"

function contactHost() {
  $varcurl -s --request GET "$(echo -e "http://$host:$port/bridge?action=$1\c"; [ -z "$2" ] || echo -e "&status=$2\c")"
}

function contactUpdateServer() {
  $varcurl -s --request GET "$webapp?userProgram=2&userChannel=$channel&userVersion=$version"
}

# checking superuser
if [[ $EUID != 0 ]]; then
  echo "Please run script as root!"
  exit 1
fi
if [[ $1 == "backup" ]]; then
  backup=$(contactHost DO_BACKUP)
  if [[ $backup == "true" ]]; then
    mount | grep /dev/sda1 > /dev/null # prüfen, ob HDD angeschlossen
    if [[ $? == 0 ]]; then
      rsync --rsync-path="sudo rsync" --delete -aze 'ssh -i /root/.ssh/id_rsa' rsyncuser@$host:/media/fileraid/ /media/backupdrive/igfserverbackup --exclude='.recycle'
      if [[ $? == 0 ]]; then
        find /media/backupdrive/igfserverbackup -type d -empty -exec rmdir {} +
        chown -R igfbackup:igfbackup /media/backupdrive/igfserverbackup
        chmod -R 700 /media/backupdrive/igfserverbackup
        contactHost BACKUP SUCCESS > /dev/null # Backup-done
        exit 0
      else
        contactHost BACKUP FAILED > /dev/null # Backup f3hler
      fi
    else
      contactHost HDD_ERROR > /dev/null # Festplatte nicht online
    fi
  else
    exit 0
  fi
fi
exit 99
if [[ $1 == "update" ]]; then
  contactUpdateServer > /dev/null || $internet=false
  if [[ $internet == true ]]; then
    update=$(contactUpdateServer)
    if [[ $update != "latest-version" ]]; then
      rm -r /etc/freemind/update
      mkdir /etc/freemind/update && cd /etc/freemind/update
      wget -q $update
      tar xzf slave.tar.gz
      chmod +x update.sh
      bash /etc/freemind/update/update.sh &
      if [[ $? == 0 ]]; then
        contactHost FM_UPDATE SUCCESS > /dev/null # Update Done
      else
        contactHost FM_UPDATE FAILED > /dev/null # Update Failed 
      fi
      exit 0
    fi
  fi
  exit 3
fi
exit 99
