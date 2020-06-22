# Planning on using pygame for the creation of the game
# I want to deploy to heroku using Flask and some html templates
# If that is not possible, given the time contraint, Ill push to pypi 

# Beta Version

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