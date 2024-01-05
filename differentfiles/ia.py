from differentfiles.colors import *
from differentfiles.pieces.board import Board
import numpy as np
import random
from differentfiles.heuristics import custom_heuristic_0

class IA:
    def __init__(self, utility=custom_heuristic_0, algorithm = 'AlphaBeta', depth = 1):
        '''
        Possible algorithms: MiniMax, AlphaBeta, Random
        '''
        self.whiteTurn = True
        self.utility = utility
        self.algorithm = algorithm
        self.depth = depth

    def set_turn(self, whiteTurn):
        self.whiteTurn = whiteTurn

    # function for best move
    def get_best_move(self, board):
        if self.algorithm == "MiniMax":
            return self.__minimax_search(board)
        elif self.algorithm == "AlphaBeta":
            return self.__alphabeta_search(board)
        elif self.algorithm == "Random":
            return self.__random_search(board)

    
    def __random_search(self, board: Board):
        """
        Selects a random move from the valid moves for the current players turn
        :param board: the current board being used for the game (pieces)
        :return: list representing move; format: [id, color, (x_start, y_start), (x_end, y_end)]
        """
        list_moves = board.get_all_moves(board.is_white_turn())

        random_piece = random.choice(list_moves)
        r_move = random.choice(random_piece[-1])
        move = [random_piece[0], random_piece[1], random_piece[2], r_move]
        return move         

    def __minimax_search(self, board: Board):
        '''
        Metodo che implementa la funzione minimax.
        board: current board instance (current state)
        depth: maximum depth of the algorithm
        '''
        max_player = board.is_white_turn()
        depth = self.depth

        def max(curr_board, depth):
            
            if (depth == 0 or curr_board.is_terminal()):
                return None, self.utility(curr_board, max_player)
            
            # initialization
            max_value = -np.inf
            max_move = None

            # algorithm iteration (max is the turn player)
            possible_moves = curr_board.get_all_moves(max_player)
            for piece in possible_moves:
                # print(piece)
                for next_position in piece[3]:
                    move = [piece[0],piece[1],piece[2],next_position]
                    next_board = Board(pieces=curr_board.get_pieces(), granularity=curr_board.granularity)
                    next_board.apply_move(move)

                    _, value = min(next_board, depth-1)
                    if value > max_value:
                        max_value = value
                        max_move = move
            return max_move, max_value
        
        def min(curr_board, depth):
            if (depth == 0 or curr_board.is_terminal()):
                return None, self.utility(curr_board, max_player)
            
            # initialization
            min_value = np.inf
            min_move = None

            # algorithm iteration (min is the turn player)
            possible_moves = curr_board.get_all_moves(not max_player)
            for piece in possible_moves:
                for next_position in piece[3]:
                    move = [piece[0],piece[1],piece[2],next_position]
                    next_board = Board(pieces=curr_board.get_pieces(), granularity=curr_board.granularity)
                    next_board.apply_move(move)

                    _, value = max(next_board, depth-1)
                    if value > min_value:
                        min_value = value
                        min_move = move
            return min_move, min_value

        move, value = max(board, depth)
        return move
    
    def __alphabeta_search(self, board: Board):
        '''
        Metodo che implementa l'algoritmo alpha-beta.
        board: current board instance (current state)
        '''
        
        max_player = board.is_white_turn()

        def max(curr_board, alpha, beta, depth):            
            if (depth == 0 or curr_board.is_terminal()):
                return None, self.utility(curr_board, max_player)
            
            # initialization
            max_value = -np.inf
            max_move = None

            # algorithm iteration (max is the turn player)
            possible_moves = curr_board.get_all_moves(max_player)
            for piece in possible_moves:
                for next_position in piece[3]:
                    move = [piece[0],piece[1],piece[2],next_position]
                    next_board = Board(pieces=curr_board.get_pieces(), granularity=curr_board.granularity)
                    next_board.apply_move(move)

                    _, value = min(next_board, alpha, beta, depth-1)
                    if value > max_value:
                        max_value = value
                        max_move = move
                    if max_value >= beta:
                        return max_move, max_value
                    if max_value >= alpha:
                        alpha = max_value

            return max_move, max_value
        
        def min(curr_board, alpha, beta, depth):
            if (depth == 0 or curr_board.is_terminal()):
                return None, self.utility(curr_board, max_player)
            
            # initialization
            min_value = np.inf
            min_move = None

            # algorithm iteration (min is the turn player)
            possible_moves = curr_board.get_all_moves(not max_player)
            for piece in possible_moves:
                for next_position in piece[3]:
                    move = [piece[0],piece[1],piece[2],next_position]
                    next_board = Board(pieces=curr_board.get_pieces(), granularity=curr_board.granularity)
                    next_board.apply_move(move)

                    _, value = max(next_board, alpha, beta, depth-1)
                    if value < min_value:
                        min_value = value
                        min_move = move
                    if min_value <= alpha:
                        return min_move, min_value
                    if min_value < beta:
                        beta = min_value
            return min_move, min_value

        move, value = max(board, -np.inf, np.inf, self.depth)
        print("Value: ", value)
        return move
    
    