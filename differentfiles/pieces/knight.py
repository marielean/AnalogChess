from .piece import Piece
from differentfiles.colors import *
from differentfiles.utils import *
import config
if config.GRAPHIC:
    from differentfiles.drawing import arc, see_through, see_through2, pygame_draw_circle
import numpy as np


class Knight(Piece):
    def __init__(self, x, y, c, deleted=False):
        super().__init__(x, y, c, deleted)
        self.set_letter("♘")
        self.set_id(knight)
        self.edge_position_angles=[]
        self.draw_first_arc = True
        self.edge_positions=[]
        self.set_weight(3)
        self.circle_radius = math.sqrt(5)

    
    def delete(self):
        return super().delete()
    
    def get_all_directions_per_piece(self, pieces):
        '''
        get_all_directions_per_piece(self, pieces)
        Restituisce una lista i cui elementi sono coppie di angoli che delimitano gli archi di movimento.
        Nota: Gli angoli sono espressi in radianti prendendo come riferimento 0 il semiasse positivo delle y e come 
        direzione di rotazione positiva quella oraria.
        '''
        list_arc = []
        if self.draw_first_arc:
            list_arc = [(self.edge_position_angles[i], self.edge_position_angles[i+1]) for i in range(0,len(self.edge_position_angles)-1,2)]
        else:
            list_arc = [(self.edge_position_angles[i], self.edge_position_angles[i+1]) for i in range(1,len(self.edge_position_angles)-1,2)]
            list_arc.append((self.edge_position_angles[-1]-2*np.pi, self.edge_position_angles[0]))
        return list_arc


    def draw_moves(self, pieces):
        Radius = self.circle_radius
        

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
                (self.circle_radius + self.radius) / 8 * 640,
                self.edge_position_angles[i],
                self.edge_position_angles[i + 1] - self.edge_position_angles[i],
                int(self.radius / 8 * 640 * 2),
            )

        # arc(see_through2, GREEN_HIGHLIGHT, to_screen_coords((self.start_x,self.start_y)),(self.circle_radius+self.radius)/8*640 ,edge_position_angles[0],edge_position_angles[1]-edge_position_angles[0],int(self.radius/8*640*2))

        # i dont know what im doing
        if not self.draw_first_arc:
            arc(
                see_through2,
                GREEN_HIGHLIGHT,
                to_screen_coords((self.start_x, self.start_y)),
                (self.circle_radius + self.radius) / 8 * 640,
                self.edge_position_angles[-1],
                math.radians(360) - self.edge_position_angles[-1],
                int(self.radius / 8 * 640 * 2),
            )
            arc(
                see_through2,
                GREEN_HIGHLIGHT,
                to_screen_coords((self.start_x, self.start_y)),
                (self.circle_radius + self.radius) / 8 * 640,
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
                (self.circle_radius + self.radius) / 8 * 640,
                width=round(self.radius * 640 / 8 * 2),
            )

    def drag(self, new_p, pieces):
        if self.grabbed:

            x = (new_p[0] - self.start_x)
            y = (new_p[1] - self.start_y)

            Radius = self.circle_radius

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
                        + math.sqrt(abs(Radius**2 - (self.start_x - self.radius) ** 2)),
                    )
                )
                edge_positions.append(
                    (
                        self.radius,
                        self.start_y
                        - math.sqrt(abs(Radius**2 - (self.start_x - self.radius) ** 2)),
                    )
                )

            if self.start_x + Radius > 8 - self.radius:
                edge_positions.append(
                    (
                        8 - self.radius,
                        self.start_y
                        + math.sqrt(abs(
                            Radius**2 - (8 - self.start_x - self.radius) ** 2
                        )),
                    )
                )
                edge_positions.append(
                    (
                        8 - self.radius,
                        self.start_y
                        - math.sqrt(abs(
                            Radius**2 - (8 - self.start_x - self.radius) ** 2
                        )),
                    )
                )

            if self.start_y - Radius < self.radius:
                edge_positions.append(
                    (
                        self.start_x
                        + math.sqrt(abs(Radius**2 - (self.start_y - self.radius) ** 2)),
                        self.radius,
                    )
                )
                edge_positions.append(
                    (
                        self.start_x
                        - math.sqrt(abs(Radius**2 - (self.start_y - self.radius) ** 2)),
                        self.radius,
                    )
                )

            if self.start_y + Radius > 8 - self.radius:
                edge_positions.append(
                    (
                        self.start_x
                        + math.sqrt(abs(
                            Radius**2 - (8 - self.start_y - self.radius) ** 2
                        )),
                        8 - self.radius,
                    )
                )
                edge_positions.append(
                    (
                        self.start_x
                        - math.sqrt(abs(
                            Radius**2 - (8 - self.start_y - self.radius) ** 2
                        )),
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
        Radius = self.circle_radius
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
                    + math.sqrt(abs(Radius**2 - (self.start_x - self.radius) ** 2)),
                )
            )
            self.edge_positions.append(
                (
                    self.radius,
                    self.start_y
                    - math.sqrt(abs(Radius**2 - (self.start_x - self.radius) ** 2)),
                )
            )
            # this is so that um uhhh uh dont worry about it :)
            pieces_in_range_angles.append(1.5 * math.pi)

        if self.start_x + Radius > 8 - self.radius:
            self.edge_positions.append(
                (
                    8 - self.radius,
                    self.start_y
                    + math.sqrt(abs(Radius**2 - (8 - self.start_x - self.radius) ** 2)),
                )
            )
            self.edge_positions.append(
                (
                    8 - self.radius,
                    self.start_y
                    - math.sqrt(abs(Radius**2 - (8 - self.start_x - self.radius) ** 2)),
                )
            )
            pieces_in_range_angles.append(0.5 * math.pi)

        if self.start_y - Radius < self.radius:
            self.edge_positions.append(
                (
                    self.start_x
                    + math.sqrt(abs(Radius**2 - (self.start_y - self.radius) ** 2)),
                    self.radius,
                )
            )
            self.edge_positions.append(
                (
                    self.start_x
                    - math.sqrt(abs(Radius**2 - (self.start_y - self.radius) ** 2)),
                    self.radius,
                )
            )
            pieces_in_range_angles.append(math.pi)

        if self.start_y + Radius > 8 - self.radius:
            self.edge_positions.append(
                (
                    self.start_x
                    + math.sqrt(abs(Radius**2 - (8 - self.start_y - self.radius) ** 2)),
                    8 - self.radius,
                )
            )
            self.edge_positions.append(
                (
                    self.start_x
                    - math.sqrt(abs(Radius**2 - (8 - self.start_y - self.radius) ** 2)),
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
        # pygame_draw_circle(see_through2, GREEN_HIGHLIGHT, to_screen_coords((self.start_x,self.start_y)), (self.circle_radius+self.radius)/8*640,width=round(self.radius*640/8*2))
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
        try:
            for angle in pieces_in_range_angles:
                if self.edge_position_angles[0] < angle < self.edge_position_angles[1]:
                    self.draw_first_arc = False
        except:
            pass
        
    def draw_paths(self, pieces):

        if self.deleted or self.targeted:
            return
        
        Radius = self.circle_radius
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
                (self.circle_radius + self.radius) / 8 * 640,
                self.edge_position_angles[i],
                self.edge_position_angles[i + 1] - self.edge_position_angles[i],
                int(self.radius / 8 * 640 * 2),
            )

        # arc(see_through2, GREEN_HIGHLIGHT, to_screen_coords((self.start_x,self.start_y)),(self.circle_radius+self.radius)/8*640 ,edge_position_angles[0],edge_position_angles[1]-edge_position_angles[0],int(self.radius/8*640*2))

        # i dont know what im doing
        if not self.draw_first_arc:
            arc(
                see_through,
                RED_HIGHLIGHT,
                to_screen_coords((self.start_x, self.start_y)),
                (self.circle_radius + self.radius) / 8 * 640,
                self.edge_position_angles[-1],
                math.radians(360) - self.edge_position_angles[-1],
                int(self.radius / 8 * 640 * 2),
            )
            arc(
                see_through,
                RED_HIGHLIGHT,
                to_screen_coords((self.start_x, self.start_y)),
                (self.circle_radius + self.radius) / 8 * 640,
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
                (self.circle_radius + self.radius) / 8 * 640,
                width=round(self.radius * 640 / 8 * 2),
            )
