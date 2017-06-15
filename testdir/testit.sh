#!/bin/bash
if [[ $EUID != 0 ]]; then
  echo "Please run script as root!"
  exit 1
else
  echo "Wie erwartet, ich bin nicht root..."
  sudo sh -c 'echo $SUDO_USER'
  exit 0
fi
