from differentfiles.pieces import *
from differentfiles.ia import IA
from differentfiles.colors import *
from differentfiles.heuristics import custom_heuristic_0, custom_heuristic_1, custom_heuristic_2
import time

# Possible heuristics: custom_heuristic_0, custom_heuristic_1, custom_heuristic_2
# Possible algorithms: MiniMax, AlphaBeta, Random

def run_match(algorithm_white, algorithm_black, depth_white, depth_black, granularity):
    start_time = time.time()

    white_ia = IA(utility=custom_heuristic_0, algorithm=algorithm_white, depth=depth_white)
    black_ia = IA(utility=custom_heuristic_0, algorithm = algorithm_black, depth=depth_black)
    # board = Board(granularity=10, pieces=chessboard_5) # Use this if you want to test a specific chessboard
    board = Board(granularity=granularity)

    turn_number = 1

    '''
    done = False
    for piece in board.get_pieces():
        piece.calc_paths(board.get_pieces())
            
    while not done:

        for piece in board.get_pieces():
            piece.calc_paths(board.get_pieces())

        #White starts playing
        if board.is_white_turn():
            if not board.is_terminal():
                best_move = white_ia.get_best_move(board)
                board.apply_move(best_move)
                # print("Turno numero: ", turn_number)
                # print("Mossa selezionata dal giocatore BIANCO: ", best_move)
                # print("Pezzo giocato dal BIANCO", best_move[0])

                turn_number += 1
                board.set_turn(False)

                if board.is_terminal():
                    # print("This is the end! White wins!")
                    done = True
                    break

        #Black plays
        if not board.is_white_turn():

            if not board.is_terminal():
                best_move = black_ia.get_best_move(board)
                board.apply_move(best_move)

                # print("Turno numero: ", turn_number)
                # print("Mossa selezionata dal giocatore NERO: ", best_move)
                # print("Pezzo giocato dal NERO", best_move[0])
            
            turn_number += 1
            board.set_turn(True)

            if board.is_terminal():
                # print("This is the end! Black wins!")
                done = True
    '''

    while True:
        for piece in board.get_pieces():
            piece.calc_paths(board.get_pieces())
        
        best_move = None
        if board.is_white_turn():
            best_move = white_ia.get_best_move(board)
        else:
            best_move = black_ia.get_best_move(board)
        board.apply_move(best_move)

        if board.is_terminal():
            end_time = time.time()
            print('#', sep='', end='')
            return board.is_white_turn(), end_time - start_time, turn_number

        board.set_turn(not board.is_white_turn())
        turn_number += 1

        
