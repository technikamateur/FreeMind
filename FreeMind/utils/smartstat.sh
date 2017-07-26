#!/bin/sh
sudo smartctl -a /dev/sda | awk '/result:/ {print $NF}'

