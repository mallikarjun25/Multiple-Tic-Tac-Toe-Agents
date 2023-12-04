# Import necessary modules
from random import choice
from math import inf

# Global variables to count the number of nodes expanded for each algorithm
minmax_count = 0
abminmax_count = 0

# 3x3 Tic-Tac-Toe board representation
board = [[0, 0, 0],
         [0, 0, 0],
         [0, 0, 0]]

# Function to display the Tic-Tac-Toe board
def displayGameBoard(board):
    chars = {1: 'X', -1: 'O', 0: ' '}
    for x in board:
        for y in x:
            ch = chars[y]
            print(f'| {ch} |', end='')
        print('\n' + '---------------')
    print('===============')
    print('Next move')


# Function to clear the Tic-Tac-Toe board
def resetBoard(board):
    for x, row in enumerate(board):
        for y, col in enumerate(row):
            board[x][y] = 0

# Function to check if a player has won
def checkWinningPlayer(board, player):
    conditions = [[board[0][0], board[0][1], board[0][2]],
                     [board[1][0], board[1][1], board[1][2]],
                     [board[2][0], board[2][1], board[2][2]],
                     [board[0][0], board[1][0], board[2][0]],
                     [board[0][1], board[1][1], board[2][1]],
                     [board[0][2], board[1][2], board[2][2]],
                     [board[0][0], board[1][1], board[2][2]],
                     [board[0][2], board[1][1], board[2][0]]]

    # Check each winning condition
    if [player, player, player] in conditions:
        return True

    return False

# Function to check if the game is won
def checkGameStatus(board):
    return checkWinningPlayer(board, 1) or checkWinningPlayer(board, -1)

# Function to print the result of the game
def displayGameStatus(board):
    if checkWinningPlayer(board, 1):
        print('X has won!, Alpha Beta Pruning  ' + '\n')
        print('No of nodes expanded by minmax is',minmax_count)
        print('No of nodes expanded by alpha beta pruning is',abminmax_count)

    elif checkWinningPlayer(board, -1):
        print('O\'s have won!, Min Max  ' + '\n')
        print('No of nodes expanded by minmax is',minmax_count)
        print('No of nodes expanded by alpha beta pruning is',abminmax_count)

    else:
        print('No more moves, Its a Draw' + '\n')
        print('No of nodes expanded by minmax is',minmax_count)
        print('No of nodes expanded by alpha beta pruning is',abminmax_count)

# Function to get the list of blank positions on the board
def checkBlanks(board):
    blank = []
    for x, row in enumerate(board):
        for y, col in enumerate(row):
            if board[x][y] == 0:
                blank.append([x, y])

    return blank

# Function to check if the Tic-Tac-Toe board is full
def checkBoardFullStatus(board):
    if len(checkBlanks(board)) == 0:
        return True
    return False

# Function to set a move on the board
def set_Move(board, x, y, player):
    board[x][y] = player

# Function to get the score of the current board position
def retrieveScore(board):
    if checkWinningPlayer(board, 1):
        return 10

    elif checkWinningPlayer(board, -1):
        return -10

    else:
        return 0
    
# Minimax algorithm for game tree traversal    
def minimax(state, depth, player):
    global minmax_count
    minmax_count += 1
    if player == -1:
        best = [-1, -1, -inf]
    else:
        best = [-1, -1, +inf]

    if depth == 0 or checkGameStatus(state):
        score = retrieveScore(state)
        return [-1, -1, score]

    for cell in checkBlanks(state):
        x, y = cell[0], cell[1]
        state[x][y] = player
        score = minimax(state, depth - 1, -player)
        state[x][y] = 0
        score[0], score[1] = x, y

        if player == -1:
            if score[2] > best[2]:
                best = score  # max value
        else:
            if score[2] < best[2]:
                best = score  # min value

    return best

# Alpha-Beta Pruning algorithm for game tree traversal
def abminimax(board, depth, alpha, beta, player):
    global abminmax_count
    abminmax_count += 1
    row = -1
    col = -1
    if depth == 0 or checkGameStatus(board):
        return [row, col, retrieveScore(board)]

    else:
        for cell in checkBlanks(board):
            set_Move(board, cell[0], cell[1], player)
            score = abminimax(board, depth - 1, alpha, beta, -player)
            if player == 1:
                # X is always the max player
                if score[2] > alpha:
                    alpha = score[2]
                    row = cell[0]
                    col = cell[1]

            else:
                if score[2] < beta:
                    beta = score[2]
                    row = cell[0]
                    col = cell[1]

            set_Move(board, cell[0], cell[1], 0)

            if alpha >= beta:
                break

        if player == 1:
            return [row, col, alpha]

        else:
            return [row, col, beta]

# Function for the computer player 'O' to make a move
def o_comp(board):
    if len(checkBlanks(board)) == 9:
        move = minimax(board, len(checkBlanks(board)), -1)
        x, y = move[0], move[1]
        set_Move(board, x, y, -1)
        displayGameBoard(board)

    else:
        result = abminimax(board, len(checkBlanks(board)), -inf, inf, -1)
        set_Move(board, result[0], result[1], -1)
        displayGameBoard(board)

# Function for the computer player 'X' to make a move
def x_comp(board):
    if len(checkBlanks(board)) == 9:
        move = minimax(board, len(checkBlanks(board)), +1)
        x, y = move[0], move[1]
        set_Move(board, x, y, 1)
        displayGameBoard(board)

    else:
        result = abminimax(board, len(checkBlanks(board)), -inf, inf, 1)
        set_Move(board, result[0], result[1], 1)
        displayGameBoard(board)

# Function to facilitate the move based on the current player and mode
def make_Move(board, player, mode):
    if mode == 1:
        if player == 1:
            x_comp(board)
        else:
            o_comp(board)
    else:
        if player == 1:
            o_comp(board)
        else:
            x_comp(board)

def adver_search():
    current_Player = -1
    while not (checkBoardFullStatus(board) or checkGameStatus(board)):
        make_Move(board, current_Player, 1)
        current_Player *= -1

    displayGameStatus(board)

print("=================================================")
print("TIC-TAC-TOE using MINIMAX with ALPHA-BETA Pruning")
print("=================================================")
adver_search()
