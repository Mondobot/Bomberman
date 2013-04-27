#! /usr/bin/env python

import socket
import sys

try:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

except socket.error, msg:
	print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
	sys.exit()

print "Socket created"

try:
	remote_ip = socket.gethostbyname( 'www.google.com' )

except socket.gaierror:
	print "Could not resolve. Exiting"
	sys.exit()

print "Ip addr of www.google.com " + 'is ' + remote_ip

hammer_ip = '192.168.15.182'

s.connect((hammer_ip, 25000))
while 1:
	s.sendall("muie putina " + sys.argv[1] + "\n")

	try:
		reply = s.recv(4096)
	
	except socket.gaierror:
		print "cannot recv"
		sys.exit()

	print reply
