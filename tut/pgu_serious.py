#! /usr/bin/env python

import pygame
from pgu import gui

def login():
	print "user: " + user.value
	print "pass: " + passwd.value
	title = "Error"

	if user.value == "" or passwd.value == "":
		err_msg = "incorrect user or password"
		CustomDialog(title, err_msg).open()

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

	def __init__(self, **params):
		self.width = params.get("width", 0)
		self.height = params.get("height", 0)

		gui.Table.__init__(self, **params)
		
		self._fill()

	def _login_attempt(self):
		

	def _fillWallpaper(self):
		w_ratio = 0.6
		h_ratio = 1
		wall_w = int(self.width * w_ratio)
		wall_h = int(self.height * h_ratio)

		print wall_h, wall_w

		self.tr()
		wall = gui.Image("abstract_0097.jpg", width = wall_w, height = wall_h)
		self.td(wall, width = wall_w, height = wall_h)

	def _fillLoginArea(self):
		area_width = int(self.width * 0.4)
		area_height = int(self.height * 1)
		login_area = gui.Table(width = area_width, height = area_height)
		login_area.tr()

		img = gui.Image("abstract_0097.jpg", width = area_width, height = int(area_height * 0.3))

		login_area.td(img, width = area_width, height = int(area_height * 0.3))

		login_area.tr()
		login_area.td(gui.Label("Username"), width = area_width, height = 30)
		login_area.tr()
		user = gui.Input(value = "", size = 8)
		user.connect("activate", login)
		login_area.td(user, width = area_width, height = 30)

		login_area.tr()
		login_area.td(gui.Label("Password"), width = area_width, height = 30)
		login_area.tr()
		passwd = gui.Input(value = "", size = 8)
		passwd.connect("activate", login)
		login_area.td(passwd, width = area_width, height = 30)

		login_area.tr()
		login_btn = gui.Button("Login")
		login_btn.connect(gui.CLICK, self._login_attempt)
		login_area.td(login_btn, width = area_width, height = 30)
		login_area.tr()
		sp_h = int(self.height * 0.7) - 150
		login_area.td(gui.Spacer(area_width, sp_h), width = area_width, height = sp_h)

		self.td(login_area, width = area_width, height = area_height)

	def _fill(self):
		self._fillWallpaper()
		self._fillLoginArea()
"""
screen = pygame.display.set_mode((800, 600))

app = gui.Desktop(width = 800, height = 600)
app.connect(gui.QUIT, app.quit, None)

login_screen = gui.Table(width = 800, height = 600, x = 0, y = 0)

img = gui.Image("abstract_0097.jpg", width = 500, height = 600, x = 0, y = 0)
login_screen.td(img, width = 500, height = 600, rowspan = 1, colspan = 1)

right_panel = gui.Table(height = 600, width = 300, x = 500, y = 0)
right_panel.td(gui.Label("Title"), width = 300, height = 200, rowspan = 1)

#right_panel.tr()
right_panel.tr()
right_panel.td(gui.Label("Username"), width = 300, height = 20)
right_panel.tr()
user = gui.Input(value = "", size = 8)
user.connect("activate", login)
right_panel.td(user, width = 300, height = 20)

right_panel.tr()
right_panel.td(gui.Label("Password"), width = 300, height = 20)
right_panel.tr()
passwd = gui.Input(value = "", size = 8)
passwd.connect("activate", login)
right_panel.td(passwd, width = 300, height = 20)

right_panel.tr()
login_btn = gui.Button("Login")
login_btn.connect(gui.CLICK, login)
right_panel.td(login_btn, width = 300, height = 100)

login_screen.td(right_panel, width = 300, height = 600, x = 0, y = 0)
"""
screen = pygame.display.set_mode((800, 600))

app = gui.Desktop(width = 800, height = 600)
app.connect(gui.QUIT, app.quit, None)

login_screen = LoginScreen(width = 800, height = 600)
app.run(login_screen)
