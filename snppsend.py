#!/usr/bin/python

# snppsend v1.8: a simple program to deliver messages to text pagers
#                  using the SNPP protocol.
# Copyright (C) 2004 - 2009 Aaron C. de Bruyn <aaron@heyaaron.com>
# 
# This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import asynchat, asyncore, socket, ConfigParser, os, sys, getopt
from asynchat import async_chat

_VER = 'v1.8'

debugflag = 0

def debug(*args):
	global debugflag
	if debugflag != 0:
		print 'debug: ', ' '.join(args)

def debugon():
	global debugflag
	print 'Setting debugflag to 1'
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
		tmp = ''.join(self.data)
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
		self.address = ''
		self.pager = ''
		self.message = ''
	
		self.chan = SNPPChannel()
		self.collect_incoming_data = self.chan.collect

		async_chat.set_terminator(self,'\r\n')

	def sendpage(self):
		if len(self.address) == 0:
			raise ValueError, 'Server address not set'
		else:
			if len(self.pager) == 0:
				raise ValueError, 'Pager number not set'
			else:
				if len(self.message) == 0:
					raise ValueError, 'Message not set'
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
		debug('__send_command: ' + command)
		self.push(command + '\r\n')

	def found_terminator(self):
		tmp = self.chan.get_data()
		debug('Server Response: ' + tmp)

		if tmp.startswith('220') and self.chan.get_state() == 1:
			pass
		elif tmp.startswith('250') and self.chan.get_state() != 1:
			pass
		elif self.chan.get_state() == 0:
			pass
		else:
			raise SNPPServerException, 'Server response unexpected: ' + tmp

		debug(str(self.chan.get_state()))
		if self.chan.get_state() == 1:
			self.__send_command('PAGE ' + self.pager)
			self.chan.set_state(2)
		elif self.chan.get_state() == 2:
			self.__send_command('MESS ' + self.message)
			self.chan.set_state(3)
		elif self.chan.get_state() == 3:
			self.__send_command('SEND')
			self.chan.set_state(4)
		elif self.chan.get_state() == 4:
			self.__send_command('QUIT')
			self.chan.set_state(0)
		elif self.chan.get_state() == 0:
			pass
		else:
			debug('Unknown SNPP state!')
			sys.exit('Oops:  I ended up with an unknown state (%s)' %(self.chan.get_state()))

	def handle_connect(self):
		debug('socket connected')
		self.chan.set_state(1)
	
	def handle_close(self):
		debug('socket closed')
		self.close()
		self.chan.set_state(0)


def main(argv):
	cfg = ConfigParser.RawConfigParser()
	cfgfile = '/etc/snppsend.conf'

	if len(argv) < 2:
		usage()

	try:                                
		opts = getopt.getopt(argv[1:], 'Vhdc:', ['ver', 'version', 'help', 'config=', 'debug'])
		for opt, param in opts[0]:
			if opt in ('-h', '--help'):
				usage()
			elif opt in ('-c', '--config'):
				debug('Using config file: ' + param)
				cfgfile = param
			elif opt in ('-V', '--ver', '--version'):
				print('snppsend %s' %(_VER))
			elif opt in ('-d', '--debug'):
				debugon()

	except getopt.GetoptError:
        	debug ('usage()')
		sys.exit(2)

	try:
		cfg.readfp(open(cfgfile,'r'))
	except IOError:
		print('Unable to locate config file [' + cfgfile + ']')
		sys.exit()

	message = ''

	for recv in opts[1]:
		try:
			receiver = cfg.get('Receivers', recv).split(',')
		except ConfigParser.NoOptionError:
			print('Invalid pager [' + recv + ']')
			continue

		try:
			provider = cfg.get('Providers', receiver[0]).split(',')
		except ConfigParser.NoOptionError:
			print('Invalid provider [' + receiver[0] + '] for pager [' + recv + ']')
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
		print('Paging [' + recv + ']')
		client.sendpage()

	try:
		asyncore.loop()
	except KeyboardInterrupt:
		debug('Windows would probably just coredump here...')

def usage():
	print('snppsend.py (-c <file> | --config=<file>) (-d | --debug) receiver')

if __name__ == '__main__':
        main(sys.argv)

