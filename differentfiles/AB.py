from .colors import *

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


# grazie a questa funzione si ottengono tutte le mosse possibili per un pezzo in base alla sua direzione
# granularity è il numero di punti che si vogliono ottenere per ogni direzione
def get_points_from_distance(x_start, x_end, y_start, y_end, granularity=2):
    list_points = []
    x_distance = abs(x_start - x_end)
    y_distance = abs(y_start - y_end)
    for i in range(1, granularity+1):
        if x_distance != 0:
            x_new = x_start + (x_distance/granularity)*i
        else:
            x_new = x_start
        if y_distance != 0:
            y_new = y_start + (y_distance/granularity)*i
        else:
            y_new = y_start
        list_points.append((x_new, y_new))
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


def evaluate(pieces):
    white_score = 0
    black_score = 0
    for piece in pieces:
        if piece.color == white and piece.deleted == False:
            white_score += piece.weight
        if piece.color == black and piece.deleted == False:
            black_score += piece.weight
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
