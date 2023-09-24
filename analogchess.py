import pygame
from differentfiles.pieces import *
from differentfiles.colors import *
from differentfiles.utils import to_game_coords
from differentfiles.drawing import (
    see_through,
    see_through2,
    draw_line_round_corners_polygon,
    draw_checkers,
    screen,
)
from differentfiles.AB import *

pygame.init()


pieces = [
    Rook(0.5, 0.5, white),
    King(4.5, 0.5, white),
    Rook(0.5, 7.5, black),
]

done = False
clock = pygame.time.Clock()
confirmed = True

# varibili per gestire i turni del gioco
turn_number = 0
whites_turn = True

pygame.display.set_caption("Analog Chess")


draw_line_round_corners_polygon(
    see_through, (120, 120), (220, 220), RED_HIGHLIGHT, 0.7 * 640 / 8
)
grabbed_piece = None

for piece in pieces:
    piece.calc_paths(pieces)
          



while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for piece in pieces:
                # print(piece.get_turn())
                # print(piece.color, piece.letter, piece.x, piece.y)
                print("turn_number: ", turn_number%2)
                print("turn: ", whites_turn)
                if whites_turn:
                    if piece.color == white:
                        piece.try_grab(to_game_coords(pygame.mouse.get_pos()))
                else:
                    if piece.color != white:
                        piece.try_grab(to_game_coords(pygame.mouse.get_pos()))
                        
                
                '''
                if whites_turn:
                    if piece.color == white:
                        whites_turn = False
                        piece.try_grab(to_game_coords(pygame.mouse.get_pos()))
                else:
                    if piece.color != white:
                        whites_turn = True
                        piece.try_grab(to_game_coords(pygame.mouse.get_pos()))
                
                '''
                
        elif event.type == pygame.MOUSEMOTION:
            for piece in pieces:
                piece.drag(to_game_coords(pygame.mouse.get_pos()), pieces)

        elif event.type == pygame.MOUSEBUTTONUP:

            new_pieces = []
            for piece in pieces:
                sol = piece.ungrab(pieces)
                
                if sol != None:
                    print("sol", sol)
                    if sol:
                        turn_number += 1
                        
                        if whites_turn:
                            whites_turn = False
                        else:
                            whites_turn = True
                #print('game_player_status', game_player_status)
                if piece.can_promote():
                    new_pieces.append(Queen(piece.x, piece.y, piece.color))
                else:
                    new_pieces.append(piece)
            pieces = new_pieces
            for piece in pieces:
                piece.calc_paths(pieces)

            ws, bs = evaluate(pieces)
            # print(ws, bs)
            

    """
    if not pygame.mouse.get_focused():
        for piece in pieces:
            piece.ungrab(pieces)
    """

    draw_checkers()


    prev_grabbed_piece = grabbed_piece
    grabbed_piece = None
    for piece in pieces:
        if piece.grabbed:
            grabbed_piece = piece   
    
    if grabbed_piece:
        for piece in pieces:
            if piece.color != grabbed_piece.color:
                piece.draw_paths(pieces)
    if grabbed_piece:
        grabbed_piece.draw_moves(pieces)

    screen.blit(see_through, (0, 0))

    screen.blit(see_through2, (0, 0))

    for piece in pieces:
        piece.draw()

    # draw grabbed piece last so it will show up on top
    if grabbed_piece:
        grabbed_piece.draw()

    pygame.display.flip()
    clock.tick(30)

    see_through.fill((0, 0, 0, 0))

    see_through2.fill((0, 0, 0, 0))

    '''
    list_directions_white, list_directions_black = get_all_directions(pieces)
    print("random_moves_white: ", list_directions_white)
    print("random_moves_black: ", list_directions_black)
    '''