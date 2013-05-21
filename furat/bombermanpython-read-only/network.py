import socket
import sys
import select

class _NetworkModule():
	"""
		Holds the basic send and recv functions for sending over a socket
	"""
	def __init__(self):
		self.status = False
		self.error = ["", ""]
		self.sv_ip = '127.0.0.1'
		self.sv_port = 25000

	"""
		Attempts a connection and in case of failure sets
		the error accordingly
	"""
	def connect(self):
		self.status = True
		self.error = ["", ""]

		try:
			self.gate = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		except socket.error, msg:
			self.error = msg
			self.status = False
			self._printError()
			return

		try:
			self.gate.connect((self.sv_ip, self.sv_port))

		except socket.error, msg:
			print "eroare"
			self.error = msg
			self.status = False
			self._printError()

	"""
		Dummy function for printing the errors we currently have
	"""
	def _printError(self):
		print 'Failed to create socket.'
		print 'Error code: ' + str(self.error[0])
		print 'Error message: ' + str(self.error[1])

	"""
		Function that returns a tuple containing error type
		error message; Used for printing popup messages
	"""
	def getError(self):
		return ('Error ' + str(self.error[0]), str(self.error[1]))

	"""
		Returns the connection status
	"""
	def isConnected(self):
		return self.status

	"""
		Normal send function
	"""
	def send(self, message):
		print("hello")
		self.gate.sendall(message + "\n")

	"""
		Dummy recv function // We should have a select here //
	"""
	def recv(self):
		reply = ""
		try:
			reply = self.gate.recv(1024)

		except socket.gaierror:
			print "cannot recv"
			return ""

		print reply
		return reply

	def recvSelect(self):
		input = [self.gate]
		timeout = 0.001
		message = ""

		inReady, outReady, exReady = select.select(input, [], [], timeout)

		if inReady != []:
			message = self.recv()

		return message


"""
This whole class is a singleton
"""
_inst = _NetworkModule()

getError = _inst.getError
isConnected = _inst.isConnected
connect = _inst.connect
send = _inst.send
recv = _inst.recv
mySelect = _inst.recvSelect
