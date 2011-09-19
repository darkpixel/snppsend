#!/usr/bin/python
_VER = 'v2.1'

# snppsend v2.1: a simple program to deliver messages to text pagers
#                using the SNPP protocol.
# Copyright (c) 2004-2011 Aaron C. de Bruyn <aaron@heyaaron.com>
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

import asynchat, asyncore, socket, ConfigParser, os, sys, getopt, urllib2
from asynchat import async_chat

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
		# SNPP Protocol States
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
		self.push(command + '\r\n')

	def found_terminator(self):
		tmp = self.chan.get_data()
		if tmp.startswith('220') and self.chan.get_state() == 1:
			pass
		elif tmp.startswith('250') and self.chan.get_state() != 1:
			pass
		elif self.chan.get_state() == 0:
			pass
		else:
			raise SNPPServerException, 'Server response unexpected: ' + tmp

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
			raise ValueError('Invalid state should never occur (%s)' %(self.chan.get_state()))

	def handle_connect(self):
		self.chan.set_state(1)
	
	def handle_close(self):
		self.close()
		self.chan.set_state(0)


def main(argv):
	cfg = ConfigParser.RawConfigParser()
        cfgdir = '/etc/snppsend.d'

	if len(argv) < 2:
		usage()
	try:                                
		opts = getopt.getopt(argv[1:], 'Vhcp:', ['ver', 'version', 'help', 'config=', 'providers'])
		for opt, param in opts[0]:
			if opt in ('-h', '--help'):
				usage()
			if opt in ('-p', '--providers'):
				print 'Providers:'
				print os.listdir(cfgdir)
				sys.exit()
			elif opt in ('-c', '--config'):
				cfgdir = param
			elif opt in ('-V', '--ver', '--version'):
				print('snppsend %s' %(_VER))

	except getopt.GetoptError:
		print 'Bad options!'
		sys.exit(2)

	message = ''

	for recv in opts[1]:
		try:
			receiverfh = open('%s/%s.receiver' %(cfgdir, recv), 'r')
			rlines = receiverfh.readlines()
			receiver_name = recv.strip()
                        receiver_number = rlines[2].strip()
			try:
				providerfh = open('%s/%s.provider' %(cfgdir, rlines[1].strip()))
				plines = providerfh.readlines()
				provider_host = plines[1].strip()
				provider_port = plines[2].strip() or 444
				provider_maxchars = plines[3].strip()
			except IOError:
				print 'Unable to locate provider (%s) for receiver %s' %(rlines[1].strip(), recv)
		except IOError:
			print 'Unable to locate receiver: %s' %(recv)

		client = SNPP()
		client.set_server_address((provider_host,int(provider_port)))
		if len(message) == 0:
			try:
				message = sys.stdin.read()
			except KeyboardInterrupt:
				sys.exit()
		client.set_message(message)
		client.set_pager(receiver_number)
		print('Paging [%s] at %s using server %s port %s' %(receiver_name, receiver_number, provider_host, provider_port))
		client.sendpage()

	try:
		asyncore.loop()
	except KeyboardInterrupt:
		sys.exit(0)

def usage():
	print('snppsend.py (-c <file> | --config=<file>) receiver')

if __name__ == '__main__':
        main(sys.argv)

