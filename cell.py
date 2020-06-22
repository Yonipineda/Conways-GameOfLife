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
                 self.board_pos = (a, b)
                 self.alive_for = alive_for
                 self.part_immune = part_immune
                 self.full_immune = False 
                 self.coordinates = ((self.board_pos[0] - board.Cushion) * board.Size)