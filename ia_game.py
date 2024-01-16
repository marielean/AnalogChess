import pygame, time, random
from differentfiles.pieces import *
from differentfiles.ia import IA
from differentfiles.colors import *
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

for piece in board.get_pieces():
    piece.calc_paths(board.get_pieces())

while not done:

    for piece in board.get_pieces():
        piece.calc_paths(board.get_pieces())

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
            print("Turno numero: ", turn_number)
            print("Mossa selezionata dal giocatore BIANCO: ", best_move)
            print("Pezzo giocato dal BIANCO", best_move[0])

            turn_number += 1
            board.set_turn(False)

            if board.is_terminal():
                print("This is the end! White wins!")
                done = True
                break

    draw_checkers()
    screen.blit(see_through, (0, 0))
    screen.blit(see_through2, (0, 0))

    for piece in board.get_pieces():
        piece.draw()

    pygame.display.flip()
    clock.tick(30)

    see_through.fill((0, 0, 0, 0))

    see_through2.fill((0, 0, 0, 0))

    #Black plays
    if not board.is_white_turn():

        if not board.is_terminal():
            best_move = black_ia.get_best_move(board)
            board.apply_move(best_move)
            print("Turno numero: ", turn_number)
            print("Mossa selezionata dal giocatore NERO: ", best_move)
            print("Pezzo giocato dal NERO", best_move[0])

            turn_number += 1
            board.set_turn(True)

        if board.is_terminal():
            print("This is the end! Black wins!")
            done = True
            pygame.display.flip()