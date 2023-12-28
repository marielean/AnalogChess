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