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

app.run(login_screen)
