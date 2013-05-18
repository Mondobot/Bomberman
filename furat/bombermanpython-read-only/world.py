# Bomberman game
# Author: Bruna Xavier
# Creation date: 04-30-2011

class World(object):
    def __init__(self, map, me = 0, players = []):
        self._map = map
        self.me = me
        self.players = players
    
    
import pygame
from map import PygameMap
from player import PygamePlayer
from bomb import PygameBomb, PygameBombModel
import protocol

class PygameWorld(World):
    
    def __init__(self, screen):
        gmap2 = [1, 1, 1, 1, 1, 1,
                 1, 0, 0, 0, 0, 1,
			  1, 0, 2, 2, 0, 1,
			  1, 0, 2, 2, 0, 1,
			  1, 0, 0, 11, 0, 1,
			  1, 1, 1, 1, 1, 1]

        super(PygameWorld, self).__init__(PygameMap(gmap2, 6, 6, screen,
	   'images/destructible_box.png', 'images/undestructible_box.png',
	   'images/rewards.png', tiles_width=32, tiles_height=32), [])

        self.__screen = screen
        self.__bomb_model = PygameBombModel('images/bomb.png', 'images/explosion.png', tiles_width=32, tiles_height=32)
        self.__bombs = []
        #self._initPlayers(1, 2)
        self.place_bomb((2, 2), 1, 20)
        self.__bombs[0].startExplosion()
        self.expl_bomb((2, 2), 2)
        self.place_bomb((1, 3), 1, 20)
        self.expl_bomb((1, 3), 2)

    def setMap(self, new_map, width, height):
        self._map.set_map(new_map, width, height)

    def _initPlayers(self, me, no_players):
        base = 'images/bomberman'

        self.players = []

        for i in range(0, no_players):
            player = PygamePlayer(self.__screen, (1, 1), (1, 0),
                                 base + str(i) + '.png', tiles_width = 32,
                                 tiles_height = 32)

            self.players += [player]

        self.me = me

    def setPlayers(self, me, pos = []):
        if pos == []:
            return

        if self.players == []:
            self._initPlayers(me, len(pos))

        if len(pos) != len(self.players):
            return

        for i in range(0, len(pos)):
            coords = pos[i]
            self.players[i].setPos(coords)

    def run(self):
        #if self.__player_can_walk():
        protocol.recvMessage(self)

        for player in self.players:
            player.walk()
        #else:
         #   self.player.cancel_movement()
            
        #self.__check_bombs()
        
    def draw(self):
        self._map.draw()

        for bomb in self.__bombs:
            bomb.draw()


            
        for pl in self.players:
            pl.draw()
      
    def place_bomb(self, position, status, radius):
        #if self.__player_can_place_bomb():
       # self.players[self.me].place_bomb()
        bomb = PygameBomb(self.__screen, self.__bomb_model, position, status, radius)
        self.__bombs.append(bomb)
    
    def clearBombs(self):
        del self.__bombs[:]
   
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

               
    def expl_bomb(self, pos, range):
		  expl = []
		  expl += self.__explode_place(pos, 0, range)
		  expl += self.__explode_place(pos, 1, range)
		  expl += self.__explode_place(pos, 2, range)
		  expl += self.__explode_place(pos, 3, range)
            
		  self.__bombs[0].explode_positions += expl

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

        expl_pos = []

        col, row = start_position
        if direction == 0:
            expl_pos += [(col, row-range, direction)] + self.__explode_place(start_position, direction, range-1)
        elif direction == 1:
            expl_pos += [(col+range, row, direction)] + self.__explode_place(start_position, direction, range-1)
        elif direction == 2:
            expl_pos += [(col, row+range, direction)] + self.__explode_place(start_position, direction, range-1)
        elif direction == 3:
            expl_pos += [(col-range, row, direction)] + self.__explode_place(start_position, direction, range-1)
        
        return expl_pos
