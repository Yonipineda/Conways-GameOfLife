import pygame 
import utils 
import grid 
import random 
import copy


class Cell:
    '''Cell class''' 
    def __init__(self, a, b, current_state, next_state, board,
                 player, part_immune=False, alive_for=0):
                 '''a, b: Coordinates for the cells with respect to the board.'''
                 self.current_State = current_state
                 self.next_state = next_state
                 self.current_player = 0
                 self.next_player = player 
                 self.board_pos = (a, b)
                 self.alive_for = alive_for
                 self.part_immune = part_immune
                 self.full_immune = False 
                 self.coordinates = ((self.board_pos[0] - board.cushion) * board.size
                                      + (board.cell_gap + board.size) // 2,
                                      (self.board_pos[1] - board.cushion) * board.size 
                                      + (board.cell_gap + board.size) // 2)


    def kill(self):
        '''Resets relevant attributes for when a cell will die.
        Does not change the NextState attribute'''
        self.next_state = utils.Dead
        self.next_player = 0 
        self.full_immune = False
        self.part_immune = False 

    
    def birth(self, state, player):
        '''
        Resets relevant attributes for when a cell will be born in the next turn.
        Does not change NextState attribute
        '''
        self.next_state = state 
        self.next_player = player 
        self.full_immune = False
        self.part_immune = False 


    def draw(self, screen, size, board, color=None):
        '''Draw cell shape'''
        x, y = self.coordinates 
        if color is None:
            # draw the dead cells
            pygame.draw.rect(screen, board.color["Dead"], 
                             (x - size // 2, y - size // 2, size, size)) 
            
            if not self.current_State == utils.Dead:
                if self.part_immune:
                    pygame.draw.circle(screen, board.color["Player" + str(self.current_player)],
                                       (x, y), size // 2)

            elif self.current_player == 0:
                pygame.draw.rect(screen, board.color["Alive"], (x - size //2, y - size // 2,
                                                                size, size))

            else: 
                pygame.draw.rect(screen, board.color["Player" + str(self.current_player)],
                                 (x - size // 2, y - size // 2, size, size))
            
        else:
            pygame.draw.rect(screen, color, (x - size // 2, y - size // 2, size, size))



    def update(self, board=None, immunity=False):
        '''Put next_state attributes in current_state attribute.'''
        self.current_State = self.next_state
        self.current_player = self.next_player
        if immunity and not self.full_immune and not self.current_State == utils.Dead:
            if self.alive_for >= board.full_immune_time:
                self.full_immune = True 
            elif self.alive_for >= board.part_immune_time:
                self.part_immune = True 
            self.alive_for += 1
    

    def check_cell_fate(self, board, players=False):
        '''
        Check whether the cell will be dead or alive at the end of the turn.
        If so, what will be the type.
        '''
        if self.part_immune:
            return self.current_State, self.current_player
        player = [0,0,0,0,0]
        a, b = self.board_pos
        # neighbors
        al = a - 1  # a left
        ar = a + 1  # a right 
        bu = b - 1  # b top
        bd = b + 1  # b bottom

        if board.wrap and a == board.width + 2 * board.cushion - 1:
            ar = 0 
        if board.wrap and b == board.height + 2 * board.cushion - 1:
            bd = 0
        alive = 0 
        for c in (a, ar, al): # checks all cells < 1 away in each direction
            for d in (b, bu, bd):
                if not (c == a and d == b) and board.cell[c][d].current_State == utils.Square:
                    alive += 1
        
        new_state = self.current_State
        new_player = self.current_player
        birth = False 
        death = False 
        if self.current_State == utils.Dead and alive == 3:
            birth = True 
            new_state = utils.Square
        elif self.current_State == utils.Square and alive not in (2,3):
            death = True
            new_state = utils.Dead
        
        if players:
            if death:
                new_player = 0
            if birth:
                for c in (a, ar, al):
                    for d in (b, bu, bd):
                        if not (c == a and d == b):
                            player[board.cell[c][d].current_player] += 1
                del player[0]
                new_player = player.index(max(player)) + 1

        return new_state, new_player




class Board:
    '''Board Class'''
    def __init__(self, state, players=False):
        self.width = state.width 
        self.height = state.height
        self.size = state.size 
        self.wrap = state.wrap 
        self.cell_gap = state.cell_gap 
        self.generations = 0
        self.cushion = state.cushion 
        self.get_square = lambda x, y: (min(x // self.size, self.width) + self.cushion,
                                        min(y // self.size, self.height) + self.cushion)
        self.color = state.color 
        self.preview_size = state.preview_size
        self.players = players 
        if self.players:
            self.part_immune_time = state.part_immune_time
            self.full_immune_time = state.full_immune_time

        self.cell = [[Cell(a, b, utils.Square, utils.Dead, self, 0)
                     for b in range(self.height + (2 * self.cushion))]
                     for a in range(self.width + 2 * self.cushion)]

        
    def set_up(self, chances, rotational_symmetry=None):
        '''
        Function for setting up the board w/ chances of cells being born or killed
        '''
        width = self.width 
        height = self.height
        if rotational_symmetry == 2:
            if width > height:
                width //= 2
            else:
                height //= 2
        elif rotational_symmetry == 4:
            width //= 2
            height //= 2
        
        if sum(chances) != 0:  # checks if there is a chance of birth 
            for a in range(width):
                for b in range(height):
                    n = random.randint(1, sum(chances))
                    for c in range(len(chances)): # random assignment of new state or player cell
                        if sum(chances[:c + 1]) > n: # according to chances defined in constants.py
                            if c != 0:
                                if not self.players:
                                    c = 0
                                self.cell[a][b].birth(utils.Square, c)
                            break 
        self.update()

        if rotational_symmetry is not None:
            if rotational_symmetry == 4:
                for a in range(width):
                    for b in range(height):
                        if self.cell[a][b].current_player != 0:
                            player = self.cell[a][b].current_player + 1
                            if player > rotational_symmetry:
                                player -= rotational_symmetry  # find players cell
                            if width > height: # birth expected 
                                self.cell[a][height + b].birth(self.cell[a][b].current_State, player)
                            else:
                                self.cell[width + a][b].birth(self.cell[a][b].current_State, player)

                if width > height:
                    height *= 2
                else:
                    width *= 2
                self.update()

            for a in range(width):
                for b in range(height):
                    if self.cell[a][b].current_player != 0:
                        player = self.cell[a][b].current_player + rotational_symmetry // 2
                        if player > rotational_symmetry: # find player cell
                            player -= rotational_symmetry # birth
                        self.cell[-1 - a][-1 - b].birth(self.cell[a][b].current_State, player)
            self.update()

    
    def draw(self, screen, preview=False, update_display=True):
        '''
        Draws the current board and updates the display
        '''
        if preview:
            size = self.preview_size
        else:
            size = self.size - self.cell_gap
        
        for a in range(self.cushion, self.cushion + self.width):
            for b in range(self.cushion, self.cushion + self.height):
                if not preview or not (self.cell[a][b].part_immune or self.cell[a][b].full_immune):
                    self.cell[a][b].draw(screen, size, self)
        
        if update_display:
            pygame.display.update()

    
    def update(self, immunity=False):
        '''
        NextState is changed here.
        Puts the nextstate var in the currentstate var and updates immunity if applicable.
        '''
        for a in range(self.width + 2 * self.cushion):
            for b in range(self.height + 2 * self.cushion):
                self.cell[a][b].update(board=self, immunity=immunity)


    def take_turn(self, update_caption=False, players=False):
        '''
        Changes nextstate var and updates the display caption
        '''
        if update_caption:
            pygame.display.set_caption("Conways Game of Life: Generation" + str(self.generations))
        if self.wrap:
            cushion = 0 
        else: 
            cushion = 1 # iterates through all cells and kills or births the cell 
        
        for a in range(cushion, self.width + (2 * self.cushion) - cushion):
            for b in range(cushion, self.height + (2 * self.cushion) - cushion):
                fate, player = self.cell[a][b].check_cell_fate(self, players=players)
                if self.cell[a][b].current_State != fate or self.cell[a][b].current_player != player:
                    if fate == utils.Dead:
                        self.cell[a][b].kill()
                    else:
                        self.cell[a][b].birth(fate, player)

    
    def reset(self, state):
        '''
        Resets board with no alive cells. Plain dark screen, or white.. idk yet.s
        '''
        self.__init__(state, players=self.players)
        self.update()


class SimulationBoard(Board):
    '''Board for the simulator'''
    def place_preset(self, screen, preset_num, a, b):
        # Using the preset grids in grid.py
        if self.wrap:
            shape = grid.get(preset_num, a, b, self)[0]
        else: 
            shape, a, b = grid.get(preset_num, a, b, self)
        
        for i in range(len(shape)):
            for j in range(len(shape[i])):
                if self.wrap:
                    if a + i >= self.width + 2 * self.cushion:
                        a -= self.width + 2 * self.cushion
                    if b + j >= self.height + 2 * self.cushion:
                        b -= self.height + 2 * self.cushion
                if shape[i][j] == 0:
                    self.cell[a + i][b + j].kill()
                else:
                    self.cell[a + i][b + j].birth(shape[i][j], 0)
        
        self.update()
        self.draw(screen)


class GameBoard(Board):
    def show_future(self, screen, actions, player, smaller=True, immunity=True):
        '''
        If I can figure out how the heck im going to do this, this child class 
        should be able to show how the board will look like a generation ahead.
        '''
        temp_board = copy.deepcopy(self)
        temp_board.impose_turns(actions. player)
        temp_board.draw(screen, update_display=False)
        if smaller:
            temp_board.take_turn(players=True)
            temp_board.update(immunity=immunity)
            temp_board.draw(screen, preview=True)
         


    def show_alive(self, screen, size, colors, turns, player):
        '''
        shows cells as numbers w/ info such as how long they've been alive.
        '''
        temp_board = copy.deepcopy(self) 
        temp_board.impose_turns(turns, player)
        for a in temp_board.cell:
            for b in a:
                b.draw(screen, self.size - self.cell_gap, self)
                if not b.current_player == 0:
                    utils.write(screen, b.coordinates[0] + self.size // 2,
                                b.coordinates[1] + self.size // 2,
                                str(b.alive_for), colors["Dead"], size,
                                alignment=("centre", "centre"))


    def impose_turns(self, turn, player_num):
        '''
        Saw this neat function in a website.

        Basically it takes the turns on the board and does something like this:
                                        
                                [generations_at_turn_num, [[a, b, kill?]...]]
        '''
        for a in range(len(turn[1])):
            if turn[0] == a:
                self.take_turn()
                self.update(immunity=True)
            if turn[1][a][2]:
                self.cell[turn[1][a][0]][turn[1][a][1]].kill()
            else:
                self.cell[turn[1][a][0]][turn[1][a][1]].birth(utils.Square, player_num)
            self.cell[turn[1][a][0]][turn[1][a][1]].update()
        if turn[0] == len(turn[1]):
            self.take_turn(players=True)
            self.update(immunity=True)