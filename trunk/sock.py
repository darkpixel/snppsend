#!/usr/bin/python

import socket


def socketchat(data, retcode):
	sbuf = ""
	sck.send(data)
	while (1):
		stmp = sck.recv(1)
		if ("\n" in stmp):
			break
		else:
			sbuf = sbuf + stmp
		
	if retcode in sbuf :
		print "Valid code returned"
		print sbuf
	else:
		print "Invalid code returned"
		print sbuf


sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sck.settimeout(5)
sck.connect(("67.115.154.70", 444))
socketchat("", "220")
socketchat('PAGE 3606901574\n', "250")

sck.shutdown(2)
sck.close



#connect, 220, "PAGE nnnnnnnnnn", 250, "MESS message", 250, "SEND", 250
#"QUIT", 221


