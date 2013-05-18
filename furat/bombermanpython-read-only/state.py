class _State():
	def __init__(self):
		self.logged_in = False
		self.in_game = False

_inst = _State()
logged_in = _inst.logged_in
in_game = _inst.in_game
