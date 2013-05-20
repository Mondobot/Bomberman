# Bomberman game
# Author: Bruna Xavier
# Creation date: 04-30-2011

class Map(object):
    
    def __init__(self, map, width, height):
        self.__map = map[:]
        self._width = width
        self._height = height
    
    def has_ublock(self, row, col):
        pos = self.__convert_position(row, col)
        element = self.__map[pos]
        return element == 1
        
    def has_dblock(self, row, col):
        pos = self.__convert_position(row, col)
        element = self.__map[pos]
        return element in [2, 21, 22, 23, 24, 25]
    
    def has_nothing(self, row, col):
        pos = self.__convert_position(row, col)
        element = self.__map[pos]
        return element in [0]#, 11, 12, 13, 14, 15, 31, 32, 33, 34, 35, 36, 37]

    def element_at_position(self, row, col):
        i = self.__convert_position(row, col)
        return self.map[i]
        
    def __convert_position(self, row, col):
        return row * self._width + col
        
    def insideBounds(self, row, col):
        if 0 > row or row > self._height :
            return False
        if 0 > col or col > self._width :
            return False
        return True
 
    def get_map(self):
        return self.__map
        
    def set_map(self, new_map, width, height):
        self.__map = new_map
        self._height = height
        self._width = width
        
    def get_dblocks(self):
        return self.__dblocks
        
    def __set_dblocks(self, other):
        self.__dblocks = other
        
    def get_rewards(self):
        return self.__rewards
        
    def __set_rewards(self, other):
        self.__rewards = other
        
    def get_forbidden_positions_dblocks(self):
        return self.__forbidden_positions_dblocks
        
    def __set_forbidden_positions_dblocks(self, other):
        self.__forbidden_positions_dblocks = other
        
    map = property(get_map)
    dblocks = property(get_dblocks)
    rewards = property(get_rewards)
    forbidden_positions_dblocks = property(get_forbidden_positions_dblocks)

EMPTY = 0


import pygame
class PygameMap(Map):

    def __init__(self, map, width, height, screen, dblock_image, ublock_image, reward_image, tiles_width=16, tiles_height=16):
        super(PygameMap, self).__init__(map, width, height)
        
        self.__screen = screen
        self.__tiles_width = tiles_width
        self.__tiles_height = tiles_height        

        dblocks = {0:3}
        rewards = {0:1}
        self.__ublock_image = self.__load_image(ublock_image, [0])
        self.__dblock_image = self.__load_image(dblock_image, dblocks.keys())
        self.__reward_image = self.__load_image(reward_image, rewards.keys())
        
    def __load_image(self, file_name, keys):
        image = pygame.image.load(file_name).convert_alpha()
        
        images = dict()
        for key in keys:
            x, y = (self.__tiles_width * key, 0)
            w, h = (self.__tiles_width, self.__tiles_height)
            rect = pygame.Rect(x, y, w, h)
            
            images[key] = image.subsurface(rect)
            
        return images
        
    def __draw_tile(self, tile, i, j):
        x, y = j * self.__tiles_width, i * self.__tiles_height
        self.__screen.blit(tile, (x,y))
        
    def draw(self):           
        for i in xrange(0, self._height):
            for j in xrange(0, self._width):
                element = super(PygameMap, self).element_at_position(i, j)
                if element == 1:
                    image = self.__ublock_image[0]
                    self.__draw_tile(image, i, j)
                elif element == 2 or  21 <= element <= 25:
                    image = self.__dblock_image[0]
                    self.__draw_tile(image, i, j)
                elif 11 <= element <= 25:
                    image = self.__reward_image[0]
                    self.__draw_tile(image, i, j)
