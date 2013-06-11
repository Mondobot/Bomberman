import pygame
from pgu import gui
import state
import network
from time import time
import protocol


class GameInfo(gui.Table):
	def __init__(self, parent, gameID, **params):
		gui.Table.__init__(self, **params)

		self.width = params.get("width", 0)
		self.height = params.get("height", 0)
		self.cls = params.get("cls", "h3")
		self.sel_txt = params.get("sel", "")

		self._timestamp = 0
		self._parent = parent
		self._selected = False

		self.gameID = gameID
		self.max_players = 4

		self.labels = []
		self._fill()

	def enableSelect(self):
		self.connect(gui.CLICK, self.click)

	def doSelect(self):
		self._selected = True
		self.sel.set_text("X")

		if self._parent.selection:
			self._parent.selection.doDeselect()
		self._parent.selection = self

	def doDeselect(self):
		self._selected = False
		self.sel.set_text("")

	def click(self, _event, _widget, _code):
		timestamp = time()

		if timestamp - self._timestamp < 0.25:
			self.doSelect()
			self._parent.join()
			print "double"

		else:
			self.doSelect()
			print "single"

		self._timestamp = timestamp

	def _fill(self):
		self.bg = pygame.image.load("images/abstract_0097.jpg")

		self.sel = gui.Label(self.sel_txt, cls = self.cls,
							width = int(self.width / 10),
							height = self.height)
		self.td(self.sel, width = int(self.width / 10),
					height = self.height)

		for i in range(0, 3):
			label = gui.Label("", cls = self.cls,
							width = int(self.width / 10) * 3,
							height = self.height,
							colspan = 1)
			self.labels += [label]

			self.td(label, width = int(self.width / 10) * 3,
						height = self.height)

	def setLabelAt(self, index, text):
		if index >= 3:
			return

		self.labels[index].set_text(text)

class GameSelect(gui.App):
	def __init__(self, screen, **params):
		gui.App.__init__(self)

		self.connect(gui.QUIT, self.quit, None)

		self.games = []
		self.selection = None
		self.count = 0

		self.width = params.get("width", 0)
		self.height = params.get("height", 0)
		self.entry_table = gui.Table(width = int(self.width / 4) * 3)

		self._fill()

	def create(self):
		ok = protocol.sendMessage(TYPE = protocol.CREATE)

		if ok:
			state.in_game_select = False
			state.in_game_lobby = True
			state.game_owner = True

		print "game_ownerrr ", state.game_owner

	def join(self):
		if self.selection:
			print "join"
			ok = protocol.sendMessage(TYPE = protocol.JOIN,
									ID = self.selection.gameID)

			if ok:
				state.in_game_select = False
				state.in_game_lobby = True
				state.game_owner = False

	def addGame(self, game):
		print "Am adaugat unul"
		game_id, name, players = game

		entry_h = int(self.height * 0.05)
		entry_w = int(self.width / 4) * 3

		entry = GameInfo(self, game_id, width = entry_w, height = entry_h)
		entry.setLabelAt(0, name)
		
		if game_id != -3:
			entry.setLabelAt(2, str(players) + " / 4")
			entry.enableSelect()

		self.entry_table.tr()
		self.entry_table.td(entry, width = entry_w, height = entry_h)
		self.games += [entry]
		self.entry_table.tr()

	def updateGames(self, games):
		if not self.ok:
			return

		my_games = self.games[:]
		new = []

		for entry in games:
			found = False
			id, name, players = entry
			
			for my_entry in my_games:
				if id == my_entry.gameID:
					my_entry.setLabelAt(2, str(players) + " / 4")
					new += [my_entry]
					found = True
					break
			
			if not found:
				self.addGame(entry)

		for x in my_games:
			if x not in new:
				self.entry_table.remove(x)
				del self.games[self.games.index(x)]

		self.entry_table.chsize()

	def _fill_splash(self, w, h):
		button_h = int(h * 0.05)
		table = gui.Table(width = w, height = h)

		img = gui.Image("images/Bomberman_logo.png", width = w,
						height = int(w / 2))
		table.td(img, width = w, height = int(w /2))

		table.tr()
		table.td(gui.Spacer(w, button_h * 16 - int(w / 2)))

		table.tr()
		create_btn = gui.Button("Create game")
		create_btn.connect(gui.CLICK, self.create)
		table.td(create_btn, width = w, height = button_h)

		table.tr()
		join_btn = gui.Button("Join game")
		join_btn.connect(gui.CLICK, self.join)
		table.td(join_btn, width = w, height = button_h)

		table.tr()
		table.td(gui.Spacer(w, button_h * 2))

		return table

	def _fill_games_list(self, w, h):
		table = gui.Table(width = w, height = h)

		entry_h = int(h * 0.05)

		table.tr()
		title =  gui.Label("Active games", cls = "h1")
		table.td(title, width = w, height = entry_h)

		table.tr()
		header = GameInfo(self, -1, width = w, height = entry_h,
						cls = "h2", sel = "Sel")
		header.setLabelAt(0, "Game owner")
		header.setLabelAt(2, "Players")
		table.td(header, width = w, height = entry_h)

		table.tr()
		self.cont = gui.ScrollArea(self.entry_table, width = w,
							height = entry_h * 18,
							hscrollbar = False)

		st = {'padding_left':6, 'padding_bottom':6}
		table.td(self.cont, style = st, width = w, 
				height = entry_h * 18)

		return table

	def _fill(self):
		self.bg = pygame.image.load("images/abstract_0097.jpg")
		self.bg_rect = self.bg.get_rect()

		table = gui.Table(width = self.width, height = self.height)

		lobby = self._fill_games_list(int(self.width / 4) * 3, self.height)
		splash = self._fill_splash(int(self.width / 4), self.height)
		
		table.td(lobby, width = int(self.width / 4) * 3, height = self.height)
		table.td(splash, width = int(self.width / 4), height = self.height)
		self.init(table, self.screen)
		print "acum e ok"
		self.ok = True

	def paint(self, s):
		self.screen.blit(self.bg, self.bg_rect)
		super(GameSelect, self).paint(s)
