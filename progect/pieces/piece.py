import math, pygame
from progect.utils import width, height, dist, to_game_coords
from progect.drawing import draw_center_text, draw_circle, screen, get_fontname
from progect.colors import *


class Piece:
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
        '''
        Delete the piece from the board
        '''
        self.deleted = True
        del self
    
    def draw_moves(self, pieces):
        pass

    def get_all_directions_per_piece(self, pieces):
        pass
