import pygame 
import constants 
import math 
import time 
import copy 
import sys 

# Initialize general constant parameters
Font = constants.FONT 

Dead = 0

Square = 1


class Player:
    '''Player Class'''
    def __init__(self, number, color, starting_turns):
        self.number = number 
        self.color = color 
        self.num_of_cells = 0
        self.spare_turns = starting_turns 


class MainMenu:
    '''
    Main Menu Class 
    '''
    def __init__(self):
        # Main Menu constant parameters
        self.button_height = constants.M_BUTTONHEIGHT
        self.button_width = constants.M_BUTTONWIDTH
        self.button_border = constants.M_BUTTONBORDER
        self.button_gap_size = constants.M_BUTTONGAPSIZE
        self.side_gap_size = constants.M_SIDEGAPSIZE
        self.text_size = constants.M_TEXTSIZE
        self.title_gap_size = constants.M_TITLEGAPSIZE
        self.title_text_size = constants.M_TitleTextSize
        self.buttons = ("Simulator", "2-Player Game", "Help", "Quit") # Options
        self.color = constants.M_COLOR


    def get_choice(self, screen):
        '''Logic for button choices in Main Menu'''
        pygame.display.set_caption("Conways Game Of Life: Main Menu")
        pygame.display.set_mode((2 * self.side_gap_size + self.button_width,
                                 2 * self.title_gap_size + len(self.buttons)
                                 * (self.button_height + self.button_gap_size)))

        screen.fill(self.color["Background"])

        fps_limiter = pygame.time.Clock() # Limits fps 

        buttons = [[screen.get_width() // 2, 2 * self.title_gap_size + a * 
                    (self.button_height + self.button_gap_size) + self.title_text_size,
                    self.buttons[a], self.color["Text"]] for a in range(len(self.buttons))]
        
        for a in range(len(self.buttons)):
            # Draw rect for button as the same color as the background
            pygame.draw.rect(screen, self.color["Border"],
                             (buttons[a][0] - self.button_width // 2,
                              buttons[a][1] - self.button_height // 2, 
                              self.button_width, self.button_height))
            
            pygame.draw.rect(screen, self.color["Background"],
                             ((buttons[a][0] - self.button_width // 2 + self.button_border,
                              buttons[a][1] - self.button_height // 2 + self.button_border,
                              self.button_width - self.button_border * 2,
                              self.button_height - self.button_border * 2)))

        # This Writes the title 
        write(screen, screen.get_width() // 2, self.title_gap_size, "Main Menu", 
              self.color["Text"], self.title_text_size, alignment=("centre", "centre"))

        while True:
            if check_quit(pygame.event.get()):
                quit_game()
            x, y = pygame.mouse.get_pos()
            for a in range(len(self.buttons)):
                buttons[a][3] = self.color["Text"] # resets the color of all buttons 
            
            width = screen.get_width()
            if width / 2 - self.button_width /2 < x < width / 2 + self.button_width / 2:
                for a in range(len(self.buttons)):
                    height = buttons[a][1]
                    if height - self.button_height / 2 < y < height + self.button_height / 2:
                        if pygame.mouse.get_pressed()[0]:
                            return buttons[a][2]
                        buttons[a][3] = self.color["Hover"] # change color again 
            
            for a in range(len(self.buttons)): # if being hovered over
                write(screen, screen.get_width() // 2, 
                      buttons[a][1], buttons[a][2], buttons[a][3], self.text_size, 
                      alignment=("centre", "centre")) # writes on the button 
                    
            pygame.display.update() # update 
            fps_limiter.tick(constants.FPS)  # limits to a certain fps 


class Simulation:
    '''
    Contains values to change how the game looks and behaves in simulator mode.
    '''
    def __init__(self):
        # Will need to instantiate Simulator constants 
        # build logic for sliders
        self.width = constants.S_WIDTH
        self.height = constants.S_HEIGHT
        self.size = constants.S_SIZE
        self.cell_gap = constants.S_CELLGAP
        self.wrap = constants.S_WRAP
        self.cushion = constants.S_CUSHION
        self.preview_size = 0
        self.set_up_chances = constants.S_SETUPCHANCES
        self.slider_size = constants.S_SLIDERSIZE
        self.highlight_size = constants.S_HIGHLIGHTSIZE
        self.num_of_notches = constants.S_NUMOFNOTCHES
        self.notch_length = constants.S_NOTCHLENGTH
        self.start_of_slider = 2 * constants.S_NOTCHLENGTH
        self.speed_size = constants.S_SPEEDSIZE
        self.end_of_slider = self.height * self.size - self.highlight_size - self.notch_length
        self.space_between_notches = (self.end_of_slider - self.start_of_slider) / (self.num_of_notches - 2)
        self.slider_y = self.size * self.width + self.cell_gap // 2 + self.slider_size // 2
        self.button_start = self.size * self.width
        self.gps = constants.S_GPS
        self.top_gps = constants.S_TOPGPS
        self.bottom_gps = constants.S_BOTTOMGPS
        self.gps_is_limited = True 
        self.paused = True 
        self.one_turn = False 
        self.held_down = {"space": True,
                          "right": True,
                          "number": True,
                          "f": True}  # Track whether a button as been pressed or held down
        self.color = constants.S_COLOR

    def run(self, screen, board):
        '''
        Runs the simulator 

        Implement the logic to run the simulation 0.o
        '''
        pygame.display.set_caption("Conways Game of Life")
        pygame.display.set_mode((board.size * board.width + self.slider_size,
                                 board.size * board.height))

        screen.fill(self.color["Background"])
        self.draw_gps_slider(screen, ((math.log(self.gps, 10) + 1) // -3)
                             * (self.end_of_slider - self.start_of_slider) 
                             + self.end_of_slider, self.gps_is_limited, board)

        last_frame = time.time()
        board.update()
        board.draw(screen)

        while not self.check_user_input(screen, board):
            board.update()
            # checks if the board should be updated 
            if (not self.paused 
                and (not self.gps_is_limited or time.time() - last_frame > 1 / self.gps))\
                or (self.paused and self.one_turn): 

                if self.one_turn:
                    self.one_turn = False

                board.take_turn(update_caption=True)
                board.update()
                board.generations += 1
                board.draw(screen)
                last_frame = time.time() # store the time the screen was updated to limit the



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
        if pygame.key.get_pressed()[pygame.K_SPACE] and not self.held_down["space"]:
            self.paused = not self.paused
        if pygame.key.get_pressed()[pygame.K_F] and not self.held_down["f"]:
            self.gps_is_limited = not self.gps_is_limited
            bottom_gps_log = math.log(self.bottom_gps, self.top_gps)
            self.draw_gps_slider(screen, self.end_of_slider 
                                 - ((math.log(self.gps, self.top_gps) - bottom_gps_log)
                                    * (self.end_of_slider - self.start_of_slider))
                                    // (1 - bottom_gps_log), self.gps_is_limited, board)
        
        if pygame.key.get_pressed()[pygame.K_RIGHT] and not self.held_down["right"]:
            self.one_turn = True 
        else: 
            self.one_turn = False
        
        if pygame.key.get_pressed()[pygame.K_RETURN]:
            board.reset(self)
            board.draw(screen)
            self.paused = True 
        if pygame.mouse.get_pressed()[0]:
            if board.size * board.width + board.cell_gap / 2 < x < (
                board.size * board.width) + self.slider_size + board.cell_gap / 2:

                if y < self.start_of_slider:  # restricts player from dragging the slider
                    y = self.start_of_slider  # out of where it should be
                elif y > self.end_of_slider:
                    y = self.end_of_slider
                
                self.gps_is_limited = True 
                self.draw_gps_slider(screen, y, self.gps_is_limited, board)
                bottom_gps_log = math.log(self.bottom_gps, self.top_gps)
                self.gps = self.top_gps ** (((1 - bottom_gps_log) * (self.end_of_slider - y)
                                            / (self.end_of_slider - self.start_of_slider))
                                            + bottom_gps_log)

            elif 0 <= a < board.width + board.cushion and 0 <= b < board.height + board.cushion:
                board.cell[a][b].birth(Square, 0)
                board.update()
                board.draw(screen)
        
        if pygame.mouse.get_pressed()[2] and 0 <= a < board.width + board.cushion and 0 <= b < board.height + board.cushion:
            board.cell[a][b].kill()
            board.update()
            board.draw(screen)
        
        number_pressed = False 

        for key in range(pygame.K_1, pygame.K_9):
            if pygame.key.get_pressed()[key]:
                if not self.held_down["number"]:
                    board.place_preset(screen, int(pygame.key.name(key)), a, b)
                number_pressed = True 
        self.held_down["number"] = number_pressed
        for key in (("space", "SPACE"), ("f", "f"), ("right", "RIGHT")):
            self.held_down[key[0]] = eval("pygame.key.get_pressed()[pygame.K_%s]" % key[1])

        return go_back
        
                        


    def draw_gps_slider(self, screen, y, gps_limit, board):
        '''
        Draw sliders with the y coordinates
        '''
        pygame.draw.rect(screen, self.color["Background"],
                         ((self.button_start, self.start_of_slider - self.notch_length),
                         (self.button_start + board.cell_gap + self.highlight_size + self.slider_size,
                         self.end_of_slider))) 


        pygame.draw.line(screen, self.color["Text"], (self.slider_y, self.start_of_slider),
                         (self.slider_y, self.end_of_slider))
        
        for n in range(self.num_of_notches): # draws the notches 
            pygame.draw.line(screen, self.color["Text"],
                             (self.slider_y - self.notch_length // 2,
                             self.start_of_slider + int(n * self.space_between_notches)),
                             (self.slider_y + self.notch_length // 2,
                             self.start_of_slider + int(n * self.space_between_notches)))
            write(screen, (self.size * self.width + self.slider_y - self.notch_length) // 2,
                  (self.start_of_slider + self.end_of_slider) // 2, "Speed", self.color["Text"],
                  self.speed_size, rotate=90, alignment=("centre", "centre"))
            if gps_limit: # retrieves correct color for the pointers 
                color = "Highlighter"
            else:
                color = "Unselected"
            
            pygame.draw.polygon(screen, self.color[color],
                                (( self.slider_y + self.notch_length // 2, y),
                                (self.slider_y + self.notch_length, y - self.notch_length // 2),
                                (self.slider_y + 2 * self.notch_length, y - self.notch_length // 2),
                                (self.slider_y + 2 * self.notch_length, y + self.notch_length // 2),
                                (self.slider_y + self.notch_length, y + self.notch_length // 2)))
            pygame.display.update()



class Game:
    '''
    Game Class   
    '''
    def __init__(self):
        '''
        Initialize all Game constants
        '''
        self.width = constants.G_WIDTH
        self.height = constants.G_HEIGTH
        self.size = constants.G_SIZE
        self.cell_gap = constants.G_CELLGAP
        self.wrap = True 
        self.cushion = 0 
        self.turns = 0 
        self.gens = 0 
        self.num_of_players = constants.G_NUMOFPLAYERS
        self.player_names = constants.G_PLAYERNAMES
        self.preview_size = constants.G_PREVIEWSIZE
        self.set_up_chances = constants.G_SETUPCHANCES[:self.num_of_players + 1]
        self.text_size = constants.G_TEXTSIZE
        self.right_column_size = constants.G_RIGHTCOLUMNSIZE
        self.button_height = constants.G_BUTTONHEIGHT
        self.button_border_size = constants.G_BUTTONBORDERSIZE
        self.win_message_width = constants.G_WINMESSAGEWIDTH
        self.win_message_height = constants.G_WINMESSAGEHEIGHT
        self.part_immune = constants.G_PARTIMMUNE
        self.part_immune_time = constants.G_PARTIMMUNETIME
        self.part_immune_kill = constants.G_PARTIMMUNEKILL
        self.full_immune = constants.G_FULLIMMUNE
        self.full_immune_time = constants.G_FULLIMMUNETIME
        self.full_immune_kill = constants.G_FULLIMMUNEKILL
        self.color = constants.G_COLOR
        self.current_player = 1 
        self.is_turn_limit = constants.G_ISTURNLIMIT
        self.turn_limit = constants.G_TURNLIMIT
        self.is_gen_limit = constants.G_ISGENLIMIT
        self.gen_limit = constants.G_GENLIMIT
        self.board_amount_win = constants.G_BOARDAMOUNTWIN
        self.board_amount = constants.G_BOARDAMOUNT
        self.player_amount_win = constants.G_PLAYERAMOUNTWIN
        self.player_amount = constants.G_PLAYERAMOUNT
        self.starting_turns = constants.G_STARTINGTURNS
        self.fairer_turns = constants.G_FAIRERTURNS
        self.started = False 
        self.turns_per_round = constants.G_TURNSPERROUND
        self.players = [Player(n, self.color["Player" + str(n)], self.starting_turns)
                        for n in range(1, self.num_of_players + 1)]



    def run(self, screen, board):
        '''Runs the Game'''
        board.update()
        board.draw(screen)
        screen = pygame.display.set_mode(board.size * board.width + self.right_column_size,
                                         board.size * board.height)

        screen.fill(self.color["Background"])
        fps_limiter = pygame.time.Clock()
        if not self.started: # sets the game 
            self.started = True 
            if self.fairer_turns:
                for p in range(self.num_of_players // 2):
                    self.players[p].spare_turns -= self.turns_per_round // 2

        while True:
            caption = " - generations:" + str(self.gens) # generation information
            if self.is_gen_limit:
                caption += ", (%s)" % str(self.gen_limit)
            caption += ", Turns:" + str(self.turns)
            if self.is_turn_limit:
                caption += " (%s)" % str(self.turn_limit)
            if self.board_amount_win:
                caption += ", Cells needed to win:" + str(math.floor(self.board_amount *
                                                                     self.width * self.height))
            
            if self.part_immune:
                caption += ", Part Immune after %s Turns" % str(self.part_immune_time)
            if self.full_immune:
                caption += ", Fully Immune after %s Turns" % str(self.full_immune_time)
            
            pygame.display.set_caption("Conways Game of Life: Game" + caption)
            player_scores = self.get_player_score(board)
            for p in range(self.num_of_players):
                self.players[p].num_of_cells = player_scores[p + 1]
            self.players[self.current_player - 1].spare_turns += self.turns_per_round # returns current
            turn = self.take_turn(screen, board, self.current_player)
            if turn == "Go Back":
                self.players[self.current_player -1].spare_turns -= self.turns_per_round
                return False # no one won, so false is returned and player loses those turns. 
            else:
                board.impose_turns(turn, self.current_player)
                self.players[self.current_player - 1].spare_turns -= len(turn[1])
                screen.fill(self.color["Background"])
                board.draw(screen)

            if turn[0] is not None:
                self.gens += 1 
            if self.current_player == self.num_of_players:
                self.current_player = 1 
                self.turns += 1
            else:
                self.current_player += 1
            
            win = self.check_for_wins(board, self.turns, self.gens)
            fps_limiter.tick(constants.FPS)

            if win is not None: # should someone win
                if win[0].startswith("T"):
                    win_message = "Turn limit reached.Player" + str(win[1]) + " wins!"
                elif win[0].startswith("G"):
                    win_message = "Generation limit reached.Player" + str(win[1]) + " Wins!"
                elif win[0].startswith("S"):
                    win_message = "Player" + str(win[1] + "got enough cells to win.")
                else:
                    win_message = "Player" + str(win[1]) + "Got more cells than their openent"

                pygame.draw.rect(screen, (self.color["Highlighter"]), 
                                 ((screen.get_width() - self.win_message_width)
                                 // 2 - self.button_border_size,
                                 (screen.get_height() - self.win_message_height)
                                 // 2 - self.button_border_size,
                                 self.win_message_width + 2 * self.button_border_size,
                                 self.win_message_height + 2 * self.button_border_size))
                
                pygame.draw.rect(screen, (self.color["Background"]),
                                 ((screen.get_width() - self.win_message_width) // 2,
                                 (screen.get_height() - self.win_message_height) // 2,
                                 self.win_message_width, self.win_message_height))                
                write(screen, screen.get_width() // 2, screen.get_height() // 2, win_message,
                      self.color["Text"], self.text_size, max_len=self.win_message_width,
                      alignment=("centre", "centre")) # this writes the win message 

                pygame.display.update()
                board_view = False # win message disappears win ESC is pressed 
                while True:
                    if check_quit(pygame.event.get()):
                        if board_view:
                            self.started = False
                            return True 
                        else:
                            board_view = True 
                            screen.fill(self.color["Background"])
                            board.draw(screen)
                            self.draw_right_column(screen, self.get_player_score(board),
                                                   (False, False), (0,0,0,0), 0, 
                                                   clickable=False)
                            
                            pygame.display.update()
                            fps_limiter.tick(constants.FPS)



    def take_turn(self, screen, board, player_num):
        ''' Returns the turn that the player wants to do '''
        board.draw(screen)
        turn = [None, []] # first value is where the gen will happe, if it all.
        turn_chosen = False # list that contains info about the turns 
        held_down = {"mouse0": True, "mouse2": False, "esc": False,
                     "space": True, "f": False, "j": False}
        show_future = True 
        show_alive_for = False 
        turns_used = [0 for _ in range(self.num_of_players)]
        fps_limiter = pygame.time.Clock()
        while not turn_chosen:
            events = pygame.event.get()
            if check_quit(events) and not held_down["esc"]: # if esc pressed but was not last turn
                if len(turn[1]) == 0 and turn[0] is None:
                    return "Go Back"
                else:
                    if turn[0] == len(turn[1]): # if the gen needs to be undone 
                        turn[0] = None
                    else:
                        t = turn[1][-1]
                        del turn[1][-1] # gives back the turns used 
                        turns_used[player_num - 1]\
                            -= self.check_turn_is_valid(board, turn, player_num, t[0],
                            t[1], t[2], self.full_immune_kill[1])

                held_down["esc"] = True
            else:
                held_down["esc"] = False 

            x, y = pygame.mouse.get_pos()
            a, b = board.get_square(x, y)
            if 0 <= a < board.width + board.cushion and 0 <= b < board.height + board.cushion:
                kill = None 
                if not (held_down["mouse0"] or held_down["mouse2"])\
                    and self.players[player_num - 1].spare_turns > turns_used[player_num - 1]:

                    if pygame.mouse.get_pressed()[0]:
                        turn_validation =\
                            self.check_turn_is_valid(board, turn, player_num, a, b, False,
                                                     self.players[player_num - 1].spare_turns
                                                     - turns_used[player_num -1])

                        if turn_validation[0]:
                            kill = False 
                    elif pygame.mouse.get_pressed()[2]:
                        turn_validation =\
                            self.check_turn_is_valid(board, turn, player_num, a, b, True,
                                                     self.players[player_num - 1].spare_turns
                                                     - turns_used[player_num - 1])

                        if turn_validation[0]:
                            kill = True
                if kill is not None: # the turn is valid 
                    turn[1].append([a, b, kill])
                    turns_used[player_num - 1] += turn_validation[1]
            if pygame.key.get_pressed()[pygame.K_SPACE] and not held_down["space"]:
                turn_chosen = True 
            if pygame.key.get_pressed()[pygame.K_F] and not held_down["f"]:
                show_future = not show_future
                show_alive_for = False 
            if pygame.key.get_pressed()[pygame.K_J] and not held_down["j"]:
                show_alive_for = not show_alive_for
                show_future = False 
            on_button = [False, False] # checks whether the mouse is on either button

            if 2 * self.button_border_size < screen.get_width()\
                - x < self.right_column_size - 2 * self.button_border_size:
                if 0 < screen.get_height() - y - self.button_border_size < self.button_height:
                    if pygame.mouse.get_pressed()[0] and not held_down["mouse0"]:
                        turn_chosen = True 
                    on_button[0] = True 
                elif 0 > y - screen.get_height() + 3 * self.button_border_size\
                    + self.button_height > -self.button_height:
                    if pygame.mouse.get_pressed()[0] and turn[0] is None:
                        turn[0] = len(turn[1])
                    on_button[1] = True 

            self.draw_right_column(screen, self.get_player_score(board, turns=turn,
                                   player_num=player_num), on_button,
                                   turns_used, not turn[0] is None, update=False)
            if show_alive_for:
                board.show_alive(screen, self.text_size, self.color, turn, player_num)
            else:
                board.show_future(screen, turn, player_num, smaller=show_future)
            
            held_down["mouse0"] = pygame.mouse.get_pressed()[0]
            held_down["mouse2"] = pygame.mouse.get_pressed()[2]
            for key in (("space", "SPACE"), ("f", "f"), ("j", "j")): # update held_down dict
                held_down[key[0]] = eval("pygame.key.get_pressed()[pygame.K_%s]" % key[1])
            pygame.display.update()
            fps_limiter.tick(constants.FPS)
        return turn 



    def check_turn_is_valid(self, board, turns, player_num, a, b, kill, turns_left):
        '''
         Returns whether or not the turn is valid:

                        Return: [bool, int]

                                bool -> whether or not turn was valid
                                int -> num of turns the move should take
        '''
        pass 


    def get_player_score(self, board, turns=None, player_num=0):
        ''' 
        Returns num of cells each player has on board
        '''
        pass 


    def draw_right_column(self, screen, player_scores, on_button, turns_used,
                          generated, clickable=None, update=True):
                          '''
                          Column drawn on right-handside of screen'''
                          pass 


    def check_for_wins(self, board, turns, generations):
        ''' Check for wins '''
        pass 



class Help:
    ''' Help Class ''' 
    def __init__(self):
        '''
        Initialize Help constants
        '''
        self.section_gap_size = constants.H_SECTIONGAPSIZE
        self.text_size = constants.H_TEXTSIZE
        self.title_size = constants.H_TITLESIZE
        self.indent_size = constants.H_INDENTSIZE
        self.slider_width = constants.H_SLIDERWIDTH
        self.slider_gap_size = constants.H_SLIDERGAPSIZE
        self.slider_length = constants.H_SLIDERLENGTH
        self.width = constants.H_Width
        self.height = 600 
        self.scroll_amount = constants.H_SCROLLAMOUNT
        self.color = constants.H_COLOR
        self.surfaces = self.get_surfaces()
       


    def display(self, screen):
        '''
        Displays help page on the given screen
        '''
        pygame.display.set_caption("Conways Game of Life: Help Screen")
        pygame.display.set_mode((self.width, self.surfaces[0].get_height()))
        screen.fill(self.color["Background"])
        self.height = screen.get_height()
        slider_range = (self.slider_gap_size + self.slider_length // 2,
                        self.height - self.slider_gap_size - self.slider_length // 2)
        slider_centre = slider_range[0]
        help_rect = self.surfaces[0].get_rect()
        help_rect.topleft = (self.section_gap_size, self.section_gap_size)
        screen.blit(self.surfaces[0], help_rect)
        self.draw(screen, self.surfaces[1], slider_centre, slider_range)
        slider_last_turn = False 
        fps_limiter = pygame.time.Clock()

        while True:
            events = pygame.event.get()
            if check_quit(events):
                break 
        x, y = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            if slider_last_turn:
                y = max(min(y + slider_range - mouse_start, slider_range[1]), slider_range[0])
                self.draw(screen, self.surfaces[1], y, slider_range)
            elif -2 * self.slider_gap_size - self.slider_width < x - self.width < 0:
                slider_last_turn = 0 
                mouse_start = y 
                # if mouse not clicked 
                if not slider_centre - self.slider_length / 2 < y < slider_centre + self.slider_length / 2:
                    slider_centre = y 
                
        elif slider_last_turn:
            slider_last_turn = False
            slider_centre += y - mouse_start # reset position of the slider
        
        if x > (self.width - self.slider_width - self.section_gap_size) / 2 - self.slider_gap_size:
            draw = False 
            for e in events:
                if e.type == pygame.MOUSEBUTTONDOWN:
                    # scroll down
                    if e.button == 4:
                        slider_centre = max(slider_centre - self.scroll_amount, slider_range[0])
                        draw = True 
                    # scroll up
                    if e.button == 5:
                        slider_centre = min(slider_centre + self.scroll_amount, slider_range[1])
                        draw = True 

            if draw:
                self.draw(screen, self.surfaces[1], slider_centre, slider_range)
        
        pygame.display.update()
        fps_limiter.tick(constants.FPS)
        


    def draw(self, screen, help_surface, slider_centre, slider_range):
        '''
        Draw the right hand side bit of text and slider at given levels
        '''
        pygame.draw.rect(screen, self.color["Background"], 
                         ((self.width - self.slider_width - self.section_gap_size)
                         // 2 - self.slider_gap_size, 0, self.width, self.height))

        pygame.draw.rect(screen, self.color["Slider"],
                         (self.width - self.slider_gap_size - self.slider_width),
                         slider_centre - self.slider_length // 2,
                         self.slider_width, self.slider_length)
        
        help_rect = help_surface.get_rect()
        text_range = (self.section_gap_size, help_surface.get_height()
                      - self.height + 2 * self.section_gap_size)

        top_y = text_range[0] - (text_range[1] - text_range[0]) * (slider_centre - slider_range[0])\
                                // (slider_range[1] - slider_range[0])
        
        help_rect.topleft = (int((self.width - self.slider_width) // 2) + self.slider_gap_size, top_y)

        screen.blit(help_surface, help_rect) # sets position of help surface in relation to the screen
        pygame.display.update()


    def get_surfaces(self):
        '''
        Retrieves surfaces for the help screen. 

        Gets the help_info.txt and outputs it when key pressed for help.
        '''
        f = "help_info.txt"
        text = open(f).read().split("++") # splits into two sections 
        for section in range(len(text)):
            text[section] = text[section].split("\n") # split into lines
        help_surfaces = []

        for section in text:
            extra = 0 # checks to see how big the surface must be for the text to fit 
            for _ in range(2): # writes it onto the surfave
                help_surface = pygame.Surface(((self.width - self.slider_width)
                                         // 2 -self.section_gap_size - self.slider_gap_size, 
                                        extra))

                help_surface.fill(self.color["Background"])
                extra = 0 
                for line in section:
                    if line.startswith("**"): # ** == bold text
                        size = self.title_size
                        line = line[2:]
                    else:
                        size =self.text_size
                    indent = 0 
                    while line.startswith("--"): # -- === indented text
                        indent += 1 
                        line = line[2:]
                    extra += write(help_surface, indent * self.indent_size, extra, line,
                                self.color["Text"], size, 
                                max_len=help_surface.get_width()
                                            - indent * self.indent_size) + self.section_gap_size

            help_surfaces.append(help_surface)
        return help_surfaces



def write(self, screen, x, y, text, color, size, max_len=None, gap=0,Font=Font, rotate=0,
            alignment=("left", "top")):
            '''
            Puts text onto the screen at point x,y. 
            '''
            font_obj = pygame.Font.SysFont(Font, size)
            if text == "": # checks if its a blank line
                line = 1 
                extra_space = size 
            else:
                line = 0 
                extra_space = 0

            while len(text.split()) > 0: 
                line += 1 
                msg_surface_obj = pygame.transform.rotate(font_obj.render(text, False, color), rotate)
                used = len(text.split()) # amount of text not used thus far 
                while max_len is not None and msg_surface_obj.get_width() > max_len:
                    used -= 1 
                    msg_surface_obj = pygame.transform.rotate(font_obj.render(" ".join(text.split()[:used]),
                                                              False, color), rotate)
                    
                    msg_surface_obj = msg_surface_obj.get_rect()
                    a, b = msg_surface_obj.get_size()

                    if alignment[0] == "centre":
                        new_x = x - a // 2
                    else:
                        new_x = x 
                    if alignment[1] == "centre":
                        new_y = y - b // 2
                    elif alignment[1] == "bottom":
                        new_y = y - b
                    else:
                        new_y = y 

                    msg_surface_obj.topleft = (new_x, new_y) # coordinates of new merged object 
                    screen.blit(msg_surface_obj, msg_surface_obj.get_height() + gap)
                    text = " ".join(text.split()[used:]) # delete text 

                return extra_space



def check_quit(self, events):
    '''
    Checks whether the player tried to quit the game.

    Bool: Returned for corresponding ESC key pressed.
    '''
    for event in events:
        if event.type == pygame.QUIT:
            quit_game()
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            return True 
    
    return False 


def quit_game(self):
    ''' Quits Game ''' 
    pygame.quit()
    sys.exit(0)



