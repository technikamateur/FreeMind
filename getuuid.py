#!/usr/bin/python
# -*- coding: utf-8 -*-
import uuid, time
print("Gathering requiered information...")
time.sleep(3)
print("Done!")
print("Creating YOUR ID...")
time.sleep(5)
mac = uuid.getnode()
print("Your ID:")
print(mac)
print("saving to file...")
time.sleep(3)
macstr = str(mac)
f = open("id.txt","w")
f.write(macstr)
f.close()
print("Everything done! This window will close itself in 5 sec! Bye!")
time.sleep(5)