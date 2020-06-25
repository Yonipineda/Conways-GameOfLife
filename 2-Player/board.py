import utils
import pygame
import random
import grid
import copy


class Cell:
    def __init__(self, a, b, current_state, next_state,
                 board, player, part_immune=False, alive_for=0):
        '''a, b: Coordinates for the cells with respect to the board.'''
        self.CurrentState = current_state
        self.NextState = next_state
        self.CurrentPlayer = 0
        self.NextPlayer = player
        self.BoardPos = (a, b)
        self.AliveFor = alive_for
        self.PartImmune = part_immune
        self.FullImmune = False
        self.Coordinates = ((self.BoardPos[0] - board.Cushion) * board.Size
                            + (board.CellGap + board.Size) // 2,
                            (self.BoardPos[1] - board.Cushion) * board.Size
                            + (board.CellGap + board.Size) // 2)

    
    def kill(self):
        '''Resets relevant attributes for when a cell will die.
        Does not change the NextState attribute'''
        self.NextState = utils.Dead
        self.NextPlayer = 0
        self.AliveFor = 0
        self.PartImmune = False
        self.FullImmune = False
        
    
    def birth(self, state, player):
        '''
        Resets relevant attributes for when a cell will be born in the next turn.
        Does not change NextState attribute
        '''
        self.NextState = state
        self.NextPlayer = player
        self.FullImmune = False
        self.PartImmune = False

    
    def draw(self, screen, size, board, colour=None):
        ''' Draws the cell '''
        x, y = self.Coordinates
        if colour is None:
            # draw the dead cell
            pygame.draw.rect(screen, board.Colour["Dead"],
                             (x - size // 2, y - size // 2, size, size))  

            if not self.CurrentState == utils.Dead:  
                if self.PartImmune:  
                    pygame.draw.circle(screen, board.Colour["Player" + str(self.CurrentPlayer)],
                                       (x, y), size // 2)
                    if not self.FullImmune:
                        pygame.draw.rect(screen, board.Colour["Player" + str(self.CurrentPlayer)],
                                         (x - size // 2, y - size // 2, size, size // 2))
                elif self.CurrentPlayer == 0:
                    pygame.draw.rect(screen, board.Colour["Alive"], (x - size // 2, y - size // 2,
                                                                     size, size))
                else:
                    pygame.draw.rect(screen, board.Colour["Player" + str(self.CurrentPlayer)],
                                     (x - size // 2, y - size // 2, size, size))
        else:
            pygame.draw.rect(screen, colour, (x - size // 2, y - size // 2, size, size))

    
    def update(self, board=None, immunity=False):
        '''Put next_state attributes in current_state attribute.'''
        self.CurrentState = self.NextState
        self.CurrentPlayer = self.NextPlayer
        if immunity and not self.FullImmune and not self.CurrentState == utils.Dead:
            if self.AliveFor >= board.FullImmuneTime:
                self.FullImmune = True
            elif self.AliveFor >= board.PartImmuneTime:
                self.PartImmune = True
            self.AliveFor += 1
            

    def check_fate(self, board, players=False):
        '''
        Check whether the cell will be dead or alive at the end of the turn.
        If so, what will be the type.
        '''
        if self.PartImmune:
            return self.CurrentState, self.CurrentPlayer
        player = [0, 0, 0, 0, 0]
        a, b = self.BoardPos

        # neighbours 
        al = a - 1  # a left 
        ar = a + 1  # a right
        bu = b - 1  # b up
        bd = b + 1  # b down

        if board.Wrap and a == board.Width + 2 * board.Cushion - 1:
            ar = 0
        if board.Wrap and b == board.Height + 2 * board.Cushion - 1:
            bd = 0

        alive = 0
        for c in (a, ar, al):  # checks all cells < 1 away in each direction
            for d in (b, bu, bd):
                if not (c == a and d == b) and board.Cell[c][d].CurrentState == utils.Square:
                    alive += 1  # if isn't checking itself and the cell its checking is alive

        new_state = self.CurrentState
        new_player = self.CurrentPlayer
        birth = False
        death = False  

        if self.CurrentState == utils.Dead and alive == 3:
            birth = True
            new_state = utils.Square
        elif self.CurrentState == utils.Square and alive not in (2, 3):
            death = True
            new_state = utils.Dead
        
        if players:
            if death:
                new_player = 0
            if birth:
                for c in (a, ar, al):
                    for d in (b, bu, bd):
                        if not (c == a and d == b):  
                            player[board.Cell[c][d].CurrentPlayer] += 1
                del player[0]  
                new_player = player.index(max(player)) + 1  
    
        return new_state, new_player


class Board:
    def __init__(self, state, players=False):
        self.Width = state.Width
        self.Height = state.Height
        self.Size = state.Size
        self.Wrap = state.Wrap
        self.CellGap = state.CellGap
        self.Generations = 0
        self.Cushion = state.Cushion
        self.get_square = lambda x, y: (min(x // self.Size, self.Width) + self.Cushion,
                                        min(y // self.Size, self.Height) + self.Cushion)
        self.Colour = state.Colour
        self.PreviewSize = state.PreviewSize
        self.Players = players

        if self.Players:
            self.PartImmuneTime = state.PartImmuneTime
            self.FullImmuneTime = state.FullImmuneTime
        self.Cell = [[Cell(a, b, utils.Square, utils.Dead, self, 0)
                      for b in range(self.Height + (2 * self.Cushion))]
                     for a in range(self.Width + 2 * self.Cushion)]

    
    def utils(self, chances, rotational_symmetry=None):
        '''
        Function for setting up the board w/ chances of cells being born or killed
        '''
        width = self.Width
        height = self.Height
        if rotational_symmetry == 2:
            if width > height:
                width //= 2
            else:
                height //= 2  
        elif rotational_symmetry == 4:  
            width //= 2
            height //= 2
        if sum(chances) != 0:  # checl for chance of birth 
            for a in range(width):
                for b in range(height):
                    n = random.randint(1, sum(chances))
                    for c in range(len(chances)):  # Randomly assigns a new state/player to cells
                        if sum(chances[:c + 1]) > n:  
                            if c != 0:
                                if not self.Players:
                                    c = 0
                                self.Cell[a][b].birth(utils.Square, c)
                            break
        self.update()

        
        if rotational_symmetry is not None:
            if rotational_symmetry == 4:  # do rotational symmetry for one half of it - fills half
                for a in range(width):   
                    for b in range(height):  # rotational symmetry with 2
                        if self.Cell[a][b].CurrentPlayer != 0:
                            player = self.Cell[a][b].CurrentPlayer + 1
                            if player > rotational_symmetry:
                                player -= rotational_symmetry 
                            if width > height:  # born
                                self.Cell[a][height + b].birth(self.Cell[a][b].CurrentState, player)
                            else:
                                self.Cell[width + a][b].birth(self.Cell[a][b].CurrentState, player)


                if width > height:
                    height *= 2
                else:
                    width *= 2
                self.update()
            for a in range(width):
                for b in range(height):
                    if self.Cell[a][b].CurrentPlayer != 0:
                        player = self.Cell[a][b].CurrentPlayer + rotational_symmetry // 2
                        if player > rotational_symmetry:  
                            player -= rotational_symmetry  
                        self.Cell[-1 - a][-1 - b].birth(self.Cell[a][b].CurrentState, player)
                        
            self.update()
    
    def draw(self, screen, preview=False, update_display=True):
        '''
        Draws the current board and updates the display
        '''
        if preview:
            size = self.PreviewSize
        else:
            size = self.Size - self.CellGap
        for a in range(self.Cushion, self.Cushion + self.Width):
            for b in range(self.Cushion, self.Cushion + self.Height):
                if not preview or not (self.Cell[a][b].PartImmune or self.Cell[a][b].FullImmune):
                    self.Cell[a][b].draw(screen, size, self)

        if update_display:
            pygame.display.update()

    
    def update(self, immunity=False):
        '''
        NextState is changed here.
        Puts the nextstate var in the currentstate var and updates immunity if applicable.
        '''
        for a in range(self.Width + 2 * self.Cushion):
            for b in range(self.Height + 2 * self.Cushion):
                self.Cell[a][b].update(board=self, immunity=immunity)

    
    def take_turn(self, update_caption=False, players=False):
        '''
        Changes nextstate var and updates the display caption
        '''
        if update_caption:
            pygame.display.set_caption("Conways Game of Life: Generation " + str(self.Generations))
        if self.Wrap:
            cushion = 0
        else:
            cushion = 1  # iterates through all cells and kills or births the cell 

        for a in range(cushion, self.Width + (2 * self.Cushion) - cushion):
            for b in range(cushion, self.Height + (2 * self.Cushion) - cushion):
                fate, player = self.Cell[a][b].check_fate(self, players=players)
                if self.Cell[a][b].CurrentState != fate or self.Cell[a][b].CurrentPlayer != player:
                    if fate == utils.Dead:
                        self.Cell[a][b].kill()
                    else:
                        self.Cell[a][b].birth(fate, player)

    
    def reset(self, state):
        '''
        Resets board to plain
        '''
        self.__init__(state, players=self.Players)
        self.update()


class SimBoard(Board):
    '''
    Sim..p board.
    '''
    def place_preset(self, screen, preset_no, a, b):
        if self.Wrap:
            shape = grid.get(preset_no, a, b, self)[0]
        else:
            shape, a, b = grid.get(preset_no, a, b, self)

        for c in range(len(shape)):
            for d in range(len(shape[c])):
                if self.Wrap:
                    if a + c >= self.Width + 2 * self.Cushion:
                        a -= self.Width + 2 * self.Cushion
                    if b + d >= self.Height + 2 * self.Cushion:
                        b -= self.Height + 2 * self.Cushion
                if shape[c][d] == 0:
                    self.Cell[a + c][b + d].kill()
                else:
                    self.Cell[a + c][b + d].birth(shape[c][d], 0)

        self.update()
        self.draw(screen)


class GameBoard(Board):
    '''
    GameBoard
    '''
    def show_future(self, screen, actions, player, smaller=True, immunity=True):
        '''
        Shows how board will look like in the future 0.o
        '''
        temp_board = copy.deepcopy(self)
        temp_board.impose_turns(actions, player)
        temp_board.draw(screen, update_display=False)

        if smaller:  
            temp_board.take_turn(players=True)
            temp_board.update(immunity=immunity)
            temp_board.draw(screen, preview=True)
    
    def show_alive(self, screen, size, colours, turns, player):
        '''
        Shows how long a cell as been alive for
        '''
        temp_board = copy.deepcopy(self)
        temp_board.impose_turns(turns, player)
        for a in temp_board.Cell:
            for b in a:
                b.draw(screen, self.Size - self.CellGap, self)

                if not b.CurrentPlayer == 0: 
                    utils.write(screen, b.Coordinates[0] + self.Size // 2,
                                 b.Coordinates[1] + self.Size // 2,
                                 str(b.AliveFor), colours["Dead"], size,
                                 alignment=("centre", "centre"))

    
    def impose_turns(self, turns, player_no):
        '''
        Saw this neat function in a website.
        Basically it takes the turns on the board and does something like this:
                                        
                                [generations_at_turn_num, [[a, b, kill?]...]]
        '''
        for a in range(len(turns[1])):
            if turns[0] == a:  
                self.take_turn()
                self.update(immunity=True)

            if turns[1][a][2]:
                self.Cell[turns[1][a][0]][turns[1][a][1]].kill()
            else:
                self.Cell[turns[1][a][0]][turns[1][a][1]].birth(utils.Square, player_no)
            self.Cell[turns[1][a][0]][turns[1][a][1]].update()
            
        if turns[0] == len(turns[1]):  
            self.take_turn(players=True)  
            self.update(immunity=True)