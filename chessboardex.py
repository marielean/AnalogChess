from differentfiles.pieces import *
from differentfiles.colors import *

# Scacchiera minimale con cavallo
chessboard_1 = [
    King(1.5,2.5,white),
    King(6.5,6.5,black),
    Bishop(3,7,black),
    Knight(4,4,white)
]

# Scacchiera minimale con pedone in più
chessboard_2 = [
    King(1.5,2.5,white),
    King(7.5,6.5,black),
    Bishop(3.5,5.5,black),
    Knight(4,5,white),
    Pawn(3,6,black)
]

# Tra re e alfiere l'algoritmo sceglie il re
chessboard_3 = [
    King(0.5,3.5,white),
    King(7.5,6.5,black),
    Bishop(5.5,3.5,white),
    Bishop(3,6,black),
    Pawn(2,2,white)
]

# 
chessboard_4 = [
    King(0.5,1.5,white),
    King(7.5,6.5,black),
    Bishop(5.5,3.5,white),
    # Bishop(3,6,black),
    # Pawn(3,5,white),
    # Pawn(2,2,white),
    # Pawn(0.5,2.5,black)
]