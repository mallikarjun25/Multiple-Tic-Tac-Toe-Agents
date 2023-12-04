# Importing classes

from random import choice
from math import inf

# Initialize the game board
board = [[0, 0, 0],
         [0, 0, 0],
         [0, 0, 0]]

# Map the numerical values on the board to characters
def createGameBoard(board):
    chars = {1: 'X', -1: 'O', 0: ' '}
    
    # Print the game board
    for x in board:
        for y in x:
            ch = chars[y]
            print(f'| {ch} |', end='')
        print('\n' + '---------------')
    print('===============')


# Clear the game board by setting all cells to 0
def resetBoard(board):
    for x, row in enumerate(board):
        for y, col in enumerate(row):
            board[x][y] = 0

def checkWinningPlayer(board, player):
    # Define the winning conditions
    options = [[board[0][0], board[0][1], board[0][2]],
                     [board[1][0], board[1][1], board[1][2]],
                     [board[2][0], board[2][1], board[2][2]],
                     [board[0][0], board[1][0], board[2][0]],
                     [board[0][1], board[1][1], board[2][1]],
                     [board[0][2], board[1][2], board[2][2]],
                     [board[0][0], board[1][1], board[2][2]],
                     [board[0][2], board[1][1], board[2][0]]]

    # Check if the player has won
    if [player, player, player] in options:
        return True

    return False

# Check if either player has won the game
def isGameWon(board):
    return checkWinningPlayer(board, 1) or checkWinningPlayer(board, -1)

# Print the result of the game
def showGameResult(board):
    if checkWinningPlayer(board, 1):
        print('X has won!, Min Max  ' + '\n')

    elif checkWinningPlayer(board, -1):
        print('O\'s have won!, Alpha Beta Pruning  ' + '\n')

    else:
        print('Draw' + '\n')

# Find and return the coordinates of blank cells on the board
def blanks(board):
    blank = []
    for x, row in enumerate(board):
        for y, col in enumerate(row):
            if board[x][y] == 0:
                blank.append([x, y])

    return blank

# Check if the game board is full
def boardFull(board):
    if len(blanks(board)) == 0:
        return True
    return False

# Set the move on the game board
def setMove(board, x, y, player):
    board[x][y] = player

# Allow the player to make a move
def playerMove(board):
    e = True
    moves = {1: [0, 0], 2: [0, 1], 3: [0, 2],
             4: [1, 0], 5: [1, 1], 6: [1, 2],
             7: [2, 0], 8: [2, 1], 9: [2, 2]}
    while e:
        try:
            move = int(input('Enter a number between 1-9: '))
            if move < 1 or move > 9:
                print('Invalid Move! Try again!')
            elif not (moves[move] in blanks(board)):
                print('Invalid Move! Try again!')
            else:
                setMove(board, moves[move][0], moves[move][1], 1)
                createGameBoard(board)
                e = False
        except(KeyError, ValueError):
            print('Enter a number!')


 # Get the score of the current game state
def getScore(board):
    if checkWinningPlayer(board, 1):
        return 10

    elif checkWinningPlayer(board, -1):
        return -10

    else:
        return 0
    
# Implement the minimax algorithm for the computer player
def minimax(state, depth, player):
    if player == -1:
        best = [-1, -1, -10000000]
    else:
        best = [-1, -1, +10000000]

    if depth == 0 or isGameWon(state):
        score = getScore(state)
        return [-1, -1, score]

    for cell in blanks(state):
        x, y = cell[0], cell[1]
        state[x][y] = player
        score = minimax(state, depth - 1, -player)
        state[x][y] = 0
        score[0], score[1] = x, y

        if player == -1:
            if score[2] > best[2]:
                 # max value
                best = score 
        else:
            if score[2] < best[2]:
                # min value
                best = score  

    return best

# Implement the minimax algorithm with alpha-beta pruning
def abminimax(board, depth, alpha, beta, player):
    row = -1
    col = -1
    if depth == 0 or isGameWon(board):
        return [row, col, getScore(board)]

    else:
        for cell in blanks(board):
            setMove(board, cell[0], cell[1], player)
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

            setMove(board, cell[0], cell[1], 0)

            if alpha >= beta:
                break

        if player == 1:
            return [row, col, alpha]

        else:
            return [row, col, beta]

# Make a move for the computer player O
def o_comp(board):
    if len(blanks(board)) == 9:
        #x = choice([0, 1, 2])
        #y = choice([0, 1, 2])
        move = minimax(board, len(blanks(board)), +1)
        x, y = move[0], move[1]
        setMove(board, x, y, -1)
        createGameBoard(board)

    else:
        result = abminimax(board, len(blanks(board)), -inf, inf, -1)
        setMove(board, result[0], result[1], -1)
        createGameBoard(board)

def x_comp(board):
    # If the board is empty (i.e., the game just started), make a random move
    if len(blanks(board)) == 9:
        #x = choice([0, 1, 2])
        #y = choice([0, 1, 2])
        move = minimax(board, len(blanks(board)), +1)
        x, y = move[0], move[1]
        setMove(board, x, y, 1)
        createGameBoard(board)

    else:
        result = abminimax(board, len(blanks(board)), -inf, inf, 1)
        setMove(board, result[0], result[1], 1)
        createGameBoard(board)

# Make a move based on the player and mode
def makeMove(board, player, mode):
    if mode == 1:
        if player == 1:
            minimax(board,len(blanks(board)),player)

        else:
            o_comp(board)
    else:
        if player == 1:
            o_comp(board)
        else:
            x_comp(board)

def pvc():
    currentPlayer = 1

    while not (boardFull(board) or isGameWon(board)):
        makeMove(board, currentPlayer, 1)
        currentPlayer *= -1
        makeMove(board, currentPlayer, -1)
        currentPlayer *= 1

    showGameResult(board)

# Driver Code
print("=================================================")
print("TIC-TAC-TOE using MINIMAX with MIN MAX OVER ALPHA-BETA Pruning")
print("=================================================")
pvc()