#!/bin/bash
#parameters
version = "1.0"
wai=$(dirname "$(readlink -e "$0")")
#main
clear
echo "Welcome to FreeMind v$version by Daniel Körsten
Press Enter to continue"; read
echo
echo "This project is licensed under Creative Commons 4.0 by-nc-sa.
For more information see 'license.txt'.
If you agree press 'Enter'. If not press 'Ctrl + c'."; read
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
echo "Installing security patches and required packages.
This might take some time."
sleep 5
sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get dist-upgrade -y
clear
sudo apt-get install python3 curl debhelper fakeroot build-essential htop btrfs-tools -y
clear
echo "All dependencies are installed and your system is up-to-date.
You should celebrate this!"
echo
echo "Installing components..."
sleep 5
mkdir hd-idle-files
mv hd-idle-1.05.tgz hd-idle-files
cd hd-idle-files
tar xfv hd-idle-1.05.tgz
sudo dpkg-buildpackage -rfakeroot
cd ..
sudo dpkg -i hd-idle_1.05_amd64.deb
sudo service hd-idle start
sudo update-rc.d hd-idle defaults
