import pygame, time, random
from differentfiles.pieces import *
from differentfiles.ia import IA
from differentfiles.colors import *
from differentfiles.utils import to_game_coords
from differentfiles.drawing import (
    see_through,
    see_through2,
    draw_line_round_corners_polygon,
    draw_checkers,
    screen,
    draw_center_text,
)
from differentfiles.heuristics import custom_heuristic_0, custom_heuristic_1, custom_heuristic_2

pygame.init()

from chessboardex import *

# Possible heuristics: custom_heuristic_0, custom_heuristic_1, custom_heuristic_2
# Possible algorithms: MiniMax, AlphaBeta, Random

white_ia = IA(utility=custom_heuristic_0, algorithm='Random', depth=2)
black_ia = IA(utility=custom_heuristic_0, algorithm = 'Random', depth = 2)
# board = Board(granularity=10, pieces=chessboard_5) # Use this if you want to test a specific chessboard
board = Board(granularity=1)

done = False
clock = pygame.time.Clock()
# confirmed = True

turn_number = 0

pygame.display.set_caption("Analog Chess")

draw_line_round_corners_polygon(
    see_through, (120, 120), (220, 220), RED_HIGHLIGHT, 0.7 * 640 / 8
)

# grabbed_piece = None

for piece in board.get_pieces():
    piece.calc_paths(board.get_pieces())
          
just_played = False

while not done:

    draw_checkers()
    screen.blit(see_through, (0, 0))
    screen.blit(see_through2, (0, 0))

    for piece in board.get_pieces():
        piece.draw()

    pygame.display.flip()
    clock.tick(30)

    see_through.fill((0, 0, 0, 0))

    see_through2.fill((0, 0, 0, 0))

    #White starts playing
    if board.is_white_turn():
        if not board.is_terminal():
            best_move = white_ia.get_best_move(board)
            board.apply_move(best_move)
            print("Mossa selezionata dal giocatore BIANCO: ", best_move)
            print("Pezzo giocato dal BIANCO", best_move[0])

            board.set_turn(False)

            if board.is_terminal():
                print("This is the end...")
                done = True
                font = pygame.font.SysFont("oldenglishtext", int(80))
                confirm_text = font.render("Wiiiiiiin", True, black)
                draw_center_text(confirm_text)
                pygame.display.flip()

    draw_checkers()
    screen.blit(see_through, (0, 0))
    screen.blit(see_through2, (0, 0))

    for piece in board.get_pieces():
        piece.draw()

    pygame.display.flip()
    clock.tick(30)

    see_through.fill((0, 0, 0, 0))

    see_through2.fill((0, 0, 0, 0))

    # Il giocatore nero gioca solamente quando il bianco ha appena finito di giocare
    if not board.is_white_turn():

        # print("Before:\n",board.get_chess_board_status())
        if not board.is_terminal():
            best_move = black_ia.get_best_move(board)
            board.apply_move(best_move)

            print("Mossa selezionata dal giocatore NERO: ", best_move)
            print("Pezzo giocato dal NERO", best_move[0])
            # print("After:\n", board.get_chess_board_status())
            # _, black_pieces = board.get_chess_board_status()
            # print("pieces: ", black_pieces)
        
        board.set_turn(True)
        just_played = False
        if board.is_terminal():
            print("This is the end...")
            done = True
            font = pygame.font.SysFont("oldenglishtext", int(80))
            confirm_text = font.render("Wiiiiiiin", True, black)
            draw_center_text(confirm_text)
            pygame.display.flip()