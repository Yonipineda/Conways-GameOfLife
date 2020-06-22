'''
Constant Parameters to be used for the game.

'''
def constant():
    # Constant variables: which is to say necessary stuff for the game

    # Board/Grid size.
    BOARD_SIZE = WIDTH, HEIGHT = 640, 480 


    # COLOR PARAMETERS 
    ## Dead colors 
    DEAD_COLORS = 0, 0, 0 # Black 

    ## Alive colors 
    ALIVE_COLORS  = 0, 255, 255 # cyna 

    Params = locals().copy()
    return Params