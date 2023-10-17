from differentfiles.colors import *
from differentfiles.pieces.board import Board
import numpy as np
from math import floor
import random
from copy import deepcopy

class IA:
    def __init__(self):
        # la prima mossa è sempre del bianco
        self.whiteTurn = True

    def set_turn(self, whiteTurn):
        self.whiteTurn = whiteTurn


    def apply_granularity(self, coordinate, granularity=1):
        rounded = round(coordinate, granularity)
        return rounded
    
    # metodo che resituisce se la partita è finita 
    def is_terminal(self, pieces, whites_turn):
        if whites_turn:
            for p in pieces:
                if p.color == black and p.id == "K" and p.deleted:
                    return True, "bianco ha vinto"
        else:
            for p in pieces:
                if p.color == white and p.id == "K" and p.deleted:
                    return True, "nero ha vinto"
        return False
    
    
    # actions: restituisce la lista di azioni possibili in uno stato della scacchiera diviso per giocatore... 
    def actions(self, board: Board, pieces: dict):
        list_directions_white, list_directions_black = board.get_all_directions_all_in_one(pieces)
        moves = []
        i = 0
        '''
        if whites_turn:
            list_moves = get_all_moves_from_distance(list_directions_white)
            for item in list_moves:
                for i in range(len(item[-1])):
                    moves.append([item[0], item[1], item[2], item[-1][i]])
            return moves
        else:
            list_moves = get_all_moves_from_distance(list_directions_black)
            for item in list_moves:
                for i in range(len(item[-1])):
                    moves.append([item[0], item[1], item[2], item[-1][i]])
            return moves
        '''
        list_moves = board.get_all_moves_from_distance(list_directions_white)
        for item in list_moves:
            for i in range(len(item[-1])):
                moves.append([item[0], item[1], item[2], item[-1][i]])
        list_moves = board.get_all_moves_from_distance(list_directions_black)
        for item in list_moves:
            for i in range(len(item[-1])):
                moves.append([item[0], item[1], item[2], item[-1][i]])

        self.verify_actions(moves)

        return moves

    def actions_per_color(self, board: Board, pieces: dict, whites_turn: bool):
        list_directions_white, list_directions_black = board.get_all_directions_all_in_one(pieces)
        moves = []
        i = 0
        if whites_turn:
            list_moves = board.get_all_moves_from_distance(list_directions_white)
            for item in list_moves:
                for i in range(len(item[-1])):
                    moves.append([item[0], item[1], item[2], item[-1][i]])
            
            self.verify_actions(moves)
            return moves
        else:
            list_moves = board.get_all_moves_from_distance(list_directions_black)
            for item in list_moves:
                for i in range(len(item[-1])):
                    moves.append([item[0], item[1], item[2], item[-1][i]])
            
            self.verify_actions(moves)
            return moves

    def is_valid_move(self, move):
        if move[2][0] == move[3][0] and move[2][1] == move[3][1]:
            return False
        return True

    def verify_actions(self, moves):
        new_moves = []
        for move in moves:
            if self.is_valid_move(move):
                new_moves.append(move)
        
        return new_moves

    def get_one_random_move(self, pieces: dict, whites_turn: bool, board: Board):
        """
        Selects a random move from the valid moves for the current players turn
        :param board: the current board being used for the game (pieces)
        :return: list representing move; format: [id, color, (x_start, y_start), (x_end, y_end)]
        """
        list_directions_white, list_directions_black = board.get_all_directions_all_in_one(pieces)
        # list_moves = get_all_moves_from_distance(list_directions_white)
        list_moves = None
        if whites_turn:
            list_moves = board.get_all_moves_from_distance(list_directions_white)
        else:
            list_moves = board.get_all_moves_from_distance(list_directions_black)
        random_piece = random.choice(list_moves)
        r_move = random.choice(random_piece[-1])
        move = [random_piece[0], random_piece[1], random_piece[2], r_move]
        return move 


    

    # function for random move
    def random_move(self, pieces, whites_turn, board):
        actions = self.actions_per_color(board, pieces, whites_turn)
        r_move = random.choice(actions)
        return r_move

    # function for best move
    def best_move(self, pieces, whites_turn, board):

        # esegue una mossa casuale
        move = self.random_move(pieces, whites_turn, board)
        return move

        # ritorna la mossa migliore in base all'algoritmo alpha-beta
        # return alpha_beta_search(pieces, depth_size, maximizingPlayer)
        
    
        
    # metodo che restituisce la mossa migliore in base all'algoritmo alpha-beta
    # pieces è la lista dei pezzi ancora in gioco e sarebbe lo stato attuale del gioco
    # depth è la profondità dell'albero di ricerca
    def alpha_beta_search(self, board: Board, depth, whites_turn):
        '''
        Metodo che implementa la funzione alpha-beta.
        Suggerimento: devono essere utilizzati i metodi:
        - game.is_terminal: controlla che lo stato sia terminale
        - game.utility: restituisce l'utilità di uno stato per un giocatore
        - game.actions: restituisce la lista di azioni possibili in uno stato
        - game.result: restituisce il risultato dell'applicazione di un'azione in uno stato
        '''
        pieces = board.get_pieces()
        fake_board = Board()
        fake_board.set_pieces(pieces)
        print(fake_board.get_pieces()[0], pieces[0])

        def max_value(fake_board: Board, pieces, depth, alpha, beta, whites_turn):
            if depth == 0 or self.is_terminal(pieces, whites_turn):
                return fake_board.utility(pieces, whites_turn)
            v = -math.inf
            action_s = self.actions_per_color(pieces, whites_turn)

            for a in action_s:
                v = max(v, min_value(self.apply_move(pieces, a), depth - 1, alpha, beta, whites_turn))
                if v >= beta:
                    return v
                alpha = max(alpha, v)
            return v

        def min_value(fake_board: Board, pieces, depth, alpha, beta, whites_turn):
            if depth == 0 or fake_board.is_terminal(pieces, whites_turn):
                return self.utility(pieces, whites_turn)
            v = math.inf
            action_s = self.actions_per_color(pieces, whites_turn)

            for a in action_s:
                v = min(v, max_value(self.apply_move(pieces, a), depth - 1, alpha, beta, whites_turn))
                if v <= alpha:
                    return v
                beta = min(beta, v)
            return v

        # Body di alpha_beta_pruning
        return max(self.actions_per_color(fake_board.get_pieces(), whites_turn), 
                   key=lambda a: min_value(fake_board, fake_board.apply_move(fake_board.get_pieces(), a), depth, -math.inf, math.inf, self.whiteTurn)) 



    def minimax_search(self, board: Board, depth, alpha, beta, whites_turn):
        '''
        metodo che restituisce la mossa migliore in base all'algoritmo minimax\n
        pieces è la lista dei pezzi ancora in gioco e sarebbe lo stato attuale del gioco\n
        depth è la profondità dell'albero di ricerca
        '''
        # whites_turn = True if White2Play and False is Black2Play
        #print("board: ", board.get_pieces())

        if depth == 0 or board.is_terminal(board.get_pieces(), whites_turn):
            return self.utility(board.get_pieces(), whites_turn)
        
        if whites_turn:
            maxEval, best_move  = -np.inf, None
            pieces = board.get_pieces()
            actions = self.actions_per_color(board, pieces, whites_turn)

            for action in actions:
                if self.is_valid_move(action):
                    fake_board = Board()
                    fake_board.set_pieces(board.get_pieces())
                    #print("fake_pieces: ", fake_pieces[0].id)

                    evalu = self.minimax_search(fake_board.board_apply_move(fake_board, action), depth - 1, alpha, beta, False)
                    val = evalu[0] if isinstance(evalu, tuple) else evalu
                    if val >= maxEval:
                        maxEval = val
                        best_move = action
                    
                    alpha = max(alpha, maxEval)
                    if beta <= alpha:
                        break
                return maxEval, best_move
        
        else:
            minEval, best_move = np.inf, None
            pieces = board.get_pieces()
            actions = self.actions_per_color(board, pieces, whites_turn)

            for action in actions:
                if self.is_valid_move(action):
                    fake_board = Board()
                    fake_board.set_pieces(board.get_pieces())
                    fake_pieces = fake_board.get_pieces()
                    #print("fake_pieces: ", fake_pieces[0].id)

                    evalu = self.minimax_search(fake_board.board_apply_move(fake_board, action), depth - 1, alpha, beta, True)
                    val = evalu[0] if isinstance(evalu, tuple) else evalu
                    if val <= minEval:
                        minEval = val
                        best_move = action
                    beta = min(beta, minEval)
                    if beta <= alpha:
                        break
                return minEval, best_move

    # utility function
    def utility(self, pieces, whites_turn):
        return self.evaluate_weith(pieces, whites_turn)

    def evaluate_position(self, pieces, whites_turn):
        white_score = 0 # punteggio bianco con valore positivo
        black_score = 0 # punteggio nero con valore negativo
        for piece in pieces:
            if piece.color == white and piece.deleted == False:
                white_score += piece.y
            if piece.color == black and piece.deleted == False:
                black_score += piece.y
        # restituisce il punteggio del giocatore che sta giocando (maximizingPlayer è il bianco, nero altrimenti)
        return white_score if whites_turn else black_score 


    def evaluate_weith(self, pieces, whites_turn):
        white_score = 0 # punteggio bianco con valore positivo
        black_score = 0 # punteggio nero con valore negativo
        for piece in pieces:
            if piece.color == white and piece.deleted == False:
                white_score += piece.weight
            if piece.color == black and piece.deleted == False:
                black_score += piece.weight
        return white_score if whites_turn else black_score


    def alpha_beta_pruning(self, depth, node_index, maximizingPlayer, nodes, alpha, beta, pieces):
        # Terminating condition. i.e
        # leaf node is reached
        if depth == depth_size or self.is_terminal(pieces, maximizingPlayer):
            return self.utility(pieces, maximizingPlayer)
        
        if maximizingPlayer:
            best = -math.inf
            
            # Recur for left and right children
            for item in nodes:
                new_pieces = []
                for p in pieces:
                    if p.id == item[0] and p.color == item[1] and p.x == item[2][0] and p.y == item[2][1]:
                        new_pieces.append()  
                val = self.alpha_beta_search(depth + 1, item, False, nodes, alpha, beta)
                best = max(best, val)
                alpha = max(alpha, best)
                
                # Alpha Beta Pruning
                if beta <= alpha:
                    break
            return best

        else:
            best = math.inf
            
            # Recur for left and
            # right children
            for item in nodes:
                val = self.alpha_beta_search(depth + 1, item, True, nodes, alpha, beta)
                best = min(best, val)
                beta = min(beta, best)
                
                # Alpha Beta Pruning
                if beta <= alpha:
                    break
            return best