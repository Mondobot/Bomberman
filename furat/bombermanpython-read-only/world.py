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

    def _initPlayers(self, me, no_players, pos):
        base = 'images/bomberman'

        self.players = []

        for i in range(0, no_players):
            player = PygamePlayer(self.__screen, pos[i], (1, 0),
                                 base + str(i) + '.png', tiles_width = 32,
                                 tiles_height = 32)

            self.players += [player]

        self.me = me

    def setPlayers(self, me, pos):
        
        print "self_pos ", me
        if pos == []:
            return

        if self.players == []:
            self._initPlayers(me, len(pos), pos)

        if len(pos) != len(self.players):
            return

        for i in range(0, len(pos)):
            coords = pos[i]
            self.players[i].setPos(coords)

    def run(self):
        #if self.__player_can_walk():

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
        print "MY BOMBS ", self.__bombs

    def expl_bomb(self, pos, range):
            expl = []
            expl += self.__explode_place((pos[0], pos[1] - 1), 0, 0, range)
            expl += self.__explode_place((pos[0] + 1, pos[1]), 1, 0, range)
            expl += self.__explode_place((pos[0], pos[1] + 1), 2, 0, range)
            expl += self.__explode_place((pos[0] - 1, pos[1]), 3, 0, range)

            bmb = None
            for i in self.__bombs:
                if i.position == pos:
                    bmb = i

            if bmb != None:
                bmb.explode_positions += expl

    def getNoBombs(self):
        return len(self.__bombs)

    def __can_explode_place(self, position):
        col, row = position
        if not self._map.insideBounds(row, col):
            return False
        
        if self._map.has_nothing(row, col):
            return True
            
        if self._map.has_ublock(row, col):
            return False
            
        if self._map.has_dblock(row, col):
            return False

        return True
    
    def __explode_place(self, start_position, direction, depth, range):
        if range == depth:
            return []

        expl_pos = []

        col, row = start_position
        if direction == 0 and self.__can_explode_place((col, row)):
            expl_pos += [(col, row, direction)]
            expl_pos += self.__explode_place((col, row-1), direction,
                                                          depth + 1, range)

        elif direction == 1 and self.__can_explode_place((col, row)):
            expl_pos += [(col, row, direction)]
            expl_pos += self.__explode_place((col+1, row), direction,
                                                          depth + 1, range)
        elif direction == 2 and self.__can_explode_place((col, row)):
            expl_pos += [(col, row, direction)]
            expl_pos += self.__explode_place((col, row + 1), direction,
                                                          depth + 1, range)
        elif direction == 3 and self.__can_explode_place((col, row)):
            expl_pos += [(col, row, direction)]
            expl_pos += self.__explode_place((col-1, row), direction,
                                                          depth + 1, range)

        return expl_pos
