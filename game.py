import pygame
from pygame import display, event
import asyncio

import config

board = []
player_turn = 1
running = True
winner = 0

pygame.init()

display.set_caption('Connect Four')

screen = display.set_mode((config.SCREEN_SIZE, config.SCREEN_SIZE))
clock = pygame.time.Clock()

#################################################
# Initialization
#################################################

def init_board():
    global board
    for r in range(config.BOARD_ROWS):
        row = []
        for c in range(config.BOARD_COLS):
            row.append(0)
        board.append(row)

def print_board():
    global board
    print(board)

def init():
    init_board()
    draw_screen()

#################################################
# Drawing
#################################################

def draw_screen():
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

# def animate_piece(piece, player_turn):
#     piece_row = piece[0]
#     piece_col = piece[1]
#     row = 0
#     color = config.RED if player_turn == 1 else config.YELLOW
#     clock = pygame.time.Clock()
#     pygame.draw.circle(screen, color,
#                       (int(piece_col * config.RECT_L + config.RECT_L/2), int(row * config.RECT_L + config.RECT_L + config.RECT_L/2)),
#                       config.RADIUS)
#
    # while(row < piece_row):
    #     draw_screen()
    #     pygame.draw.circle(screen, color,
    #                   (int(piece_col * config.RECT_L + config.RECT_L/2), int(row * config.RECT_L + config.RECT_L + config.RECT_L/2)),
    #                   config.RADIUS)
    #     row += 1
    #     display.update()
        # await asyncio.sleep(1)

# def draw_pieces(piece):
#     # Dont draw the piece given
#     global board
#     global player_turn
#     for row in range(config.BOARD_ROWS):
#         for col in range(config.BOARD_COLS):
#             if (row, col) != piece:
#                 color = config.RED if board[row][col] == 1 else config.YELLOW
#                 pygame.draw.circle(screen, color,
#                                   (int(col * config.RECT_L + config.RECT_L/2), int(row * config.RECT_L + config.RECT_L + config.RECT_L/2)),
#                                   config.RADIUS)

def hover_circle(mouse_pos):
    global player_turn
    pygame.draw.rect(screen, config.BLACK,
                    (0, 0, config.BOARD_COLS * config.RECT_L, config.RECT_H))
    display.update()
    color = config.RED if player_turn == 1 else config.YELLOW
    mouse_pos = pygame.mouse.get_pos()
    hover_col = mouse_pos[0] // config.RECT_L
    center_pos = (config.RECT_L * hover_col + config.RECT_L // 2, config.RECT_H // 2)
    pygame.draw.circle(screen, color, center_pos, config.RADIUS)
    display.update()

#################################################
# Piece placement
#################################################

def get_player_move(mouse_pos):
    return mouse_pos[0] // config.RECT_L

def is_valid_location(move):
    global board
    return board[0][move] == 0

# Returns tuple of position of piece that was just placed
def place_piece(move):
    global player_turn
    row = _get_row(move)
    return (row, move)

def _get_row(move):
    global board
    global player_turn
    row = 0
    while row < config.BOARD_ROWS and board[row][move] == 0:
        row += 1
    row -= 1
    board[row][move] = player_turn
    return row

def draw_piece(pos):
    global player_turn
    row, col = pos
    color = config.RED if player_turn == 1 else config.YELLOW
    pygame.draw.circle(screen, color,
                      (int(col * config.RECT_L + config.RECT_L/2), int(row * config.RECT_L + config.RECT_L + config.RECT_L/2)),
                      config.RADIUS)


#################################################
# Text messages
#################################################
def make_text():
    font = pygame.font.Font(None, 64)
    text = font.render('Piece placed', True, config.RED)
    screen.blit(text, (0,0))
    display.update()
    return

def error_message():
    global clock
    # font = pygame.font.Font(None, 64)
    # orig_surf = font.render('Enter your text', True, blue)
    # txt_surf = orig_surf.copy()
    # # This surface is used to adjust the alpha of the txt_surf.
    # alpha_surf = pygame.Surface(txt_surf.get_size(), pygame.SRCALPHA)
    # alpha = 255  # The current alpha value of the surface.
    #
    # if alpha > 0:
    #     # Reduce alpha each frame, but make sure it doesn't get below 0.
    #     alpha = max(alpha-4, 0)
    #     txt_surf = orig_surf.copy()  # Don't modify the original text surf.
    #     # Fill alpha_surf with this color to set its alpha value.
    #     alpha_surf.fill((255, 255, 255, alpha))
    #     # To make the text surface transparent, blit the transparent
    #     # alpha_surf onto it with the BLEND_RGBA_MULT flag.
    #     txt_surf.blit(alpha_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    screen.fill((30, 30, 30))
    screen.blit(txt_surf, (30, 60))
    display.flip()
    clock.tick(30)

#################################################
# Check win
#################################################
def check_win():
    global board
    global player_turn
    for row in range(config.BOARD_ROWS):
        for col in range(config.BOARD_COLS):
            if board[row][col] == player_turn:
                horWin = _check_horizontal(row)
                verWin = _check_vertical(col)
                posDiagWin = _check_pos_diagonal(row, col)
                negDiagWin = _check_neg_diagonal(row, col)
                if horWin or verWin or posDiagWin or negDiagWin:
                    return True
    return False

def _check_horizontal(row):
    global board
    global player_turn
    piece_count = 0
    for piece in board[row]:
        if piece == player_turn:
            piece_count += 1
            if piece_count == 4:
                return True
        else:
            if piece_count != 0:
                piece_count = 0
    return False

def _check_vertical(col):
    global board
    global player_turn
    piece_count = 0
    for row in board:
        if row[col] == player_turn:
            piece_count += 1
            if piece_count == 4:
                return True
        else:
            if piece_count != 0:
                piece_count = 0
    return False

def _check_pos_diagonal(row, col):
    global board
    global player_turn
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

def _check_neg_diagonal(row, col):
    global board
    global player_turn
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

#################################################
# Game start
#################################################

init()

while running:
    events = event.get()

    hover_circle(pygame.mouse.get_pos())

    for e in events:
        if e.type == pygame.QUIT:
            running = False

        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                running = False

        if e.type == pygame.MOUSEBUTTONDOWN:
            move = get_player_move(pygame.mouse.get_pos())
            if is_valid_location(move):
                pos = place_piece(move)
                draw_piece(pos)
                # draw_pieces(pos)
                # animate_piece(piece, player_turn)
                # make_text()
            else:
                while not is_valid_location(move):
                    error_message()
                    move = get_player_move(pygame.mouse.get_pos())
            if check_win():
                winner = player_turn
                running = False
            player_turn = 1 if player_turn == 2 else 2
