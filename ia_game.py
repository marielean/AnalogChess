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
# pygame.init()

print("pygame is running:", pygame.get_init()) 



heuristic_0 = 'custom_heuristic_0'
heuristic_1 = 'custom_heuristic_1'
heuristic_2 = 'custom_heuristic_2'
alpha_beta = 'AlphaBeta'
minimax = 'MiniMax'
rand = 'Random'


white_depth = 2
black_depth = 2

white_ia_algorithm = rand
black_ia_algorithm = alpha_beta

granularity = 5

import differentfiles.heuristics as get_heuristics
white_heuristic = getattr(get_heuristics, heuristic_0)
black_heuristic = getattr(get_heuristics, heuristic_2)



# ia = IA(utility=custom_heuristic_0, algorithm = 'AlphaBeta', depth = 2)
white_ia = IA(utility=white_heuristic, algorithm = white_ia_algorithm, depth = white_depth)
black_ia = IA(utility=black_heuristic, algorithm = black_ia_algorithm, depth = black_depth)

board = Board(granularity=granularity)

not_done = True
white_turn = True



done = False
clock = pygame.time.Clock()
confirmed = True

turn_number = 1

pygame.display.set_caption("Analog Chess")

draw_line_round_corners_polygon(
    see_through, (120, 120), (220, 220), RED_HIGHLIGHT, 0.7 * 640 / 8
)
grabbed_piece = None

for piece in board.get_pieces():
    piece.calc_paths(board.get_pieces())

just_played = False
white_turn = True
pygame.display.quit()
print("pygame is running:", pygame.display.get_init())
print(f"Gioco iniziato con white algorithm: {white_ia_algorithm} e depth: {white_depth} con euristica: {white_heuristic.__name__}")
print(f"Gioco iniziato con black algorithm: {black_ia_algorithm} e depth: {black_depth} con euristica: {black_heuristic.__name__}")
print(f"Granularità: {granularity}")
while not done:
    print("Turno numero: ", turn_number)
    if board.is_white_turn():
        if not board.is_terminal():
            print("Turno del bianco")
            best_move = white_ia.get_best_move(board)
            print(f"Mossa selezionata dal bianco: {best_move} con algoritmo: {white_ia_algorithm} e depth: {white_depth} con euristica: {white_heuristic.__name__} e granularità: {granularity}")
            board.apply_move(best_move)

            
            print("Pezzo giocato dal bianco", best_move[0])
            # print("After:\n", board.get_chess_board_status())
            # _, white_pieces = board.get_chess_board_status()
            # print("pieces: ", white_pieces)

            board.set_turn(False)
            white_turn = False
            turn_number += 1
    
    if not board.is_white_turn():
        # print("Before:\n",board.get_chess_board_status())
        if not board.is_terminal():
            print("Turno del nero")
            best_move = black_ia.get_best_move(board)
            print(f"Mossa selezionata dal nero: {best_move} con algoritmo: {black_ia_algorithm} e depth: {black_depth} con euristica: {black_heuristic.__name__} e granularità: {granularity}")
            board.apply_move(best_move)

            
            print("Pezzo giocato dal nero", best_move[0])
            # print("After:\n", board.get_chess_board_status())
            # _, black_pieces = board.get_chess_board_status()
            # print("pieces: ", black_pieces)
        
            board.set_turn(True)
            white_turn = True
            turn_number += 1

        
        
        # gioco finito
        if board.is_terminal():
            print(f"This is the end... Winner is {white if not board.is_white_turn() else black}")
            print(f"Turn number: {turn_number}")
            print(f"Algoritmo del vincitore usato: {white_ia_algorithm if not board.is_white_turn() else black_ia_algorithm}")
            print(f"Profondità del vincitore usato: {white_depth if not board.is_white_turn() else black_depth}")
            print(f"Euristica del vincitore usato: {white_heuristic.__name__ if not board.is_white_turn() else black_heuristic.__name__}")
            print(f"Algoritmo del perdente usato: {white_ia_algorithm if board.is_white_turn() else black_ia_algorithm}")
            print(f"Profondità del perdente usato: {white_depth if board.is_white_turn() else black_depth}")
            print(f"Euristica del perdente usato: {white_heuristic.__name__ if board.is_white_turn() else black_heuristic.__name__}")
            print(f"Granularità: {granularity}")
            done = True
            if pygame.display.get_init():
                font = pygame.font.SysFont("oldenglishtext", int(80))
                confirm_text = font.render("Wiiiiiiin", True, black)
                draw_center_text(confirm_text)
                pygame.display.flip()

    

