from .piece import Piece
from differentfiles.colors import *
from differentfiles.utils import *
import config

if config.GRAPHIC:
    from differentfiles.drawing import (
        see_through,
        see_through2,
        draw_line_round_corners_polygon,
    )


class Rook(Piece):
    def __init__(self, x, y, c, deleted=False):
        super().__init__(x, y, c, deleted)
        self.set_letter("♖")
        self.set_id(rook)
        self.set_weight(5)
    
    def delete(self):
        return super().delete()

    def draw_moves(self, pieces):
        '''fake_piece = Rook(self.start_x, self.start_y, self.color)

        end_positions = []

        directions = [[10, 0], [0, 10], [-10, 0], [0, -10]]
        for d in directions:
            fake_piece.slide(d[0], d[1], [p for p in pieces if p != self], fake=True)
            end_positions.append((fake_piece.x, fake_piece.y))
            fake_piece.slide(0, 0, [p for p in pieces if p != self], fake=True)
        #print("end_positions rook", end_positions)'''

        end_positions = self.get_all_directions_per_piece(pieces)
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
