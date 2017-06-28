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

# this script must run as sudo!
if [[ $EUID != 0 ]]; then
  exit 1
fi
# cleaning up...
rm -f /tmp/smart.dat
rm -f /tmp/mem.dat
# get S.M.A.R.T.
# disks.conf wird eingelesen und der smart status wird ermittelt. Die drei Typen
# passed, failed und unknown werden in /tmp/smart.dat geschrieben. Wird später in
# python eingelesen und mit /tmp/mem.dat gematcht. Da beides zeitgleich ausgeführt
# wird, steht eine Zeile für jede HDD, die mittels /tmp/mem.dat zugeordnet werden können.
while read line; do
  if [[ $line == *"#"* ]] || [[ $line == *"<"* ]]; then
    :
  else
    hdd="$(echo $line | awk '$1 ~ "/dev" {print $1}')"
    status="$(smartctl -H $hdd | grep result | awk '{print $6}')"
    status="$(echo $status | tr A-Z a-z)"
    if [[ $status == "passed" ]]; then
      echo "passed" >> /tmp/smart.dat
    elif [[ $status == "fail" ]]; then
      echo "failed" >> /tmp/smart.dat
    else
      echo "unknown" >> /tmp/smart.dat
    fi
  fi
done <$(dirname "$(readlink -e "$0")")/disks.conf
# get memory
while read line; do
  if [[ $line == *"#"* ]] || [[ $line == *"<"* ]]; then
    :
  else
    hdd="$(echo $line | awk '$1 ~ "/dev" {print $1}')"
    hddtype="$(echo $line | awk '$1 ~ "/dev" {print $2}')"
    hddname="$(echo $line | awk '$1 ~ "/dev" {print $3}')"
    if [[ $hddtype == "btrfs" ]]; then
      memis="$(btrfs fi show | grep $hdd | awk '{print $6}')"
      memtotal="$(btrfs fi show | grep $hdd | awk '{print $4}')"
    else
      memis="$(df -h | grep $hdd | awk '{print $3}')"
      memtotal="$(df -h | grep $hdd | awk '{print $2}')"
    fi
    echo $hdd+$hddname+$memis+$memtotal >> /tmp/mem.dat
  fi
done < $(dirname "$(readlink -e "$0")")/disks.conf

chmown fmuser /tmp/mem.dat
chmown fmuser /tmp/smart.dat
