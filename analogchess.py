import pygame, time, random
from differentfiles.pieces.pawn import *
from differentfiles.pieces import *
from differentfiles.colors import *
from differentfiles.utils import to_game_coords
from differentfiles.drawing import (
    see_through,
    see_through2,
    draw_line_round_corners_polygon,
    draw_checkers,
    screen,
    draw_center_text,
)
from differentfiles.AB import *

pygame.init()


pieces = [
    Pawn(0.5, 1.5, white),
    Rook(0.5, 0.5, white),
    King(4.5, 0.5, white),
    Knight(1.5, 0.5, white),
    Knight(6.5, 7.5, black),
    King(4.5, 7.5, black),
    Rook(0.5, 7.5, black),
    Pawn(0.5, 6.5, black),
]

pieces1 = [
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

        # turno del giocatore e cioè il bianco (in seguito fare che si sceglie il colore durante la creazione della partita)
        if whites_turn:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for piece in pieces:
                    # print(piece.get_turn())
                    # print(piece.color, piece.letter, piece.x, piece.y)
                    # print("turn_number: ", turn_number%2)
                    # print("whites_turn: ", whites_turn)
                    # piece.try_grab(to_game_coords(pygame.mouse.get_pos()))
                    
                    if whites_turn:
                        if piece.color == white:
                            piece.try_grab(to_game_coords(pygame.mouse.get_pos()))
                    else:
                        if piece.color != white:
                            piece.try_grab(to_game_coords(pygame.mouse.get_pos()))
                            # move = alpha_beta_search(pieces, 3, whites_turn)
                            # apply_move(pieces, move)
                            
                                
                    
            elif event.type == pygame.MOUSEMOTION:
                for piece in pieces:
                    piece.drag(to_game_coords(pygame.mouse.get_pos()), pieces)

            elif event.type == pygame.MOUSEBUTTONUP:

                new_pieces = []
                for piece in pieces:
                    sol = piece.ungrab(pieces)
                    
                    if sol != None:
                        # print("sol:", sol)
                        if sol == True:
                            if whites_turn:
                                whites_turn = False
                            else:
                                whites_turn = True
                    if piece.can_promote():
                        new_pieces.append(Queen(piece.x, piece.y, piece.color))
                    else:
                        new_pieces.append(piece)
                pieces = new_pieces

                for piece in pieces:
                    if piece.deleted and piece.id == king:
                        done = True
                        font = pygame.font.SysFont("oldenglishtext", int(80))
                        confirm_text = font.render("Wiiiiiiin", True, black)
                        draw_center_text(confirm_text)
                        pygame.display.flip()

                
                '''
                for piece in pieces:
                    whites_turn = piece.white_turn
                '''

                for piece in pieces:
                    piece.calc_paths(pieces)
            
            # giocatore nero e cioè l'IA (in seguito fare che si sceglie il colore durante la creazione della partita)
            if whites_turn == False:
                move = best_move(pieces, whites_turn)
                alpha_beta = alpha_beta_search(pieces, 1, whites_turn)
                print("alpha_beta: ", alpha_beta)
                whites_turn = True
            
            

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
        # pass
        piece.draw()

    # draw grabbed piece last so it will show up on top
    if grabbed_piece:
        grabbed_piece.draw()

    pygame.display.flip()
    clock.tick(30)

    see_through.fill((0, 0, 0, 0))

    see_through2.fill((0, 0, 0, 0))

    
    # list_directions_white, list_directions_black = get_all_directions_all_in_one(pieces)
    # print("list_directions_white: ", list_directions_white)
    # print("list_directions_black: ", list_directions_black)

    # print("\n\n\n")
    # all_point_white = get_all_moves_from_distance(list_directions_white)
    # print("all_point_white: ", all_point_white)

    # print("action: ", actions(pieces, whites_turn))
    