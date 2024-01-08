from . import *
from differentfiles.colors import *
import numpy as np


class Board:

    def __init__(self, pieces = None, granularity = 1):
        '''
        ### init method to create new Board instance. 
        pieces: boolean flag. It must be true if you want to create a new board with all the pieces, false otherway. Default=True.
        granularity: number of points for each direction. Default=1.
        '''
        self.pieces = []
        self.granularity = granularity
        
        if pieces:
            self.set_pieces(pieces)
        else:
            self.new_board()

        self.whiteTurn = True

    
    def set_pieces(self, new_pieces):
        '''
        Board.set_pieces(self, new_pieces)
        Metodo che setta i pezzi della Board a un nuovo stato.
        new_pieces: lista di istanze Piece presenti nel nuovo stato
        '''
        self.pieces = []
        for p in new_pieces:
            if isinstance(p, Pawn):
                self.pieces.append(Pawn(p.start_x, p.start_y, p.color, p.deleted))
            elif isinstance(p, Rook):
                self.pieces.append(Rook(p.start_x, p.start_y, p.color, p.deleted))
            elif isinstance(p, Knight):
                self.pieces.append(Knight(p.start_x, p.start_y, p.color, p.deleted))
            elif isinstance(p, Bishop):
                self.pieces.append(Bishop(p.start_x, p.start_y, p.color, p.deleted))
            elif isinstance(p, Queen):
                self.pieces.append(Queen(p.start_x, p.start_y, p.color, p.deleted))
            elif isinstance(p, King):
                self.pieces.append(King(p.start_x, p.start_y, p.color, p.deleted))
            else:
                print("ERROR: Piece not found")
        
    # metodo che resituisce se la partita è finita 
    def is_terminal(self):
        count = 0
        for p in self.get_pieces():
            if isinstance(p, King) and p.deleted == False:
                count += 1
        return True if count < 2 else False
    
    def apply_move(self, move):
        '''
        ## applica una mossa sulla scacchiera cambiando lo stato della board modificando le coordinate di un pezzo\n
        board: stato della scacchiera\n
        restituisce la stessa istanza della board ma con le coordinate modificate del pezzo interessato
        '''
        pieces = self.get_pieces()
        # print(pieces)
        for i in range(len(pieces)):
            if (pieces[i].id == move[0]) and (pieces[i].color == move[1]) and (pieces[i].start_x == move[2][0]) and (pieces[i].start_y == move[2][1]):
                # Move the piece
                pieces[i].x = move[3][0]
                pieces[i].y = move[3][1]
                pieces[i].start_x = move[3][0]
                pieces[i].start_y = move[3][1]

                for j in range(len(pieces)):
                    if (j != i) and (not pieces[j].deleted) and (pieces[i].color != pieces[j].color) and (((pieces[i].start_x - pieces[j].start_x)**2 + (pieces[i].start_y - pieces[j].start_y)**2) <= ((2*pieces[i].radius)*(1-1e-15))**2): # Il fattore 1-1e-15 serve per far sì che il pezzo venga mangiato solo se si sovrappone anche solo minimamente e non se tange (o comunque per non lasciare al troncamento della variabile la decisione)
                        pieces[j].deleted = True
                        pieces[j].start_x, pieces[j].x = 100, 100 # Render outside the board
                break
        self.set_pieces(pieces)
        self.__update_state() # Update state

    def __update_state(self):
        new_pieces_list = []
        for p in self.get_pieces():
            if p.can_promote():
                new_pieces_list.append(Queen(p.start_x, p.start_y, p.color))
            else:
                new_pieces_list.append(p)
        self.set_pieces(new_pieces_list)

        for p in self.get_pieces():
            p.calc_paths(self.get_pieces())

    def set_turn(self, whiteTurn: bool):
        self.whiteTurn = whiteTurn

    def is_white_turn(self):
        return self.whiteTurn

    def new_board(self):
        self.pieces = [
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
    def get_chess_board_status(self):
        white_status = []
        black_status = []
        for piece in self.get_pieces():
            if piece.color == white and piece.deleted == False:
                white_status.append([piece.id, piece.start_x, piece.start_y])
            elif piece.color == black and piece.deleted == False:
                black_status.append([piece.id, piece.start_x, piece.start_y])
        return white_status, black_status
    
    def get_pieces(self):
        return self.pieces


    # grazie a questa funzione si ottengono tutte le mosse possibili per un pezzo in base alla sua direzione
    # granularity è il numero di punti che si vogliono ottenere per ogni direzione
    def get_points_from_distance(self, x_start, y_start, x_end, y_end, knight_flag=False, king_rook_flag=False):
        '''
        get_points_from_distance(x_start, y_start, x_end, y_end, knight_flag=False)
        The function returns all the possible moves in the following format:
        [(x1, y1), (x2, y2), ...]
        x_start: starting x of the path (current x position if the piece is a knight)
        y_start: starting y of the path (current y position if the piece is a knight)
        x_end: final x of the path (start angle if the piece is a knight)
        y_end: final y of the path (final angle if the piece is a knight)
        knight_flag: boolean flag. It must be true if the piece is a knight, false otherway. Default=False.
        '''
        list_points = []
        x_new, y_new = None, None
        # if king_rook_flag:
        #     #if the turn of king is first then we can do castling


        #     return list_points
        if not knight_flag:
            # If the piece is not a knight, the movement can be on a point in a line. 
            # In this case (x_start, y_start) are the coordinate of the first point of the line and (x_end, y_end) is the final point
            dx = (x_end - x_start)/self.granularity
            dy = (y_end - y_start)/self.granularity

            x_new = dx*np.arange(1, self.granularity+1) + x_start
            y_new = dy*np.arange(1, self.granularity+1) + y_start
        else:
            # If the piece is a knight, the movements are on a circonference arc with center (x_start, y_start). 
            # The variables x_end, y_end in this case are not really x and y but are the angles (in rad) of the first point of arc and of the last. 
            # In this sense we will rename them for a better readability. Finally, note that the angles are calculated from the positive semi-axis of y.
            start_ang, end_ang = x_end, y_end
            radius = math.sqrt(5) # I remember that the radius of the knight is sqrt(5) but you can change it if it is wrong

            if self.granularity == 1:
                x_new = np.cos(-(np.array([end_ang])-np.pi/2))*radius + x_start
                y_new = np.sin(-(np.array([end_ang])-np.pi/2))*radius + y_start
            else:
                delta = (end_ang - start_ang)/(self.granularity-1) # Angles variation (Let's do an example to explain why I have used granularity-1 as denominator. In the simplest case with only 2 points for arc, I want that the points are the first and the last points of the arc. Then, the delta have to be the total length of the arc.)
                x_new = np.cos(-(np.arange(self.granularity)*delta+start_ang-np.pi/2))*radius + x_start
                y_new = np.sin(-(np.arange(self.granularity)*delta+start_ang-np.pi/2))*radius + y_start
                # The two previous lines calculate the coordinates x and y of the avaiable moves from the possible angles. 
                # The main problems are that the angles are calculated from the positive y semi-axis and that are considered positives the clock-wise angles (the opposite of "normal" algebra). 
                # Then the formulas are not very trivial... The idea is to firstly transform the angles in a "conventional" representation and then compute the sin or cos.
        list_points = [(x_new[i], y_new[i]) for i in range(len(x_new))]
        return list_points


    # restituisce tutte le mosse possibili per tutti i pezzi presenti nella list_pieces nella forma [id, colore, (x_start, y_start), [(x_end, y_end), (x_end, y_end), ...]]
    def get_all_moves_from_distance(self, list_pieces):
        #print("list_pieces: ", list_pieces)
        list_moves = []

        for curr_piece in list_pieces:
            # curr_piece is [piece_name, color, current_position, final_positions_list]
            list_moves.append([curr_piece[0], curr_piece[1], curr_piece[2], []]) # the last empty list will contain the possible future moves

            for final_pos in curr_piece[3]: 
                
                is_knight = (curr_piece[0]==knight)
                is_king_rook = (curr_piece[0]==king) and curr_piece
                list_point = self.get_points_from_distance(curr_piece[2][0], curr_piece[2][1], final_pos[0], final_pos[1], knight_flag=is_knight, king_rook_flag=is_king_rook)
                
                list_moves[-1][-1] += list_point # list_moves
        return list_moves

    # restituisce tutte le direzioni di tutti i pezzi presenti diviso per colori nella forma [id, colore, (x_start, y_start), [(x_end, y_end), (x_end, y_end), ...]]
    def get_all_directions_all_in_one(self):
        '''
        DA FARE: non ha senso passare pieces visto che siamo nella classe board.
        Dopo aver adattato tutto si può togliere. Nel mentre ho messo un valore
        default e si può non usare il parametro (scelta migliore).
        '''
        pieces = self.get_pieces()

        list_directions_white = []
        list_directions_black = []
        for p in pieces:
            if not p.deleted:
                if p.color == black:
                    direction = p.get_all_directions_per_piece(pieces)
                    list_directions_black.append([p.id, p.color, (p.start_x, p.start_y), direction, p.turn])
                elif p.color == white:
                    direction = p.get_all_directions_per_piece(pieces)
                    list_directions_white.append([p.id, p.color, (p.start_x, p.start_y), direction, p.turn])
        
        return list_directions_white, list_directions_black
    
    def get_all_moves(self, turn):
        '''
        board.get_all_moves(self, turn)
        
        This method returns all the possible moves for the selected player in
        the following format: [id, color, (x_start, y_start), [(x_end, y_end),
        (x_end, y_end), ...]]
        turn: boolean that is true if is white turn, false if it is black turn
        '''

        white_directions, black_directions = self.get_all_directions_all_in_one()
        if turn:
            '''
            white turn
            '''
            return self.get_all_moves_from_distance(white_directions)
        
        '''
        black turn
        '''
        return self.get_all_moves_from_distance(black_directions)
    


    