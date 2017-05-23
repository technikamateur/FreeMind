#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
FreeMind is a composition of software and config files. It will help you to manage your Linux fileserver.
Copyright (C) 2017  Daniel Körsten aka TechnikAmateur

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import sys
import libary


# 1=OS-Update; 2=FM-Update; 3=Backup-done; 4=Do-Backup?
if sys.argv[1] < 4:
    libary.create()
    libary.insert_actionlog(2, sys.argv[1])
else: # Do Backup?
    pass
print(result)
