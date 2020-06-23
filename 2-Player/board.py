import pygame 
import cell
import utils 
import grid 
import random 
import copy

class Board:
    '''Board Class'''
    def __init__(self, state, players=False):
        self.width = state.width 
        self.height = state.height
        self.size = state.size 
        self.wrap = state.wrap 
        self.cell_gap = state.cell_gap 
        self.generations = 0
        self.cushion = state.cushion 
        self.get_square = lambda x, y: (min(x // self.size, self.width) self.cushion,
                                        min(y // self.size, self.height) + self.cushion)
        self.color = state.color 
        self.preview_size = state.preview_size
        self.players = players 
        if self.players:
            self.part_immune_time = state.part_immune_time
            self.full_immune_time = state.full_immune_time

        self.cell = [[cell(a, b, utils.Square, utils.Dead, self, 0)
                     for b in range(self.height + (2 * self.cushion))]
                     for a in range(self.width + 2 * self.cushion)]

        
    def set_up(self, chances, rotational_symmetry=None):
        '''
        Function for setting up the board w/ chances of cells being born or killed
        '''
        pass 