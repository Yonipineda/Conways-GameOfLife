# Constant Parameters 

'''
Initial Explainer:

            M -> Main Menu Parameters 
            S -> Simulator Parameters 
            G -> Game Mode Parameters 
'''

## General Aspects 
FONT = "Arial"  #  The font used in the game


FPS = 30  # Default Frames Per Second(fps)


## Main Menu Parameters
M_BUTTONHEIGHT= 90  # The height of the buttons

M_BUTTONWIDTH = 450  # The width of the buttons

M_BUTTONBORDER = 4  # The thickness of the borders on the buttons


M_BUTTONGAPSIZE = 40  # The gap between each button

M_SIDEGAPSIZE = 250  
#  The size of the gap at each side (between the button and the edge of the screen)

M_TEXTSIZE = 30  #  The size of the text in the buttons

M_TITLEGAPSIZE = 60  # The gap between the title and the top of the screen

M_TitleTextSize = 60  # Size of the text on the title 

M_COLOR = {"Border": (0, 0, 0), 
            #  The color of the borders on the buttons
            
            "Text": (0, 0, 0),  
            #  The color of all text
            
            "Hover": (0, 255, 100),  
            #  The color of the text when you hover over a button
            
            "Background": (120, 120, 120)}  
            #  The color of the background


## Simulator Parameters 
S_WIDTH = 40  # How many squares wide the board is 

S_HEIGHT = 25  # Squares in height the board is

S_SIZE = 22  # The size of the sides of each square (in pixels)

S_CELLGAP = 2  # The gap between each cell

S_WRAP = True  # Whether the board wraps around on itself

S_CUSHION = 0  # How far the board extends beyond the visible amount

S_SETUPCHANCES = (0, 0)  # Chances of a cell being dead or alive when game starts

S_SLIDERSIZE = 50  # The gap at the side of the board for the FPS slider

S_HIGHLIGHTSIZE = 5  # The size of the slider pointer

S_NUMOFNOTCHES = 9  # The number of notches on the slider

S_NOTCHLENGTH = 10  # The (horizontal) length of the notches

S_SPEEDSIZE = 20  # The size of the writing of "Speed" next to the GPS slider

S_GPS = 10 # How many Generations Per Seconds at the start of the game

S_TOPGPS = 50  # The GPS at the top of the slider.

S_BOTTOMGPS = 0.5  # The GPS at the bottom of slider.

S_COLOR = {"Alive": (0, 0, 0),  # (0, 0, 0)
            #  The color of an alive cell
            
            "Dead": (255, 255, 255), 
            #  The color of a dead cell
            
            "Highlighter": (0, 255, 100),
            #  The color of the slider pointer when active
            
            "Background": (120, 120, 120), 
            #  The color of the background
            
            "Text": (0, 0, 0),  # (0, 0, 0)
            #  The color of the text
            
            "Unselected": (160, 160, 160)} 
            #  The color of the slider pointer whe not active


## Game Mode Parameters 

G_WIDTH = 24  # How many squares wide the board is - Must be divisible by 2

G_HEIGTH = 16  # Squares height the board is - Must be divisible by 2

G_SIZE = 36  # The size of the sides of each square (in pixels)

G_CELLGAP = 2  # The gap between each cell

G_NUMOFPLAYERS = 2 # How many players there are : 2-4

G_PlayerNames = ["Player1", "Player2", "Player3", "Player4"] # Player's name

G_PREVIEWSIZE = 18  # The size of the cells in preview mode

G_SETUPCHANCES = (10, 2, 1, 1, 1)  # The likleyhood of each player's cells spawning in a cell 
                                # (first one is chance of none spawning) at the start of a game

G_TEXTSIZE = 32  # The size of the text

G_RIGHTCOLUMNSIZE = 150  # The size of the column on the right

G_BUTTONHEIGHT = 50  # The height of the button

G_BUTTONBORDERSIZE = 3  # The size of the border of the button

G_WINMESSAGEWIDTH = 500  # The width of the win message

G_WINMESSAGEHEIGHT = 300  # The height of the win message

G_COLOR = {"Player1": (150, 205, 80), 
            #  The color of Player 1's cells
            
            "Player2": (0, 175, 240),  
            #  The color of Player 2's cells
            
            "Player3": (255, 210, 50),  
            #  The color of  Player 3's cells
            
            "Player4": (190, 120, 150),  
            #  The color of  Player 4's cells
            
            "Dead": (255, 255, 255), 
            #  The color of dead cells
            
            "Highlighter": (0, 255, 100), 
            #  The color of the button when your mouse is hovering over it
            
            "Unselectable": (200, 200, 200), 
            #  The color of a button that is not clickable
            
            "Background": (120, 120, 120),  
            #  The color of the background
            
            "Text": (0, 0, 0),  
            #  The color of the text
            
            "ButtonBorder": (0, 0, 0)}  
            #  The color of the border of the button



G_PARTIMMUNE = True  # Whether or not the game creates part immune cells

G_PARTIMMUNETIME = 4  # The number of turns a cell has to be alive before it becomes part immune
# (doesn't die unless your opponent kills it)

G_PARTIMMUNEKILL = 2  # The number of turns it costs to kill a part immune cell

G_FULLIMMUNE = True  # Whether or not the game creates full immune cells

G_FULLIMMUNETIME = 8  # The number of turns a cell has to be alive before it becomes fully immune
# (nothing can kill it except you). Must be be bigger than G_PartImmuneTime

G_FULLIMMUNEKILL = 4  # The number of turns it costs to kill a fully immune cell



G_ISTURNLIMIT = True  # Whether there is a limit on the amount of turns in a game

G_TURNLIMIT = 20  # The amount of turns each player can have before the game ends

G_ISGENLIMIT = False  # Whether there is a limit on the amount of generations in a game

G_GENLIMIT = 10  # The amount of generations in total before the game ends

G_BOARDAMOUNTWIN = True  # Whether the game ends when a player gets a certain amount of the board

G_BOARDAMOUNT = 0.25  # The amount of the board a player must get to win: an amount between 0 and 1

G_PLAYERAMOUNTWIN = True  # Whether the game ends when a player has a certain amount of cells more than the opponent

G_PLAYERAMOUNT = 0.25 # If one player has this ratio of cells compared to his opponent that player loses



G_STARTINGTURNS = 3  # The amount of turns each player starts with.

G_FAIRERTURNS = True  # if this is True, instead of taking it in turns to go,
# the first player starting with only half as many turns as you get per round.

G_TURNSPERROUND = 2 # How many turns each player gets per round.
# If FairerTurns is True, the first player gets half this many on their first go.



## Help Screen Parameters
### Probably wont get around to implementing this

H_SECTIONGAPSIZE = 5  # The size of the gap between the 2 sections of text

H_TEXTSIZE = 20 # The size of the text

H_TITLESIZE = 30  # The size of titles

H_INDENTSIZE = 40 # The size of indents

H_SLIDERWIDTH = 10 # The width of the slider

H_SLIDERGAPSIZE = 5  # The gap between the slider and the edge/text

H_SLIDERLENGTH = 100  # The length of the slider

H_Width = 1000 + H_SLIDERWIDTH + H_SLIDERGAPSIZE # The width of the window

H_SCROLLAMOUNT = 50  # The amount scrolled with each turn of the wheel

H_COLOR = {"Background": (120, 120, 120), 
            #  The color of the background

            "Text": (0, 0, 0),  
            #  The color of text

            "Slider": (0, 255, 100)} 
            #  The color of the slider