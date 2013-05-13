#! /usr/bin/env python

"""
 Bomberman game
 Author: Bruna Xavier
 Creation date: 04-30-2011
"""
import pygame
from world import PygameWorld
from login_screen import LoginScreen
from pgu import gui
from state import State

FPS     =   40
WIDTH   =   800
HEIGHT  =   600
BLACK   =   (0, 0, 0)
GREY    =   (132, 130, 132)


pygame.init()

screen = pygame.display.set_mode( [WIDTH, HEIGHT] )
pygame.display.set_caption("Bomberman Game")

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

done = False

statea = State()

world = PygameWorld(screen)
#login_screen = gui.App(width = WIDTH, height = HEIGHT)
#login_screen.connect(gui.QUIT, login_screen.quit, None)
#login_screen.init(LoginScreen(statea, screen, width = WIDTH, height = HEIGHT), screen)
login_screen = LoginScreen(statea, screen, width = WIDTH, height = HEIGHT)

#login_screen.run(LoginScreen(statea, screen, width = WIDTH, height = HEIGHT))

# -------- Main Program Loop -----------
while world.player.is_alive() and not done:
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done = True # Flag that we are done so we exit this loop
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                world.player.change_direction(world.player.NORTH)
            elif event.key == pygame.K_DOWN:
                world.player.change_direction(world.player.SOUTH)
            elif event.key == pygame.K_RIGHT:
                world.player.change_direction(world.player.RIGHT)
            elif event.key == pygame.K_LEFT:
                world.player.change_direction(world.player.LEFT)
            elif event.key == pygame.K_b:
                world.place_bomb()

        else:
            login_screen.event(event)
                
    # make things happen
    if statea.logged_in == True:
        world.run()
    
    # Set the screen background
        screen.fill( GREY )
    
    # draw world
        world.draw()
    

    else:
        login_screen.update()
        
    # Limit to 20 frames per second
    clock.tick( FPS )
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
	
	
# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()
