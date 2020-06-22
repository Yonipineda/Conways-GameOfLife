import pygame 
import constants 
import math 
import time 
import copy 
import sys 

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
    '''
    Main Menu Class 
    '''
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


    def get_choice(self, screen):
        '''Logic for button choices in Main Menu'''
        pygame.display.set_caption("Conways Game Of Life: Main Menu")
        pygame.display.set_mode((2 * self.side_gap_size + self.button_width,
                                 2 * self.title_gap_size + len(self.buttons)
                                 * (self.button_height + self.button_gap_size)))

        screen.fill(self.color["Background"])

        fps_limiter = pygame.time.Clock() # Limits fps 

        buttons = [[screen.get_width() // 2, 2 * self.title_gap_size + a * 
                    (self.button_height + self.button_gap_size) + self.title_text_size,
                    self.buttons[a], self.color["Text"]] for a in range(len(self.buttons))]
        
        for a in range(len(self.buttons)):
            # Draw rect for button as the same color as the background
            pygame.draw.rect(screen, self.color["Border"],
                             (buttons[a][0] - self.button_width // 2,
                              buttons[a][1] - self.button_height // 2, 
                              self.button_width, self.button_height))
            
            pygame.draw.rect(screen, self.color["Background"],
                             ((buttons[a][0] - self.button_width // 2 + self.button_border,
                              buttons[a][1] - self.button_height // 2 + self.button_border,
                              self.button_width - self.button_border * 2,
                              self.button_height - self.button_border * 2)))

        # This Writes the title 
        write(screen, screen.get_width() // 2, self.title_gap_size, "Main Menu", 
              self.color["Text"], self.title_text_size, alignment=("centre", "centre"))

        while True:
            if check_quit(pygame.event.get()):
                quit_game()
            x, y = pygame.mouse.get_pos()
            for a in range(len(self.buttons)):
                buttons[a][3] = self.color["Text"] # resets the color of all buttons 
            
            width = screen.get_width()
            if width / 2 - self.button_width /2 < x < width / 2 + self.button_width / 2:
                for a in range(len(self.buttons)):
                    height = buttons[a][1]
                    if height - self.button_height / 2 < y < height + self.button_height / 2:
                        if pygame.mouse.get_pressed()[0]:
                            return buttons[a][2]
                        buttons[a][3] = self.color["Hover"] # change color again 
            
            for a in range(len(self.buttons)): # if being hovered over
                write(screen, screen.get_width() // 2, 
                      buttons[a][1], buttons[a][2], buttons[a][3], self.text_size, 
                      alignment=("centre", "centre")) # writes on the button 
                    
            pygame.display.update() # update 
            fps_limiter.tick(constants.FPS)  # limits to a certain fps 


class Simulation:
    '''
    Contains values to change how the game looks and behaves in simulator mode.
    '''
    def __init__(self):
        # Will need to instantiate Simulator constants 
        # build logic for sliders
        pass

    def run(self, screen, board):
        '''
        Runs the simulator 

        Implement the logic to run the simulation 0.o
        '''
        pass

    def check_user_input(self, screen, board):
        '''
        Check for user input and act accordingly. 

        Event handling implementation??

        Hover, keyword, keyboard, gps, interaction, etc..?
        '''
        pass 

    def draw_gps_slider(self, screen, y, gps_limit, board):
        '''
        Draw sliders with the y coordinates
        '''
        pass 



class Game:
    '''
    Game Class   
    '''
    def __init__(self):
        '''
        Initialize all Game constants
        '''
        pass

    def run(self, screen, board):
        '''Runs the Game'''
        pass 


    def take_turn(self, screen, board, player_num):
        ''' Returns the turn that the player wants to do '''
        pass 

    def check_turn_is_valid(self, board, turns, player_num, a, b, kill, turns_left):
        '''
         Returns whether or not the turn is valid:

                        Return: [bool, int]

                                bool -> whether or not turn was valid
                                int -> num of turns the move should take
        '''
        pass 


    def get_player_score(self, board, turns=None, player_num=0):
        ''' 
        Returns num of cells each player has on board
        '''
        pass 


    def draw_right_column(self, screen, player_scores, on_button, turns_used,
                          generated, clickable=None, update=True):
                          '''
                          Column drawn on right-handside of screen'''
                          pass 


    def check_for_wins(self, board, turns, generations):
        ''' Check for wins '''
        pass 



class Help:
    ''' Help Class ''' 
    def __init__(self):
        '''
        Initialize Help constants
        '''
        pass 


    def display(self, screen):
        '''
        Displays help page on the given screen
        '''
        pass 

    def draw(self, screen, help_surface, slider_centre, slider_range):
        '''
        Draw the right hand side bit of text and slider at given levels
        '''
        pass 


    def get_surfaces(self):
        '''
        Retrieves surfaces for the help screen. 
        '''
        pass 


    def write(self, screen, x, y, text, color, size, max_len=None, gap=0, rotate=0,
              alignment=("left", "top")):
              '''
              Puts text onto the screen at point x,y. 
              '''
              pass 


    def check_quit(self, events):
        '''
        Checks whether the player tried to quit the game.

        Bool: Returned for corresponding ESC key pressed.
        '''
        pass 


    def quit_game(self):
        ''' Quits Game ''' 
        pygame.quit()
        sys.exit(0)



