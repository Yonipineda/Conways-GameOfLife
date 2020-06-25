import pygame
import constants
import math 
import time
import copy

# Initialize general constant parameters
Font = constants.FONT

Dead = 0

Square = 1


class Player:
    '''Player Class'''
    def __init__(self, number, colour, starting_turns):
        self.Number = number
        self.Colour = colour
        self.NoOfCells = 0
        self.SpareTurns = starting_turns


class Menu:
    '''
    Main Menu Class 
    '''
    def __init__(self):
        # Main Menu constant parameters
        self.ButtonHeight = constants.M_BUTTONHEIGHT
        self.ButtonWidth = constants.M_BUTTONWIDTH
        self.ButtonBorder = constants.M_BUTTONBORDER
        self.ButtonGapSize = constants.M_BUTTONGAPSIZE
        self.SideGapSize = constants.M_SIDEGAPSIZE
        self.TextSize = constants.M_TEXTSIZE
        self.TitleGapSize = constants.M_TITLEGAPSIZE
        self.TitleTextSize = constants.M_TitleTextSize
        self.Buttons = ("Simulator", "2-Player Game", "Help", "Quit") # menu Options
        self.Colour = constants.M_COLOR

    
    def get_choice(self, screen):
        '''Logic for button choices in Main Menu'''
        pygame.display.set_caption("Conways Game Of Life: Main Menu")
        pygame.display.set_mode((2 * self.SideGapSize + self.ButtonWidth,
                                 2 * self.TitleGapSize + len(self.Buttons)
                                 * (self.ButtonHeight + self.ButtonGapSize)))

        screen.fill(self.Colour["Background"])

        fps_limiter = pygame.time.Clock()  # Limits fps 

        buttons = [[screen.get_width() // 2, 2 * self.TitleGapSize
                    + a * (self.ButtonHeight + self.ButtonGapSize) + self.TitleTextSize,
                    self.Buttons[a], self.Colour["Text"]] for a in range(len(self.Buttons))]

        for a in range(len(self.Buttons)):
            # Draw rect for button as the same color as the background
            pygame.draw.rect(screen, self.Colour["Border"],
                             (buttons[a][0] - self.ButtonWidth // 2,
                              buttons[a][1] - self.ButtonHeight // 2,
                              self.ButtonWidth, self.ButtonHeight))

            pygame.draw.rect(screen, self.Colour["Background"],
                             ((buttons[a][0] - self.ButtonWidth // 2 + self.ButtonBorder,
                               buttons[a][1] - self.ButtonHeight // 2 + self.ButtonBorder,
                               self.ButtonWidth - self.ButtonBorder * 2,
                               self.ButtonHeight - self.ButtonBorder * 2)))

        # Writes the title
        write(screen, screen.get_width() // 2, self.TitleGapSize, "Main Menu", self.Colour["Text"],
              self.TitleTextSize, alignment=("centre", "centre"))  
        
        while True:
            if check_quit(pygame.event.get()):
                quit_game()

            x, y = pygame.mouse.get_pos()
            for a in range(len(self.Buttons)):
                buttons[a][3] = self.Colour["Text"]  # resets the color of all buttons 

            width = screen.get_width()
            if width / 2 - self.ButtonWidth / 2 < x < width / 2 + self.ButtonWidth / 2:
                for a in range(len(self.Buttons)):
                    height = buttons[a][1]
                    if height - self.ButtonHeight / 2 < y < height + self.ButtonHeight / 2:
                        if pygame.mouse.get_pressed()[0]:
                            return buttons[a][2]
                        buttons[a][3] = self.Colour["Hover"]  # Change color again


            for a in range(len(self.Buttons)):   # if being hovered over
                write(screen, screen.get_width() // 2, buttons[a][1], 
                buttons[a][2], buttons[a][3],
                self.TextSize, alignment=("centre", "centre"))  # Writes on the buttons
             
            pygame.display.update()
            fps_limiter.tick(constants.FPS)  # Limits to a certain FPS


class Sim:
    '''   
     Contains values to change how the game looks and behaves in simulator mode.
    '''    
    def __init__(self):
        self.Width = constants.S_WIDTH
        self.Height = constants.S_HEIGHT
        self.Size = constants.S_SIZE
        self.CellGap = constants.S_CELLGAP
        self.Wrap = constants.S_WRAP
        self.Cushion = constants.S_CUSHION
        self.PreviewSize = 0
        self.SetUpChances = constants.S_SETUPCHANCES
        self.SliderSize = constants.S_SLIDERSIZE
        self.HighlightSize = constants.S_HIGHLIGHTSIZE
        self.NoOfNotches = constants.S_NUMOFNOTCHES
        self.NotchLength = constants.S_NOTCHLENGTH
        self.StartOfSlider = 2 * self.NotchLength
        self.SpeedSize = constants.S_SPEEDSIZE
        self.EndOfSlider = self.Height * self.Size - self.HighlightSize - self.NotchLength
        self.SpaceBetweenNotches = (self.EndOfSlider - self.StartOfSlider) / (self.NoOfNotches - 1)
        self.SliderY = self.Size * self.Width + self.CellGap // 2 + self.SliderSize // 2
        self.ButtonStart = self.Size * self.Width
        self.GPS = constants.S_GPS
        self.TopGPS = constants.S_TOPGPS
        self.BottomGPS = constants.S_BOTTOMGPS
        self.GPSIsLimited = True
        self.Paused = True
        self.OneTurn = False
        self.HeldDown = {"space": True,  # This is used to keep track of whether a button has just
                         "right": True,  # been pressed or was held down during the last check too.
                         "number": True,
                         "f": True}
        self.Colour = constants.S_COLOR
    
    def run(self, screen, board):
        ''' Runs the simulation '''
        pygame.display.set_caption("Conways Game of Life")
        pygame.display.set_mode((board.Size * board.Width + self.SliderSize,
                                 board.Size * board.Height))

        screen.fill(self.Colour["Background"])
        self.draw_gps_slider(screen, ((math.log(self.GPS, 10) + 1) // -3)
                             * (self.EndOfSlider - self.StartOfSlider) + self.EndOfSlider,
                             self.GPSIsLimited, board)

        last_frame = time.time()
        board.update()
        board.draw(screen)
        
        while not self.check_user_input(screen, board):
            board.update()
            if (not self.Paused
                and (not self.GPSIsLimited or time.time() - last_frame > 1 / self.GPS))\
                    or (self.Paused and self.OneTurn):  # If the board should be updated
                if self.OneTurn:
                    self.OneTurn = False

                board.take_turn(update_caption=True)
                board.update()
                board.Generations += 1
                board.draw(screen)
                last_frame = time.time()  # Stores the time the screen was updated 
    
    def check_user_input(self, screen, board):
        '''
        Check for user input and act accordingly. 
        Event handling implementation??
        Hover, keyword, keyboard, gps, interaction, etc..?
        '''
        # checks if player tried to quit the game
        go_back = check_quit(pygame.event.get())  
        
        # check user position
        x, y = pygame.mouse.get_pos()
        a, b = board.get_square(x, y)
        if pygame.key.get_pressed()[pygame.K_SPACE] and not self.HeldDown["space"]:
            self.Paused = not self.Paused
        if pygame.key.get_pressed()[pygame.K_f] and not self.HeldDown["f"]:
            self.GPSIsLimited = not self.GPSIsLimited
            bottom_gps_log = math.log(self.BottomGPS, self.TopGPS)
            self.draw_gps_slider(screen, self.EndOfSlider
                                 - ((math.log(self.GPS, self.TopGPS) - bottom_gps_log)
                                    * (self.EndOfSlider - self.StartOfSlider))
                                 // (1 - bottom_gps_log), self.GPSIsLimited, board)

        if pygame.key.get_pressed()[pygame.K_RIGHT] and not self.HeldDown["right"]:
            self.OneTurn = True
        else:
            self.OneTurn = False
        if pygame.key.get_pressed()[pygame.K_RETURN]:
            board.reset(self)
            board.draw(screen)
            self.Paused = True
        if pygame.mouse.get_pressed()[0]:
            if board.Size * board.Width + board.CellGap / 2 < x < (
                        board.Size * board.Width) + self.SliderSize + board.CellGap / 2:

                # restricts slider from being dragged out of the screen        
                if y < self.StartOfSlider:  
                    y = self.StartOfSlider 
                elif y > self.EndOfSlider:
                    y = self.EndOfSlider


                self.GPSIsLimited = True
                self.draw_gps_slider(screen, y, self.GPSIsLimited, board)
                bottom_gps_log = math.log(self.BottomGPS, self.TopGPS)
                self.GPS = self.TopGPS ** (((1 - bottom_gps_log) * (self.EndOfSlider - y)
                                            / (self.EndOfSlider - self.StartOfSlider)) + bottom_gps_log)


            elif 0 <= a < board.Width + board.Cushion and 0 <= b < board.Height + board.Cushion:
                board.Cell[a][b].birth(Square, 0)  
                board.update()  
                board.draw(screen)

        if pygame.mouse.get_pressed()[2] and 0 <= a < board.Width\
                + board.Cushion and 0 <= b < board.Height + board.Cushion:
            board.Cell[a][b].kill()
            board.update()
            board.draw(screen)

        number_pressed = False
        for key in range(pygame.K_1, pygame.K_9):
            if pygame.key.get_pressed()[key]:
                if not self.HeldDown["number"]:
                    board.place_preset(screen, int(pygame.key.name(key)), a, b)
                number_pressed = True
        self.HeldDown["number"] = number_pressed
        for key in (("space", "SPACE"), ("f", "f"), ("right", "RIGHT")):
            self.HeldDown[key[0]] = eval("pygame.key.get_pressed()[pygame.K_%s]" % key[1])
        
        return go_back

    
    def draw_gps_slider(self, screen, y, gps_limit, board):
        '''
        Draw sliders with the y coordinates
        '''
        pygame.draw.rect(screen, self.Colour["Background"],  
                         ((self.ButtonStart, self.StartOfSlider - self.NotchLength),  
                          (self.ButtonStart + board.CellGap + self.HighlightSize + self.SliderSize,
                           self.EndOfSlider)))


        pygame.draw.line(screen, self.Colour["Text"], (self.SliderY, self.StartOfSlider),
                         (self.SliderY, self.EndOfSlider))

        # Draws the notches                
        for n in range(self.NoOfNotches):  
            pygame.draw.line(screen, self.Colour["Text"],
                             (self.SliderY - self.NotchLength // 2,
                              self.StartOfSlider + int(n * self.SpaceBetweenNotches)),
                             (self.SliderY + self.NotchLength // 2,
                              self.StartOfSlider + int(n * self.SpaceBetweenNotches)))

        write(screen, (self.Size * self.Width + self.SliderY - self.NotchLength) // 2,
              (self.StartOfSlider + self.EndOfSlider) // 2, "Speed", self.Colour["Text"],
              self.SpeedSize, rotate=90, alignment=("centre", "centre"))

        if gps_limit:  
            colour = "Highlighter"
        else:
            colour = "Unselected"
        pygame.draw.polygon(screen, self.Colour[colour],  # Draws the pointer
                            ((self.SliderY + self.NotchLength // 2, y),
                             (self.SliderY + self.NotchLength, y - self.NotchLength // 2),
                             (self.SliderY + 2 * self.NotchLength, y - self.NotchLength // 2),
                             (self.SliderY + 2 * self.NotchLength, y + self.NotchLength // 2),
                             (self.SliderY + self.NotchLength, y + self.NotchLength // 2)))
        pygame.display.update()


class Game:
    '''
    Game Class
    '''
    def __init__(self):
        self.Width = constants.G_WIDTH
        self.Height = constants.G_HEIGTH
        self.Size = constants.G_SIZE
        self.CellGap = constants.G_CELLGAP
        self.Wrap = True
        self.Cushion = 0
        self.Turns = 0
        self.Gens = 0
        self.NoOfPlayers = constants.G_NUMOFPLAYERS
        self.PlayerNames = constants.G_PLAYERNAMES[:self.NoOfPlayers]
        self.PreviewSize = constants.G_PREVIEWSIZE
        self.SetUpChances = constants.G_SETUPCHANCES[:self.NoOfPlayers + 1]
        self.TextSize = constants.G_TEXTSIZE
        self.RightColumnSize = constants.G_RIGHTCOLUMNSIZE
        self.ButtonHeight = constants.G_BUTTONHEIGHT
        self.ButtonBorderSize = constants.G_BUTTONBORDERSIZE
        self.WinMessageWidth = constants.G_WINMESSAGEWIDTH
        self.WinMessageHeight = constants.G_WINMESSAGEHEIGHT
        self.PartImmune = constants.G_PARTIMMUNE
        self.PartImmuneTime = constants.G_PARTIMMUNETIME
        self.PartImmuneKill = constants.G_PARTIMMUNEKILL
        self.FullImmune = constants.G_FULLIMMUNE
        self.FullImmuneTime = constants.G_FULLIMMUNETIME
        self.FullImmuneKill = constants.G_FULLIMMUNEKILL
        self.Colour = constants.G_COLOR
        self.CurrentPlayer = 1
        self.IsTurnLimit = constants.G_ISTURNLIMIT
        self.TurnLimit = constants.G_TURNLIMIT
        self.IsGenLimit = constants.G_ISGENLIMIT
        self.GenLimit = constants.G_GENLIMIT
        self.BoardAmountWin = constants.G_BOARDAMOUNTWIN
        self.BoardAmount = constants.G_BOARDAMOUNT
        self.PlayerAmountWin = constants.G_PLAYERAMOUNTWIN
        self.PlayerAmount = constants.G_PLAYERAMOUNT
        self.StartingTurns = constants.G_STARTINGTURNS
        self.FairerTurns = constants.G_FAIRERTURNS
        self.Started = False
        self.TurnsPerRound = constants.G_TURNSPERROUND
        self.Players = [Player(n, self.Colour["Player" + str(n)], self.StartingTurns)
                        for n in range(1, self.NoOfPlayers + 1)]

    
    def run(self, screen, board):
        """Runs the game"""
        board.update()
        board.draw(screen)
        screen = pygame.display.set_mode((board.Size * board.Width + self.RightColumnSize,
                                          board.Size * board.Height))


        screen.fill(self.Colour["Background"])
        fps_limiter = pygame.time.Clock()
        if not self.Started:  # sets the game 
            self.Started = True
            if self.FairerTurns:
                for p in range(self.NoOfPlayers // 2):
                    self.Players[p].SpareTurns -= self.TurnsPerRound // 2


        while True:
            caption = " - Generations: " + str(self.Gens)  
            if self.IsGenLimit:
                caption += ", (%s)" % str(self.GenLimit)
            caption += ", Turns: " + str(self.Turns)
            if self.IsTurnLimit:
                caption += " (%s)" % str(self.TurnLimit)
            if self.BoardAmountWin:
                caption += ", Cells needed to win: " + str(math.floor(self.BoardAmount
                                                                       * self.Width * self.Height))


            if self.PartImmune:
                caption += ", Part Immune after %s Turns" % str(self.PartImmuneTime)
            if self.FullImmune:
                caption += ", Fully Immune after %s Turns" % str(self.FullImmuneTime)

            pygame.display.set_caption("Conways Game of Life: Game" + caption)
            player_scores = self.get_player_scores(board)

            for p in range(self.NoOfPlayers):
                self.Players[p].NoOfCells = player_scores[p + 1]
            self.Players[self.CurrentPlayer - 1].SpareTurns += self.TurnsPerRound  # returns current
            turn = self.take_turn(screen, board, self.CurrentPlayer) 


            if turn == "Go Back":
                self.Players[self.CurrentPlayer - 1].SpareTurns -= self.TurnsPerRound
                return False  

            else:  
                board.impose_turns(turn, self.CurrentPlayer)
                self.Players[self.CurrentPlayer - 1].SpareTurns -= len(turn[1])
                screen.fill(self.Colour["Background"])
                board.draw(screen)

            if turn[0] is not None:
                self.Gens += 1
            if self.CurrentPlayer == self.NoOfPlayers:
                self.CurrentPlayer = 1
                self.Turns += 1
            else:
                self.CurrentPlayer += 1
            win = self.check_for_wins(board, self.Turns, self.Gens)
            fps_limiter.tick(constants.FPS)


            if win is not None:  # If someone won
                if win[0].startswith("T"):
                    win_message = "Turn limit reached.Player " + str(win[1]) + " wins!"
                elif win[0].startswith("G"):
                    win_message = "Generation limit reached.Player " + str(win[1]) + " wins!"
                elif win[0].startswith("S"):
                    win_message = "Player " + str(win[1]) + " got enough points to win!"
                else:
                    win_message = "Player " + str(win[1]) +\
                                  " got more cells than the other player by enough to win"


                pygame.draw.rect(screen, (self.Colour["Highlighter"]),  
                                 ((screen.get_width() - self.WinMessageWidth)
                                  // 2 - self.ButtonBorderSize,
                                  (screen.get_height() - self.WinMessageHeight)
                                  // 2 - self.ButtonBorderSize,
                                  self.WinMessageWidth + 2 * self.ButtonBorderSize,
                                  self.WinMessageHeight + 2 * self.ButtonBorderSize))

                pygame.draw.rect(screen, (self.Colour["Background"]),  
                                 ((screen.get_width() - self.WinMessageWidth) // 2,
                                  (screen.get_height() - self.WinMessageHeight) // 2,
                                  self.WinMessageWidth, self.WinMessageHeight))
                # Writes the win message
                write(screen, screen.get_width() // 2, screen.get_height() // 2, win_message,
                      self.Colour["Text"], self.TextSize, max_len=self.WinMessageWidth,
                      alignment=("centre", "centre")) 

                pygame.display.update()
                board_view = False  

                while True:  
                    if check_quit(pygame.event.get()):  # if ESC is pressed - first press displays
                        if board_view:  # the board, the second goes back to the main menu
                            self.Started = False
                            return True
                        else:
                            board_view = True
                            screen.fill(self.Colour["Background"])
                            board.draw(screen)
                            self.draw_right_column(screen, self.get_player_scores(board),
                                                   (False, False), (0, 0, 0, 0), 0, clickable=False)
                            pygame.display.update()
                            fps_limiter.tick(constants.FPS)
    

    def take_turn(self, screen, board, player_no):
        ''' Returns the turn that the player wants to do '''
        board.draw(screen)
        turn = [None, []]  # first value is where the gen will happe, if it all.
        turn_chosen = False  # the second is a list containing info about the turns
        held_down = {"mouse0": True, "mouse2": False, "esc": False,
                     "space": True, "f": False, "j": False}

        show_future = True
        show_alive_for = False

        turns_used = [0 for _ in range(self.NoOfPlayers)]
        fps_limiter = pygame.time.Clock()

        while not turn_chosen:
            events = pygame.event.get()
            if check_quit(events) and not held_down["esc"]:  # if ESC pressed but wasn't last turn
                if len(turn[1]) == 0 and turn[0] is None:
                    return "Go Back"
                else:
                    if turn[0] == len(turn[1]):  # if the generation needs to be undone
                        turn[0] = None
                    else:
                        t = turn[1][-1]
                        del turn[1][-1]  # Gives back the turns used to make the turn
                        turns_used[player_no - 1]\
                        -= self.check_turn_is_valid(board, turn, player_no, t[0], t[1], t[2],
                                                        self.FullImmuneKill)[1]

                held_down["esc"] = True
            else:
                held_down["esc"] = False


            x, y = pygame.mouse.get_pos()
            a, b = board.get_square(x, y)

            if 0 <= a < board.Width + board.Cushion and 0 <= b < board.Height + board.Cushion:
                kill = None  # if on the board check if anything needs adding to turn
                if not (held_down["mouse0"] or held_down["mouse2"])\
                        and self.Players[player_no - 1].SpareTurns > turns_used[player_no - 1]:
                    if pygame.mouse.get_pressed()[0]:
                        turn_validation =\
                            self.check_turn_is_valid(board, turn, player_no, a, b, False,
                                                     self.Players[player_no - 1].SpareTurns
                                                     - turns_used[player_no - 1])

                        if turn_validation[0]:
                            kill = False
                    elif pygame.mouse.get_pressed()[2]:
                        turn_validation =\
                            self.check_turn_is_valid(board, turn, player_no, a, b, True,
                                                     self.Players[player_no - 1].SpareTurns
                                                     - turns_used[player_no - 1])

                        if turn_validation[0]:
                            kill = True
                if kill is not None:  # If the turn was valid
                    turn[1].append([a, b, kill])
                    turns_used[player_no - 1] += turn_validation[1]

            if pygame.key.get_pressed()[pygame.K_SPACE] and not held_down["space"]:
                turn_chosen = True

            if pygame.key.get_pressed()[pygame.K_f] and not held_down["f"]:
                show_future = not show_future
                show_alive_for = False

            if pygame.key.get_pressed()[pygame.K_j] and not held_down["j"]:
                show_alive_for = not show_alive_for
                show_future = False


            on_button = [False, False]  # checks whether the mouse is on either button
            if 2 * self.ButtonBorderSize < screen.get_width()\
                    - x < self.RightColumnSize - 2 * self.ButtonBorderSize:
                if 0 < screen.get_height() - y - self.ButtonBorderSize < self.ButtonHeight:
                    if pygame.mouse.get_pressed()[0] and not held_down["mouse0"]:
                        turn_chosen = True
                    on_button[0] = True

                elif 0 > y - screen.get_height() + 3 * self.ButtonBorderSize\
                        + self.ButtonHeight > -self.ButtonHeight:
                    if pygame.mouse.get_pressed()[0] and turn[0] is None:
                        turn[0] = len(turn[1])
                    on_button[1] = True

            
            self.draw_right_column(screen, self.get_player_scores(board, turns=turn,
                                                                  player_no=player_no), on_button,
                                   turns_used, not turn[0] is None, update=False)

            if show_alive_for:
                board.show_alive(screen, self.TextSize, self.Colour, turn, player_no)
            else:
                board.show_future(screen, turn, player_no, smaller=show_future)
            held_down["mouse0"] = pygame.mouse.get_pressed()[0]
            held_down["mouse2"] = pygame.mouse.get_pressed()[2]

            for key in (("space", "SPACE"), ("f", "f"), ("j", "j")):  # Updates held_down dictionary
                held_down[key[0]] = eval("pygame.key.get_pressed()[pygame.K_%s]" % key[1])
            pygame.display.update()
            fps_limiter.tick(constants.FPS)

        return turn
    
    def check_turn_is_valid(self, board, turns, player_no, a, b, kill, turns_left):
        '''
         Returns whether or not the turn is valid:
                        Return: [bool, int]
                                bool -> whether or not turn was valid
                                int -> num of turns the move should take
        '''
        temp_board = copy.deepcopy(board)  
        temp_board.impose_turns(turns, player_no)  

        if temp_board.Cell[a][b].CurrentPlayer == player_no:
            return kill, 1

        elif temp_board.Cell[a][b].CurrentState == Dead:
            return not kill, 1

        else:
            if temp_board.Cell[a][b].FullImmune:
                if turns_left >= self.FullImmuneKill:
                    return kill, self.FullImmuneKill

                else:
                    return False, 1

            elif temp_board.Cell[a][b].PartImmune:
                if turns_left >= self.PartImmuneKill:
                    return kill, self.PartImmuneKill

                else:
                    return False, 1

            else:
                return kill, 1

    
    def get_player_scores(self, board, turns=None, player_no=0):
        ''' 
        Returns num of cells each player has on board
        '''
        player_scores = [0 for _ in range(self.NoOfPlayers + 1)]
        if turns is None:
            for a in range(self.Width):
                for b in range(self.Height):
                    player_scores[board.Cell[a][b].CurrentPlayer] += 1

        else:
            temp_board = copy.deepcopy(board)
            temp_board.impose_turns(turns, player_no)
            for a in range(self.Width):
                for b in range(self.Height):
                    player_scores[temp_board.Cell[a][b].CurrentPlayer] += 1

        return player_scores
    
    def draw_right_column(self, screen, player_scores, on_button, turns_used, generated,
                          clickable=None, update=True):
        '''
        Column drawn on right-handside of screen
        '''
        pygame.draw.rect(screen, self.Colour["Background"],
                         (screen.get_width() - self.RightColumnSize, 0,
                          self.RightColumnSize, screen.get_height()))

        # Erases the last drawing of the column
        write(screen, screen.get_width() - self.RightColumnSize // 2, self.ButtonBorderSize,
              self.PlayerNames[self.CurrentPlayer - 1] + "'s turn",
              self.Colour["Player" + str(self.CurrentPlayer)], self.TextSize,
              max_len=self.RightColumnSize, alignment=("centre", "top"))


        button_centres = [[screen.get_width() - self.RightColumnSize // 2,
                           screen.get_height() - 2 * self.ButtonBorderSize - self.ButtonHeight // 2
                           - a * (self.ButtonHeight + 2 * self.ButtonBorderSize)] for a in range(2)]

        # draws the buttons
        for a in range(2):  
            pygame.draw.rect(screen, self.Colour["ButtonBorder"],
                             (button_centres[a][0] - self.RightColumnSize // 2
                              + self.ButtonBorderSize,
                              button_centres[a][1] - self.ButtonHeight // 2 + self.ButtonBorderSize,
                              self.RightColumnSize - 2 * self.ButtonBorderSize, self.ButtonHeight))

            pygame.draw.rect(screen, self.Colour["Background"],
                             (button_centres[a][0] - self.RightColumnSize // 2
                              + 2 * self.ButtonBorderSize,
                              button_centres[a][1] - self.ButtonHeight // 2
                              + 2 * self.ButtonBorderSize,
                              self.RightColumnSize - 4 * self.ButtonBorderSize,
                              self.ButtonHeight - self.ButtonBorderSize - 2))

        if clickable is None:  
            button_colours = [self.Colour["Text"] for _ in range(2)]
            if on_button[0]:
                button_colours[0] = self.Colour["Highlighter"]
            if generated:
                button_colours[1] = self.Colour["Unselectable"]
            else:
                if on_button[1]:
                    button_colours[1] = self.Colour["Highlighter"]
        else:
            button_colours = [self.Colour["Unselectable"] for _ in range(2)]

            
        button_text = ("End Turn", "Generate")
        for a in range(2):  # writes in the buttons
            write(screen, button_centres[a][0], button_centres[a][1], button_text[a],
                  button_colours[a], self.TextSize, max_len=self.RightColumnSize,
                  alignment=("centre", "centre"))

        bottom = (screen.get_width() - self.RightColumnSize + self.ButtonBorderSize,
                  button_centres[-1][1] - self.ButtonBorderSize - self.ButtonHeight // 2)

        extra_space = 0
        for n in [self.NoOfPlayers - a - 1 for a in range(self.NoOfPlayers)]:  
            col = self.Players[n].Colour  

            extra_space += 4 * self.ButtonBorderSize

            extra_space += write(screen, bottom[0], bottom[1] - extra_space,
                                 "Spare Turns: " + str(self.Players[n].SpareTurns - turns_used[n]),
                                 col, int(self.TextSize / 1.5),
                                 alignment=("left", "bottom")) + 2 * self.ButtonBorderSize

            extra_space += write(screen, bottom[0], bottom[1] - extra_space,
                                 "Cells: " + str(player_scores[n + 1]), col,
                                 int(self.TextSize / 1.5),
                                 alignment=("left", "bottom")) + 2 * self.ButtonBorderSize

            extra_space += write(screen, bottom[0], bottom[1] - extra_space, self.PlayerNames[n],
                                 col, int(self.TextSize / 1.2),
                                 max_len=self.RightColumnSize - 2 * self.ButtonBorderSize,
                                 alignment=("left", "bottom"))

        if update:
            pygame.display.update()

    
    def check_for_wins(self, board, turns, generations):
        '''
        Check for wins
        '''
        player_scores = self.get_player_scores(board)
        del player_scores[0]

        if self.IsTurnLimit and turns >= self.TurnLimit:
            return "Turn Limit Reached", player_scores.index(max(player_scores)) + 1

        if self.IsGenLimit and generations >= self.GenLimit:
            return "Generation Limit Reached", player_scores.index(max(player_scores)) + 1

        board_tot = self.Height * self.Width
        for a in range(len(player_scores)):
            if self.BoardAmountWin and player_scores[a] > board_tot * self.BoardAmount:
                return "Board Amount Passed", a + 1

            for b in range(len(player_scores)):
                if self.PlayerAmountWin and player_scores[a] * self.PlayerAmount > player_scores[b]:
                    return "Score Difference Passed", a + 1
                

class Help:
    def __init__(self):
        self.SectionGapSize = constants.H_SECTIONGAPSIZE
        self.TextSize = constants.H_TEXTSIZE
        self.TitleSize = constants.H_TITLESIZE
        self.IndentSize = constants.H_INDENTSIZE
        self.SliderWidth = constants.H_SLIDERWIDTH
        self.SliderGapSize = constants.H_SLIDERGAPSIZE
        self.SliderLength = constants.H_SLIDERLENGTH
        self.Width = constants.H_WIDTH
        self.Height = 600  
        self.ScrollAmount = constants.H_SCROLLAMOUNT
        self.Colour = constants.H_COLOR
        self.Surfaces = self.get_surfaces()
    
    def display(self, screen):
        '''
        Displays help page on the given screen
        '''
        pygame.display.set_caption("Conways Game of Life: Help Screen")
        pygame.display.set_mode((self.Width, self.Surfaces[0].get_height()))
        screen.fill(self.Colour["Background"])
        self.Height = screen.get_height()
        slider_range = (self.SliderGapSize + self.SliderLength // 2,
                        self.Height - self.SliderGapSize - self.SliderLength // 2)

        slider_centre = slider_range[0]
        help_rect = self.Surfaces[0].get_rect()  
        help_rect.topleft = (self.SectionGapSize, self.SectionGapSize)
        screen.blit(self.Surfaces[0], help_rect)  
        self.draw(screen, self.Surfaces[1], slider_centre, slider_range)

        slider_last_turn = False
        fps_limiter = pygame.time.Clock()
        while True:
            events = pygame.event.get()
            if check_quit(events):
                break

            x, y = pygame.mouse.get_pos()
            if pygame.mouse.get_pressed()[0]:
                if slider_last_turn:
                    y = max(min(y + slider_centre - mouse_start, slider_range[1]), slider_range[0])
                    self.draw(screen, self.Surfaces[1], y, slider_range)

                elif -2 * self.SliderGapSize - self.SliderWidth < x - self.Width < 0:
                    slider_last_turn = True
                    mouse_start = y
                    if not slider_centre - self.SliderLength / 2 <\
                            y < slider_centre + self.SliderLength / 2: 
                        slider_centre = y 
            
            # reset the position of the slider
            elif slider_last_turn:
                slider_last_turn = False
                slider_centre += y - mouse_start  

            if x > (self.Width - self.SliderWidth - self.SectionGapSize) / 2 - self.SliderGapSize:
                draw = False

                for e in events:
                    if e.type == pygame.MOUSEBUTTONDOWN:
                        if e.button == 4:  # if scrolled down 
                            slider_centre = max(slider_centre - self.ScrollAmount, slider_range[0])
                            draw = True

                        if e.button == 5:  # if scrolled up
                            slider_centre = min(slider_centre + self.ScrollAmount, slider_range[1])
                            draw = True

                if draw:
                    self.draw(screen, self.Surfaces[1], slider_centre, slider_range)

            pygame.display.update()
            fps_limiter.tick(constants.FPS)
    
    def draw(self, screen, help_surface, slider_centre, slider_range):
        '''
        Draw the right hand side bit of text and slider at given levels
        '''
        pygame.draw.rect(screen, self.Colour["Background"],  
                         ((self.Width - self.SliderWidth - self.SectionGapSize)
                          // 2 - self.SliderGapSize, 0, self.Width, self.Height))

        pygame.draw.rect(screen, self.Colour["Slider"],  
                         (self.Width - self.SliderGapSize - self.SliderWidth,
                          slider_centre - self.SliderLength // 2,
                          self.SliderWidth, self.SliderLength))

        help_rect = help_surface.get_rect()
        text_range = (self.SectionGapSize, help_surface.get_height()
                      - self.Height + 2 * self.SectionGapSize)

        top_y = text_range[0] - (text_range[1] - text_range[0]) * (slider_centre - slider_range[0])\
                                // (slider_range[1] - slider_range[0])  

        help_rect.topleft = (int((self.Width - self.SliderWidth) // 2) + self.SliderGapSize, top_y)
        screen.blit(help_surface, help_rect)

        pygame.display.update()
    
    def get_surfaces(self):
        '''
        Retrieves surfaces for the help screen. 
        Gets the help_info.txt and outputs it when key pressed for help.
        '''
        text = open("help_info.txt").read().split("++")  # split into the two sections
        for section in range(len(text)):
            text[section] = text[section].split("\n")  # splits into lines
        help_surfaces = []
        
        for section in text:
            extra = 0  
            for _ in range(2):  
                help_surface = pygame.Surface(((self.Width - self.SliderWidth)
                                               // 2 - self.SectionGapSize - self.SliderGapSize,
                                               extra))
                help_surface.fill(self.Colour["Background"])
                extra = 0
                for line in section:
                    if line.startswith("**"):  # bold text
                        size = self.TitleSize
                        line = line[2:]
                    else:
                        size = self.TextSize
                    indent = 0
                    while line.startswith("--"):  # indented text
                        indent += 1
                        line = line[2:]
                    extra += write(help_surface, indent * self.IndentSize, extra, line,
                                   self.Colour["Text"], size,
                                   max_len=help_surface.get_width()
                                        - indent * self.IndentSize) + self.SectionGapSize
            help_surfaces.append(help_surface)
        return help_surfaces


def write(screen, x, y, text, colour, size, max_len=None, gap=0, font=Font, rotate=0,
          alignment=("left", "top")):
    '''
    Puts x and y onto the screen.

    x: left, centre, right
    y: top, centre, bottom
    '''
    font_obj = pygame.font.SysFont(font, size)
    if text == "":  # check if it blinks
        line = 1
        extra_space = size
    else:
        line = 0
        extra_space = 0

    while len(text.split()) > 0:  # not written
        line += 1
        msg_surface_obj = pygame.transform.rotate(font_obj.render(text, False, colour), rotate)
        used = len(text.split()) 
        while max_len is not None and msg_surface_obj.get_width() > max_len:  
            used -= 1                              
            msg_surface_obj = pygame.transform.rotate(font_obj.render(" ".join(text.split()[:used]),
                                                                      False, colour), rotate)

        msg_rect_obj = msg_surface_obj.get_rect()
        a, b = msg_surface_obj.get_size()
        if alignment[0] == "centre":
            new_x = x - a // 2
        elif alignment[0] == "right":
            new_x = x - a
        else:
            new_x = x
        if alignment[1] == "centre":
            new_y = y - b // 2
        elif alignment[1] == "bottom":
            new_y = y - b
        else:
            new_y = y

        msg_rect_obj.topleft = (new_x, new_y)  # where the two objects will be merged
        screen.blit(msg_surface_obj, msg_rect_obj)  # merges them

        y += msg_surface_obj.get_height() + gap
        extra_space += msg_surface_obj.get_height() + gap
        text = " ".join(text.split()[used:])  # deletes used text

    return extra_space                      


def check_quit(events):
    ''' if ESC pressed, quits the game. '''
    for event in events:
        if event.type == pygame.QUIT:
            quit_game()
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            return True
    return False


def quit_game():
    ''' 
    Quits the game 
    '''
    pygame.quit()
    import sys
    sys.exit(0)