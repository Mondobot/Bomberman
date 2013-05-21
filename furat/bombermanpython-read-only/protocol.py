import network
import state
import game_select
import world
NONE = "-1"
LOGIN = "0"
CREATE = "1"
JOIN = "2"
START = "3"
MOVE = "4"
DROP = "5"
MAP = "6"
GAMES_LIST = "7"

class _ProtocolsModule():

	def __init__(self):
		pass

	def sendMessage(self, **params):
		msg_type = params.get("TYPE", -1)

		if msg_type == LOGIN:
			return self._handleLogin(**params)

		elif msg_type == START:
			self._sendStart()

		elif msg_type == CREATE:
			return self._sendCreate()

		elif msg_type == JOIN:
			game_id = params.get("ID", 0)
			return self._sendJoin(game_id)

		elif msg_type == MOVE:
			new_dir = params.get("DIR", 0)
			self._sendMove(new_dir)

		elif msg_type == DROP:
			self._sendDrop()

		else:
			print "ce plm de mesaj e " + msg_type

	def recvMessage(self, world, lobby):
		if not network.isConnected():
			network.connect()

		if not network.isConnected():
			return ""

		message = network.mySelect()

		if message == "":
			return

		msg_type = message[0]

		if msg_type == MAP:
			self._handleMapRecv(message[1:], world)

		elif msg_type == START:
			state.in_game = True

		elif msg_type == GAMES_LIST:
			self._handleGamesList(message[1:], lobby)

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
		height = ord(codedMap[head])
		width = ord(codedMap[head + 1])

		head += 2
		map_ceva = map(ord, codedMap[head : head + height * width])
		world.setMap(map_ceva, width, height)

		head += height * width
		client_id = ord(codedMap[head])
		no_clients = ord(codedMap[head + 1])

		# Populate the clients
		head += 2
		aux = map(ord, codedMap[head : head + no_clients * 2])
		players_pos = []

		for i in range(0, no_clients * 2, 2):
			players_pos += [(aux[i], aux[i + 1])]

		world.setPlayers(client_id, players_pos)

		# Populate the bombs
		head += no_clients * 2
		no_bombs = ord(codedMap[head])

		world.clearBombs()
		head += 1
		bombs_pos = []
		aux = map(ord, codedMap[head : head + no_bombs * 2])

		for i in range(0, no_bombs * 2, 2):
			world.place_bomb((aux[i], aux[i + 1]), 1, 20)

		head += no_bombs * 2
		no_expl = ord(codedMap[head])

		head += 1

		aux = map(ord, codedMap[head : head + no_expl * 4 + 2])

		for i in range(0, no_expl * 4, 4):
			world.place_bomb((aux[i], aux[i + 1]), 3, aux[i + 3])
			index = world.getNoBombs()

			world.expl_bomb((aux[i], aux[i + 1]), aux[i + 3])

	def _handleGamesList(self, message, game_select):
		head = 0

		no_games = ord(message[head])
		head += 1

		games = []

		for i in range(0, no_games):
			id = ord(message[head])

			head += 1
			name_len = ord(message[head])

			head += 1
			game_name = message[head : head + name_len]

			head += name_len
			no_players = ord(message[head])

			games += [(id, game_name, no_players)]

			head += 1

		game_select.updateGames(games)

	def _sendStart(self):
		network.send(START)
		if not self._getAck(START):
			print "PLM, NU MERGE START"

		else:
			state.in_game = True

	def _sendCreate(self):
		network.send(CREATE)
		if not self._getAck(CREATE):
			print "PLM, NU MERGE CREAT"
			return False

		return True

	def _sendJoin(self, game_id):
		network.send(JOIN + str(game_id))
		if not self._getAck(JOIN):
			print "PLM, NU MERGE JOIN"
			return False

		return True

	def _getAck(self, msg_type):
		msg = network.recv()

		if msg == "":
			return False

		if msg != "OK " + msg_type:
			return False

		return True

	def _sendMove(self, direction):
		network.send(MOVE + direction)

	def _sendDrop(self):
		network.send(DROP)

_inst = _ProtocolsModule()

sendMessage = _inst.sendMessage
recvMessage = _inst.recvMessage
