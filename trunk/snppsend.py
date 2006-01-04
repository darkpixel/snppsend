#!/usr/bin/python

# snppsend v2.00a: a simple program to deliver messages to text pagers
#                 using the SNPP protocol.
# Copyright (C) 2004 - 2005 Aaron C. de Bruyn <code@darkpixel.com>
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
# The latest version of snppsend should always be available
# on my website at http://www.darkpixel.com/
# 
# Some shout-outs
# darklordmaven for hammering away at my scripts, looking
#   for bugs, moral support, and games of Halo 2.
# jeek in #pound-perl.pm on EFNet for his words of wisdom.
#   Though he spoke not more than ten words, he pointed
#   out my total perl noobness.
# Steve Kaylor and Brandon Zehm - their original script
#   inspired this program and I borrowed a chunk of
#   their socket and snpp server communication code for
#   the original version of snppsend which was written
#   in perl.

import MySQLdb

db = MySQLdb.connect(host="localhost", user="tools", passwd="uttoolspass101!",db="uberhost")
cursor = db.cursor()
cursor.execute("SELECT * FROM Accounts")
result = cursor.fetchall()
for records in result:
	print records[0], "-->", records[1]

