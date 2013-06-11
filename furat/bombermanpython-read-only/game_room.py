import pygame
from pgu import gui
import state
import network
import protocol

class GameRoom(gui.App):
	def __init__(self, screen, **params):
		gui.App.__init__(self)

		self.connect(gui.QUIT, self.quit, None)

		self.screen = screen
		self.width = params.get("width", 0)
		self.height = params.get("height", 0)

		self._fill()

	def startGame(self):
		ok = protocol.sendMessage(TYPE = protocol.START)
		print "am trimis start"

		if ok:
			state.in_game_lobby = False
			state.in_game = True

	def _fill_splash(self, w, h):
		button_h = int(h * 0.05)
		table = gui.Table(width = w, height = h)
		
		img = gui.Image("images/Bomberman_logo.png", width = w,
						height = int(w / 2))
		table.td(img, width = w, height = int(w /2))
		
		table.tr()
		table.td(gui.Spacer(w, button_h * 17 - int(w / 2)))
		
		table.tr()

		print "game owner :", state.game_owner

		if state.game_owner:
			self.start_btn = gui.Button("Start game")
			self.start_btn.connect(gui.CLICK, self.startGame)
			table.td(self.start_btn, width = w, height = button_h)

		else:
			table.td(gui.Spacer(w, button_h))

		table.tr()
		table.td(gui.Spacer(w, button_h * 2))

		self.table = table
		return table

	def _fill(self):
		self.bg = pygame.image.load("images/abstract_0097.jpg")
		self.bg_rect = self.bg.get_rect()

		table = gui.Table(width = self.width, height = self.height)

		#lobby = self._fill_games_list(int(self.width / 4) * 3, self.height)
		splash = self._fill_splash(int(self.width / 4), self.height)

		table.td(gui.Spacer(int(self.width / 4) * 3, self.height), width = int(self.width / 4) * 3, height = self.height)
		table.td(splash, width = int(self.width / 4), height = self.height)
		self.init(table, self.screen)
		self.ok = True
		#self.run(table)

	def paint(self, s):
		#if state.in_game_lobby == True and state.game_owner == False:
		#	if self.start_btn:
	#			self.table.remove(self.start_btn)
	#			self.start_btn = None
	#			self.table.chsize()

		self.screen.blit(self.bg, self.bg_rect)
		super(GameRoom, self).paint(s)
