#! /usr/bin/env python

import pygame
import operator
import random

# Global vars
width = 400
height = 400
running = True

initial_x = width / 2
initial_y = height / 2
food = 20, 20
size = 10

# Colors
black = 0, 0, 0
white = 255, 255, 255
background = black

# Direction
NORTH = 0, -1
SOUTH = 0, 1
EAST = 1, 0
WEST = -1, 0
SAME = 0, 0

# Clasa pentru un inel al ramei
class Worm_segment:
	def __init__(self, pos, dir):
		self.pos_x = pos[0]
		self.pos_y = pos[1]

		self.dir_x = dir[0]
		self.dir_y = dir[1]

	def set_dir(self, dir):
		self.dir_x = dir[0]
		self.dir_y = dir[1]

	def get_pos(self):
		return self.pos_x, self.pos_y

	def get_dir(self):
		return self.dir_x, self.dir_y

	def move(self):
		global width, height
		self.pos_x += self.dir_x
		self.pos_y += self.dir_y

		if self.pos_x > width:
			self.pos_x = 0
		elif self.pos_x < 0:
			self.pos_x = width

		if self.pos_y > height:
			self.pos_y = 0
		elif self.pos_y < 0:
			self.pos_y = height

	def draw_self(self, surface):
		surface.set_at((self.pos_x, self.pos_y), white)

class Worm:
	def __init__(self, pos, dir, size):
		self.head_x = pos[0]
		self.head_y = pos[1]
		self.dir = dir
		self.size = 0
		self.segments = []

		for i in range(0, size):
			self.grow()

	def get_head_pos(self):
		return self.segments[0].get_pos()

	def get_dir(self):
		return self.segments[0].get_dir()

	def set_dir(self, dir):
		self.dir = dir

	def grow(self):
		if self.size == 0:
			self.segments.append(Worm_segment((self.head_x, self.head_y),
										self.dir))

		else:
			dir = self.segments[-1].get_dir()
			new_pos = map(operator.sub, self.segments[-1].get_pos(), dir)

			self.segments.append(Worm_segment(new_pos, dir))

		self.size += 1

	def move(self):
#		print len(self.segments)
		for i in range(len(self.segments) - 1, 0, -1):
			self.segments[i].set_dir(self.segments[i - 1].get_dir())
			self.segments[i].move()

		if self.dir != SAME:
			self.segments[0].set_dir(self.dir)
		self.segments[0].move()

	def draw(self, surface):
		for i in self.segments:
			i.draw_self(surface)

def euclidist(d1, d2):
	a1 = d1[0] - d2[0]
	a2 = d1[1] - d2[1]
	return a1 * a1 + a2 * a2


Jim = Worm((initial_x, initial_y), EAST, size)
clock = pygame.time.Clock()
screen = pygame.display.set_mode((width, height))

while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				Jim.set_dir(NORTH)

			elif event.key == pygame.K_DOWN:
				Jim.set_dir(SOUTH)

			elif event.key == pygame.K_LEFT:
				Jim.set_dir(WEST)

			elif event.key == pygame.K_RIGHT:
				Jim.set_dir(EAST)

			elif event.key == pygame.K_SPACE:
				for i in range(0, 20):
					Jim.grow()

	screen.fill(black)

	Jim.move()
	Jim.draw(screen);
	
	pos = Jim.get_head_pos()
	

	if euclidist(Jim.get_head_pos(), food) < 18:
		for i in range(0, 20):
			Jim.grow()

		food = random.randint(0, width), random.randint(0, height)

	for i in range(food[0] - 3, food[0] + 3):
		for j in range(food[1] - 3, food[1] + 3):
			screen.set_at((i, j), white)
	

	pygame.display.flip()
	clock.tick(100)

