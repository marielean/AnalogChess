import math
from differentfiles.utils import width, height, dist, to_game_coords, dist2
import config
if config.GRAPHIC:
    import pygame
    from differentfiles.drawing import draw_center_text, draw_circle, screen, get_fontname
from differentfiles.colors import *

class Piece:
    # x pos and y pos are on a grid of size 8, normal cartesian coordinates
    def __init__(self, x_pos, y_pos, color, deleted=False):
        diameter = 0.7 
        self.__diameter2 = diameter**2 # private variable useful to reduce the number of calculations
        self.x = x_pos
        self.y = y_pos
        self.radius = diameter / 2
        self.__radius2 = self.radius**2 # private variable useful to reduce the number of calculations
        self.grabbed = False
        self.targeted = False
        self.color = color

        self.start_x = self.x
        self.start_y = self.y
        text_scale = 0.85
        self.letter = "X"
        self.id = "XX"
        if config.GRAPHIC:
            self.font = pygame.font.SysFont(
                get_fontname(), int(diameter / 8 * 640 * text_scale)
            )
            self.text = self.font.render(self.letter, True, (255, 255, 255))
        else: 
            self.font = None
            self.text = None
        self.direction = False
        self.targeted = False
        self.turn = 0
        self.deleted = deleted
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
        if self.font is not None:
            if self.grabbed is False:
                self.text = self.font.render(
                    self.letter,
                    True,
                    (255 - self.color[0], 255 - self.color[1], 255 - self.color[2]),
                )
            else:
                self.text = self.font.render(self.letter, True, (0, 255, 0))
        else:
            self.text = self.letter

    def can_promote(self):
        return False


    #this is only used by the Knight so we can only calculate paths once instead of every frame
    def calc_paths(self,pieces):
        pass
    
    def draw_paths(self, pieces):
        pass

    def target(self):
        self.targeted = True
        if self.font is not None:
            self.text = self.font.render(self.letter, True, (255, 0, 0))
        else:
            self.text = self.letter
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
        if dist2(pos, (self.x, self.y)) < self.__radius2:
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

                    # elimino il pezzo dal vettore di pezzi quindi elimino proprio l'oggetto
                    del piece
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
                        if (dist2(to_game_coords(pygame.mouse.get_pos()), (self.x, self.y)) < self.__radius2):
                            self.confirm(pieces)
                            print("Pezzo giocato", self.id)
                                
                            if self.white_turn and self.color == white:
                                #print("white turn, next turn black")
                                self.white_turn = False
                                for one_piece in pieces:
                                    one_piece.white_turn = False
                                return True
                            elif self.white_turn is False and self.color == black:
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
        return dist2((self.x, self.y), (piece.x, piece.y)) < self.__diameter2

    # math shit
    def slide(self, dx, dy, pieces, capture=True, fake=False):
        all_pieces = pieces
        if capture:
            pieces = [
                p
                for p in pieces
                # verifico se il prodotto scalare tra p e il pezzo che sto muovendo è positivo
                if (p.x - self.start_x) * dx + (p.y - self.start_y) * dy > 0
                and p != self
                and p.color == self.color
            ]
        if fake:
            pieces = [
                p
                for p in pieces
                # verifico se il prodotto scalare tra p e se stesso è positivo
                if (p.x - self.start_x) * dx + (p.y - self.start_y) * dy > 0
                and p != self
                and p.color == self.color
                and p.targeted == False
            ]
        else:
            pieces = [
                p
                for p in pieces
                # verifico se il prodotto scalare tra p e se stesso è positivo
                if (p.x - self.start_x) * dx + (p.y - self.start_y) * dy > 0
                and p != self
            ]

        # viene calcolato l'angolo dello spostamento desiderato del pezzo in base a dx e dy
        angle = math.atan2(dy, dx)

        # resolve wall collisions
        # dont do this if the piece is off the board it wont work right

        # questo serve per verificare se lo spostamento desiderato è fuori dalla scacchiera
        # se è così allora vengono calcolati i nuovi dx e dy in modo che il pezzo non esca dalla scacchiera
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
                    abs(dist((self.start_x, self.start_y), (piece.x, piece.y)) ** 2 - h**2)
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
                    4 * self.__radius2 - block_perp_dist**2
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
                    abs(dist((self.start_x, self.start_y), (piece.x, piece.y)) ** 2
                    - block_perp_dist**2)
                )
                new_new_dist = block_dist - math.sqrt(
                    4 * self.__radius2 - block_perp_dist**2
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
                d2 = dist2((piece.x, piece.y), (self.start_x, self.start_y))
                hit_dist = math.sqrt(abs(d2 - h**2)) - math.sqrt(abs(
                    4 * piece.__radius2 - h**2)
                )
                if hit_dist < first_hit_dist:
                    first_hit_dist = hit_dist
                    perp_dist = h
                    first_piece_hit = piece

        if fake is False:
            for piece in all_pieces:
                piece.untarget()

        if first_piece_hit:
            if self.overlaps(first_piece_hit):
                if fake is False:
                    first_piece_hit.target()
            elif dist(
                (self.x, self.y), (self.start_x, self.start_y)
            ) > first_hit_dist + 2 * math.sqrt(4 * piece.__radius2 - perp_dist**2):
                new_dist = first_hit_dist + 2 * math.sqrt(4 * piece.__radius2 - perp_dist**2)
                if fake is False:
                    first_piece_hit.target()

        if abs(full_dist) > 0:
            self.x = self.start_x + dx * new_dist / full_dist
            self.y = self.start_y + dy * new_dist / full_dist

        # Still could be colliding with pieces, check collisions with all other pieces and target them
        if fake is False:
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
