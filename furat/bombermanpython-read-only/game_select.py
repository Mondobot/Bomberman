import pygame
from pgu import gui
import state
import network
from time import time

class GameInfo(gui.Container):
	def __init__(self, parent, gameID, **params):
		gui.Container.__init__(self)

		self.width = params.get("width", 0)
		self.height = params.get("height", 0)
		self._timestamp = 0
		self._parent = parent

		self.gameID = gameID
		self.max_players = 4

		self.labels = []

		self._fill()

	def enableSelect(self):
		self.connect(gui.CLICK, self.click)

	def click(self, _event, _widget, _code):
		timestamp = time()

		if timestamp - self._timestamp < 0.25:
#			self.parent.joinSelected()
			print "double"

		else:
#			self.parent.selectCurrent()
			print "single"

		self._timestamp = timestamp

	def setPlayers(self, no_players):
		self._no_players = no_players

	def _fill(self):
		table = gui.Table(width = self.width, height = self.height)

		for i in range(0, 3):
			label = gui.Label("")
			self.labels += [label]

			self.table.td(label, width = int(self.width / 3),
						height = self.height)

		self.add(table, 0, 0)

	def setLabelAt(self, index, text):
		if index >= 3:
			return

		self.labels[index].set_text(text)

class GameSelect(gui.App):
	def __init__(self, state, screen, **params):
		gui.App.__init__(self)

		self.connect(gui.QUIT, self.quit, None)


		self.width = params.get("width", 0)
		self.height = params.get("height", 0)

		self._fill()

		#t = GameInfo(self, width = 400, height = 200)
		#box = gui.ScrollArea(t, width = 200, height = 100)
		#self.run(box)

	def _create(self):
		print "create"

	def _join(self):
		print "join"

	def _fill_splash(self, w, h):

		button_h = int(h * 0.05)
		table = gui.Table(width = w, height = h)

		img = gui.Image("images/Bomberman_logo.png", width = w,
						height = int(w / 2))
		table.td(img, width = w, height = 2 * 4)

		table.tr()
		table.td(gui.Spacer(w, button_h * 16 - int(w / 2)))

		table.tr()
		create_btn = gui.Button("Create game")
		create_btn.connect(gui.CLICK, self._create)
		table.td(create_btn, width = w, height = button_h)

		table.tr()
		create_btn = gui.Button("Join game", )
		create_btn.connect(gui.CLICK, self._join)
		table.td(create_btn, width = w, height = button_h)

		table.tr()
		table.td(gui.Spacer(w, button_h * 2))

		return table

	def _fill_rest(self, w, h):
		return gui.Spacer(w, h)

	def _fill(self):
		self.bg = pygame.image.load("images/abstract_0097.jpg")
		self.bg_rect = self.bg.get_rect()

		table = gui.Table(width = self.width, height = self.height)

		lobby = self._fill_rest(int(self.width / 4) * 3, self.height)
		splash = self._fill_splash(int(self.width / 4), self.height)
		
		table.td(lobby, width = int(self.width / 4) * 3, height = self.height)
		table.td(splash, width = int(self.width / 4), height = self.height)

		self.run(table)

	def paint(self, s):
		self.screen.blit(self.bg, self.bg_rect)
		super(GameSelect, self).paint(s)


ceva = GameSelect(None, None, width = 800, height = 600)

