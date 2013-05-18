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
import state
import network
import protocol
import time

FPS     =   40
WIDTH   =   800
HEIGHT  =   600
BLACK   =   (0, 0, 0)
GREY    =   (132, 130, 132)

NONE = "-1"
LOGIN = "0"
CREATE = "1"
JOIN = "2"
START = "3"
MOVE = "4"
DROP = "5"
MAP = "6"

WEST = "3"
SOUTH = "2"
EAST = "1"
NORTH = "4"

pygame.init()

screen = pygame.display.set_mode( [WIDTH, HEIGHT] )
pygame.display.set_caption("Bomberman Game")

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

done = False


world = PygameWorld(screen)
#login_screen = gui.App(width = WIDTH, height = HEIGHT)
#login_screen.connect(gui.QUIT, login_screen.quit, None)
#login_screen.init(LoginScreen(statea, screen, width = WIDTH, height = HEIGHT), screen)
login_screen = LoginScreen(state, screen, width = WIDTH, height = HEIGHT)

#login_screen.run(LoginScreen(statea, screen, width = WIDTH, height = HEIGHT))

# -------- Main Program Loop -----------
network.connect()
protocol.sendMessage(TYPE = CREATE)
time.sleep(3)
protocol.sendMessage(TYPE = START)

while not done:
    for event in pygame.event.get(): # User did something
        print "state.in_game ", state.in_game
        if event.type == pygame.QUIT: # If user clicked close
            done = True # Flag that we are done so we exit this loop


        elif state.in_game == True and event.type == pygame.KEYUP:
            if not world.players[world.me].walking:
                 if event.key == pygame.K_UP:
                    protocol.sendMessage(TYPE = MOVE, DIR = NORTH)
                 elif event.key == pygame.K_DOWN:
                    protocol.sendMessage(TYPE = MOVE, DIR = SOUTH)
                 elif event.key == pygame.K_RIGHT:
                    protocol.sendMessage(TYPE = MOVE, DIR = EAST)
                 elif event.key == pygame.K_LEFT:
                    protocol.sendMessage(TYPE = MOVE, DIR = WEST)
                 elif event.key == pygame.K_b:
                    protocol.sendMessage(TYPE = DROP)

        else:
            login_screen.event(event)
                
    # make things happen
    protocol.recvMessage(world)
    if state.logged_in == False and state.in_game == True:
        print "ruleaza"
        world.run()
    
    # Set the screen background
        screen.fill( GREY )
    
    # draw world
        world.draw()
    

    #else:
     #   login_screen.update()
        
    # Limit to 20 frames per second
    clock.tick( FPS )
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
	
	
# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()
