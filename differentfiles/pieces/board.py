from . import *
from differentfiles.colors import *
import numpy as np


class Board:

    def __init__(self):
        self.pieces = []
        self.pieces1 = []
        self.whiteTurn = True

    # settare i pezzi con uno stato nuovo della classe Piece
    def set_pieces(self, piecesss: dict):
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
        
    # metodo che resituisce se la partita è finita 
    def is_terminal(self, pieces: dict, whites_turn: bool):
        if whites_turn:
            for p in pieces:
                if p.color == black and p.id == "K" and p.deleted:
                    return True, "bianco ha vinto"
        else:
            for p in pieces:
                if p.color == white and p.id == "K" and p.deleted:
                    return True, "nero ha vinto"
        return False
    
    # applichi una mossa sulla scacchiera cambiando lo stato della board modificando le coordinate di un pezzo
    def board_apply_move(self, board, move: dict):
        '''
        ## applichi una mossa sulla scacchiera cambiando lo stato della board modificando le coordinate di un pezzo\n
        board: stato della scacchiera\n
        restituisce la stessa istanza della board ma con le coordinate modificate del pezzo interessato
        '''
        pieces = board.get_pieces()
        print("pieces:", pieces[0].id)
        for p in pieces:
            if p.id == move[0] and p.color == move[1] and p.x == move[2][0] and p.y == move[2][1]:
                #print(move[0], move[1], move[2][0], move[2][1])
                p.x = move[3][0]
                p.y = move[3][1]
                break
        return board
    
    # metodo che restituisce la nuova disposizione dei pezzi in base alla mossa effettuata (move del tipo [id, colore, (x_start, y_start), (x_end, y_end)])
    def apply_move(self, pieces, move):
        #print("apply_move: ", move)
        for p in pieces:
            if p.id == move[0] and p.color == move[1] and p.x == move[2][0] and p.y == move[2][1]:
                #print(move[0], move[1], move[2][0], move[2][1])
                p.x = move[3][0]
                p.y = move[3][1]
                break
        return pieces

    def set_turn(self, whiteTurn: bool):
        self.whiteTurn = whiteTurn

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

    #restituisce lo stato della scacchiera con le posizioni di tutti i pezzi ancora in gioco diviso per colori
    def get_chess_board_status(self, pieces):
        white_status = []
        black_status = []
        for piece in pieces:
            if piece.color == white and piece.deleted == False:
                white_status.append(piece.letter, piece.x, piece.y)
            elif piece.color == black and piece.deleted == False:
                black_status.append(piece.letter, piece.x, piece.y)
        return white_status, black_status
    
    def get_pieces(self):
        return self.pieces


    # grazie a questa funzione si ottengono tutte le mosse possibili per un pezzo in base alla sua direzione
    # granularity è il numero di punti che si vogliono ottenere per ogni direzione
    def get_points_from_distance(self, x_start, y_start, x_end, y_end, granularity=2, knight_flag=False):
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
    def get_all_moves_from_distance(self, list_pieces: dict):
        #print("list_pieces: ", list_pieces)
        list_moves = []

        for curr_piece in list_pieces:
            # curr_piece is [piece_name, color, current_position, final_positions_list]
            list_moves.append([curr_piece[0], curr_piece[1], curr_piece[2], []]) # the last empty list will contain the possible future moves

            for final_pos in curr_piece[3]: 
                
                is_knight = (curr_piece[0]==knight)
                list_point = self.get_points_from_distance(curr_piece[2][0], curr_piece[2][1], final_pos[0], final_pos[1], knight_flag=is_knight)
                
                list_moves[-1][-1] += list_point # list_moves
        return list_moves

    # restituisce tutte le direzioni di tutti i pezzi presenti diviso per colori nella forma [id, colore, (x_start, y_start), [(x_end, y_end), (x_end, y_end), ...]]
    def get_all_directions_all_in_one(self, pieces):
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