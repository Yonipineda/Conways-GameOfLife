import pygame
import sys 
import cell 

# initialize Constants 
# Constant variables: which is to say necessary stuff for the game

# Board/Grid size.
BOARD_SIZE = WIDTH, HEIGHT = 1080, 660 


# COLOR PARAMETERS 
## Dead colors 
DEAD_COLORS = 0, 0, 0 # Black 

## Alive colors 
ALIVE_COLORS  = 0, 255, 255 # cyna 

class LifeGame: 
    ''' game class using PyGame '''
    def __init__(self):
        # Initialize pygame 
        pygame.init() 

        # Screen output when running 
        self.screen =  pygame.display.set_mode(BOARD_SIZE)

        # Initialize Grid 
        self.init_grid()

    def init_grid(self):
        '''Active Grid and Inactive Grid as an empty array'''
        self.game_grid_active = [
            [0,0,0],
            [0,0,0],
            [0,0,0],
        ]

        self.game_grid_inactive = []

    def clear_screen(self):
        '''Clears screen'''
        self.screen.fill(DEAD_COLORS)    

    def update_generation(self):
        # Inspects current active cell generation 
        # If the grid is inactive, update it to store new generations 
        # And, swap out the active grid 
        pass 

    def draw_grid(self):
        # Create shapes -> Circle 
        #circle_rect = pygame.draw.circle(self.screen, ALIVE_COLORS, (50,50), 5, 0)
        pygame.display.flip()
             
    def handle_events(self):
        '''
        Event Handler
        
        Params: 
                s -> Start
                r -> Randomize 
                q -> Quit 
        '''
        for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit() 

    def run_game(self):
        # Clear screen 
        self.clear_screen()

        # Flip 
        pygame.display.flip()


        while True: 
            # For Keyword 's' in event, pause game. 
            # For Keyword 'r' in event, randomize game. 
            # For Keyword 'q' in event, quit game. 
            self.handle_events()

            # Update the generation 
            self.update_generation()

            # Draw the grid 
            self.draw_grid()

            # Starts with a black screen 
            self.screen.fill(DEAD_COLORS)
 


            

if __name__ == '__main__':
    Game = LifeGame()  
    Game.run_game()