#! /usr/bin/env python

import pygame

pygame.init()
#width = raw_input("Width:")
#height = raw_input("Height:")

width = 1024
height = 600
blue = 0, 0, 255
black = 0, 0, 0
slices = 30

screen = pygame.display.set_mode((width, height))

while 1:
	event = pygame.event.poll()
	if event.type == pygame.QUIT:
		break

	screen.fill(black)

	for i in range(1, slices):
		pygame.draw.line(screen, blue, (0, height * i / slices), 
					(width - width * i / slices, 0))
		pygame.draw.line(screen, blue, (0, height * i / slices),
					(width * i / slices, height))
		pygame.draw.line(screen, blue, (width, height - height * i / slices),
					(width - width * i / slices, 0))
		pygame.draw.line(screen, blue, (width, height - height * i / slices),
					(width * i / slices, height))

#	pygame.draw.aaline(screen, blue, (width, 0), (0, height))
	pygame.display.flip()
#	count += 1
