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

def processFile(file):
    current = open(file)
    lines = []
    for line in current:
        trimmedLine = line.strip()
        if trimmedLine.startswith("//") == False and trimmedLine.startswith("*") == False:
            if trimmedLine.find("throw new") != -1 and search('"[^"\\\r\n]*(?:\\.[^"\\\r\n]*)*"', trimmedLine) != None:
                lines.append(trimmedLine)
            if trimmedLine.startswith("@Message") == False and search('"[^"\\\r\n]*\w\s.*(?:\\.[^"\\\r\n]*)*"', trimmedLine) != None:
                lines.append(trimmedLine)
    if len(lines) > 0:
        print(str(file) + ":")
        for line in lines:
            print("    " + line)
            print("")

def processDir(dir):
    files = listdir(dir)
    for file in files:
        file_path = path.join(dir, file)
        if path.isfile(file_path) & file_path.endswith(".java"):
            processFile(file_path)
        elif path.isdir(file_path):
            processDir(file_path)

parser = argparse.ArgumentParser(description="Check messages")
parser.add_argument("-f", "--file", metavar="FILE", type=str, dest="filename", help="The file or directory to scan messages for.")

args = parser.parse_args()

if not path.exists(args.filename):
    raise Exception("File '" + args.filename + "' not found.")


#filename = "/home/jperkins/projects/jboss-as/controller/src/main/java"
#filename = "/home/jperkins/projects/jboss-as/controller/src/main/java/org/jboss/as/controller/parsing/CommonXml.java"
if path.isdir(args.filename):
    processDir(args.filename)
elif path.isfile(args.filename):
    processFile(args.filename)