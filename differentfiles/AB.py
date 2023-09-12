

depth = 2

def apply_granularity(coordinate, granularity=1):
    rounded = round(coordinate, granularity)
    return rounded


def evaluate(pieces):
    white_score = 0
    black_score = 0
    for piece in pieces:
        if piece.color == (0,0,0) and piece.deleted == False:
            white_score += piece.weight
        if piece.color == (255,255,255) and piece.deleted == False:
            black_score += piece.weight
    return white_score, black_score