#! /usr/bin/env python

import pygame
import random

width = 1024
height = 600
running = 1
off = 10
m_x, m_y = 0, 0
map = []
clock = pygame.time.Clock()

screen = pygame.display.set_mode((width, height))

while running:
	event = pygame.event.poll()

	if event.type == pygame.QUIT:
		running = 0

	elif event.type == pygame.MOUSEMOTION:
		m_x, m_y = event.pos

	elif event.type == pygame.MOUSEBUTTONDOWN:
		map.append(event.pos)

	screen.fill((0, 0, 0))

	for ceva in map:
		pygame.draw.line(screen, (255, 255, 255), (ceva[0], ceva[1]),
					(ceva[0], ceva[1]))

	pygame.draw.line(screen, (0, 0, 255), (m_x, 0),
				(m_x, height))
	pygame.draw.line(screen, (0, 0, 255), (0, m_y),
				(width, m_y))

	pygame.display.flip()

	clock.tick(100)
