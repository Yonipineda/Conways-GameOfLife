import pygame
import sys 

# initialize Constants 
# Constant variables: which is to say necessary stuff for the game

# Board/Grid size.
BOARD_SIZE = WIDTH, HEIGHT = 1080, 660 


# COLOR PARAMETERS 
## Dead colors 
DEAD_COLORS = 0, 0, 0 # Black 

## Alive colors 
ALIVE_COLORS  = 0, 255, 255 # cyna 

class GameOfLife: 
    ''' game class using PyGame '''
    def __init__(self):
        # Initialize pygame 
        pygame.init() 

        # Screen output when running 
        self.screen =  pygame.display.set_mode(BOARD_SIZE)

    def clear_screen(self):
        '''Clears screen'''
        self.screen.fill(DEAD_COLORS)    

    def update_generation(self):
        pass 

    def run_game(self):

        # Create shapes -> Circle 
        circle_rect = pygame.draw.circle(self.screen, ALIVE_COLORS, (50,50), 5, 0)


        pygame.display.flip()


        while True: 
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit() 

            # Starts with a black screen 
            self.screen.fill(DEAD_COLORS)

            

if __name__ == '__main__':
    Game = GameOfLife()  
    Game.run_game()

'''------------------------------------------------------------------------------------------'''

# Planning on using pygame for the creation of the game
# I want to deploy to heroku using Flask and some html templates
# If that is not possible, given the time contraint, Ill push to pypi 

class Game:
    '''
    Defining the Game Class. 
    '''
    def __init__(self, initial_state, rules, max_size):
        '''
        Params: 

                initial_state: The state of the game at its infancy.
                rules: Rules the game will abide to.
                max_size: width * height 
        '''
        self.initial_state = initial_state
        self.rules = rules 
        self.max_size =  max_size

    def start_game(self, it):
        state = self.initial_state
        previous_state = None # default for previous state. 
        progression = [] # empty list to keep track of the game 

        i = 0 # incrememter 

        while (not state.equals(previous_state) and i < it):
            i += 1 
            previous_state = state.copy()
            progression.append(previous_state)
            state = state.apply