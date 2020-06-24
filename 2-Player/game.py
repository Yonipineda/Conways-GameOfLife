import pygame 
import utils 
import board 

'''
Main file for the game.
'''

# Initialize pygame 
pygame.init()

# Initialize screen display 
Screen = pygame.display.set_mode((1080, 650))
pygame.display.set_icon(pygame.image.load("assets/Grid_Icon.png"))
pygame.event.set_allowed(None) # Tells pygame not to check for any inputs

# Allowed events 
allowed_events = (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN, pygame.KEYUP,
                  pygame.QUIT)

for event in allowed_events:
    pygame.event.set_allowed(event)

# initialize Simulation
Simulation = utils.Simulation()
SimulationBoard = board.SimulationBoard(Simulation)
SimulationBoard.set_up(Simulation.set_up_chances)

# Initialize Game 
Game = None 
GameBoard = None 
GameBoard.set_up(Game.set_up_chances)

# Initialize Help Menu 
Help = utils.Help()

# Initialize Main Menu 
Menu = utils.MainMenu()
MenuChoice = Menu.get_choice(Screen)

