from .colors import *

depth = 2

def apply_granularity(coordinate, granularity=1):
    rounded = round(coordinate, granularity)
    return rounded

# restituisce tutte le direzioni di tutti i pezzi presenti diviso per colori
def get_all_directions(pieces):
    list_directions_white = []
    list_directions_black = []
    for p in pieces:
        if not p.deleted:
            if p.color == (0,0,0):
                direction = p.get_all_directions_per_piece(pieces)
                list_directions_black.append([p.id, p.color, direction])
            elif p.color == (255,255,255):
                direction = p.get_all_directions_per_piece(pieces)
                list_directions_white.append([p.id, p.color, direction])
    
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
