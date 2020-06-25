import pygame
import utils
import board

'''
Main file for the game.
'''

# a,b refers to cell (a,b) whereas x,y refers to pixel coordinates

# Initialize pygame 
pygame.init()

# Initialize screen display 
Screen = pygame.display.set_mode((1080, 650))
pygame.display.set_icon(pygame.image.load("assets/grid.png"))
pygame.event.set_allowed(None) # Tells pygame not to check for any inputs

# allowed events
allowed_events = (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN,
                  pygame.KEYDOWN, pygame.KEYUP, pygame.QUIT)

for event in allowed_events:        
    pygame.event.set_allowed(event)  

# Simulation 
Sim = utils.Sim()  
SimBoard = board.SimBoard(Sim)
SimBoard.utils(Sim.SetUpChances)

# Game
Game = utils.Game()
GameBoard = board.GameBoard(Game, players=True)
GameBoard.utils(Game.SetUpChances, rotational_symmetry=Game.NoOfPlayers)

# Help
Help = utils.Help()

# Main Menu
Menu = utils.Menu()
MenuChoice = Menu.get_choice(Screen)

while MenuChoice in (Menu.Buttons[:3]):  # Ff non-quit button was pressed.
    if MenuChoice == Menu.Buttons[0]:  # If the Simulator button was pressed
        Sim.run(Screen, SimBoard)
    elif MenuChoice == Menu.Buttons[1]:  # If the Game button was pressed
        if Game.run(Screen, GameBoard):  # Run Game
            Game = utils.Game()         # End Game
            GameBoard = board.GameBoard(Game, players=True)  # Reset Game
            GameBoard.utils(Game.SetUpChances, rotational_symmetry=Game.NoOfPlayers)
    elif MenuChoice == Menu.Buttons[2]:  # Help me
        Help.display(Screen)
    MenuChoice = Menu.get_choice(Screen)  # Another choice is made when menu is returned to

utils.quit_game()