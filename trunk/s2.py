#!/usr/bin/python
import socket

class snppsocket:
	def __init__(self,sock=None):
		if sock is None:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.sock.settimeout(5)
		else:
			self.sock = sock

	def __chat(self,dataout,response):
		if dataout:
			self.sock.send(dataout)
		datain = ''
		while 1:
			try:
				chunk = self.sock.recv(1)
				if chunk == '':
					break
			except:
				break
			datain = datain + chunk
		print "Chat Data: [%s]" %(datain)
		print "Looking: [%s]" %(datain[0:3])
		if str(datain[0:3]) == str(response): return True


	def sendmessage(self,host,port,message):
		self.sock.connect((host, port))


		#if not self.__chat(None, 220): print "Connection returned failure"
		#if not self.__chat("PAGE 3606901574\n", 250) == None: print "Pager number not accepted"

		return "Sent..."

s = snppsocket()
print s.sendmessage("67.115.154.70",444,"test message")



#connect, 220, "PAGE nnnnnnnnnn", 250, "MESS message", 250, "SEND", 250
#"QUIT", 221


