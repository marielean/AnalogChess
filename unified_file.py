import numpy as np
import random, math, pygame
from pygame import gfxdraw

class Board:

    def __init__(self, pieces = True, granularity = 1):
        '''
        ### init method to create new Board instance. 
        pieces: boolean flag. It must be true if you want to create a new board with all the pieces, false otherway. Default=True.
        granularity: number of points for each direction. Default=1.
        '''
        self.pieces = []
        self.granularity = granularity
        
        if pieces:
            self.new_board()
        else:
            self.finite_pieces()

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
                self.pieces.append(Pawn(p.start_x, p.start_y, p.color))
            elif isinstance(p, Rook):
                self.pieces.append(Rook(p.start_x, p.start_y, p.color))
            elif isinstance(p, Knight):
                self.pieces.append(Knight(p.start_x, p.start_y, p.color))
            elif isinstance(p, Bishop):
                self.pieces.append(Bishop(p.start_x, p.start_y, p.color))
            elif isinstance(p, Queen):
                self.pieces.append(Queen(p.start_x, p.start_y, p.color))
            elif isinstance(p, King):
                self.pieces.append(King(p.start_x, p.start_y, p.color))
            else:
                print("ERROR: Piece not found")
        
    # metodo che resituisce se la partita è finita 
    def is_terminal(self):
        cont = 0
        for p in self.get_pieces():
            if isinstance(p, King) and p.deleted == False:
                cont += 1
        print("cont: ", cont)
        return True if cont < 2 else False
    
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
                    if (j != i) and (pieces[i].color != pieces[j].color) and (((pieces[i].start_x - pieces[j].start_x)**2 + (pieces[i].start_y - pieces[j].start_y)**2) < (2*pieces[i].radius)**2):
                        pieces[j].deleted = True
                        pieces[j].start_x, pieces[j].x = 100, 100 # Render outside the board
                break

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

    def finite_pieces(self):
        self.pieces = [
            King(1.5,1.5,white),
            King(6.5,6.5,black),
            Bishop(4,2,white),
            Bishop(3,7,black),
        ]
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
        # self.pieces = [
        #     Rook(0.5, 0.5, white),
        #     Knight(1.5, 0.5, white),
        #     King(4.5, 0.5, white),
        #     Pawn(0.5, 1.5, white),
        #     Rook(0.5, 7.5, black),
        #     Knight(6.5, 7.5, black),
        #     King(4.5, 7.5, black),
        #     Pawn(0.5, 6.5, black)
        # ] 

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
    def get_points_from_distance(self, x_start, y_start, x_end, y_end, knight_flag=False):
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
                list_point = self.get_points_from_distance(curr_piece[2][0], curr_piece[2][1], final_pos[0], final_pos[1], knight_flag=is_knight)
                
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
                    list_directions_black.append([p.id, p.color, (p.start_x, p.start_y), direction])
                elif p.color == white:
                    direction = p.get_all_directions_per_piece(pieces)
                    list_directions_white.append([p.id, p.color, (p.start_x, p.start_y), direction])
        
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
    
class IA:
    def __init__(self, utility=custom_heuristic_0, algorithm = 'AlphaBeta', depth = 1):
        '''
        Possible algorithms: MiniMax, AlphaBeta, Random
        '''
        self.whiteTurn = True
        self.utility = utility
        self.algorithm = algorithm
        self.depth = depth

    def set_turn(self, whiteTurn):
        self.whiteTurn = whiteTurn

    # function for best move
    def get_best_move(self, board):
        if self.algorithm == "MiniMax":
            return self.__minimax_search(board)
        elif self.algorithm == "AlphaBeta":
            return self.__alphabeta_search(board)
        elif self.algorithm == "Random":
            return self.__random_search(board)

    
    def __random_search(self, board: Board):
        """
        Selects a random move from the valid moves for the current players turn
        :param board: the current board being used for the game (pieces)
        :return: list representing move; format: [id, color, (x_start, y_start), (x_end, y_end)]
        """
        list_moves = board.get_all_moves(board.is_white_turn())

        random_piece = random.choice(list_moves)
        r_move = random.choice(random_piece[-1])
        move = [random_piece[0], random_piece[1], random_piece[2], r_move]
        return move         

    def __minimax_search(self, board: Board):
        '''
        Metodo che implementa la funzione minimax.
        board: current board instance (current state)
        depth: maximum depth of the algorithm
        '''
        max_player = board.is_white_turn()
        depth = self.depth

        def max(curr_board, depth):
            
            if (depth == 0 or curr_board.is_terminal()):
                return None, self.utility(curr_board, max_player)
            
            # initialization
            max_value = -np.inf
            max_move = None

            # algorithm iteration (max is the turn player)
            possible_moves = curr_board.get_all_moves(max_player)
            for piece in possible_moves:
                # print(piece)
                for next_position in piece[3]:
                    move = [piece[0],piece[1],piece[2],next_position]
                    next_board = Board(curr_board.get_pieces())
                    next_board.apply_move(move)

                    _, value = min(next_board, depth-1)
                    if value > max_value:
                        max_value = value
                        max_move = move
            return max_move, max_value
        
        def min(curr_board, depth):
            if (depth == 0 or curr_board.is_terminal()):
                return None, self.utility(curr_board, max_player)
            
            # initialization
            min_value = np.inf
            min_move = None

            # algorithm iteration (min is the turn player)
            possible_moves = curr_board.get_all_moves(not max_player)
            for piece in possible_moves:
                for next_position in piece[3]:
                    move = [piece[0],piece[1],piece[2],next_position]
                    next_board = Board(curr_board.get_pieces())
                    next_board.apply_move(move)

                    _, value = max(next_board, depth-1)
                    if value > min_value:
                        min_value = value
                        min_move = move
            return min_move, min_value

        move, value = max(board, depth)
        return move
    
    def __alphabeta_search(self, board: Board):
        '''
        Metodo che implementa l'algoritmo alpha-beta.
        board: current board instance (current state)
        '''
        max_player = board.is_white_turn()

        def max(curr_board, alpha, beta, depth):
            
            if (depth == 0 or curr_board.is_terminal()):
                return None, self.utility(curr_board, max_player)
            
            # initialization
            max_value = -np.inf
            max_move = None

            # algorithm iteration (max is the turn player)
            possible_moves = curr_board.get_all_moves(max_player)
            for piece in possible_moves:
                # print(piece)
                for next_position in piece[3]:
                    move = [piece[0],piece[1],piece[2],next_position]
                    next_board = Board(curr_board.get_pieces())
                    next_board.apply_move(move)

                    _, value = min(next_board, alpha, beta, depth-1)
                    if value > max_value:
                        max_value = value
                        max_move = move
                    if max_value >= beta:
                        return max_move, max_value
                    if max_value >= alpha:
                        alpha = max_value
            return max_move, max_value
        
        def min(curr_board, alpha, beta, depth):
            if (depth == 0 or curr_board.is_terminal()):
                return None, self.utility(curr_board, max_player)
            
            # initialization
            min_value = np.inf
            min_move = None

            # algorithm iteration (min is the turn player)
            possible_moves = curr_board.get_all_moves(not max_player)
            for piece in possible_moves:
                for next_position in piece[3]:
                    move = [piece[0],piece[1],piece[2],next_position]
                    next_board = Board(curr_board.get_pieces())
                    next_board.apply_move(move)

                    _, value = max(next_board, alpha, beta, depth-1)
                    if value < min_value:
                        min_value = value
                        min_move = move
                    if min_value <= alpha:
                        return min_move, min_value
                    if min_value < beta:
                        beta = min_value
            return min_move, min_value

        move, value = max(board, -np.inf, np.inf, self.depth)
        return move


class Piece:
    width, height = 640, 640
    size = (width, height)


    def dist(p1, p2):
        return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


    def to_game_coords(p):
        return (p[0] / width * 8, 8 - p[1] / height * 8)


    def to_screen_coords(p):
        return (p[0] / 8 * width, height - p[1] / 8 * width)


    def clamp(n, smallest, largest):
        return max(smallest, min(n, largest))



    black = (0, 0, 0)
    white = (255, 255, 255)
    light_gray = (255, 222, 173)
    dark_gray = (222, 184, 135)


    RED_HIGHLIGHT = (240, 50, 50, 150)

    GREEN_HIGHLIGHT = (0, 255, 0, 80)


    pawn = "P"
    rook = "R"
    knight = "K"
    bishop = "B"
    queen = "Q"
    king = "Ki"

    depth_size = 1

    Radius = math.sqrt(5)

    screen = pygame.display.set_mode(size)

    see_through = pygame.Surface((width, height)).convert_alpha()
    see_through2 = pygame.Surface((width, height)).convert_alpha()
    see_through.fill((0, 0, 0, 0))


    def get_fontname():
        # Clever way to get the best font for the system (from @andychase)
        # font_options = ["segoeuisymbol", "applesymbols", "DejaVuSans"]
        # font_to_use = font_options[0]
        font_to_use = "DejaVuSans"
        # for font in font_options:
        #     if font in pygame.font.get_fonts():
        #         font_to_use = font
        return font_to_use


    def draw_checkers():
        for i in range(8):
            for j in range(8):
                size = width // 8
                color = dark_gray
                if (i + j) % 2 == 0:
                    color = light_gray
                pygame.draw.rect(screen, color, (i * size, j * size, size, size))


    def draw_circle(surface, x, y, radius, color):
        gfxdraw.aacircle(surface, x, y, radius, color)
        gfxdraw.filled_circle(surface, x, y, radius, color)


    def pygame_draw_circle(surface, color, screen_coords, radius, **kwargs):
        pygame.draw.circle(surface, color, screen_coords, radius, **kwargs)


    def draw_circle_outline(surface, x, y, radius, color):
        gfxdraw.aacircle(surface, x, y, radius, color)
        gfxdraw.circle(
            surface, x, y, radius, (255 - color[0], 255 - color[1], 255 - color[2])
        )


    def draw_center_text(text):
        screen.blit(
            text,
            (
                width // 2 - text.get_width() // 2,
                height // 2 - text.get_height() // 2,
            ),
        )


    def draw_line_round_corners_polygon(surf, p1, p2, c, w):
        if p1 != p2:
            p1v = pygame.math.Vector2(p1)
            p2v = pygame.math.Vector2(p2)
            lv = (p2v - p1v).normalize()
            lnv = pygame.math.Vector2(-lv.y, lv.x) * w // 2
            pts = [p1v + lnv, p2v + lnv, p2v - lnv, p1v - lnv]
            pygame.draw.polygon(surf, c, pts)
            pygame.draw.circle(surf, c, p1, round(w / 2))
            pygame.draw.circle(surf, c, p2, round(w / 2))
        else:
            pygame.draw.circle(surf, c, p1, round(w / 2))


    def getpolygon(origin, radius, N, start=0, end=None):
        out = []
        x, y = origin
        Nf = float(N)
        if end is None:
            end = math.pi * 2
        for i in range(N):
            xp = x + radius * math.sin(end * i / Nf + start)
            yp = y - radius * math.cos(end * i / Nf + start)
            out.append((xp, yp))
        return out


    def arc(surf, color, origin, radius, start=0, end=None, width=0, N=64):
        if width == 0 or width >= radius * 0.5:
            p2 = [origin]
        else:
            p2 = getpolygon(origin, radius - width, N, start=start, end=end)
            p2.reverse()
        p1 = getpolygon(origin, radius, N, start=start, end=end)
        p1.extend(p2)
        r = pygame.draw.polygon(surf, color, p1)
        return r


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
    # x pos and y pos are on a grid of size 8, normal cartesian coordinates
    def __init__(self, x_pos, y_pos, color):
        diameter = 0.7
        self.x = x_pos
        self.y = y_pos
        self.radius = diameter / 2
        self.grabbed = False
        self.targeted = False
        self.color = color

        self.start_x = self.x
        self.start_y = self.y
        text_scale = 0.85
        self.letter = "X"
        self.id = "XX"
        self.font = pygame.font.SysFont(
            get_fontname(), int(diameter / 8 * 640 * text_scale)
        )
        self.text = self.font.render(self.letter, True, (255, 255, 255))
        self.direction = False
        self.targeted = False
        self.turn = 0
        self.deleted = False
        self.weight = 0

        self.white_turn = True

    def delete(self):
        del self

    def set_id(self, id):
        self.id = id

    def get_turn(self):
        return self.white_turn

    def set_weight(self, weight):
        self.weight = weight

    def set_letter(self, letter):
        self.letter = letter
        if not self.grabbed:
            self.text = self.font.render(
                self.letter,
                True,
                (255 - self.color[0], 255 - self.color[1], 255 - self.color[2]),
            )
        else:
            self.text = self.font.render(self.letter, True, (0, 255, 0))

    def can_promote(self):
        return False


    #this is only used by the Knight so we can only calculate paths once instead of every frame
    def calc_paths(self,pieces):
        pass
    
    def draw_paths(self, pieces):
        pass

    def target(self):
        self.targeted = True
        self.text = self.font.render(self.letter, True, (255, 0, 0))

    def untarget(self):
        self.targeted = False
        self.set_letter(self.letter)

    def draw(self):
        x = int(self.x / 8 * width)
        y = height - int(self.y / 8 * height)
        # draw_circle(screen,x,y,int(self.radius/8*width),(255-self.color[0],255-self.color[1],255-self.color[2]))
        draw_circle(screen, x, y, int(self.radius / 8 * width), self.color)
        screen.blit(
            self.text,
            (x - self.text.get_width() // 2, y - 2 - self.text.get_height() // 2),
        )

    def try_grab(self, pos):
        if dist(pos, (self.x, self.y)) < self.radius:
            self.grabbed = True
            self.text = self.font.render(self.letter, True, (0, 255, 0))

    def cancel(self, pieces):
        if self.grabbed:
            self.grabbed = False
            for piece in pieces:
                if piece.targeted:
                    piece.untarget()
            self.direction = False
            self.text = self.font.render(
                self.letter,
                True,
                (255 - self.color[0], 255 - self.color[1], 255 - self.color[2]),
            )
            self.x = self.start_x
            self.y = self.start_y

    def confirm(self, pieces):

        new_pieces = []
        if self.grabbed:
            self.grabbed = False
            for piece in pieces:
                if piece.targeted:
                    piece.deleted = True
                    piece.x = 100
                    piece.start_x = 100
                    piece.delete()
                else:
                    new_pieces.append(piece)
            self.direction = False
            self.text = self.font.render(
                self.letter,
                True,
                (255 - self.color[0], 255 - self.color[1], 255 - self.color[2]),
            )

            self.start_x = self.x
            self.start_y = self.y
            self.turn += 1

        pieces = new_pieces
        
        return new_pieces


    def ungrab(self, pieces):
        if self.grabbed:

            if (
                abs(self.x - self.start_x) < 1 / 1000
                and abs(self.y - self.start_y) < 1 / 1000
            ):
                self.cancel(pieces)
                return

            font = pygame.font.SysFont("oldenglishtext", int(80))
            confirm_text = font.render("Confirm?", True, black)
            draw_center_text(confirm_text)

            pygame.display.flip()
            # while not done:
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    if event.type == pygame.MOUSEBUTTONUP:
                        if (dist(to_game_coords(pygame.mouse.get_pos()), (self.x, self.y)) < self.radius):
                            self.confirm(pieces)
                            print("Pezzo giocato", self.id)
                                
                            if self.white_turn and self.color == white:
                                #print("white turn, next turn black")
                                self.white_turn = False
                                for one_piece in pieces:
                                    one_piece.white_turn = False
                                return True
                            elif not self.white_turn and self.color == black:
                                #print("black turn, next turn white")
                                self.white_turn = True
                                for one_piece in pieces:
                                    one_piece.white_turn = True
                                return True
                            # print("confirm", self.white_turn)
                            return True
                        else:
                            self.cancel(pieces)
                            # print("cancel", self.white_turn)
                            return False

                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            self.confirm(pieces)
                            print("confirm")
                            return True
                        elif event.key == pygame.K_ESCAPE:
                            self.cancel(pieces)
                            print("cancel")
                            return False

    def overlaps(self, piece):
        return dist((self.x, self.y), (piece.x, piece.y)) < self.radius * 2

    def apply_granularity(self, coordinate, granularity=1):
        rounded = round(coordinate, granularity)
        return rounded

    # math shit
    def slide(self, dx, dy, pieces, capture=True, fake=False):

        dx = self.apply_granularity(dx)
        dy = self.apply_granularity(dy)

        all_pieces = pieces
        if capture:
            pieces = [
                p
                for p in pieces
                if (p.x - self.start_x) * dx + (p.y - self.start_y) * dy > 0
                and p != self
                and p.color == self.color
            ]
        if fake:
            pieces = [
                p
                for p in pieces
                if (p.x - self.start_x) * dx + (p.y - self.start_y) * dy > 0
                and p != self
                and p.color == self.color
                and p.targeted == False
            ]
        else:
            pieces = [
                p
                for p in pieces
                if (p.x - self.start_x) * dx + (p.y - self.start_y) * dy > 0
                and p != self
            ]

        angle = math.atan2(dy, dx)

        # resolve wall collisions
        # dont do this if the piece is off the board it wont work right
        if 0 <= self.start_x <= 8 and 0 <= self.start_y <= 8:
            if abs(dx) > 0:
                if self.start_x + dx + self.radius > 8:
                    ratio = dy / dx
                    dx = (8 - self.start_x) - self.radius
                    dy = ratio * ((8 - self.start_x) - self.radius)

                if self.start_x + dx - self.radius < 0:
                    ratio = dy / dx
                    dx = -self.start_x + self.radius
                    dy = ratio * (-self.start_x + self.radius)

            if abs(dy) > 0:
                if self.start_y + dy + self.radius > 8:
                    ratio = dx / dy
                    dy = (8 - self.start_y) - self.radius
                    dx = ratio * ((8 - self.start_y) - self.radius)
                if self.start_y + dy - self.radius < 0:
                    ratio = dx / dy
                    dy = -self.start_y + self.radius
                    dx = ratio * (-self.start_y + self.radius)

        first_block = False
        block_dist = 99999999
        block_perp_dist = 999999999

        full_dist = math.sqrt(dx**2 + dy**2)
        new_dist = full_dist
        # find first piece that intersects with the line of travel. Move it back behind this piece.
        for piece in pieces:
            # formula for distance from point to line
            h = abs(
                math.cos(angle) * (self.y - piece.y)
                - math.sin(angle) * (self.x - piece.x)
            )

            if h < piece.radius * 2:
                proj_dist = math.sqrt(
                    dist((self.start_x, self.start_y), (piece.x, piece.y)) ** 2 - h**2
                )
                if proj_dist < block_dist:
                    block_dist = proj_dist
                    block_perp_dist = h
                    first_block = piece

        hit_first_block = False
        if first_block:
            distance = dist(
                (first_block.x, first_block.y), (self.start_x + dx, self.start_y + dy)
            )
            if math.sqrt(dx**2 + dy**2) > block_dist:
                hit_first_block = True
                new_dist = block_dist - math.sqrt(
                    4 * self.radius**2 - block_perp_dist**2
                )

        if abs(full_dist) > 0:
            self.x = self.start_x + dx * new_dist / full_dist
            self.y = self.start_y + dy * new_dist / full_dist

        new_new_dist = new_dist
        first_hit_piece = False
        # Still could be colliding with pieces, check collisions with all other pieces and move it behind minimum distance collision
        for piece in pieces:
            if self.overlaps(piece):
                block_perp_dist = abs(
                    math.cos(angle) * (self.y - piece.y)
                    - math.sin(angle) * (self.x - piece.x)
                )
                block_dist = math.sqrt(
                    dist((self.start_x, self.start_y), (piece.x, piece.y)) ** 2
                    - block_perp_dist**2
                )
                new_new_dist = block_dist - math.sqrt(
                    4 * self.radius**2 - block_perp_dist**2
                )
                if new_new_dist < new_dist:
                    new_dist = new_new_dist
                    first_hit_piece = piece

        if abs(full_dist) > 0:
            self.x = self.start_x + dx * new_dist / full_dist
            self.y = self.start_y + dy * new_dist / full_dist
        else:
            self.x = self.start_x
            self.y = self.start_y

        if capture:
            self.slide_attack(
                (self.x - self.start_x), self.y - self.start_y, all_pieces, fake=fake
            )
        
        '''print("letter, ", self.letter, "start_x ", self.start_x, "start_y, ", self.start_y, "dx ", dx, 
              ", ", "dy ", dy, ", \n", "new_dist ", new_dist, ", ", "new_new_dist", new_new_dist, 
              "full_dist ", full_dist, "first_hit_piece ", first_hit_piece, 
              "\nfirst_block ", first_block, "hit_first_block ", hit_first_block)'''

    def slide_attack(self, dx, dy, pieces, fake=False):

        angle = math.atan2(dy, dx)
        all_pieces = pieces
        pieces = [
            p
            for p in pieces
            if (p.x - self.start_x) * dx + (p.y - self.start_y) * dy > 0
            and p != self
            and p.color != self.color
        ]

        first_piece_hit = False
        first_hit_dist = 99999999
        perp_dist = 999999999

        full_dist = math.sqrt(dx**2 + dy**2)
        new_dist = full_dist

        # find piece that will be hit first
        for piece in pieces:
            # formula for distance from point to line
            h = abs(
                math.cos(angle) * (self.y - piece.y)
                - math.sin(angle) * (self.x - piece.x)
            )

            if h < piece.radius * 2:
                d = dist((piece.x, piece.y), (self.start_x, self.start_y))
                hit_dist = math.sqrt(d**2 - h**2) - math.sqrt(
                    4 * piece.radius**2 - h**2
                )
                if hit_dist < first_hit_dist:
                    first_hit_dist = hit_dist
                    perp_dist = h
                    first_piece_hit = piece

        if not fake:
            for piece in all_pieces:
                piece.untarget()

        if first_piece_hit:
            if self.overlaps(first_piece_hit):
                if not fake:
                    first_piece_hit.target()
            elif dist(
                (self.x, self.y), (self.start_x, self.start_y)
            ) > first_hit_dist + 2 * math.sqrt(4 * piece.radius**2 - perp_dist**2):
                new_dist = first_hit_dist + 2 * math.sqrt(4 * piece.radius**2 - perp_dist**2)
                if not fake:
                    first_piece_hit.target()

        if abs(full_dist) > 0:
            self.x = self.start_x + dx * new_dist / full_dist
            self.y = self.start_y + dy * new_dist / full_dist

        # Still could be colliding with pieces, check collisions with all other pieces and target them
        if not fake:
            for piece in pieces:
                if self.overlaps(piece):
                    piece.target()

    def select_path(self, start, paths, point):
        min_h = 9999999
        min_path = None
        for path in paths:
            h = abs(
                (path[0]) * (start[1] - point[1]) - (start[0] - point[0]) * path[1]
            ) / math.sqrt((path[0]) ** 2 + path[1] ** 2)
            if h < min_h:
                min_h = h
                min_path = path
                dot_prod = path[0] * (point[0] - start[0]) + path[1] * (
                    point[1] - start[1]
                )
                if dot_prod == 0:
                    min_l = 0
                else:
                    min_l = (
                        math.sqrt(dist(point, start) ** 2 - h**2)
                        * dot_prod
                        / abs(dot_prod)
                    )

        return (min_path, min_l)

    def draw_moves(self, pieces):
        pass

    def get_all_directions_per_piece(self, pieces):
        pass

class Bishop(Piece):
    def __init__(self, x, y, c):
        super().__init__(x, y, c)
        self.set_letter("♗")
        self.set_id(bishop)
        self.set_weight(3)

    def delete(self):
        return super().delete()

    def get_all_directions_per_piece(self, pieces):
        fake_piece = Bishop(self.start_x, self.start_y, self.color)
        directions = [[10, 10], [-10, -10], [10, -10], [-10, 10]]
        end_positions = []
        for d in directions:
            fake_piece.slide(d[0], d[1], [p for p in pieces if p != self], fake=True)
            end_positions.append((fake_piece.x, fake_piece.y))
            fake_piece.slide(0, 0, [p for p in pieces if p != self], fake=True)

        end_positions_purified = []
        for end_position in end_positions:
            if end_position != (self.start_x, self.start_y):
                end_positions_purified.append(end_position)
        return end_positions_purified


    def draw_moves(self, pieces):
        fake_piece = Bishop(self.start_x, self.start_y, self.color)
        directions = [[10, 10], [-10, -10], [10, -10], [-10, 10]]
        end_positions = []
        for d in directions:
            fake_piece.slide(d[0], d[1], [p for p in pieces if p != self], fake=True)
            end_positions.append((fake_piece.x, fake_piece.y))
            fake_piece.slide(0, 0, [p for p in pieces if p != self], fake=True)

        for end_pos in end_positions:
            draw_line_round_corners_polygon(
                see_through2,
                to_screen_coords((self.start_x, self.start_y)),
                to_screen_coords(end_pos),
                GREEN_HIGHLIGHT,
                self.radius * 2 * 640 / 8,
            )

    def drag(self, new_p, pieces):
        if self.grabbed:
            self.slide(0, 0, pieces)
            path, dist = self.select_path(
                (self.start_x, self.start_y), [[1, 1], [-1, 1]], new_p
            )
            path_len = math.sqrt(path[0] ** 2 + path[1] ** 2)
            self.slide(path[0] * dist / path_len, path[1] * dist / path_len, pieces)

    def draw_paths(self, pieces):
        if self.targeted:
            return

        if self.deleted:
            return

        fake_piece = Bishop(self.start_x, self.start_y, self.color)

        directions = [[10, 10], [-10, -10], [10, -10], [-10, 10]]
        end_positions = []
        for d in directions:
            fake_piece.slide(d[0], d[1], [p for p in pieces if p != self], fake=True)
            end_positions.append((fake_piece.x, fake_piece.y))
            fake_piece.slide(0, 0, [p for p in pieces if p != self], fake=True)

        for end_pos in end_positions:
            draw_line_round_corners_polygon(
                see_through,
                to_screen_coords((self.start_x, self.start_y)),
                to_screen_coords(end_pos),
                RED_HIGHLIGHT,
                self.radius * 2 * 640 / 8,
            )

class King(Piece):
    def __init__(self, x, y, c):
        super().__init__(x, y, c)
        self.set_letter("♔")
        self.set_id(king)
        self.set_weight(100)
        self.turn = 0

    def delete(self):
        return super().delete()

    def get_all_directions_per_piece(self, pieces):
        fake_piece = King(self.start_x, self.start_y, self.color)

        long_castle = True
        short_castle = True
        left_rook = None
        right_rook = None

        back_row = 0.5
        if self.color == black:
            back_row = 7.5

        for p in pieces:
            if isinstance(p, Rook) and p.color == self.color and p.turn == 0:
                if p.x < 4:
                    left_rook = p
                else:
                    right_rook = p
                continue
            if p == self:
                continue
            if abs(p.y - back_row) < self.radius * 2:
                if 0.5 < p.x < 4.5:
                    long_castle = False
                if 4.5 < p.x < 7.5:
                    short_castle = False
        '''if self.turn == 0:
            if long_castle:
                if left_rook:
                    if left_rook.turn == 0:
                        pygame_draw_circle(
                            see_through2,
                            GREEN_HIGHLIGHT,
                            to_screen_coords((self.start_x - 2, self.start_y)),
                            self.radius / 8 * 640,
                        )
            if short_castle:
                if right_rook:
                    if right_rook.turn == 0:
                        pygame_draw_circle(
                            see_through2,
                            GREEN_HIGHLIGHT,
                            to_screen_coords((self.start_x + 2, self.start_y)),
                            self.radius / 8 * 640,
                        )
'''
        if self.turn == 0:
            pieces = [p for p in pieces if (p != left_rook and p != right_rook)]

        directions = [
            [1, 1],
            [-1, -1],
            [1, -1],
            [-1, 1],
            [0, 1],
            [0, -1],
            [1, 0],
            [-1, 0],
        ]
        end_positions = []
        for d in directions:
            fake_piece.slide(d[0], d[1], [p for p in pieces if p != self], fake=True)
            end_positions.append((fake_piece.x, fake_piece.y))
            fake_piece.slide(0, 0, [p for p in pieces if p != self], fake=True)

        end_positions_purified = []
        for end_position in end_positions:
            if end_position != (self.start_x, self.start_y):
                end_positions_purified.append(end_position)
        return end_positions_purified

    def draw_moves(self, pieces):
        fake_piece = King(self.start_x, self.start_y, self.color)

        long_castle = True
        short_castle = True
        left_rook = None
        right_rook = None

        back_row = 0.5 if self.color == black else 7.5

        for p in pieces:
            if isinstance(p, Rook) and p.color == self.color and p.turn == 0:
                if p.x < 4:
                    left_rook = p
                else:
                    right_rook = p
                continue
            if p == self:
                continue
            if abs(p.y - back_row) < self.radius * 2:
                if 0.5 < p.x < 4.5:
                    long_castle = False
                if 4.5 < p.x < 7.5:
                    short_castle = False

        if self.turn == 0:
            if long_castle and left_rook and left_rook.turn == 0:
                pygame_draw_circle(
                    see_through2,
                    GREEN_HIGHLIGHT,
                    to_screen_coords((self.start_x - 2, self.start_y)),
                    self.radius / 8 * 640,
                )
            if short_castle and right_rook and right_rook.turn == 0:
                pygame_draw_circle(
                    see_through2,
                    GREEN_HIGHLIGHT,
                    to_screen_coords((self.start_x + 2, self.start_y)),
                    self.radius / 8 * 640,
                )

        if self.turn == 0:
            pieces = [p for p in pieces if p != left_rook and p != right_rook]

        directions = [
            [1, 1],
            [-1, -1],
            [1, -1],
            [-1, 1],
            [0, 1],
            [0, -1],
            [1, 0],
            [-1, 0],
        ]
        end_positions = []
        for d in directions:
            fake_piece.slide(d[0], d[1], [p for p in pieces if p != self], fake=True)
            end_positions.append((fake_piece.x, fake_piece.y))
            fake_piece.slide(0, 0, [p for p in pieces if p != self], fake=True)

        for end_pos in end_positions:
            draw_line_round_corners_polygon(
                see_through2,
                to_screen_coords((self.start_x, self.start_y)),
                to_screen_coords(end_pos),
                GREEN_HIGHLIGHT,
                self.radius * 2 * 640 / 8,
            )

    def drag(self, new_p, pieces):
        if self.grabbed:
            long_castle = True
            short_castle = True
            left_rook = None
            right_rook = None
            back_row = 0.5 if self.color == black else 7.5

            for p in pieces:
                if isinstance(p, Rook) and p.color == self.color and p.turn == 0:
                    if p.x < 4:
                        left_rook = p
                    else:
                        right_rook = p
                    continue
                if p == self:
                    continue
                if abs(p.y - back_row) < self.radius * 2:
                    if 0.5 < p.x < 4.5:
                        long_castle = False
                    if 4.5 < p.x < 7.5:
                        short_castle = False
            if left_rook:
                left_rook.x = left_rook.start_x
            if right_rook:
                right_rook.x = right_rook.start_x

            self.x = self.start_x
            self.y = self.start_y

            path, dist = self.select_path(
                (self.start_x, self.start_y), [[1, 1], [-1, 1], [1, 0], [0, 1]], new_p
            )
            path_len = math.sqrt(path[0] ** 2 + path[1] ** 2)
            self.slide(
                clamp(path[0] * dist / path_len, -1, 1),
                clamp(path[1] * dist / path_len, -1, 1),
                pieces,
            )

            if self.turn == 0:
                if long_castle and left_rook and left_rook.turn == 0 and new_p[0] < self.start_x - 1.5:
                    self.slide(0, 0, pieces)
                    self.slide(-2, 0, pieces)
                    left_rook.x = self.x + 1

                if short_castle and right_rook and right_rook.turn == 0 and new_p[0] > self.start_x + 1.5:
                    self.slide(0, 0, pieces)
                    self.slide(2, 0, pieces)
                    right_rook.x = self.x - 1

    def confirm(self, pieces):
        new_pieces = []
        if self.grabbed:
            self.grabbed = False
            for piece in pieces:
                if piece.targeted:
                    piece.deleted = True
                    piece.x = 100
                    piece.start_x = 100
                    piece.delete()
                else:
                    new_pieces.append(piece)
            self.direction = False
            self.text = self.font.render(
                self.letter,
                True,
                (255 - self.color[0], 255 - self.color[1], 255 - self.color[2]),
            )

            self.start_x = self.x
            self.start_y = self.y
            self.turn += 1

        # Update start positions and turns for pieces that have moved
        for p in new_pieces:
            if p.x != p.start_x or p.y != p.start_y:
                p.start_x = p.x
                p.start_y = p.y
                p.turn += 1

        return new_pieces

    def draw_paths(self, pieces):
        if self.targeted or self.deleted:
            return

        directions = [
            (1, 1),
            (-1, -1),
            (1, -1),
            (-1, 1),
            (0, 1),
            (0, -1),
            (1, 0),
            (-1, 0),
        ]
        end_positions = []
        for dx, dy in directions:
            end_x = self.start_x + dx
            end_y = self.start_y + dy
            end_positions.append((end_x, end_y))

        for end_pos in end_positions:
            draw_line_round_corners_polygon(
                see_through,
                to_screen_coords((self.start_x, self.start_y)),
                to_screen_coords(end_pos),
                RED_HIGHLIGHT,
                self.radius * 2 * 640 / 8,
            )

class Knight(Piece):
    def __init__(self, x, y, d):
        super().__init__(x, y, d)
        self.set_letter("♘")
        self.set_id(knight)
        self.edge_position_angles=[]
        self.draw_first_arc = True
        self.edge_positions=[]
        self.set_weight(3)

    
    def delete(self):
        return super().delete()
    
    def get_all_directions_per_piece(self, pieces):
        list_arc = []
        if self.draw_first_arc:
            list_arc = [(self.edge_position_angles[i], self.edge_position_angles[i+1]) for i in range(0,len(self.edge_position_angles)-1,2)]
        else:
            list_arc = [(self.edge_position_angles[i], self.edge_position_angles[i+1]) for i in range(1,len(self.edge_position_angles)-1,2)]
            list_arc.append((self.edge_position_angles[-1]-2*np.pi, self.edge_position_angles[0]))
        return list_arc


    def draw_moves(self, pieces):
        Radius = math.sqrt(5)
        

        start = 0 if self.draw_first_arc else 1

        for pos in self.edge_positions:
            pygame_draw_circle(
                see_through2, GREEN_HIGHLIGHT, to_screen_coords(pos), 0.35 / 8 * 640
            )
        for i in range(start, len(self.edge_position_angles) - 1, 2):
            arc(
                see_through2,
                GREEN_HIGHLIGHT,
                to_screen_coords((self.start_x, self.start_y)),
                (math.sqrt(5) + self.radius) / 8 * 640,
                self.edge_position_angles[i],
                self.edge_position_angles[i + 1] - self.edge_position_angles[i],
                int(self.radius / 8 * 640 * 2),
            )

        # arc(see_through2, GREEN_HIGHLIGHT, to_screen_coords((self.start_x,self.start_y)),(math.sqrt(5)+self.radius)/8*640 ,edge_position_angles[0],edge_position_angles[1]-edge_position_angles[0],int(self.radius/8*640*2))

        # i dont know what im doing
        if not self.draw_first_arc:
            arc(
                see_through2,
                GREEN_HIGHLIGHT,
                to_screen_coords((self.start_x, self.start_y)),
                (math.sqrt(5) + self.radius) / 8 * 640,
                self.edge_position_angles[-1],
                math.radians(360) - self.edge_position_angles[-1],
                int(self.radius / 8 * 640 * 2),
            )
            arc(
                see_through2,
                GREEN_HIGHLIGHT,
                to_screen_coords((self.start_x, self.start_y)),
                (math.sqrt(5) + self.radius) / 8 * 640,
                0,
                self.edge_position_angles[0],
                int(self.radius / 8 * 640 * 2),
            )
            pygame_draw_circle(
                see_through2,
                GREEN_HIGHLIGHT,
                to_screen_coords([self.start_x, self.start_y + Radius]),
                0.35 / 8 * 640,
            )
        if len(self.edge_positions) == 0:
            pygame_draw_circle(
                see_through2,
                GREEN_HIGHLIGHT,
                to_screen_coords((self.start_x, self.start_y)),
                (math.sqrt(5) + self.radius) / 8 * 640,
                width=round(self.radius * 640 / 8 * 2),
            )

    def drag(self, new_p, pieces):
        if self.grabbed:

            x = self.apply_granularity(new_p[0] - self.start_x)
            y = self.apply_granularity(new_p[1] - self.start_y)

            Radius = math.sqrt(5)

            if math.sqrt(x**2 + y**2) > 40 / 640 * 8:
                distance = math.sqrt(x**2 + y**2)

                self.x = self.start_x + Radius * x / distance
                self.y = self.start_y + Radius * y / distance

            edge_positions = []
            for piece in pieces:
                d = dist((self.start_x, self.start_y), (piece.x, piece.y))
                if (
                    d < Radius + 2 * self.radius
                    and d > Radius - 2 * self.radius
                    and piece != self
                    and piece.color == self.color
                ):
                    # use law of cosines to find the angle that put the knight on the edge of the piece
                    cos_angle = ((2 * self.radius) ** 2 - Radius**2 - d**2) / (
                        -2 * Radius * d
                    )
                    if cos_angle <= 1:
                        theta = math.acos(cos_angle)
                        piece_angle = math.atan2(
                            piece.y - self.start_y, piece.x - self.start_x
                        )
                        edge_positions.append(
                            (
                                self.start_x
                                + Radius * math.cos(piece_angle + theta + 0.001),
                                self.start_y
                                + Radius * math.sin(piece_angle + theta + 0.001),
                            )
                        )
                        edge_positions.append(
                            (
                                self.start_x
                                + Radius * math.cos(piece_angle - theta - 0.001),
                                self.start_y
                                + Radius * math.sin(piece_angle - theta - 0.001),
                            )
                        )

            if self.start_x - Radius < self.radius:
                edge_positions.append(
                    (
                        self.radius,
                        self.start_y
                        + math.sqrt(Radius**2 - (self.start_x - self.radius) ** 2),
                    )
                )
                edge_positions.append(
                    (
                        self.radius,
                        self.start_y
                        - math.sqrt(Radius**2 - (self.start_x - self.radius) ** 2),
                    )
                )

            if self.start_x + Radius > 8 - self.radius:
                edge_positions.append(
                    (
                        8 - self.radius,
                        self.start_y
                        + math.sqrt(
                            Radius**2 - (8 - self.start_x - self.radius) ** 2
                        ),
                    )
                )
                edge_positions.append(
                    (
                        8 - self.radius,
                        self.start_y
                        - math.sqrt(
                            Radius**2 - (8 - self.start_x - self.radius) ** 2
                        ),
                    )
                )

            if self.start_y - Radius < self.radius:
                edge_positions.append(
                    (
                        self.start_x
                        + math.sqrt(Radius**2 - (self.start_y - self.radius) ** 2),
                        self.radius,
                    )
                )
                edge_positions.append(
                    (
                        self.start_x
                        - math.sqrt(Radius**2 - (self.start_y - self.radius) ** 2),
                        self.radius,
                    )
                )

            if self.start_y + Radius > 8 - self.radius:
                edge_positions.append(
                    (
                        self.start_x
                        + math.sqrt(
                            Radius**2 - (8 - self.start_y - self.radius) ** 2
                        ),
                        8 - self.radius,
                    )
                )
                edge_positions.append(
                    (
                        self.start_x
                        - math.sqrt(
                            Radius**2 - (8 - self.start_y - self.radius) ** 2
                        ),
                        8 - self.radius,
                    )
                )

            valid_edge_positions = []
            """
            #remove edge positions that place the knight off the board
            for pos in edge_positions:
                x=pos[0]
                y=pos[1]
                if x+self.radius<=8 and x-self.radius>=0 and y+self.radius<=8 and y-self.radius>=0:
                    valid=True
                    #and edge positions that are overlapping a piece
                    for piece in pieces:
                        if piece.color == self.color:
                            if piece.overlaps(Knight(x,y,self.color)) and piece!=self:
                                valid=False
                    if valid:     
                        valid_edge_positions.append(pos)
                
            edge_positions = valid_edge_positions
            """

            move_to_edge = False
            for piece in pieces:
                if (
                    self.overlaps(piece)
                    and piece != self
                    and piece.color == self.color
                    or self.x + self.radius > 8
                    or self.x - self.radius < 0
                    or self.y + self.radius > 8
                    or self.y - self.radius < 0
                ):
                    move_to_edge = True

            if move_to_edge:
                if len(edge_positions) > 0:
                    closest_dist = 9999999
                    closest = None
                    for pos in edge_positions:
                        d = dist(pos, (self.x, self.y))
                        if d < closest_dist:
                            x = pos[0]
                            y = pos[1]
                            if (
                                x + self.radius <= 8
                                and x - self.radius >= 0
                                and y + self.radius <= 8
                                and y - self.radius >= 0
                            ):
                                valid = True
                                for piece in pieces:
                                    if piece.color == self.color:
                                        if (
                                            piece.overlaps(Knight(x, y, self.color))
                                            and piece != self
                                        ):
                                            valid = False
                                if valid:
                                    closest_dist = d
                                    closest = pos

                    self.x = closest[0]
                    self.y = closest[1]

            for piece in pieces:
                piece.untarget()
                if self.overlaps(piece) and piece.color != self.color:
                    piece.target()
            """
            if move_to_edge:
                if len(valid_edge_positions)>0:
                    closest_dist=9999999
                    closest = None
                    for pos in valid_edge_positions:
                        d = dist(pos,(self.x,self.y))
                        if d<closest_dist:
                            closest_dist=d
                            closest=pos
                        
                                
                    self.x=closest[0]
                    self.y=closest[1]
            """


    def calc_paths(self,pieces):
        if self.deleted:
            return

        self.edge_positions = []
        Radius = math.sqrt(5)
        pieces_in_range_angles = []
        for piece in pieces:
            d = dist((self.start_x, self.start_y), (piece.x, piece.y))
            if (
                d < Radius + 2 * self.radius
                and d > Radius - 2 * self.radius
                and piece != self
                and piece.color == self.color
            ):

                # use law of cosines to find the angle that put the knight on the edge of the piece
                cos_angle = ((2 * self.radius) ** 2 - Radius**2 - d**2) / (
                    -2 * Radius * d
                )
                if cos_angle <= 1:
                    theta = math.acos(cos_angle)
                    angle = math.radians(90) - math.atan2(
                        piece.y - self.start_y, piece.x - self.start_x
                    )
                    if angle < 0:
                        angle = 2 * math.pi + angle
                    pieces_in_range_angles.append(angle)
                    piece_angle = math.atan2(
                        piece.y - self.start_y, piece.x - self.start_x
                    )
                    self.edge_positions.append(
                        (
                            self.start_x
                            + Radius * math.cos(piece_angle + theta + 0.001),
                            self.start_y
                            + Radius * math.sin(piece_angle + theta + 0.001),
                        )
                    )
                    self.edge_positions.append(
                        (
                            self.start_x
                            + Radius * math.cos(piece_angle - theta - 0.001),
                            self.start_y
                            + Radius * math.sin(piece_angle - theta - 0.001),
                        )
                    )

        if self.start_x - Radius < self.radius:
            self.edge_positions.append(
                (
                    self.radius,
                    self.start_y
                    + math.sqrt(Radius**2 - (self.start_x - self.radius) ** 2),
                )
            )
            self.edge_positions.append(
                (
                    self.radius,
                    self.start_y
                    - math.sqrt(Radius**2 - (self.start_x - self.radius) ** 2),
                )
            )
            # this is so that um uhhh uh dont worry about it :)
            pieces_in_range_angles.append(1.5 * math.pi)

        if self.start_x + Radius > 8 - self.radius:
            self.edge_positions.append(
                (
                    8 - self.radius,
                    self.start_y
                    + math.sqrt(Radius**2 - (8 - self.start_x - self.radius) ** 2),
                )
            )
            self.edge_positions.append(
                (
                    8 - self.radius,
                    self.start_y
                    - math.sqrt(Radius**2 - (8 - self.start_x - self.radius) ** 2),
                )
            )
            pieces_in_range_angles.append(0.5 * math.pi)

        if self.start_y - Radius < self.radius:
            self.edge_positions.append(
                (
                    self.start_x
                    + math.sqrt(Radius**2 - (self.start_y - self.radius) ** 2),
                    self.radius,
                )
            )
            self.edge_positions.append(
                (
                    self.start_x
                    - math.sqrt(Radius**2 - (self.start_y - self.radius) ** 2),
                    self.radius,
                )
            )
            pieces_in_range_angles.append(math.pi)

        if self.start_y + Radius > 8 - self.radius:
            self.edge_positions.append(
                (
                    self.start_x
                    + math.sqrt(Radius**2 - (8 - self.start_y - self.radius) ** 2),
                    8 - self.radius,
                )
            )
            self.edge_positions.append(
                (
                    self.start_x
                    - math.sqrt(Radius**2 - (8 - self.start_y - self.radius) ** 2),
                    8 - self.radius,
                )
            )
            pieces_in_range_angles.append(0)

        valid_edge_positions = []
        # remove edge positions that place the knight off the board
        for pos in self.edge_positions:
            x = pos[0]
            y = pos[1]
            if (
                x + self.radius <= 8
                and x - self.radius >= 0
                and y + self.radius <= 8
                and y - self.radius >= 0
            ):
                valid = True
                # and edge positions that are overlapping a piece
                for piece in pieces:
                    if piece.color == self.color:
                        if piece.overlaps(Knight(x, y, self.color)) and piece != self:
                            valid = False
                if valid:
                    valid_edge_positions.append(pos)

        self.edge_positions = valid_edge_positions
        # pygame_draw_circle(see_through2, GREEN_HIGHLIGHT, to_screen_coords((self.start_x,self.start_y)), (math.sqrt(5)+self.radius)/8*640,width=round(self.radius*640/8*2))
        self.edge_position_angles = []
        for pos in self.edge_positions:
            angle = math.radians(90) - math.atan2(
                pos[1] - self.start_y, pos[0] - self.start_x
            )
            if angle < 0:
                angle = 2 * math.pi + angle
            self.edge_position_angles.append(angle)

        # sort edge positions by angle

        self.edge_position_angles.sort()
        self.draw_first_arc = True
        for angle in pieces_in_range_angles:
            if self.edge_position_angles[0] < angle < self.edge_position_angles[1]:
                self.draw_first_arc = False
        
    def draw_paths(self, pieces):

        if self.deleted or self.targeted:
            return
        
        Radius = math.sqrt(5)
        start = 0 if self.draw_first_arc else 1
        for pos in self.edge_positions:
            pygame_draw_circle(
                see_through, RED_HIGHLIGHT, to_screen_coords(pos), 0.35 / 8 * 640
            )
        for i in range(start, len(self.edge_position_angles) - 1, 2):
            arc(
                see_through,
                RED_HIGHLIGHT,
                to_screen_coords((self.start_x, self.start_y)),
                (math.sqrt(5) + self.radius) / 8 * 640,
                self.edge_position_angles[i],
                self.edge_position_angles[i + 1] - self.edge_position_angles[i],
                int(self.radius / 8 * 640 * 2),
            )

        # arc(see_through2, GREEN_HIGHLIGHT, to_screen_coords((self.start_x,self.start_y)),(math.sqrt(5)+self.radius)/8*640 ,edge_position_angles[0],edge_position_angles[1]-edge_position_angles[0],int(self.radius/8*640*2))

        # i dont know what im doing
        if not self.draw_first_arc:
            arc(
                see_through,
                RED_HIGHLIGHT,
                to_screen_coords((self.start_x, self.start_y)),
                (math.sqrt(5) + self.radius) / 8 * 640,
                self.edge_position_angles[-1],
                math.radians(360) - self.edge_position_angles[-1],
                int(self.radius / 8 * 640 * 2),
            )
            arc(
                see_through,
                RED_HIGHLIGHT,
                to_screen_coords((self.start_x, self.start_y)),
                (math.sqrt(5) + self.radius) / 8 * 640,
                0,
                self.edge_position_angles[0],
                int(self.radius / 8 * 640 * 2),
            )
            pygame_draw_circle(
                see_through,
                RED_HIGHLIGHT,
                to_screen_coords([self.start_x, self.start_y + Radius]),
                0.35 / 8 * 640,
            )
        if len(self.edge_positions) == 0:
            pygame_draw_circle(
                see_through,
                RED_HIGHLIGHT,
                to_screen_coords((self.start_x, self.start_y)),
                (math.sqrt(5) + self.radius) / 8 * 640,
                width=round(self.radius * 640 / 8 * 2),
            )

class Pawn(Piece):
    def __init__(self, x, y, d):
        super().__init__(x, y, d)
        self.set_letter("♙")
        self.set_id(pawn)
        self.set_weight(1)

    def delete(self):
        return super().delete()

    def get_all_directions_per_piece(self, pieces):
        fake_piece = Pawn(self.start_x, self.start_y, self.color)

        end_positions = []
        forward_dist = 1
        if self.turn == 0:
            forward_dist = 2

        if self.color == white:
            directions = [[1, 1], [-1, 1]]
            fake_piece.slide(
                0, forward_dist, [p for p in pieces if p != self], capture=False
            )
            end_positions.append((fake_piece.x, fake_piece.y))
            fake_piece.slide(0, 0, [p for p in pieces if p != self], capture=False)
        else:
            directions = [[-1, -1], [1, -1]]
            fake_piece.slide(
                0, -forward_dist, [p for p in pieces if p != self], capture=False
            )
            end_positions.append((fake_piece.x, fake_piece.y))
            fake_piece.slide(0, 0, [p for p in pieces if p != self], capture=False)

        for d in directions:
            fake_piece.slide(d[0], d[1], [p for p in pieces if p != self], fake=True)
            end_positions.append((fake_piece.x, fake_piece.y))
            fake_piece.slide(0, 0, [p for p in pieces if p != self], fake=True)

        end_positions_purified = []
        for end_position in end_positions:
            if end_position != (self.start_x, self.start_y):
                end_positions_purified.append(end_position)
        return end_positions_purified

    def draw_moves(self, pieces):

        fake_piece = Pawn(self.start_x, self.start_y, self.color)

        end_positions = []
        # Determine forward distance based on the turn
        forward_dist = 2 if self.turn == 0 else 1

        if self.color == white:
            directions = [[1, 1], [-1, 1]]
            fake_piece.slide(
                0, forward_dist, [p for p in pieces if p != self], capture=False
            )
            end_positions.append((fake_piece.x, fake_piece.y))
            fake_piece.slide(0, 0, [p for p in pieces if p != self], capture=False)
        else:
            directions = [[-1, -1], [1, -1]]
            fake_piece.slide(
                0, -forward_dist, [p for p in pieces if p != self], capture=False
            )
            end_positions.append((fake_piece.x, fake_piece.y))
            fake_piece.slide(0, 0, [p for p in pieces if p != self], capture=False)

        for d in directions:
            fake_piece.slide(d[0], d[1], [p for p in pieces if p != self], fake=True)
            end_positions.append((fake_piece.x, fake_piece.y))
            fake_piece.slide(0, 0, [p for p in pieces if p != self], fake=True)

        for end_pos in end_positions:
            draw_line_round_corners_polygon(
                see_through2,
                to_screen_coords((self.start_x, self.start_y)),
                to_screen_coords(end_pos),
                GREEN_HIGHLIGHT,
                self.radius * 2 * 640 / 8,
            )


    def drag(self, new_p, pieces):
        if self.grabbed:
            self.slide(0, 0, pieces)
            if self.color == white:
                path, dist = self.select_path(
                    (self.start_x, self.start_y), [[1, 1], [-1, 1], [0, 1]], new_p
                )
                path_len = math.sqrt(path[0] ** 2 + path[1] ** 2)
                self.direction = path
                if self.direction == [1, 1]:
                    self.slide(
                        clamp(path[0] * dist / path_len, 0, 1),
                        clamp(path[1] * dist / path_len, 0, 1),
                        pieces,
                    )
                elif self.direction == [-1, 1]:
                    self.slide(
                        clamp(path[0] * dist / path_len, -1, 0),
                        clamp(path[1] * dist / path_len, 0, 1),
                        pieces,
                    )
                else:
                    max_move = 1
                    if self.turn == 0:
                        max_move = 2
                    self.slide(
                        0,
                        clamp(path[1] * dist / path_len, 0, max_move),
                        pieces,
                        capture=False,
                    )
            else:
                path, dist = self.select_path(
                    (self.start_x, self.start_y), [[1, -1], [-1, -1], [0, -1]], new_p
                )
                path_len = math.sqrt(path[0] ** 2 + path[1] ** 2)
                self.direction = path
                if self.direction == [1, -1]:
                    self.slide(
                        clamp(path[0] * dist / path_len, 0, 1),
                        clamp(path[1] * dist / path_len, -1, 0),
                        pieces,
                    )
                elif self.direction == [-1, -1]:
                    self.slide(
                        clamp(path[0] * dist / path_len, -1, 0),
                        clamp(path[1] * dist / path_len, -1, 0),
                        pieces,
                    )
                else:
                    max_move = 1
                    if self.turn == 0:
                        max_move = 2
                    self.slide(
                        0,
                        clamp(path[1] * dist / path_len, -max_move, 0),
                        pieces,
                        capture=False,
                    )

    def can_promote(self):
        if self.color == white:
            if self.y - self.radius > 7:
                return True
        if self.color == black:
            if self.y + self.radius < 1:
                return True

    def ungrab(self, pieces):
        if self.grabbed:
            #print("ungrab pawn", self.color) 
            attacked = False
            for piece in pieces:
                if piece.targeted:
                    attacked = True

            if self.direction:
                if not attacked and (self.direction[0] != 0):
                    self.cancel(pieces)
                    #self.cancel(pieces)
                    return

            sol = super().ungrab(pieces)
            #print("pawn ungrab", sol)
            return sol

    def draw_paths(self, pieces):

        if self.deleted:
            return

        if self.targeted:
            return
        fake_piece = Pawn(self.start_x, self.start_y, self.color)

        if self.color == white:
            directions = [[1, 1], [-1, 1]]
        else:
            directions = [[-1, -1], [1, -1]]

        end_positions = []
        for d in directions:
            fake_piece.slide(d[0], d[1], [p for p in pieces if p != self], fake=True)
            end_positions.append((fake_piece.x, fake_piece.y))
            fake_piece.slide(0, 0, [p for p in pieces if p != self], fake=True)

        for end_pos in end_positions:
            draw_line_round_corners_polygon(
                see_through,
                to_screen_coords((self.start_x, self.start_y)),
                to_screen_coords(end_pos),
                RED_HIGHLIGHT,
                self.radius * 2 * 640 / 8,
            )

class Queen(Piece):
    def __init__(self, x, y, c):
        super().__init__(x, y, c)
        self.set_letter("♕")
        self.set_id(queen)
        self.set_weight(9)
    
    def delete(self):
        return super().delete()

    def get_all_directions_per_piece(self, pieces):
        fake_piece = Queen(self.start_x, self.start_y, self.color)

        directions = [
            [10, 10],
            [-10, -10],
            [10, -10],
            [-10, 10],
            [0, 10],
            [0, -10],
            [10, 0],
            [-10, 0],
        ]
        end_positions = []
        for d in directions:
            fake_piece.slide(d[0], d[1], [p for p in pieces if p != self], fake=True)
            end_positions.append((fake_piece.x, fake_piece.y))
            fake_piece.slide(0, 0, [p for p in pieces if p != self], fake=True)

        end_positions_purified = []
        for end_position in end_positions:
            if end_position != (self.start_x, self.start_y):
                end_positions_purified.append(end_position)
        return end_positions_purified

    def draw_moves(self, pieces):

        fake_piece = Queen(self.start_x, self.start_y, self.color)

        directions = [
            [10, 10],
            [-10, -10],
            [10, -10],
            [-10, 10],
            [0, 10],
            [0, -10],
            [10, 0],
            [-10, 0],
        ]
        end_positions = []
        for d in directions:
            fake_piece.slide(d[0], d[1], [p for p in pieces if p != self], fake=True)
            end_positions.append((fake_piece.x, fake_piece.y))
            fake_piece.slide(0, 0, [p for p in pieces if p != self], fake=True)

        for end_pos in end_positions:
            draw_line_round_corners_polygon(
                see_through2,
                to_screen_coords((self.start_x, self.start_y)),
                to_screen_coords(end_pos),
                GREEN_HIGHLIGHT,
                self.radius * 2 * 640 / 8,
            )

    def drag(self, new_p, pieces):
        if self.grabbed:
            self.slide(0, 0, pieces)
            path, dist = self.select_path(
                (self.start_x, self.start_y), [[1, 1], [-1, 1], [1, 0], [0, 1]], new_p
            )
            path_len = math.sqrt(path[0] ** 2 + path[1] ** 2)
            self.slide(path[0] * dist / path_len, path[1] * dist / path_len, pieces)

    def draw_paths(self, pieces):

        if self.targeted:
            return
        if self.deleted:
            return

        fake_piece = Queen(self.start_x, self.start_y, self.color)

        directions = [
            [10, 10],
            [-10, -10],
            [10, -10],
            [-10, 10],
            [0, 10],
            [0, -10],
            [10, 0],
            [-10, 0],
        ]
        end_positions = []
        for d in directions:
            fake_piece.slide(d[0], d[1], [p for p in pieces if p != self], fake=True)
            end_positions.append((fake_piece.x, fake_piece.y))
            fake_piece.slide(0, 0, [p for p in pieces if p != self], fake=True)

        for end_pos in end_positions:
            draw_line_round_corners_polygon(
                see_through,
                to_screen_coords((self.start_x, self.start_y)),
                to_screen_coords(end_pos),
                RED_HIGHLIGHT,
                self.radius * 2 * 640 / 8,
            )

class Rook(Piece):
    def __init__(self, x, y, d):
        super().__init__(x, y, d)
        self.set_letter("♖")
        self.set_id(rook)
        self.set_weight(5)
    
    def delete(self):
        return super().delete()

    def draw_moves(self, pieces):
        fake_piece = Rook(self.start_x, self.start_y, self.color)

        end_positions = []

        directions = [[10, 0], [0, 10], [-10, 0], [0, -10]]
        for d in directions:
            fake_piece.slide(d[0], d[1], [p for p in pieces if p != self], fake=True)
            end_positions.append((fake_piece.x, fake_piece.y))
            fake_piece.slide(0, 0, [p for p in pieces if p != self], fake=True)
        #print("end_positions rook", end_positions)

        for end_pos in end_positions:
            draw_line_round_corners_polygon(
                see_through2,
                to_screen_coords((self.start_x, self.start_y)),
                to_screen_coords(end_pos),
                GREEN_HIGHLIGHT,
                self.radius * 2 * 640 / 8,
            )

    def get_all_directions_per_piece(self, pieces):
        fake_piece = Rook(self.start_x, self.start_y, self.color)

        end_positions = []

        directions = [[10, 0], [0, 10], [-10, 0], [0, -10]]
        for d in directions:
            fake_piece.slide(d[0], d[1], [p for p in pieces if p != self], fake=True)
            end_positions.append((fake_piece.x, fake_piece.y))
            fake_piece.slide(0, 0, [p for p in pieces if p != self], fake=True)
        #print("end_positions rook", end_positions)
        
        end_positions_purified = []
        for end_position in end_positions:
            if end_position != (self.start_x, self.start_y):
                end_positions_purified.append(end_position)
        return end_positions_purified

    def drag(self, new_p, pieces):
        if self.grabbed:
            self.slide(0, 0, pieces)
            path, dist = self.select_path(
                (self.start_x, self.start_y), [[1, 0], [0, 1]], new_p
            )
            path_len = math.sqrt(path[0] ** 2 + path[1] ** 2)
            self.slide(path[0] * dist / path_len, path[1] * dist / path_len, pieces)
            #print("start_x ", self.start_x, "start_y, ", self.start_y, "path ", path, ", ", "dist ", dist, ", ", "path_len", path_len, "new_p ", new_p)
            

    def draw_paths(self, pieces):
        if self.deleted:
            return

        if self.targeted:
            return

        fake_piece = Rook(self.start_x, self.start_y, self.color)

        directions = [[0, 10], [0, -10], [10, 0], [-10, 0]]
        end_positions = []
        for d in directions:
            fake_piece.slide(d[0], d[1], [p for p in pieces if p != self], fake=True)
            end_positions.append((fake_piece.x, fake_piece.y))
            fake_piece.slide(0, 0, [p for p in pieces if p != self], fake=True)
        
        '''
        file = open("rook.txt", "a")
        print("end_positions rook", end_positions)
        for riga in end_positions:
            file.write(str(riga) + "\n")
        '''
        
        for end_pos in end_positions:
            draw_line_round_corners_polygon(
                see_through,
                to_screen_coords((self.start_x, self.start_y)),
                to_screen_coords(end_pos),
                RED_HIGHLIGHT,
                self.radius * 2 * 640 / 8,
            )


