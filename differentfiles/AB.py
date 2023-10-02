from .colors import *
import numpy as np
from math import floor

depth = 2

def apply_granularity(coordinate, granularity=1):
    rounded = round(coordinate, granularity)
    return rounded

def random_move():
    """
    Selects a random move from the valid moves for the current players turn
    :param board: the current board being used for the game (Board)
    :return: tuple representing move; format: ((sourceX, sourceY), (destX, destY))
    """
    pass


def max_alpha_beta():
    max_value = -math.inf
    pass

def min_alpha_beta():
    min_value = math.inf
    pass 

# grazie a questa funzione si ottengono tutte le mosse possibili per un pezzo in base alla sua direzione
# granularity è il numero di punti che si vogliono ottenere per ogni direzione
# def get_points_from_distance(x_start, x_end, y_start, y_end, granularity=2):
#     list_points = []
#     x_distance = abs(x_start - x_end)
#     y_distance = abs(y_start - y_end)
#     for i in range(1, granularity+1):
#         if x_distance != 0:
#             x_new = x_start + (x_distance/granularity)*i
#         else:
#             x_new = x_start
#         if y_distance != 0:
#             y_new = y_start + (y_distance/granularity)*i
#         else:
#             y_new = y_start
#         list_points.append((x_new, y_new))
#     return list_points

# Metodo leggermente più efficiente (penso)
def get_points_from_distance(x_start, x_end, y_start, y_end, granularity=2):
    n = floor(abs(x_end-x_start)/granularity) # number of points for x and y (only 45 or 0 degree movements # are avaiables)
    
    # Calculation on all the possible x_values
    if (x_end-x_start)!=0:
        x_list = np.arange(1, n+1)/(x_end-x_start)+x_start
    else:
        x_list = np.full(n, x_start)
    
    # Calculation on all the possible x_values
    if (y_end-y_start)!=0:
        y_list = np.arange(1, n+1)/(y_end-y_start)+y_start
    else:
        y_list = np.full(n, y_start)
    
    list_points = [(x_list[i],y_list[i]) for i in range(len(x_list))]
    return list_points


def get_all_moves_from_distance(list_pieces):
    #print("list_pieces: ", list_pieces)
    list_moves = []
    for d in list_pieces:
        #print("d: ", d)
        for i in range(len(d[3])):
            list_point_x = []
            list_point_y = []
            #print("i: ", d[3][i])
            #print(d[2][0], d[3][i][0], d[2][1], d[3][i][1])
            list_point = get_points_from_distance(d[2][0], d[3][i][0], d[2][1], d[3][i][1])
            # print("list point per piece: ", d[0], d[1], d[2], list_point)
            # list_moves.append(get_points_from_distance(d[2][0], d[3][i][0], d[2][1], d[3][i][1]))
            for j in range(len(list_point)):
                # lista nella forma [id, colore, (x_start, y_start), [(x_end, y_end), (x_end, y_end), ...]], 
                # dove l'ultima lista corrisponde ai punti possibli per una direzione direzione
                list_moves.append([d[0], d[1], d[2], list_point[j]])


    return list_moves

# restituisce tutte le direzioni di tutti i pezzi presenti diviso per colori
def get_all_directions(pieces):
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


def alpha_beta_pruning(depth, node_index, maximizingPlayer, nodes, alpha, beta, pieces):
    
    # Terminating condition. i.e
    # leaf node is reached
    if depth == 3:
        return 
    
    if maximizingPlayer:
        best = -math.inf
        
        # Recur for left and right children
        for item in nodes:
            new_pieces = []
            for p in pieces:
                if p.id == item[0] and p.color == item[1] and p.x == item[2][0] and p.y == item[2][1]:
                  new_pieces.append()  
            val = alpha_beta_pruning(depth + 1, item, False, nodes, alpha, beta)
            best = max(best, val)
            alpha = max(alpha, best)
            
            # Alpha Beta Pruning
            if beta <= alpha:
                break
        return best

def evaluate_position(pieces):
    white_score = 0 # punteggio bianco con valore positivo
    black_score = 0 # punteggio nero con valore negativo
    for piece in pieces:
        if piece.color == white and piece.deleted == False:
            white_score += piece.x + piece.y
        if piece.color == black and piece.deleted == False:
            black_score -= piece.x + piece.y
    return white_score, black_score

def evaluate_weith(pieces):
    white_score = 0 # punteggio bianco con valore positivo
    black_score = 0 # punteggio nero con valore negativo
    for piece in pieces:
        if piece.color == white and piece.deleted == False:
            white_score += piece.weight
        if piece.color == black and piece.deleted == False:
            black_score -= piece.weight
    return white_score, black_score


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
