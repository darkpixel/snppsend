#!/usr/bin/python

import asyncore
import socket

class snpp_client(asyncore.dispatcher):
	def __init__(self, host, port):
		asyncore.dispatcher.__init__(self)
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connect((host, port))
	
	def handle_connect(self):
		pass

	def handle_read(self):
		data = self.recv(8192)
		print data
	
	def writable(self):
		return (len(self.buffer) > 0)

	def handle_write(self):
		sent = self.send(self.buffer)
		self.buffer = self.buffer[sent:]

sk = socket.socket()
sc = snpp_client(sk, "67.115.154.70", "444")


#connect, 220, "PAGE nnnnnnnnnn", 250, "MESS message", 250, "SEND", 250
#"QUIT", 221


