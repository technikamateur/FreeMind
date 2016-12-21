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

#parameters
version = "1.0"
wai=$(dirname "$(readlink -e "$0")")
#main
clear
echo -e "Welcome to FreeMind v$version by Daniel Körsten.\nPress Enter to continue"; read
echo
echo "This project is licensed under Creative Commons 4.0 by-nc-sa."
echo "For more information see 'license.txt'."
echo "If you agree press 'Enter'. If not press 'Ctrl + c'."; read
echo
if (( $EUID != 0 ))
then
  echo "Please run as superuser (sudo)"
  exit 1
fi
if ! [ "$wai" == "/etc/freemind" ]
then
  echo "I am not in '/etc/freemind'. Create this folder and try again."
  exit 1
fi
echo -e "Installing security patches and required packages.\nThis might take some time."
sleep 5
apt-get update
apt-get upgrade -y
apt-get dist-upgrade -y
clear
apt-get install -y python3 curl debhelper fakeroot build-essential htop btrfs-tools sudo
clear
echo -e "All dependencies are installed and your system is up-to-date.\nYou should celebrate this!"
echo
echo "Installing components..."
sleep 5
mkdir hd-idle-files
mv hd-idle-1.05.tgz hd-idle-files #fehlerhaft, da beim entpacken auch ein ordner erstellt wird.
cd hd-idle-files
tar xfv hd-idle-1.05.tgz
dpkg-buildpackage -rfakeroot
cd ..
dpkg -i hd-idle_1.05_amd64.deb
service hd-idle start
update-rc.d hd-idle defaults
