from .colors import *
import numpy as np
from math import floor
import random



def apply_granularity(coordinate, granularity=1):
    rounded = round(coordinate, granularity)
    return rounded





# metodo che resituisce se la partita è finita 
def is_terminal(pieces, whites_turn):
    if whites_turn:
        for p in pieces:
            if p.color == black and p.id == "K" and p.deleted:
                return True, "bianco ha vinto"
    else:
        for p in pieces:
            if p.color == white and p.id == "K" and p.deleted:
                return True, "nero ha vinto"
    return False


# grazie a questa funzione si ottengono tutte le mosse possibili per un pezzo in base alla sua direzione
# granularity è il numero di punti che si vogliono ottenere per ogni direzione
def get_points_from_distance(x_start, y_start, x_end, y_end, granularity=2, knight_flag=False):
    '''
    get_points_from_distance(x_start, y_start, x_end, y_end, granularity=2, knight_flag=False)
    The function returns all the possible moves in the following format:
    [(x1, y1), (x2, y2), ...]
    x_start: starting x of the path (current x position if the piece is a knight)
    y_start: starting y of the path (current y position if the piece is a knight)
    x_end: final x of the path (start angle if the piece is a knight)
    y_end: final y of the path (final angle if the piece is a knight)
    granularity: number of point per path (analogous chess -> granularity high). Default 2
    knight_flag: boolean flag. It must be true if the piece is a knight, false otherway. Default=False.
    '''
    list_points = []
    if not knight_flag:
        # If the piece is not a knight, the movement can be on a point in a line. 
        # In this case (x_start, y_start) are the coordinate of the first point of the line and (x_end, y_end) is the final point
        dx = (x_end - x_start)/granularity
        dy = (y_end - y_start)/granularity

        x_new = dx*np.arange(1, granularity+1) + x_start
        y_new = dy*np.arange(1, granularity+1) + y_start
    else:
        # If the piece is a knight, the movements are on a circonference arc with center (x_start, y_start). 
        # The variables x_end, y_end in this case are not really x and y but are the angles (in rad) of the first point of arc and of the last. 
        # In this sense we will rename them for a better readability. Finally, note that the angles are calculated from the positive semi-axis of y.
        start_ang, end_ang = x_end, y_end
        radius = math.sqrt(5) # I remember that the radius of the knight is sqrt(5) but you can change it if it is wrong

        delta = (end_ang - start_ang)/(granularity-1) # Angles variation (Let's do an example to explain why I have used granularity-1 as denominator. In the simplest case with only 2 points for arc, I want that the points are the first and the last points of the arc. Then, the delta have to be the total length of the arc.)
        x_new = np.cos(-(np.arange(granularity)*delta+start_ang-np.pi/2))*radius + x_start
        y_new = np.sin(-(np.arange(granularity)*delta+start_ang-np.pi/2))*radius + y_start
        # The two previous lines calculate the coordinates x and y of the avaiable moves from the possible angles. 
        # The main problems are that the angles are calculated from the positive y semi-axis and that are considered positives the clock-wise angles (the opposite of "normal" algebra). 
        # Then the formulas are not very trivial... The idea is to firstly transform the angles in a "conventional" representation and then compute the sin or cos.

    list_points = [(x_new[i], y_new[i]) for i in range(len(x_new))]
    return list_points


# restituisce tutte le mosse possibili per tutti i pezzi presenti nella list_pieces nella forma [id, colore, (x_start, y_start), [(x_end, y_end), (x_end, y_end), ...]]
def get_all_moves_from_distance(list_pieces):
    #print("list_pieces: ", list_pieces)
    list_moves = []

    for curr_piece in list_pieces:
        # curr_piece is [piece_name, color, current_position, final_positions_list]
        list_moves.append([curr_piece[0], curr_piece[1], curr_piece[2], []]) # the last empty list will contain the possible future moves

        for final_pos in curr_piece[3]: 
            
            is_knight = (curr_piece[0]==knight)
            list_point = get_points_from_distance(curr_piece[2][0], curr_piece[2][1], final_pos[0], final_pos[1], knight_flag=is_knight)
            
            list_moves[-1][-1] += list_point # list_moves
    return list_moves

# restituisce tutte le direzioni di tutti i pezzi presenti diviso per colori nella forma [id, colore, (x_start, y_start), [(x_end, y_end), (x_end, y_end), ...]]
def get_all_directions_all_in_one(pieces):
    list_directions_white = []
    list_directions_black = []
    for p in pieces:
        if not p.deleted:
            if p.color == black:
                direction = p.get_all_directions_per_piece(pieces)
                list_directions_black.append([p.id, p.color, (p.x, p.y), direction])
            elif p.color == white:
                direction = p.get_all_directions_per_piece(pieces)
                list_directions_white.append([p.id, p.color, (p.x, p.y), direction])
    
    return list_directions_white, list_directions_black


    
# actions: restituisce la lista di azioni possibili in uno stato della scacchiera diviso per giocatore... 
def actions(pieces, maximizingPlayer):
    list_directions_white, list_directions_black = get_all_directions_all_in_one(pieces)
    moves = []
    i = 0
    if maximizingPlayer:
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


def get_one_random_move(pieces, whites_turn):
    """
    Selects a random move from the valid moves for the current players turn
    :param board: the current board being used for the game (pieces)
    :return: list representing move; format: [id, color, (x_start, y_start), (x_end, y_end)]
    """
    list_directions_white, list_directions_black = get_all_directions_all_in_one(pieces)
    # list_moves = get_all_moves_from_distance(list_directions_white)
    list_moves = None
    if whites_turn:
        list_moves = get_all_moves_from_distance(list_directions_white)
    else:
        list_moves = get_all_moves_from_distance(list_directions_black)
    random_piece = random.choice(list_moves)
    r_move = random.choice(random_piece[-1])
    move = [random_piece[0], random_piece[1], random_piece[2], r_move]
    return move 


# metodo che restituisce la nuova disposizione dei pezzi in base alla mossa effettuata (move del tipo [id, colore, (x_start, y_start), (x_end, y_end)])
def apply_move(pieces, move):
    for p in pieces:
        if p.id == move[0] and p.color == move[1] and p.x == move[2][0] and p.y == move[2][1]:
            p.x = move[3][0]
            p.y = move[3][1]
            break
    return pieces

# function for random move
def random_move(pieces, whites_turn):
    move = get_one_random_move(pieces, whites_turn)
    print("random_move: ", move)
    apply_move(pieces, move)

# function for best move
def best_move(pieces, whites_turn):

    # esegue una mossa casuale
    random_move(pieces, whites_turn)

    # ritorna la mossa migliore in base all'algoritmo alpha-beta
    # return alpha_beta_search(pieces, depth_size, maximizingPlayer)
    

    
# metodo che restituisce la mossa migliore in base all'algoritmo alpha-beta
# pieces è la lista dei pezzi ancora in gioco e sarebbe lo stato attuale del gioco
# depth è la profondità dell'albero di ricerca
def alpha_beta_search(pieces, depth, whites_turn):
    '''
    Metodo che implementa la funzione alpha-beta.
    Suggerimento: devono essere utilizzati i metodi:
    - game.is_terminal: controlla che lo stato sia terminale
    - game.utility: restituisce l'utilità di uno stato per un giocatore
    - game.actions: restituisce la lista di azioni possibili in uno stato
    - game.result: restituisce il risultato dell'applicazione di un'azione in uno stato
    '''

    def max_value(pieces, depth, alpha, beta, whites_turn):
        if depth == 0 or is_terminal(pieces, whites_turn):
            return utility(pieces, whites_turn)
        v = -math.inf
        action_s = actions(pieces, whites_turn)

        for a in action_s:
            v = max(v, min_value(apply_move(pieces, a), depth - 1, alpha, beta, whites_turn))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(pieces, depth, alpha, beta, whites_turn):
        if depth == 0 or is_terminal(pieces, whites_turn):
            return utility(pieces, whites_turn)
        v = math.inf
        action_s = actions(pieces, whites_turn)

        for a in action_s:
            v = min(v, max_value(apply_move(pieces, a), depth - 1, alpha, beta, whites_turn))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # Body di alpha_beta_pruning
    return max(actions(pieces, whites_turn), key=lambda a: min_value(apply_move(pieces, a), depth, -math.inf, math.inf, whites_turn)) 


def alpha_beta_pruning(depth, node_index, maximizingPlayer, nodes, alpha, beta, pieces):
    # Terminating condition. i.e
    # leaf node is reached
    if depth == depth_size or is_terminal(pieces, maximizingPlayer):
        return utility(pieces, maximizingPlayer)
    
    if maximizingPlayer:
        best = -math.inf
        
        # Recur for left and right children
        for item in nodes:
            new_pieces = []
            for p in pieces:
                if p.id == item[0] and p.color == item[1] and p.x == item[2][0] and p.y == item[2][1]:
                  new_pieces.append()  
            val = alpha_beta_search(depth + 1, item, False, nodes, alpha, beta)
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
            val = alpha_beta_search(depth + 1, item, True, nodes, alpha, beta)
            best = min(best, val)
            beta = min(beta, best)
            
            # Alpha Beta Pruning
            if beta <= alpha:
                break
        return best

# utility function
def utility(pieces, maximizingPlayer):
    return evaluate_position(pieces, maximizingPlayer)

def evaluate_position(pieces, maximizingPlayer):
    white_score = 0 # punteggio bianco con valore positivo
    black_score = 0 # punteggio nero con valore negativo
    for piece in pieces:
        if piece.color == white and piece.deleted == False:
            white_score += piece.x + piece.y
        if piece.color == black and piece.deleted == False:
            black_score -= piece.x + piece.y
    # restituisce il punteggio del giocatore che sta giocando (maximizingPlayer è il bianco, nero altrimenti)
    return white_score if maximizingPlayer else black_score 


def evaluate_weith(pieces, maximizingPlayer):
    white_score = 0 # punteggio bianco con valore positivo
    black_score = 0 # punteggio nero con valore negativo
    for piece in pieces:
        if piece.color == white and piece.deleted == False:
            white_score += piece.weight
        if piece.color == black and piece.deleted == False:
            black_score -= piece.weight
    return white_score if maximizingPlayer else black_score


#restituisce lo stato della scacchiera con le posizioni di tutti i pezzi ancora in gioco diviso per colori
def get_chess_board_status(pieces):
    white_status = []
    black_status = []
    for piece in pieces:
        if piece.color == white and piece.deleted == False:
            white_status.append(piece.letter, piece.x, piece.y)
        elif piece.color == black and piece.deleted == False:
            black_status.append(piece.letter, piece.x, piece.y)
    return white_status, black_status
