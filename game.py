import pygame
from pygame import display, event
import os, time

import config

board = []
player_turn = 1

pygame.init()

display.set_caption('Connect Four')

screen = display.set_mode((config.SCREEN_SIZE, config.SCREEN_SIZE))

def init_board():
    global board
    for r in range(config.BOARD_ROWS):
        row = []
        for c in range(config.BOARD_COLS):
            row.append(0)
        board.append(row)

def create_board():
    global board
    # Draw blue squares
    for row in range(config.BOARD_ROWS):
        for col in range(config.BOARD_COLS):
            pygame.draw.rect(screen, config.BLUE,
                            (col * config.RECT_H, row * config.RECT_L + config.RECT_L,
                            config.RECT_H, config.RECT_L))

    # Draw black holes where pieces will be placed
    for row in range(config.BOARD_ROWS):
        for col in range(config.BOARD_COLS):
            pygame.draw.circle(screen, config.BLACK,
                              (int(col * config.RECT_L + config.RECT_L/2), int(row * config.RECT_L + config.RECT_L + config.RECT_L/2)),
                              config.RADIUS)
    display.update()

def print_board():
    global board
    print(board)

def get_player_move(mouse_pos):
    return mouse_pos[0] // config.RECT_L

# def is_valid_move(move):
#     global board
#     try:
#         move = int(move)
#         assert move >= 0 & move < config.BOARD_COLS
#         return True
#     except:
#         print('Invalid move. Please input an int between 0-6.')
#         return False

def is_valid_location(move):
    global board
    return board[0][move] == 0

def place_piece(player_turn, move):
    row = _get_row(player_turn, move)
    draw_piece(player_turn, row, move)
    return

def _get_row(player_turn, move):
    global board
    row = 0
    while row < config.BOARD_ROWS and board[row][move] == 0:
        row += 1
    row -= 1
    board[row][move] = player_turn
    return row

def draw_piece(player_turn, row, col):
    color = config.RED if player_turn == 1 else config.YELLOW
    pygame.draw.circle(screen, color,
                      (int(col * config.RECT_L + config.RECT_L/2), int(row * config.RECT_L + config.RECT_L + config.RECT_L/2)),
                      config.RADIUS)

def drop_animation(start_pos, end_pos, player_turn):
    pass

def check_win(player_turn):
    global board
    for row in range(config.BOARD_ROWS):
        for col in range(config.BOARD_COLS):
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
    piece_count = 0
    row_arr = board[row]
    for piece, index in enumerate(row_arr):
        if row_arr[index] == player_turn:
            if piece_count == 4:
                print('hor win found')
                return True
            piece_count += 1
        else:
            if piece_count != 0:
                return False

def _check_vertical(player_turn, col):
    global board
    piece_count = 0
    for row in board:
        if row[col] == player_turn:
            if piece_count == 4:
                return True
            piece_count += 1
        else:
            if piece_count != 0:
                return False

def _check_consecutive(pieces):
    pieces.sort(key=lambda piece:piece[0])
    difference = 0
    for pos, index in enumerate(pieces):
        difference = pieces[0]

    return True

def _check_pos_diagonal(player_turn, row, col):
    global board
    rowIter = row
    colIter = col
    count = 0
    while (rowIter >= 0 and rowIter < config.BOARD_ROWS and
          colIter >= 0 and colIter < config.BOARD_COLS):
        if count == 4:
            return True
        if board[rowIter][colIter] == player_turn:
            count = count + 1
        rowIter -= 1
        colIter += 1

    # Checking backwards
    rowIter = row - 1
    colIter = col - 1
    while (rowIter >= 0 and rowIter < config.BOARD_ROWS and
          colIter >= 0 and colIter < config.BOARD_COLS):
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
    while (rowIter >= 0 and rowIter < config.BOARD_ROWS and
          colIter >= 0 and colIter < config.BOARD_COLS):
        if count == 4:
            return True
        if board[rowIter][colIter] == player_turn:
            count = count + 1
        rowIter -= 1
        colIter -= 1

    # Checking backwards
    rowIter = row + 1
    colIter = col + 1
    while (rowIter >= 0 and rowIter < config.BOARD_ROWS and
          colIter >= 0 and colIter < config.BOARD_COLS):
        if count == 4:
            return True
        if board[rowIter][colIter] == player_turn:
            count = count + 1
        rowIter += 1
        colIter += 1
    return False

def init():
    init_board()
    create_board()

def hover_circle(mouse_pos, player_turn):
    pygame.draw.rect(screen, config.BLACK,
                    (0, 0, config.BOARD_COLS * config.RECT_L, config.RECT_H))
    display.update()
    color = config.RED if player_turn == 1 else config.YELLOW
    mouse_pos = pygame.mouse.get_pos()
    hover_col = mouse_pos[0] // config.RECT_L
    center_pos = (config.RECT_L * hover_col + config.RECT_L // 2, config.RECT_H // 2)
    pygame.draw.circle(screen, color, center_pos, config.RADIUS)
    display.update()


init()

running = True
winner = 0

# while running:
#     move = get_player_move(player_turn)
#     while move is None:
#         move = get_player_move(player_turn)
#     place_piece(player_turn, move)
#     if check_win(player_turn):
#         winner = player_turn
#         break
#     print_board()
#     player_turn = 1 if player_turn == 2 else 2

# GUI
while running:
    events = event.get()

    if check_win(player_turn):
        winner = player_turn
        break

    hover_circle(pygame.mouse.get_pos(), player_turn)

    for e in events:
        if e.type == pygame.QUIT:
            running = False

        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                running = False

        if e.type == pygame.MOUSEBUTTONDOWN:
            move = get_player_move(pygame.mouse.get_pos())
            if is_valid_move(move):
                place_piece(player_turn, move)
            else:
                error_message(player_turn, move)
            player_turn = 1 if player_turn == 2 else 2
