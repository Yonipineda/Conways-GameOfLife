import random
import sys
import pygame


class LifeGame:

    def __init__(self, screen_width=800, screen_height=600, cell_size=10, alive_color=(0, 255, 255),
                 dead_color=(0, 0, 0), max_fps=10):
        """
        Initializes parameters 
        """
        pygame.init()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.cell_size = cell_size
        self.alive_color = alive_color
        self.dead_color = dead_color

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clear_screen()
        pygame.display.flip()

        self.max_fps = max_fps

        self.active_grid = 0
        self.num_cols = int(self.screen_width / self.cell_size)
        self.num_rows = int(self.screen_height / self.cell_size)
        self.grids = []
        self.init_grids()
        self.set_grid()

        self.paused = False
        self.game_over = False

    def init_grids(self):
        """
        creates and stores default active and inactive grid. 
        """
        def create_grid():
            """
            generates an empty 2 dim array
            """
            rows = []
            for row_num in range(self.num_rows):
                list_of_columns = [0] * self.num_cols
                rows.append(list_of_columns)
            return rows
        self.grids.append(create_grid())
        self.grids.append(create_grid())

    def set_grid(self, value=None, grid=0):
        """
        Sets the grid
        """
        for r in range(self.num_rows):
            for c in range(self.num_cols):
                if value is None:
                    cell_value = random.randint(0, 1)
                else:
                    cell_value = value
                self.grids[grid][r][c] = cell_value

    def draw_grid(self):
        """
        draws grid given the grid and cell state.
        """
        self.clear_screen()
        for c in range(self.num_cols):
            for r in range(self.num_rows):
                if self.grids[self.active_grid][r][c] == 1:
                    color = self.alive_color
                else:
                    color = self.dead_color
                pygame.draw.circle(self.screen,
                                   color,
                                   (int(c * self.cell_size + (self.cell_size / 2)),
                                    int(r * self.cell_size + (self.cell_size / 2))),
                                   int(self.cell_size / 2),
                                   0)
        pygame.display.flip()

    def clear_screen(self):
        """
        clear screen
        """
        self.screen.fill(self.dead_color)

    def get_cell(self, row_num, col_num):
        """
        get the alive or dead state of a specific cell in grid 
        """
        try:
            cell_value = self.grids[self.active_grid][row_num][col_num]
        except:
            cell_value = 0
        return cell_value

    def check_cell_neighbors(self, row_index, col_index):
        """
        Logic to determine if a cell is over populated, underpopulated, or is to be birthed.
        Checks if its alive, dead, born. Following rules of game 
        """
        num_alive_neighbors = 0
        num_alive_neighbors += self.get_cell(row_index - 1, col_index - 1)
        num_alive_neighbors += self.get_cell(row_index - 1, col_index)
        num_alive_neighbors += self.get_cell(row_index - 1, col_index + 1)

        num_alive_neighbors += self.get_cell(row_index, col_index - 1)
        num_alive_neighbors += self.get_cell(row_index, col_index + 1)

        num_alive_neighbors += self.get_cell(row_index + 1, col_index - 1)
        num_alive_neighbors += self.get_cell(row_index + 1, col_index)
        num_alive_neighbors += self.get_cell(row_index + 1, col_index + 1)

        # Rules for life and death
        if self.grids[self.active_grid][row_index][col_index] == 1:
            ''' Is Alive ''' 
            if num_alive_neighbors > 3:  # overpopulated
                return 0
            if num_alive_neighbors < 2:  # underpopulated 
                return 0
            if num_alive_neighbors == 2 or num_alive_neighbors == 3:
                return 1
        elif self.grids[self.active_grid][row_index][col_index] == 0:
            ''' Is dead '''
            if num_alive_neighbors == 3:
                return 1  # birth

        return self.grids[self.active_grid][row_index][col_index]

    def update_generation(self):
        """
        Inspects current gen and prepares the next one.
        """
        self.set_grid(0, self.inactive_grid())
        for r in range(self.num_rows - 1):
            for c in range(self.num_cols - 1):
                next_gen_state = self.check_cell_neighbors(r, c)
                self.grids[self.inactive_grid()][r][c] = next_gen_state
        self.active_grid = self.inactive_grid()

    def inactive_grid(self):
        """
        Gets the index of an inactive grid. 

        Ex: If active grid == 0, returns 1. Vice versa
        """
        return (self.active_grid + 1) % 2

    def handle_events(self):
        '''
        Event Handler
        
        Params: 
                s -> Start
                r -> Randomize 
                q -> Quit 
        '''
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                print("Key has been pressed.")
                if event.unicode == 's':
                    print("Pausing the game.")
                    if self.paused:
                        self.paused = False
                    else:
                        self.paused = True

                elif event.unicode == 'r':
                    print("Randomizing the grid.")
                    self.active_grid = 0
                    self.set_grid(None, self.active_grid)  # randomize
                    self.set_grid(0, self.inactive_grid())  
                    self.draw_grid()

                elif event.unicode == 'q':
                    print("Exiting Game.")
                    self.game_over = True
            if event.type == pygame.QUIT:
                sys.exit()

    def run_game(self):
        """
       Start the game. use the event handler keys to randomize, pause, or quit
        """

        # time 
        clock = pygame.time.Clock()

        while True:
            if self.game_over:
                return

            self.handle_events()

            if not self.paused:
                self.update_generation()
                self.draw_grid()

            clock.tick(self.max_fps)
