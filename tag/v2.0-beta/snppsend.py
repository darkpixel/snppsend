#!/usr/bin/python

# snppsend v2.00a: a simple program to deliver messages to text pagers
#                  using the SNPP protocol.
# Copyright (C) 2004 - 2006 Aaron C. de Bruyn <code@darkpixel.com>
# 
# This app is GPL.  I know it says I have to past a bunch of shit
# in the header here--but I really don't want the first 100 lines
# of my app to be GPL shit.  Just know that it's GPL and you're
# bound by it.  Good times.
#
# The latest version of snppsend should always be available
# on my website at http://www.darkpixel.com/
# 
# Special thanks to...
# darklordmaven for hammering away at my scripts, looking
#   for bugs, moral support, and games of Halo 2.
# jeek in #pound-perl.pm on EFNet for pointing out my perl noobness
# Steve Kaylor and Brandon Zehm - their original script that inspired this app

import asynchat, asyncore, socket, ConfigParser, os, sys, getopt
from asynchat import async_chat

debugflag = 0
def debug(*args):
	global debugflag
	if debugflag != 0:
		print "debug: ", " ".join(args)

def debugon():
	global debugflag
	print "Setting debugflag to 1"
	debugflag = 1

class SNPPServerException(Exception):
	def __init__(self,value):
		self.value = value

	def __str__(self):
		return repr(self.value)

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
	def __init__(self):
		async_chat.__init__(self)
		self.create_socket(socket.AF_INET,socket.SOCK_STREAM)
		self.address = ""
		self.pager = ""
		self.message = ""
	
		self.chan = SNPPChannel()
		self.collect_incoming_data = self.chan.collect

		async_chat.set_terminator(self,"\r\n")

	def sendpage(self):
		if len(self.address) == 0:
			raise ValueError, "Server address not set"
		else:
			if len(self.pager) == 0:
				raise ValueError, "Pager number not set"
			else:
				if len(self.message) == 0:
					raise ValueError, "Message not set"
				else:
					self.connect(self.address)

	def set_message(self,message):
		self.message = message

	def get_message(self):
		return self.message

	def set_pager(self,pager):
		self.pager = pager

	def get_pager(self):
		return self.pager

	def set_server_address(self,address):
		self.address = address

	def get_server_address(self):
		return self.address

	def __send_command(self,command):
		debug("__send_command: " + command)
		self.push(command + "\r\n")

	def found_terminator(self):
		tmp = self.chan.get_data()
		debug("Server Response: " + tmp)

		if tmp.startswith("220") and self.chan.get_state() == 1:
			pass
		elif tmp.startswith("250") and self.chan.get_state() != 1:
			pass
		elif self.chan.get_state() == 0:
			pass
		else:
			raise SNPPServerException, "Server responded with: " + tmp

		debug(str(self.chan.get_state()))
		if self.chan.get_state() == 1:
			self.__send_command("PAGE " + self.pager)
			self.chan.set_state(2)
		elif self.chan.get_state() == 2:
			self.__send_command("MESS " + self.message)
			self.chan.set_state(3)
		elif self.chan.get_state() == 3:
			self.__send_command("SEND")
			self.chan.set_state(4)
		elif self.chan.get_state() == 4:
			self.__send_command("QUIT")
			self.chan.set_state(0)
		elif self.chan.get_state() == 0:
			pass
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


def main(argv):
	cfg = ConfigParser.RawConfigParser()
	cfgfile = "/etc/snpp/snppsend.ini"

	if len(argv) < 2:
		usage()


	try:                                
		opts = getopt.getopt(argv[1:], "Vhdc:", ["ver", "version", "help", "config=", "debug"])
		for opt, param in opts[0]:
			if opt in ("-h", "--help"):
				usage()
			elif opt in ("-c", "--config"):
				debug("Using config file: " + param)
				cfgfile = param
			elif opt in ("-V", "--ver", "--version"):
				print("snppsend v2.0a")
			elif opt in ("-d", "--debug"):
				debugon()

	except getopt.GetoptError:
        	debug ("usage()")
		sys.exit(2)

	try:
		cfg.readfp(open(cfgfile,"r"))
	except IOError:
		print("Unable to locate config file [" + cfgfile + "]")
		sys.exit()

	message = ""

	for recv in opts[1]:
		try:
			receiver = cfg.get("Receivers", recv).split(",")
		except ConfigParser.NoOptionError:
			print("Invalid pager [" + recv + "]")
			continue

		try:
			provider = cfg.get("Providers", receiver[0]).split(",")
		except ConfigParser.NoOptionError:
			print("Invalid provider [" + receiver[0] + "] for pager [" + recv + "]")
			continue

		client = SNPP()
		client.set_server_address((provider[0],int(provider[1])))
		if len(message) == 0:
			try:
				message = sys.stdin.read()
			except KeyboardInterrupt:
				sys.exit()
		client.set_message(message)
		client.set_pager(receiver[1])
		print("Paging [" + recv + "]")
		client.sendpage()

	try:
		asyncore.loop()
	except KeyboardInterrupt:
		debug("Windows would probably just coredump here...")

def usage():
	print("snppsend.py (-c <file> | --config=<file>) (-d | --debug) receiver")

if __name__ == "__main__":
        main(sys.argv)

