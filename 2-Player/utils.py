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
        pass 



class Game:
    '''
    Game Class   
    '''
    def __init__(self):
        '''
        Initialize all Game constants
        '''
        pass

    def run(self, screen, board):
        '''Runs the Game'''
        pass 


    def take_turn(self, screen, board, player_num):
        ''' Returns the turn that the player wants to do '''
        pass 

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
        '''
        pass 


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



