from differentfiles.colors import *
from differentfiles.pieces.board import Board
import numpy as np
from math import floor
import random
from copy import deepcopy
from differentfiles.heuristics import custom_heuristic_0

class IA:
    def __init__(self, utility=custom_heuristic_0, algorithm = 'MiniMax', depth = 1, alpha = None, beta = None):
        self.whiteTurn = True
        self.utility = utility
        self.algorithm = algorithm
        self.depth = depth
        self.alpha = alpha
        self.beta = beta

    def set_turn(self, whiteTurn):
        self.whiteTurn = whiteTurn

    def apply_granularity(self, coordinate, granularity=1):
        rounded = round(coordinate, granularity)
        return rounded

    # function for best move
    def get_best_move(self, board):
        if self.algorithm == "MiniMax":
            return self.minimax_search(board)
        elif self.algorithm == "AlphaBeta":
            pass
        elif self.algorithm == "Random":
            return self.get_one_random_move(board)

    
    def get_one_random_move(self, board: Board):
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
        

    def minimax_search(self, board: Board):
        '''
        Metodo che implementa la funzione minimax.
        board: current board instance (current state)
        depth: maximum depth of the algorithm
        '''
        turn = board.is_white_turn()
        depth = self.depth

        def max(curr_board, depth):
            
            if (depth == 0 or curr_board.is_terminal(turn)):
                return None, self.utility(curr_board, turn)
            
            # initialization
            max_value = -np.inf
            max_move = None

            # algorithm iteration (max is the turn player)
            possible_moves = curr_board.get_all_moves(turn)
            for piece in possible_moves:
                print(piece)
                for next_position in piece[3]:
                    move = [piece[0],piece[1],piece[2],next_position]
                    next_board = Board(curr_board.get_pieces())
                    next_board.apply_move(move)

                    _, value = min(next_board, depth-1)
                    if value > max_value:
                        max_value = value
                        max_move = move
            return max_move, max_value
        
        def min(curr_board, depth):
            if (depth == 0 or curr_board.is_terminal(turn)):
                return None, self.utility(curr_board, turn)
            
            # initialization
            min_value = np.inf
            min_move = None

            # algorithm iteration (min is the turn player)
            possible_moves = curr_board.get_all_moves(not turn)
            for piece in possible_moves:
                for next_position in piece[3]:
                    move = [piece[0],piece[1],piece[2],next_position]
                    next_board = Board(curr_board.get_pieces())
                    next_board.apply_move(move)

                    _, value = min(next_board, depth-1)
                    if value > min_value:
                        min_value = value
                        min_move = move
            return min_move, min_value

        move, value = max(board, depth)
        return move

    
    # def alpha_beta_pruning(self, depth, node_index, maximizingPlayer, nodes, alpha, beta, pieces):
    #     # Terminating condition. i.e
    #     # leaf node is reached
    #     if depth == depth_size or self.is_terminal(pieces, maximizingPlayer):
    #         return self.utility(pieces, maximizingPlayer)
        
    #     if maximizingPlayer:
    #         best = -math.inf
            
    #         # Recur for left and right children
    #         for item in nodes:
    #             new_pieces = []
    #             for p in pieces:
    #                 if p.id == item[0] and p.color == item[1] and p.x == item[2][0] and p.y == item[2][1]:
    #                     new_pieces.append()  
    #             val = self.alpha_beta_search(depth + 1, item, False, nodes, alpha, beta)
    #             best = max(best, val)
    #             alpha = max(alpha, best)
                
    #             # Alpha Beta Pruning
    #             if beta <= alpha:
    #                 break
    #         return best

    #     else:
    #         best = math.inf
            
    #         # Recur for left and
    #         # right children
    #         for item in nodes:
    #             val = self.alpha_beta_search(depth + 1, item, True, nodes, alpha, beta)
    #             best = min(best, val)
    #             beta = min(beta, best)
                
    #             # Alpha Beta Pruning
    #             if beta <= alpha:
    #                 break
    #         return best