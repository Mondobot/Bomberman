import network

NONE = "-1"
LOGIN = "0"
CREATE = "1"
JOIN = "2"
START = "3"
MOVE = "4"
DROP = "5"
MAP = 6

class _ProtocolsModule():
	def __init__(self):
		pass

	def sendMessage(self, **params):
		msg_type = params.get("TYPE", -1)

		if msg_type == LOGIN:
			return self._handleLogin(**params)

		elif msg_type == START:
			return self._sendStart()

	def recvMessage(self, world):
		if not network.isConnected():
			network.connect()

		if not network.isConnected():
			return ""

		message = network.mySelect()
		
		if message == "":
			return

		msg_type = int(message[0])

		if msg_type == MAP:
			self._handleMapRecv(message[1:], world)


	def _handleLogin(self, **params):
		user = params.get("USER")
		password = params.get("PASS")
		message = LOGIN + " " + user + " " + password

		# Send the credentials
		network.send(message)

		ans = network.recv()
		if ans == "ok":
			return True

		return False


	def _handleMapRecv(self, codedMap, world):
		head = 0

		# Read the map
		height = int(codedMap[head])
		width = int(codedMap[head + 1])

		head += 2
		map = map(int, codedMap[head : head + height * width])

		head += height * width
		client_id = int(codedMap[head])
		no_clients = int(codedMap[head + 1])

		# Populate the clients
		head += 2
		aux = map(int, codedMap[head : head + no_clients * 2])
		players_pos = []

		for i in range(0, len(players_pos), 2):
			players_pos += [(aux[i], aux[i + 1])]
		world.setPLayers(client_id, players_pos)

		# Populate the bombs
		head += no_clinets * 2
		no_bombs == int(codedMap[head])

		world.clearBombs()
		head += 1
		bombs_pos = []
		aux = map(int, codedMap[head : head + no_bombs * 2])
		
		for i in range(0, no_bombs * 2, 2):
			world.place_bomb((aux[i], aux[i + 1]), 1, 20)

		head += no_bombs * 2
		no_expl = codedMap[head]
		#if no_expl > 0:


		head += 1
		aux = map(int, codedMap[head : head + no_expl * 3])
		for i in range(0, no_expl * 3, 3):
			world.place_bomb((aux[i], aux[i + 1]), 3, aux[i + 2])
			world.expl_bomb((aux[i], aux[i + 1]), aux[i + 2])

	def _sendStart(self):
		network.send(START)

_inst = _ProtocolsModule()

sendMessage = _inst.sendMessage
recvMessage = _inst.recvMessage
