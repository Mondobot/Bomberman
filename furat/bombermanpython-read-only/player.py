# Bomberman game
# Author: Bruna Xavier
# Creation date: 04-30-2011

import operator

class Player(object):
    
    def __init__(self, position, direction):
        self.life = 3
        
        # if player is trying to align to grid
        self.walking = False
        
        # virtual position
        self.__start_position = position
        self.position = position
        
        # direction of movement
        self.__start_direction = direction
        self._direction = direction
        
        self.__bombs = 0
        self.__max_bombs = 1
        
        # speed
        self._speed = (4, 4)
        
    def is_alive(self):
        return self.life > 0
        
    def _reset(self):
        self.life -= 1
        self.position = self.__start_position
        self._direction = self.__start_direction

    """
    def explode_bomb(self):
        self.__bombs -= 1
        
    def place_bomb(self):
        self.__bombs += 1
        
    def can_place_bomb(self):
        return self.__bombs < self.__max_bombs
    """        

    def cancel_movement(self):
        x, y = self.position
        dx, dy = self._direction
        self.position = x-dx, y-dy
        self.walking = False
        
    def change_direction(self, other):
        if not self.walking:
            self._direction = other
            self.__update_position()
            self.walking = True

    def __update_position(self):        
        x, y = self.position
        dx, dy = self._direction
        self.position = x+dx, y+dy

    def setPos(self, coords):
        if self.walking:
            return

        if coords != self.position:
            self.walking = True
            new_dir = tuple(map(operator.sub, self.position, coords))
            self.change_direction(new_dir)

        self.position = coords
            
import pygame
class PygamePlayer(Player):

    NORTH   =   (0, -1)
    SOUTH   =   (0, 1)
    RIGHT   =   (1, 0)
    LEFT    =   (-1, 0)
    
    def __init__(self, screen, position, direction, player_image, tiles_per_direction=3, tiles_width=16, tiles_height=16):
        super(PygamePlayer, self).__init__(position, direction)

        self.__screen = screen
        self.__screen_position = (position[0] * tiles_width, position[1] * tiles_height)
        self.__player_image = pygame.image.load(player_image).convert_alpha()        
        
        self.__tiles_per_direction = tiles_per_direction
        self.__tiles_width = tiles_width
        self.__tiles_height = tiles_height

        self.__tiles = dict()
        self.__tiles[self.NORTH] = self.__load_image(self.__tiles_per_direction * 0)
        self.__tiles[self.RIGHT] = self.__load_image(self.__tiles_per_direction * 1)
        self.__tiles[self.SOUTH] = self.__load_image(self.__tiles_per_direction * 2)
        self.__tiles[self.LEFT] = self.__load_image(self.__tiles_per_direction * 3)
        
        self.__current_tile = 0
        
    def reset(self):
        super(PygamePlayer, self)._reset()
        self.__screen_position = (self.position[0] * self.__tiles_width, self.position[1] * self.__tiles_height)
    
    def walk(self):
        if not self.walking:
            # stay in this position if not walking
            self.__current_tile = 0
            return
            
        # final position
        fx, fy = self.position
        fx, fy = fx * self.__tiles_height, fy * self.__tiles_width
        
        # move toward self._direction with speed self._speed
        dx, dy = self._speed[0] * self._direction[0], self._speed[1] * self._direction[1]
        x, y = self.__screen_position
        x, y = x + dx, y + dy
        
        # stop walking if player is horizontally align with grid
        if abs(fx - x) < abs(dx):
            x = fx
            self.walking = False
        
        # stop walking if player is vertically align with grid        
        if abs(fy - y) < abs(dy):
            y = fy
            self.walking = False
            
        # update screen position
        self.__screen_position = x, y
        
        # update tile
        self.__current_tile = (self.__current_tile + 1) % self.__tiles_per_direction
    
    def draw(self):
        tile = self.__tiles[self._direction][self.__current_tile]
        self.__screen.blit(tile, self.__screen_position)
        
    def __load_image(self, start):
        images = list()
        for i in xrange(start, start + self.__tiles_per_direction):
            x, y = (self.__tiles_width * i, 0)
            w, h = (self.__tiles_width, self.__tiles_height)
            rect = pygame.Rect(x, y, w, h)
            
            images.append(self.__player_image.subsurface(rect))
            
        return images
