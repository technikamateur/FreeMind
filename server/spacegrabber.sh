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

# create array with disks
diskbunch=(sda2 sdd1) # add here your NON RAID disks
btrfsbunch=(sdb1 sdc1) # add here your BtrFS RAID disks
diskerror=false # setting diskerror false 0 programm will change that if necessary
# checking root
if (( $EUID != 0 ))
then
    exit 1
fi
# preparing disks for diskchecker
for i in ${diskbunch[@]}; do
  echo $i >> disks.dat
done
for i in ${btrfsbunch[@]}; do
  echo $i >> disks.dat
done
# start diskchecker script
bash diskchecker.sh
# start real spacegrabber
if ! [[ -e disk_error.dat ]]; then
  for i in ${diskbunch[@]}; do
    disks+=($i)
  done
  for i in ${btrfsbunch[@]}; do
    disks+=($i)
  done
  for i in ${diskbunch[@]}; do
    mems+=($(df -h | grep $i | awk '{print $3}'))
    total+=($(df -h | grep $i | awk '{print $2}'))
  done
  for i in ${btrfsbunch[@]}; do
    mems+=($(btrfs fi show | grep $i | awk '{print $6}'))
    total+=($(btrfs fi show | grep $i | awk '{print $4}'))
  done
else
  while read line
  do
    errdisks+=($line)
  done < disk_error.dat
  for i in ${diskbunch[@]}; do
    disks+=($i)
  done
  for i in ${btrfsbunch[@]}; do
    disks+=($i)
  done
  for i in ${diskbunch[@]}; do
    for j in ${errdisks[@]}; do
      if [[ $j == $i ]]; then
        diskerror=true
      fi
    done
    if [[ $diskerror == true ]]; then
      mems+=("0G")
      total+=("0G")
      diskerror=false
    else
      mems+=($(df -h | grep $i | awk '{print $3}'))
      total+=($(df -h | grep $i | awk '{print $2}'))
    fi
  done
  for i in ${btrfsbunch[@]}; do
    for j in ${errdisks[@]}; do
      if [[ $j == $i ]]; then
        diskerror=true
      fi
    done
    if [[ $diskerror == true ]]; then
      mems+=("0GiB")
      total+=("0GiB")
      diskerror=false
    else
      mems+=($(btrfs fi show | grep $i | awk '{print $6}'))
      total+=($(btrfs fi show | grep $i | awk '{print $4}'))
    fi
  done
fi
count=$((${#diskbunch[@]} + ${#btrfsbunch[@]}))
for (( i = 0; i < $count; i++ )); do
  echo ${disks[i]}+${mems[i]}+${total[i]} >> mem.dat # mem.dat is only tempoary
done
rm disk_error.dat
exit 0
