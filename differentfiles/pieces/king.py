from .piece import Piece
from differentfiles.colors import *
from differentfiles.utils import *
from differentfiles.pieces.rook import Rook
from differentfiles.pieces.queen import Queen
import config
if config.GRAPHIC:
    from differentfiles.drawing import (
        see_through,
        see_through2,
        pygame_draw_circle,
        draw_line_round_corners_polygon,
    )


class King(Piece):
    def __init__(self, x, y, c, deleted=False):
        super().__init__(x, y, c, deleted)
        self.set_letter("♔")
        self.set_id(king)
        self.set_weight(1000)
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
        if self.turn == 0:
            if long_castle:
                if left_rook:
                    if left_rook.turn == 0 and config.GRAPHIC:
                        pygame_draw_circle(
                            see_through2,
                            GREEN_HIGHLIGHT,
                            to_screen_coords((self.start_x - 2, self.start_y)),
                            self.radius / 8 * 640,
                        )
            if short_castle:
                if right_rook:
                    if right_rook.turn == 0 and config.GRAPHIC:
                        pygame_draw_circle(
                            see_through2,
                            GREEN_HIGHLIGHT,
                            to_screen_coords((self.start_x + 2, self.start_y)),
                            self.radius / 8 * 640,
                        )

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
        # print("end_king", end_positions_purified)
        return end_positions_purified

    def draw_moves(self, pieces):
        '''fake_piece = King(self.start_x, self.start_y, self.color)

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
            fake_piece.slide(0, 0, [p for p in pieces if p != self], fake=True)'''

        end_positions = self.get_all_directions_per_piece(pieces)
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

        '''directions = [
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
            end_positions.append((end_x, end_y))'''
        
        end_positions = self.get_all_directions_per_piece(pieces)

        for end_pos in end_positions:
            draw_line_round_corners_polygon(
                see_through,
                to_screen_coords((self.start_x, self.start_y)),
                to_screen_coords(end_pos),
                RED_HIGHLIGHT,
                self.radius * 2 * 640 / 8,
            )
