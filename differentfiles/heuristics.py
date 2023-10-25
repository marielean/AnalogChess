from .colors import *
import numpy as np
from differentfiles.pieces.knight import *
from differentfiles.pieces.pawn import *
from differentfiles.pieces.queen import *
from differentfiles.pieces.rook import *
from differentfiles.pieces.king import *
from differentfiles.pieces.bishop import *


def mean_path(piece):
    '''
    This function simpy returns the mean path length for piece given the piece. I write
    this information here because the mean path length is not a deterministic
    value but depends on the specific game. The expected value returned by this
    function is an hypothesis and technically represents an hyperparameter of
    the AI algorithm.
    '''
    if isinstance(piece, Pawn): return 1.2
    elif isinstance(piece, King): return 0.5
    elif isinstance(piece, Rook): return 10
    elif isinstance(piece, Queen): return 15
    elif isinstance(piece, Knight): return 7
    elif isinstance(piece, Bishop): return 10


def total_path_len(piece, edge_positions):
    '''
    total_path_len(curr_pos, edge_positions, weight, is_knight)
    This function calculates the total length of the avaiable path for a given
    piece. The length is simply the length of a line for all pieces except for
    the knight. In the last case the length is the length of the correspondents
    arc.
    piece: current piece object
    edge_positions: list of the edge positions [(x1, y1), (x2, y2), ...]. For
    the knight are the edge angles (NB. the list is returned by the method
    get_all_directions_per_piece of piece class)
    '''
    curr_pos = (piece.x, piece.y)
    weight = piece.weight
    is_knight = isinstance(piece, Knight)

    total_len = 0
    if is_knight:
        radius = np.sqrt(5)
        for edge_pos in edge_positions:
            total_len += weight*(radius*np.abs(edge_pos[1]-edge_pos[0]))/mean_path(piece) # A possibility is to set a penality. For example it can be related to the possiblity that the piece could be eatten (it is not easy to do)
    else:
        for edge_pos in edge_positions:
            total_len += weight*np.sqrt((curr_pos[0] - edge_pos[0])**2 + (curr_pos[1] - edge_pos[1])**2)/mean_path(piece)
    return total_len


def custom_heuristic_1(board, player):
    '''
    custom_heuristic_1(pieces, player)
    This function calculates a score for players based on a custom heuristic
    function. The function is based on the total length of the avaiable path per
    piece, weighted on the piece weight, and normalized on the mean path of the piece
    '''
    pieces = board.get_pieces()
    white_score = 0 # white score
    black_score = 0 # white score

    for piece in pieces:
        if piece.color == white and piece.deleted == False:
            white_score += total_path_len(piece, piece.get_all_directions_per_piece(pieces))
        if piece.color == black and piece.deleted == False:
            black_score += total_path_len(piece, piece.get_all_directions_per_piece(pieces))

    return white_score-black_score if player else black_score-white_score

def custom_heuristic_0(board, player):
    '''
    custom_heuristic_0(pieces, player)
    This function calculates a score for players based on a custom heuristic
    function. The function is based on the pieces weight difference
    '''
    pieces = board.get_pieces()

    white_score = 0
    black_score = 0
    for piece in pieces:
        if piece.color == white and piece.deleted == False:
            white_score += piece.weight
        if piece.color == black and piece.deleted == False:
            black_score += piece.weight
    return white_score-black_score if player else black_score-white_score