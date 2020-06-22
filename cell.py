class Cell:
    '''Cell class''' 
    def __init__(self, alive=False):
        '''Params:  alive -> False as Default'''
        self.alive = alive 

    def cell_state(self):
        if self.alive:
            self.alive = False
        else:
            self.alive = True 

    def __str__(self):
        return str(self.alive) 

    def __repr__(self):
        return self.__str__()