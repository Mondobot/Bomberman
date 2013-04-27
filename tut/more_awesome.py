#! /usr/bin/env python
import pygame

y = 0
dir = 1
running = 1
barheight = 200
colorsize = 255
screen = pygame.display.set_mode((800, 600))

barcolor = []
for i in range(1, barheight / 2):
	barcolor.append((0, 0, i* colorsize / barheight * 2))
for i in range(1, barheight / 2):
	barcolor.append((0, 0, 255 - i* colorsize / barheight * 2))

while running:
	event = pygame.event.poll()
	if event.type == pygame.QUIT:
		running = 0
	
	screen.fill((0, 0, 0))
	for i in range(0, barheight - 2):
		pygame.draw.line(screen, barcolor[i], (0, y+i), (799, y+i))

	#y += dir
	if y + barheight > 599 or y < 0:
		dir *= -1
	
	pygame.display.flip()
