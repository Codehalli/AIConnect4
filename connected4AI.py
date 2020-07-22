# The purpose of this project was to create a GUI based AI connect 4 game, implementing the Minimax Algorithm
# connected4AI.py
# By Pranav Rao

import numpy as np # library to work with arrays
import pygame # libary that generates the actual game screen widget
import sys #access certain perameters for run time efficiency
import math #basic libary to calculate certain math functions
import random #random number generator

#global color variables used by the pygame graphcis
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

#global column and row count
ROW_NUM = 6
COL_NUM = 7

#This is assigned to determine who gets to go first based on the random
# number
PLAYER = 0
AI = 1

# This Global variable is to distinguish players
PLAYER_P = 1
AI_P = 2

# condition to check the state
EMPTY = 0
BOX = 4


# This function will create matrix
def create_board():
    board = np.zeros((ROW_NUM, COL_NUM))
    return board


# This function will drop the piece in proper location
def drop_piece(board, row, col, pieces):
    board[row][col] = pieces
    pass


# This function will check if the 0 and return it
def is_valid_location(board, col):
    return board[ROW_NUM - 1][col] == 0


# This function find the next open row based on the pieces
def get_next_open_row(board, col):
    for r in range(ROW_NUM):
        if board[r][col] == 0:
            return r
    pass


# Prints the board
def print_board(board):
    print(np.flip(board, 0))


# This function purpose to check the different connect 4 combinations, therefore -3 for col or row
def get_wining_move(board, piece):
    # This will check for horizontal wins
    for c in range(COL_NUM - 3):
        for r in range(ROW_NUM):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][
                c + 3] == piece:
                return True

    # This will check for vertical wins
    for c in range(COL_NUM):
        for r in range(ROW_NUM - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][
                c] == piece:
                return True

    # This will check for diagonal-positive since only 1 piece inside the row or column
    for c in range(COL_NUM - 3):
        for r in range(ROW_NUM - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][
                c + 3] == piece:
                return True

    # This will check for diagonal-negative since only 1 piece inside the row or column
    for c in range(COL_NUM - 3):
        for r in range(3, ROW_NUM):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][
                c + 3] == piece:
                return True


# This function will evaluate the condition of a 4 frame and rank the order of importances to place a piece for the AI
def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_P
    if piece == PLAYER_P:
        opp_piece = AI_P
    
    # Goes from 4 to 3 to 2
    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 10
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2

    # Exception case
    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4
    
    return score

# This function helps determine the possible condtions for the AI
def score_position(board, piece):
    score = 0
    # Score
    center_array = [int(i) for i in list(board[:, COL_NUM // 2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    ##Horizontal
    for r in range(ROW_NUM):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COL_NUM - 3):
            window = row_array[c:c + BOX]
            score += evaluate_window(window, piece)

    ##Vertical
    for c in range(COL_NUM):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW_NUM - 3):
            window = col_array[r:r + BOX]
            score += evaluate_window(window, piece)

    ##Positive Slope Digaonal
    for r in range(ROW_NUM - 3):
        for c in range(COL_NUM - 3):
            window = [board[r + i][c + i] for i in range(BOX)]
            score += evaluate_window(window, piece)

    ##negative slope diagonal
    for r in range(ROW_NUM - 3):
        for c in range(COL_NUM - 3):
            window = [board[r + 3 - i][c + i] for i in range(BOX)]
            score += evaluate_window(window, piece)

    return score

#This node funtion gets the the winning board or valid based on the AI performance
def is_terminal_node(board):
    return get_wining_move(board, PLAYER_P) or get_wining_move(board, AI_P) or len(get_valid_location(board)) == 0

#Eessntially This algorithm is the main Algorithm that makes AI smarter. The Minimax
def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_location = get_valid_location(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if get_wining_move(board, AI_P):
                return None, 100000000000000000
            elif get_wining_move(board, PLAYER_P):
                return None, -10000000000000000
            else:#game is over/no valid movies
                return 0
        else:
            return None, score_position(board, AI_P)
#Maximimizng option to winthe game
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_location)
        for col in valid_location:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_P)
            new_score = minimax(b_copy, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
        alpha = max(alpha, value) #alpha-beta pruning alg
            if alpha >= beta:
                break
        return column, value
    else:  # Minimizing player
        value = math.inf
        column = random.choice(valid_location)
        for col in valid_location:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_P)
            new_score = minimax(b_copy, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value) #alpha-beta pruning alg
            if alpha >= beta:
                break
        return col, value

# Function checks to see if its a valid location
def get_valid_location(board):
    valid_locations = []
    for col in range(COL_NUM):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations

# Function based on the above funciton evaluate window it determines the best move
def choose_best_move(board, piece):
    valid_location = get_valid_location(board)
    best_score = -10000
    best_col = random.choice(valid_location)
    for col in valid_location:
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col
    return best_col


# drawing the gui board
def draw_board(board):
    for c in range(COL_NUM):
        for r in range(ROW_NUM):
            pygame.draw.rect(screen, BLUE, (c * SQUARE_SIZE, r * SQUARE_SIZE + SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(screen, BLACK, (
                int(c * SQUARE_SIZE + SQUARE_SIZE / 2), int(r * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE / 2)), Rad)

    for c in range(COL_NUM):
        for r in range(ROW_NUM):
            if board[r][c] == PLAYER_P:
                pygame.draw.circle(screen, RED, (
                    int(c * SQUARE_SIZE + SQUARE_SIZE / 2),
                    height - int(r * SQUARE_SIZE + SQUARE_SIZE / 2)),
                                   Rad)
            elif board[r][c] == AI_P:
                pygame.draw.circle(screen, YELLOW, (
                    int(c * SQUARE_SIZE + SQUARE_SIZE / 2),
                    height - int(r * SQUARE_SIZE + SQUARE_SIZE / 2)),
                                   Rad)
# Updates the game once is choose the move
    pygame.display.update()


# This will display the board layout
board = create_board()
print_board(board)
game_over = False
turn = random.randint(PLAYER, AI)

# Going to create the game into game library
pygame.init()

# This is the specifications for the window size
SQUARE_SIZE = 100

#This is giving the widght and height of the board size
width = COL_NUM * SQUARE_SIZE
height = (ROW_NUM + 1) * SQUARE_SIZE
size = (width, height)

#This is for the circle radius in the game
Rad = int(SQUARE_SIZE / 2 - 5)

#This command will draw the board size and redraw after each moves
screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

#This is the font of the text
myfont = pygame.font.SysFont("monospace", 75)

# While loop to make the game continuing till its over
while not game_over:

    # condition when the game is running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        # Mouse motion based on the location of the matrix
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, RED, (posx, int(SQUARE_SIZE / 2)), Rad)
        pygame.display.update()

         # Mouse button clicked
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
            # Player one input
            if turn == PLAYER:
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARE_SIZE))

                # This is if cases for player 1 turns
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, PLAYER_P)

                    # Checks if Player 1 wins and ends the while loop
                    if get_wining_move(board, PLAYER_P):
                        label = myfont.render("Play 1 Wins!!", 1, RED)
                        screen.blit(label, (40, 10))
                        game_over = True
                    #Keeps taking turns
                    turn += 1
                    turn = turn % 2
                    #draws the board again
                    print_board(board)
                    draw_board(board)

    # Player two input
    if turn == AI and not game_over:
        
        #essentially calls the minimax AI algorithm
        col, minimax_score = minimax(board, 4, -math.inf, math.inf, True)

        if is_valid_location(board, col):
            # pygame.time.wait(500)
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, AI_P)

            # Checks if Player 1 wins and ends the while loop
            if get_wining_move(board, AI_P):
                label = myfont.render("Player 2 Wins!!", 1, YELLOW)
                screen.blit(label, (40, 10))
                game_over = True

            print_board(board)  # prints the grid
            draw_board(board)

            # This will keep alternating between player 1 and 2
            turn += 1
            turn = turn % 2
    # once the game is over it will wait for about 35 seconds and then terminate
    if game_over:
        pygame.time.wait(3500)
