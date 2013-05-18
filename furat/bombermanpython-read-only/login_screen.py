#! /usr/bin/env python

import pygame
from pgu import gui
import state
import network
import protocol

class CustomDialog(gui.Dialog):
	"""
		Pop-up dialog with custom title and message
		We might need to move it from here
	"""
	def __init__(this, title, msg):
		title_label = gui.Label(title)
		msg_label = gui.Label(msg)

		gui.Dialog.__init__(this, title_label, msg_label)

class LoginScreen(gui.App):
	"""
		Class that holds the login screen as an app.
		Currently it has a wallpaper, a logo and
		a login area
	"""

	def __init__(self, state, screen, **params):
		# Init the app and connect the quit action
		gui.App.__init__(self)

		self.connect(gui.QUIT, self.quit, None)

		# Init the inner variables
		self.width = params.get("width", 0)
		self.height = params.get("height", 0)
		self.state = state
		self.screen = screen
		self.table = gui.Table(**params)

		# Add object to the table and finish initializing the app
		self._fill()
		self.init(self.table, self.screen)

	"""
		Handles the login procedures
		Later this should call the networking module
	"""
	def _login(self):
		user = self.user.value;
		passwd = self.passwd.value;

		if not network.isConnected():
			network.connect()

		# plain silly, we need to remove this
		if network.isConnected():
			ans = protocol.sendMessage(TYPE = protocol.LOGIN, USER = user, PASS = passwd)

			if ans == True:
				self.state.logged_in = True
				return

			else:
				title = "Error"
				err_msg = "Invalid username or password"

		else:
			title, err_msg = network.getError()

		# If the login was incorrect prompt the user
		CustomDialog(title, err_msg).open()

	"""
		Adds object to the wallpaper area
	"""
	def _fillWallpaper(self):
		wall_width = int(self.width * 0.6)
		wall_height = int(self.height * 1)

		self.table.tr()
		wall = gui.Image("images/Wallpaper.png", width = wall_width, height = wall_height)
		self.table.td(wall, width = wall_width, height = wall_height)

	"""
		Adds objects to the login area
	"""
	def _fillLoginArea(self):
		area_width = int(self.width * 0.4)
		area_height = int(self.height * 1)

		login_area = gui.Table(width = area_width, height = area_height)

		login_area.tr()
		img = gui.Image("images/Bomberman_logo.png", width = area_width, height = int(area_height * 0.3))
		login_area.td(img, width = area_width, height = int(area_height * 0.3))

		login_area.tr()
		login_area.td(gui.Label("Username"), width = area_width, height = 30)
		login_area.tr()
		self.user = gui.Input(value = "", size = 8)
		self.user.connect("activate", self._login)
		login_area.td(self.user, width = area_width, height = 30)

		login_area.tr()
		login_area.td(gui.Label("Password"), width = area_width, height = 30)
		login_area.tr()
		self.passwd = gui.Input(value = "", size = 8)
		self.passwd.connect("activate", self._login)
		login_area.td(self.passwd, width = area_width, height = 30)

		login_area.tr()
		login_btn = gui.Button("Login")
		login_btn.connect(gui.CLICK, self._login)
		login_area.td(login_btn, width = area_width, height = 30)

		login_area.tr()
		sp_h = int(self.height * 0.7) - 150
		login_area.td(gui.Spacer(area_width, sp_h), width = area_width, height = sp_h)

		self.table.td(login_area, width = area_width, height = area_height)

	"""
		Wrapper for the functions that fill the table with objects.
		Also inits the background
	"""
	def _fill(self):
		self.bg = pygame.image.load("images/abstract_0097.jpg")
		self.bg_rect = self.bg.get_rect()

		self._fillWallpaper()
		self._fillLoginArea()

	"""
		Override the paint function so it displays the background first.
		It'a basically a hack because widgets have backgrounds, but I
		can't seem to understand how to use them. Oh well :)
	"""
	def paint(self, s):
		self.screen.blit(self.bg, self.bg_rect)
		super(LoginScreen, self).paint(s)
