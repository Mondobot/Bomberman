#! /usr/bin/env python

import pygame
from pgu import gui
from threading import Thread
"""
app = gui.App()
e = gui.Button("Hello World")
app.connect(gui.QUIT, app.quit)
app.run(e)
"""
X = 0

def hey(ceva):
	global X
	X += 1
	print "hello " + str(X)

class Chat(Thread):
	def __init__(self):
		Thread.__init__(self)

		self.app = gui.Desktop()
		self.app.connect(gui.QUIT, self.app.quit, None)

		self.c = gui.Table(width = 200, height = 120)
		self.e = gui.Button("Chat")
		self.e.connect(gui.CLICK, hey, None)
		self.c.add(self.e, 0, 0)

	def run(self):
		self.app.run(self.c)


app = gui.Desktop()
app.connect(gui.QUIT, app.quit, None)


c = gui.Table(width = 300, height = 420)
e = gui.Button("Quit")
e.connect(gui.CLICK, hey, None)
c.td(e)

#app.run(c)
#chat = Chat()
#chat.start()
app.run(c)
