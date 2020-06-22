import pygame 
import random 
import grid
import utils 
import copy 

class Cell:
    '''Cell class''' 
    def __init__(self, a, b, current_state, next_state, board,
                 player, part_immune=False, alive_for=0):
                 '''a, b: Coordinates for the cells with respect to the board.'''
                 self.current_State = current_state
                 self.next_state = next_state
                 self.current_player = 0
                 self.next_player = player 
                 self.board_pos = (a, b)
                 self.alive_for = alive_for
                 self.part_immune = part_immune
                 self.full_immune = False 
                 self.coordinates = ((self.board_pos[0] - board.Cushion) * board.Size
                                      + (board.CellGap + board.Size) // 2,
                                      (self.board_pos[1] - board.Cushion) * board.Size 
                                      + (board.CellGap + board.Size) // 2)


    def kill(self):
        '''Resets relevant attributes for when a cell will die.
        Does not change the NextState attribute'''
        self.next_state = utils.Dead
        self.next_player = 0 
        self.full_immune = False
        self.part_immune = False 

    
    def birth(self, state, player):
        '''
        Resets relevant attributes for when a cell will be born in the next turn.
        Does not change NextState attribute
        '''
        self.next_state = state 
        self.next_player = player 
        self.full_immune = False
        self.part_immune = False 


    def draw_cell(self, screen, size, board, color=None):
        '''Draw cell shape'''
        pass 


    def update(self, board=None, immunity=False):
        '''Put next_state attributes in current_state attribute.'''
        self.current_State = self.next_state
        self.current_player = self.next_player
        pass 
    

    def check_cell_fate(self, board, players=False):
        '''
        Check whether the cell will be dead or alive at the end of the turn.
        If so, what will be the type.
        '''
        pass 