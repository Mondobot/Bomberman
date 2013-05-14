# Bomberman game
# Author: Bruna Xavier
# Creation date: 04-30-2011

class Map(object):
    
    def __init__(self, map, width, height):
        self.__map = map[:]
        self._width = width
        self._height = height
        #self.__dblocks = dblocks.copy()
        #self.__rewards = rewards.copy()
        #self.__forbidden_positions_dblocks = [self.__convert_position(x, y) for x, y in forbidden_positions_dblocks[:]]
        
        #self.__fill_map_with_dblocks_and_rewards()
    """
    def __position_allowed_for_dblocks(self, pos):
        return (self.__map[pos] == None) and (pos not in self.__forbidden_positions_dblocks)
        
    def __fill_map_with_dblocks_and_rewards(self):
        from random import sample
        from random import shuffle
        from random import choice
        
        # list of rewards
        rewards = list()
        count = sum(self.__rewards.values())
        for x, y in self.__rewards.iteritems():
            if y > 0:
                rewards += [x] * y
        shuffle(rewards)
        
        # list of dblocks
        dblocks = list()
        count = sum(self.__dblocks.values())
        for x, y in self.__dblocks.iteritems():
            if y > 0:
                dblocks += [x] * y
        shuffle(dblocks)    
        
        # dblocks used to hide rewards
        selected_dblocks = sample(dblocks, len(rewards))
        
        # remove selected dblocks from list of dblocks
        for dblock in selected_dblocks:
            dblocks.remove(dblock)
        
        pieces = zip(selected_dblocks, rewards) + zip(dblocks, [None] * len(dblocks))
        num_pieces = len(pieces)
        
        # get possible places to put a destructible block
        allowed_positions_for_dblocks = filter(lambda i: self.__position_allowed_for_dblocks(i), range(len(self.__map)))
        
        # select some places to put dblocks
        try:
            allowed_positions_for_dblocks = sample(allowed_positions_for_dblocks, num_pieces)
        except ValueError as e:
            print e
        
        for piece in pieces:
            # choose a place to put a piece
            position = choice(allowed_positions_for_dblocks)
            
            # put the piece
            self.__map[position] = piece
            
            # remove position from positions for dblocks
            allowed_positions_for_dblocks.remove(position)
    """
    """
    def has_ublock(self, row, col):
        pos = self.__convert_position(row, col)
        element = self.__map[pos]
        return isinstance(element, int)
        
    def has_dblock(self, row, col):
        pos = self.__convert_position(row, col)
        element = self.__map[pos]
        return isinstance(element, tuple) and element[0] != None
        
    def has_reward(self, row, col):
        pos = self.__convert_position(row, col)
        element = self.__map[pos]
        return isinstance(element, tuple) and element[1] != None
        
    def has_nothing(self, row, col):
        pos = self.__convert_position(row, col)
        element = self.__map[pos]
        return element == None
        
    def destroy_dblock(self, row, col):
        if self.has_dblock(row, col):
            pos = self.__convert_position(row, col)
            if self.has_reward(row, col):
                self.__map[pos] = (None, self.__map[pos][1])
            else:
                self.__map[pos] = None
            
    def destroy_reward(self, row, col):
        if self.has_reward(row, col):
            pos = self.__convert_position(row, col)
            self.__map[pos] = None
            
    def get_reward(self, row, col):
        if self.has_reward(row, col):
            pos = self.__convert_position(row, col)
            reward = self.__map[pos][1]
            self.__map[pos] = None
            return reward
    """     
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
        
    def __set_map(self, other):
        self.__map = other
        
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
