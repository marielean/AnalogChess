

depth = 2

def apply_granularity(coordinate, granularity=1):
    rounded = round(coordinate, granularity)
    return rounded

def get_random_moves(pieces):
    list_directions = []
    for p in pieces:
        directions = p.get_all_directions(pieces)
        list_directions.append([p.id, p.color ,directions])
    
    return list_directions


def evaluate(pieces):
    white_score = 0
    black_score = 0
    for piece in pieces:
        if piece.color == (255,255,255) and piece.deleted == False:
            white_score += piece.weight
        if piece.color == (0,0,0) and piece.deleted == False:
            black_score += piece.weight
    return white_score, black_score

def get_chess_board_status(pieces):
    white_status = []
    black_status = []
    for piece in pieces:
        if piece.color == (255,255,255) and piece.deleted == False:
            white_status.append(piece.letter, piece.x, piece.y)
        elif piece.color == (0,0,0) and piece.deleted == False:
            black_status.append(piece.letter, piece.x, piece.y)
    return white_status, black_status
