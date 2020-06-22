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


    
