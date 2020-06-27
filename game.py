import pygame
from pygame import display, event
import os, time

import config

pieces = []
board = []
player_turn = 1

pygame.init()

display.set_caption('Connect Four')

# screen = display.set_mode((config.SCREEN_SIZE, config.SCREEN_SIZE))

def create_board():
    global board
    for r in range(config.BOARD_ROWS):
        row = []
        for c in range(config.BOARD_COLS):
            row.append(0)
        board.append(row)

def print_board():
    global board
    print(board)

def draw_board():
    global board
    for row in range()


def get_player_move(player_turn):
    input_str = 'Player ' + str(player_turn) + ' please make a move (0-' + str(config.BOARD_COLS - 1) + '): '
    move = input(input_str)
    return int(move) if is_valid_move(move) and is_valid_location(int(move)) else None

def is_valid_move(move):
    global board
    try:
        move = int(move)
        assert move >= 0 & move < config.BOARD_COLS
        return True
    except:
        print('Invalid move. Please input an int between 0-6.')
        return False

def is_valid_location(move):
    global board
    return board[0][move] == 0

def place_piece(player_turn, move):
    global board
    row = 0
    while row < config.BOARD_ROWS and board[row][move] == 0:
        row += 1
    row -= 1
    board[row][move] = player_turn
    return

def check_win(player_turn):
    global board
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == player_turn:
                horWin = _check_horizontal(player_turn, row)
                verWin = _check_vertical(player_turn, col)
                posDiagWin = _check_pos_diagonal(player_turn, row, col)
                negDiagWin = _check_neg_diagonal(player_turn, row, col)
                if horWin or verWin or posDiagWin or negDiagWin:
                    return True
    return False

def _check_horizontal(player_turn, row):
    global board
    return board[row].count(player_turn) == 4

def _check_vertical(player_turn, col):
    global board
    piece_count = 0
    for row in board:
        if row[col] == player_turn:
            piece_count += 1
    return piece_count == 4

def _check_pos_diagonal(player_turn, row, col):
    global board
    rowIter = row
    colIter = col
    count = 0
    while (rowIter >= 0 and rowIter < len(board) and
          colIter >= 0 and colIter < len(board[0])):
        if count == 4:
            return True
        if board[rowIter][colIter] == player_turn:
            count = count + 1
        rowIter -= 1
        colIter += 1

    rowIter = row - 1
    colIter = col - 1
    while (rowIter >= 0 and rowIter < len(board) and
          colIter >= 0 and colIter < len(board[0])):
        if count == 4:
            return True
        if board[rowIter][colIter] == player_turn:
            count = count + 1
        rowIter += 1
        colIter -= 1
    return False

def _check_neg_diagonal(player_turn, row, col):
    global board
    rowIter = row
    colIter = col
    count = 0
    while (rowIter >= 0 and rowIter < len(board) and
          colIter >= 0 and colIter < len(board[0])):
        if count == 4:
            return True
        if board[rowIter][colIter] == player_turn:
            count = count + 1
        rowIter -= 1
        colIter -= 1

    rowIter = row + 1
    colIter = col + 1
    while (rowIter >= 0 and rowIter < len(board) and
          colIter >= 0 and colIter < len(board[0])):
        if count == 4:
            return True
        if board[rowIter][colIter] == player_turn:
            count = count + 1
        rowIter += 1
        colIter += 1
    return False

def init():
    create_board()

def get_mouse_pos(mouse_pos):
    pass

create_board()

running = True
winner = 0

while running:
    move = get_player_move(player_turn)
    while move is None:
        move = get_player_move(player_turn)
    place_piece(player_turn, move)
    if check_win(player_turn):
        winner = player_turn
        break
    print_board()
    player_turn = 1 if player_turn == 2 else 2
print('player ', winner, ' has won')

# GUI
x = False
while x:
    events = event.get()

    for e in events:
        if e.type == pygame.QUIT:
            running = False

        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                running = False

        if e.type == pygame.MOUSEBUTTONDOWN:
            get_mouse_pos()
