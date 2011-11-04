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
from tempfile import mkstemp
from shutil import move
from os import remove, close, path

def generateIds(filename, i):
    # Create temp file
    fh, temp_path = mkstemp()
    new_file = open(temp_path,'w')
    old_file = open(filename)
    for line in old_file:
        if line.find("@Message(v") != -1:
            new_file.write(line.replace("@Message(v", "@Message(id = " + str(i) + ", v"))
            i += 1
        else:
            new_file.write(line)
    # Close temp file
    new_file.close()
    close(fh)
    old_file.close()
    # Remove original file
    remove(filename)
    # Move new file
    move(temp_path, filename)

parser = argparse.ArgumentParser(description="Generate message id's")
parser.add_argument("-f", "--file", metavar="FILE", type=str, dest="filename", help="The file to generate the id's for.")
parser.add_argument("-id", metavar="N", type=int, dest="i", help="The starting id.")

args = parser.parse_args()

if not path.exists(args.filename):
    raise Exception("File '" + args.filename + "' not found.")

generateIds(args.filename, args.i)


