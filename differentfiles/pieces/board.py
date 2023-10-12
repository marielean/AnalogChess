from . import *
from differentfiles.colors import *


class Board:

    def __init__(self):
        self.pieces = []
        self.pieces1 = []

    def new_board(self):
        self.pieces = [
            Pawn(0.5, 1.5, white),
            Rook(0.5, 0.5, white),
            King(4.5, 0.5, white),
            Knight(1.5, 0.5, white),
            Knight(6.5, 7.5, black),
            King(4.5, 7.5, black),
            Rook(0.5, 7.5, black),
            Pawn(0.5, 6.5, black),
        ]

        self.pieces1 = [
            Rook(0.5, 0.5, white),
            Rook(7.5, 0.5, white),
            Knight(1.5, 0.5, white),
            Knight(6.5, 0.5, white),
            Bishop(5.5, 0.5, white),
            Bishop(2.5, 0.5, white),
            King(4.5, 0.5, white),
            Queen(3.5, 0.5, white),
            Pawn(0.5, 1.5, white),
            Pawn(1.5, 1.5, white),
            Pawn(2.5, 1.5, white),
            Pawn(3.5, 1.5, white),
            Pawn(4.5, 1.5, white),
            Pawn(5.5, 1.5, white),
            Pawn(6.5, 1.5, white),
            Pawn(7.5, 1.5, white),
            Rook(0.5, 7.5, black),
            Rook(7.5, 7.5, black),
            Knight(1.5, 7.5, black),
            Knight(6.5, 7.5, black),
            Bishop(5.5, 7.5, black),
            Bishop(2.5, 7.5, black),
            King(4.5, 7.5, black),
            Queen(3.5, 7.5, black),
            Pawn(0.5, 6.5, black),
            Pawn(1.5, 6.5, black),
            Pawn(2.5, 6.5, black),
            Pawn(3.5, 6.5, black),
            Pawn(4.5, 6.5, black),
            Pawn(5.5, 6.5, black),
            Pawn(6.5, 6.5, black),
            Pawn(7.5, 6.5, black),
        ] 

    
        

    def get_pieces(self):
        return self.pieces


    # settare i pezzi con uno stato nuovo della classe Piece
    def set_pieces(self, piecesss):
        for p in piecesss:
            if p.id == pawn:
                self.pieces.append(Pawn(p.x, p.y, p.color))
            elif p.id == rook:
                self.pieces.append(Rook(p.x, p.y, p.color))
            elif p.id == knight:
                self.pieces.append(Knight(p.x, p.y, p.color))
            elif p.id == bishop:
                self.pieces.append(Bishop(p.x, p.y, p.color))
            elif p.id == queen:
                self.pieces.append(Queen(p.x, p.y, p.color))
            elif p.id == king:
                self.pieces.append(King(p.x, p.y, p.color))
            else:
                print("ERROR: Piece not found")