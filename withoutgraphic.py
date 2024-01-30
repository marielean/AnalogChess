from differentfiles.pieces import *
from differentfiles.ia import IA
from differentfiles.colors import *
from differentfiles.heuristics import custom_heuristic_0, custom_heuristic_1, custom_heuristic_2
import time
import numpy as np

# Possible heuristics: custom_heuristic_0, custom_heuristic_1, custom_heuristic_2
# Possible algorithms: MiniMax, AlphaBeta, Random

def run_match(utility_white, utility_black, algorithm_white, algorithm_black, depth_white, depth_black, granularity, timeout=np.inf):
    start_time = time.time()

    white_ia = IA(utility=utility_white, algorithm=algorithm_white, depth=depth_white, timeout=timeout)
    black_ia = IA(utility=utility_black, algorithm = algorithm_black, depth=depth_black, timeout=timeout)
    # board = Board(granularity=10, pieces=chessboard_5) # Use this if you want to test a specific chessboard
    board = Board(granularity=granularity)

    turn_number = 1

    while True:
        
        best_move = None
        if board.is_white_turn():
            best_move = white_ia.get_best_move(board)
        else:
            best_move = black_ia.get_best_move(board)
        board.apply_move(best_move)
        print(f'Mossa giocata: {best_move}')

        if board.is_terminal():
            end_time = time.time()
            print('#', sep='', end='', flush=True)
            return board.is_white_turn(), end_time - start_time, turn_number
        if turn_number >= 2000:
            end_time = time.time()
            print('#', sep='', end='', flush=True)
            return None, end_time - start_time, turn_number
        
        board.set_turn(not board.is_white_turn())
        turn_number += 1

        
