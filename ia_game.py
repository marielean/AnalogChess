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
#from chessboardex import *
import configparser
pygame.init()

print("pygame is running:", pygame.get_init()) 



heuristic_0 = 'custom_heuristic_0'
heuristic_1 = 'custom_heuristic_1'
alpha_beta = 'AlphaBeta'
minimax = 'MiniMax'
rand = 'Random'


white_depth = 2
black_depth = 2

granularity = 3

import differentfiles.heuristics as get_heuristics
white_heuristic = getattr(get_heuristics, heuristic_0)
black_heuristic = getattr(get_heuristics, heuristic_0)

# ia = IA(utility=custom_heuristic_0, algorithm = 'AlphaBeta', depth = 2)
white_ia = IA(utility=white_heuristic, algorithm = rand, depth = white_depth)
black_ia = IA(utility=black_heuristic, algorithm = alpha_beta, depth = black_depth)

board = Board(granularity=granularity)

not_done = True
white_turn = True



done = False
clock = pygame.time.Clock()
confirmed = True

turn_number = 0

pygame.display.set_caption("Analog Chess")

draw_line_round_corners_polygon(
    see_through, (120, 120), (220, 220), RED_HIGHLIGHT, 0.7 * 640 / 8
)
grabbed_piece = None

for piece in board.get_pieces():
    piece.calc_paths(board.get_pieces())

just_played = False
white_turn = True
while not done:

    draw_checkers()


    prev_grabbed_piece = grabbed_piece
    grabbed_piece = None
    for piece in board.get_pieces():
        if piece.grabbed:
            grabbed_piece = piece   
    
    if grabbed_piece:
        for piece in board.get_pieces():
            if piece.color != grabbed_piece.color:
                piece.draw_paths(board.get_pieces())
    if grabbed_piece:
        grabbed_piece.draw_moves(board.get_pieces())

    screen.blit(see_through, (0, 0))

    screen.blit(see_through2, (0, 0))

    for piece in board.get_pieces():
        piece.draw()

    # draw grabbed piece last so it will show up on top
    if grabbed_piece:
        grabbed_piece.draw()

    pygame.display.flip()
    clock.tick(30)

    see_through.fill((0, 0, 0, 0))

    see_through2.fill((0, 0, 0, 0))

    if white_turn:
        if not board.is_terminal():
            print("Turno del bianco")
            best_move = white_ia.get_best_move(board)
            print("Mossa selezionata dal bianco: ", best_move)
            board.apply_move(best_move)

            
            print("Pezzo giocato dal bianco", best_move[0])
            # print("After:\n", board.get_chess_board_status())
            # _, white_pieces = board.get_chess_board_status()
            # print("pieces: ", white_pieces)

            board.set_turn(False)
            white_turn = False
            
    draw_checkers()


    prev_grabbed_piece = grabbed_piece
    grabbed_piece = None
    for piece in board.get_pieces():
        if piece.grabbed:
            grabbed_piece = piece   
    
    if grabbed_piece:
        for piece in board.get_pieces():
            if piece.color != grabbed_piece.color:
                piece.draw_paths(board.get_pieces())
    if grabbed_piece:
        grabbed_piece.draw_moves(board.get_pieces())

    screen.blit(see_through, (0, 0))

    screen.blit(see_through2, (0, 0))

    for piece in board.get_pieces():
        piece.draw()

    # draw grabbed piece last so it will show up on top
    if grabbed_piece:
        grabbed_piece.draw()

    pygame.display.flip()
    clock.tick(30)

    see_through.fill((0, 0, 0, 0))

    see_through2.fill((0, 0, 0, 0))



    if not white_turn:
        # print("Before:\n",board.get_chess_board_status())
        if not board.is_terminal():
            print("Turno del nero")
            best_move = black_ia.get_best_move(board)
            print("Mossa selezionata dal nero: ", best_move)
            board.apply_move(best_move)

            
            print("Pezzo giocato dal nero", best_move[0])
            # print("After:\n", board.get_chess_board_status())
            # _, black_pieces = board.get_chess_board_status()
            # print("pieces: ", black_pieces)
        
            board.set_turn(True)
            white_turn = True
    
    # gioco finito
    if board.is_terminal():
        print(f"This is the end... Winner is ")
        done = True
        font = pygame.font.SysFont("oldenglishtext", int(80))
        confirm_text = font.render("Wiiiiiiin", True, black)
        draw_center_text(confirm_text)
        pygame.display.flip()

    

