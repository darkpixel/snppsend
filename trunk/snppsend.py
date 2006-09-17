#!/usr/bin/python

# snppsend v2.00a: a simple program to deliver messages to text pagers
#                  using the SNPP protocol.
# Copyright (C) 2004 - 2006 Aaron C. de Bruyn <code@darkpixel.com>
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
# Special thanks to...
# darklordmaven for hammering away at my scripts, looking
#   for bugs, moral support, and games of Halo 2.
# jeek in #pound-perl.pm on EFNet for pointing out my perl noobness
# Steve Kaylor and Brandon Zehm - their original script that inspired this app

import asynchat, asyncore, socket, sys, ConfigParser
from asynchat import async_chat


def debug(*args):
    print "debug: ", " ".join(args)

class SNPPChannel:
	def __init__(self):
		self.data= []
		self.state = 0

	def get_data(self):
		tmp = "".join(self.data)
		del self.data[:]
		return tmp

	def collect(self,data):
		self.data.append(data)

	def set_state(self,newstate):
		self.state = newstate
		# 0 - Initialized
		# 1 - Connected (Send Pager ID)
		# 2 - Pager Accepted (Send message)
		# 3 - Message Accepted (Quit)
		# 4 = Message Sent
		# 5 = Quitting

	def get_state(self):
		return self.state
	

class SNPP(async_chat):
	def __init__(self,addr, pager, message):
		async_chat.__init__(self)
		self.remote = addr
		self.create_socket(socket.AF_INET,socket.SOCK_STREAM)
		self.connect(addr)
		self.pager = pager
		self.message = message
	
		self.chan = SNPPChannel()
		self.collect_incoming_data = self.chan.collect

		async_chat.set_terminator(self,"\r\n")

	def send_command(self,command):
		debug("send_command: " + command)
		self.push(command + "\r\n")

	def found_terminator(self):
		tmp = self.chan.get_data()
		debug("found_terminator: " + tmp)

		if tmp.startswith("220"):
			debug("IT STARTS WITH 220!  WOOT!")

		debug(str(self.chan.get_state()))
		if self.chan.get_state() == 1:
			self.send_command("PAGE " + self.pager)
			self.chan.set_state(2)
		elif self.chan.get_state() == 2:
			self.send_command("MESS Test message...")
			self.chan.set_state(3)
		elif self.chan.get_state() == 3:
			self.send_command("SEND")
			self.chan.set_state(4)
		elif self.chan.get_state() == 4:
			self.send_command("QUIT")
		else:
			debug("Unknown SNPP state!")
			sys.exit("Invalid socket state")

	def handle_connect(self):
		debug("socket connected")
		self.chan.set_state(1)
	
	def handle_close(self):
		debug("socket closed")
		self.close()
		self.chan.set_state(0)
	


#cfg = RawConfigParser
#cfg.add_section("Providers")


client = SNPP(("67.115.154.70", 444), "3600000000", "Test message...")

try:
	asyncore.loop()
except KeyboardInterrupt:
	debug("Windows would probably just coredump here...")

