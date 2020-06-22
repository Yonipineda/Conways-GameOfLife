import pygame 
import constants 
import math 
import time 
import copy 

# Initialize general constant parameters
Font = constants.FONT 

Dead = 0

Square = 1


class Player:
    '''Player Class'''
    def __init__(self, number, color, starting_turns):
        self.numver = number 
        self.color = color 
        self.num_of_cells = 0
        self.spare_turns = starting_turns 


class MainMenu:
    def __init__(self):
        # Main Menu constant parameters
        self.button_height = constants.M_BUTTONHEIGHT
        self.button_width = constants.M_BUTTONWIDTH
        self.button_border = constants.M_BUTTONBORDER
        self.button_gap_size = constants.M_BUTTONGAPSIZE
        self.side_gap_size = constants.M_SIDEGAPSIZE
        self.text_size = constants.M_TEXTSIZE
        self.title_gap_size = constants.M_TITLEGAPSIZE
        self.title_text_size = constants.M_TitleTextSize
        self.buttons = ("Simulator", "2-Player Game", "Help", "Quit") # Options
        self.color = constants.M_COLOR

        