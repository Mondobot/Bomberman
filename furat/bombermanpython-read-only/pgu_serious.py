#! /usr/bin/env python

import pygame
from pgu import gui
import state

class CustomDialog(gui.Dialog):
	def __init__(this, title, msg):
		title_label = gui.Label(title)
		msg_label = gui.Label(msg)

		gui.Dialog.__init__(this, title_label, msg_label)


class LoginScreen(gui.Table):
	""" Class that holds the login screen as a table
		currently it has a wallpaper, a logo and
		a login area 
	"""

	def __init__(self, state, screen, **params):
		self.width = params.get("width", 0)
		self.height = params.get("height", 0)
		self.state = state
		self.screen = screen

		gui.Table.__init__(self, **params)
		
		self._fill()

	def _login(self):
		user = self.user.value;
		passwd = self.passwd.value;

		if user == "gigel" and passwd == "mamaliga":
			self.state.logged_in = True
			print "trece"

		CustomDialog("Error", "Invalid username or password").open()


	def _fillWallpaper(self):
		w_ratio = 0.6
		h_ratio = 1
		wall_w = int(self.width * w_ratio)
		wall_h = int(self.height * h_ratio)

		print wall_h, wall_w

		self.tr()
		wall = gui.Image("Wallpaper.png", width = wall_w, height = wall_h)
		self.td(wall, width = wall_w, height = wall_h)

	def _fillLoginArea(self):
		area_width = int(self.width * 0.4)
		area_height = int(self.height * 1)

#		bb = gui.Table(width = area_width, height = area_height)
#		bck = gui.Image("abstract_0097.jpg", width = area_width, height = area_height)
#		bb.td(bck, width = area_width, height = area_height)

		login_area = gui.Table(width = area_width, height = area_height)
		login_area.tr()

		img = gui.Image("Bomberman_logo.png", width = area_width, height = int(area_height * 0.3))

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

		self.td(login_area, width = area_width, height = area_height)

	def _fill(self):
		self.bg = pygame.image.load("abstract_0097.jpg")
		self.bg_rect = self.bg.get_rect()
		#screen.blit(background, bg_rect)

		self._fillWallpaper()
		self._fillLoginArea()


	def paint(self, s):
		self.screen.blit(self.bg, self.bg_rect)
		super(LoginScreen, self).paint(s)

"""
screen = pygame.display.set_mode((800, 600))

app = gui.App(width = 800, height = 600)
app.connect(gui.QUIT, app.quit, None)

login_screen = LoginScreen(width = 800, height = 600)
app.run(login_screen)
"""
