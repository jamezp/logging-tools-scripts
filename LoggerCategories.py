#!/usr/bin/env python

# JBoss, Home of Professional Open Source.
# Copyright 2011, Red Hat, Inc., and individual contributors
# as indicated by the @author tags. See the copyright.txt file in the
# distribution for a full listing of individual contributors.
#
# This is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation; either version 2.1 of
# the License, or (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this software; if not, write to the Free
# Software Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA
# 02110-1301 USA, or see the FSF site: http://www.fsf.org.

__author__ = 'jperkins'

import argparse
from os import path, listdir
from re import search


def processFile(file, printFileName):
    current = open(file)
    lines = []
    for line in current:
        trimmedLine = line.strip()
        # Skip comments
        if trimmedLine.startswith("//") == False and trimmedLine.startswith("*") == False:
            if trimmedLine.find("Logger.getLogger") > -1:
                m = search('"[^"\\\r\n]*(?:\\.[^"\\\r\n]*)*"', trimmedLine)
                if m != None:
                    lines.append(m.group(0))
                m = search('\([^"\\\r\n]*(?:\\.[^"\\\r\n]*)*\.class\)', trimmedLine)
                if m != None:
                    lines.append(m.group(0))
    # Check to see if lines were found and print
    if len(lines) > 0:
        if printFileName:
            print(str(file) + ":")
            for line in lines:
                print("    " + line)
                print("")
        else:
            for line in lines:
                print(line)


def processDir(dir, printFileName):
    files = listdir(dir)
    for file in files:
        file_path = path.join(dir, file)
        if path.isfile(file_path) & file_path.endswith(".java"):
            processFile(file_path, printFileName)
        elif path.isdir(file_path):
            processDir(file_path, printFileName)

# Parse the incoming parameters
parser = argparse.ArgumentParser(description="List Logging Categories")
parser.add_argument("-f", "--file", metavar="FILE", type=str, dest="filename", help="The file or directory to scan for logging categories.")
parser.add_argument("-printFileName", type=bool, dest="printFileName", help="Print the file name with the category.", required=False, default=False)
args = parser.parse_args()

if not path.exists(args.filename):
    raise Exception("File '" + args.filename + "' not found.")

printFileName = args.printFileName

if path.isdir(args.filename):
    processDir(args.filename, printFileName)
elif path.isfile(args.filename):
    processFile(args.filename, printFileName)