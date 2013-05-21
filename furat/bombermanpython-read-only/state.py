class _State():
	def __init__(self):
		self.logged_in = False
		self.in_game = False
		self.in_game_select = False
		self.in_game_lobby = False
		self.ntw_owner = None

_inst = _State()
logged_in = _inst.logged_in
in_game = _inst.in_game
in_game_select = _inst.in_game_select
in_game_lobby = _inst.in_game_lobby
