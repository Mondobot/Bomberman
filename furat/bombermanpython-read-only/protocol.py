import network
NONE = -1
LOGIN = 0
CREATE = 1
JOIN = 2
START = 3
MOVE = 4
DROP = 5

class _ProtocolsModule():
	def __init__(self):
		pass

	def sendMessage(self, **params):
		msg_type = params.get(msg_type, -1)

		if msg_type == LOGIN:
			return self._handleLogin(params)

	def _handleLogin(self, **params):
		user = params.get("USER")
		password = params.get("PASS")
		message = LOGIN + " " + user + " " + password

		# Send the credentials
		network.send(messge)

		ans = network.recv()
		if recv == "ok":
			return True

		return False

_inst = _ProtocolsModule()

sendMsg = _inst.sendMessage
