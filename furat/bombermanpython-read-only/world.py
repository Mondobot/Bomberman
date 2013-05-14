# Bomberman game
# Author: Bruna Xavier
# Creation date: 04-30-2011

class World(object):
    def __init__(self, map, players = []):
        self._map = map
        self.players = players
    
    
import pygame
from map import PygameMap
from player import PygamePlayer
from bomb import PygameBomb, PygameBombModel

class PygameWorld(World):
    
    def __init__(self, screen):
        gmap = [0, 0, 0, 0, 0, 0,
                0, None, None, None, None, 0,
                0, None, None, None, None, 0,
                0, None, None, None, None, 0,
                0, None, None, None, None, 0,
               # 0, None, None, None, None, 0,
                0, 0, 0, 0, 0, 0]
        gmap2 = [1, 1, 1, 1, 1, 1,
                 1, 0, 0, 0, 0, 1,
			  1, 0, 2, 2, 0, 1,
			  1, 0, 2, 2, 0, 1,
			  1, 0, 0, 11, 0, 1,
			  1, 1, 1, 1, 1, 1]
        players = [PygamePlayer(screen, (1, 1), (1, 0), 'images/bomberman.png', tiles_width=32, tiles_height=32),
				PygamePlayer(screen, (1, 2), (1, 0), 'images/bomberman.png', tiles_width=32, tiles_height=32)]


        super(PygameWorld, self).__init__(PygameMap(gmap2, 6, 6, screen,
	   'images/destructible_box.png', 'images/undestructible_box.png',
	   'images/rewards.png', tiles_width=32, tiles_height=32), players)
        self.__screen = screen
        self.__bomb_model = PygameBombModel('images/bomb.png', 'images/explosion.png', tiles_width=32, tiles_height=32)
        self.__bombs = []
        
    def run(self):
        #if self.__player_can_walk():
        self.players[0].walk()
        #else:
         #   self.player.cancel_movement()
            
        self.__check_bombs()
        
    def draw(self):
        self._map.draw()

        for bomb in self.__bombs:
            bomb.draw()
            
        for pl in self.players:
            pl.draw()
      
    def place_bomb(self):
        if self.__player_can_place_bomb():
            self.players[0].place_bomb()
            bomb = PygameBomb(self.__screen, self.__bomb_model, self.players[0].position, 1)
            self.__bombs.append(bomb)
   
    def __player_can_place_bomb(self):
        col, row = self.players[0].position
        
        if self._map.has_nothing(row, col):
            return self.players[0].can_place_bomb()
            
        return False
        
    def __player_can_walk(self):
        col, row = self.players[0].position
        if not self._map.insideBounds(row, col):
            return False
        
        if self._map.has_nothing(row, col):
            return True
            
        if self._map.has_ublock(row, col) or self._map.has_dblock(row, col):
            return False
            
        if self._map.has_reward(row, col):
            print "GET REWARD!!", self._map.get_reward(row, col)
            self._map.destroy_reward(row, col)
            return True

           
    def __check_bombs(self):
        for bomb in self.__bombs:
            if bomb.startExplosion():
                bomb.explode_positions = self.__explode_place(bomb.position, 0, bomb.range) + self.__explode_place(bomb.position, 1, bomb.range) + self.__explode_place(bomb.position, 2, bomb.range) + self.__explode_place(bomb.position, 3, bomb.range)

                for col, row, direction in bomb.explode_positions:
                    if self.players[0].position == (col, row):
                        self.players[0].reset()
                
            if bomb.finishExplosion():
                self.players[0].explode_bomb()

        self.__bombs = filter(lambda bomb: not bomb.finishExplosion(), self.__bombs)
        
    def __can_explode_place(self, position):
        col, row = position
        if not self._map.insideBounds(row, col):
            return False
        
        if self._map.has_nothing(row, col):
            return True
            
        if self._map.has_ublock(row, col):
            return False
            
        if self._map.has_dblock(row, col):
            self._map.destroy_dblock(row, col)
            return False
            
        if self._map.has_reward(row, col):
            self._map.destroy_reward(row, col)
            return True
    
    def __explode_place(self, start_position, direction, range):
        if range == 0:
            return []

        col, row = start_position
        if direction == 0:
            if self.__can_explode_place((col, row-range)):
                return [(col, row-range, direction)] + self.__explode_place(start_position, direction, range-1)
        elif direction == 1:
            if self.__can_explode_place((col+range, row)):
                return [(col+range, row, direction)] + self.__explode_place(start_position, direction, range-1)
        elif direction == 2:
            if self.__can_explode_place((col, row+range)):
                return [(col, row+range, direction)] + self.__explode_place(start_position, direction, range-1)
        elif direction == 3:
            if self.__can_explode_place((col-range, row)):
                return [(col-range, row, direction)] + self.__explode_place(start_position, direction, range-1)
        return []
