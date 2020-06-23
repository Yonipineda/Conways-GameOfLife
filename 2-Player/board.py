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
        self.get_square = lambda x, y: (min(x // self.size, self.width) + self.cushion,
                                        min(y // self.size, self.height) + self.cushion)
        self.color = state.color 
        self.preview_size = state.preview_size
        self.players = players 
        if self.players:
            self.part_immune_time = state.part_immune_time
            self.full_immune_time = state.full_immune_time

        self.cell = [[cell.Cell(a, b, utils.Square, utils.Dead, self, 0)
                     for b in range(self.height + (2 * self.cushion))]
                     for a in range(self.width + 2 * self.cushion)]

        
    def set_up(self, chances, rotational_symmetry=None):
        '''
        Function for setting up the board w/ chances of cells being born or killed
        '''
        pass 

    
    def draw(self, screen, preview=False, update_display=True):
        '''
        Draws the current board and updates the display
        '''
        if preview:
            size = self.preview_size
        else:
            size = self.size - self.cell_gap
        
        for a in range(self.cushion, self.cushion + self.width):
            for b in range(self.cushion, self.cushion + self.height):
                if not preview or not (self.cell[a][b].part_immune or self.cell[a][b].full_immune):
                    self.cell[a][b].draw(screen, size, self)
        
        if update_display:
            pygame.display.update()

    
    def update(self, immunity=False):
        '''
        NextState is changed here.
        Puts the nextstate var in the currentstate var and updates immunity if applicable.
        '''
        pass


    def take_turn(self, update_caption=False, players=False):
        '''
        Changes nextstate var and updates the display caption
        '''
        pass

    
    def reset(self, state):
        '''
        Resets board with no alive cells. Plain dark screen, or white.. idk yet.s
        '''
        self.__init__(state, players=self.players)
        self.update()


class SimulationBoard(Board):
    '''Board for the simulator'''
    def place_preset(self, screen, preset_num, a, b):
        # Using the preset grids in grid.py
        if self.wrap:
            shape = grid.get(preset_num, a, b, self)[0]
        else: 
            shape, a, b = grid.get(preset_num, a, b, self)
        
        for i in range(len(shape)):
            for j in range(len(shape[i])):
                if self.wrap:
                    if a + i >= self.width + 2 * self.cushion:
                        a -= self.width + 2 * self.cushion
                    if b + j >= self.height + 2 * self.cushion:
                        b -= self.height + 2 * self.cushion
                if shape[i][j] == 0:
                    self.cell[a + i][b + j].kill()
                else:
                    self.cell[a + i][b + j].birth(shape[i][j], 0)
        
        self.update()
        self.draw(screen)