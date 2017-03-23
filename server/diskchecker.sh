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

# for disks in defhdd.conf
# is root necessary?
# install quickdic :)
while read line
do
  disks+=($line)
done < disks.dat
for i in ${disks[@]}; do
  if ! [ "$(mount | grep /dev/$i>/dev/null)" ]; then
    echo $i >> disk_error.dat
  fi
done
rm disks.dat
