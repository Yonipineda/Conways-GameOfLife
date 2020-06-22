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
allowed_events = "Not Yet Implemented"