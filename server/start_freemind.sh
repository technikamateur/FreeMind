#!/bin/bash
# This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit creativecommons.org/licenses/by-nc-sa/4.0/
# or send a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.
#
# setting up some basic parameters
version="1.0"
internet=true
# checking for update
curl -s --request GET http://46.182.19.177:8002/index.php?userversion=$version > /dev/null/temp || $internet=false
if [ $internet == true ]
then
  update=$(curl -s --request GET http://46.182.19.177:8002/index.php?userversion=$version)
  if ! [ "$update" == "latest-version" ]
  then
      wget -N -q -P /etc/freemid/update $update/freemind.tar.gz > /dev/null/temp
  fi
fi
