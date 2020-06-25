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
pygame.display.set_icon(pygame.image.load("grid.png"))
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
Game = utils.Game() 
GameBoard = board.GameBoard(Game, players=True)
GameBoard.set_up(Game.set_up_chances, rotational_symmetry=Game.num_of_players)

# Initialize Help Menu 
Help = utils.Help()

# Initialize Main Menu 
Menu = utils.MainMenu()
MenuChoice = Menu.get_choice(Screen)


# while game is running
while MenuChoice in (Menu.buttons[:3]): # if non-quit button was pressed.
    if MenuChoice == Menu.buttons[0]: # simulator button
        Simulation.run(Screen, SimulationBoard)
    elif MenuChoice == Menu.buttons[1]: # game button 
        if Game.run(Screen, GameBoard): # run the game
            Game = utils.Game() 
            GameBoard = board.GameBoard(Game, players=True) # reset to play again
            GameBoard.set_up(Game.set_up_chances, rotational_symmetry=Game.num_of_players)
    elif MenuChoice == Menu.buttons[2]: # Help button
        Help.display(Screen)
    MenuChoice = Menu.get_choice(Screen) # another choice is requested when menu is returned

set_up.quit_game()

