#!/usr/bin/python3
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
# -*- coding: utf-8 -*-
import sqlite3
import os


def create():
    if not os.path.isfile("freemind.db"):
        connection = sqlite3.connect("freemind.db")
        cursor = connection.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS errorlog(
                          id INTEGER PRIMARY KEY,
                          error INTEGER,
                          date TEXT,
                          time TEXT);""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS updatelog(
                          id INTEGER PRIMARY KEY,
                          date TEXT,
                          time TEXT,
                          update INTEGER);""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS backupready(
                          id INTEGER PRIMARY KEY,
                          ready INTEGER);""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS backuplog(
                          id INTEGER PRIMARY KEY,
                          date TEXT,
                          time TEXT,
                          error INTEGER);""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS memory(
                          id INTEGER PRIMARY KEY,
                          total TEXT,
                          free TEXT,
                          drive INTEGER);""")
        connection.commit()
        connection.close()
