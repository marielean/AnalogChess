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
from differentfiles.heuristics import custom_heuristic_0, custom_heuristic_1

pygame.init()

ia = IA(utility=custom_heuristic_1, algorithm = 'MiniMax', depth = 1)
board = Board()

# pieces = board.get_pieces()

done = False
clock = pygame.time.Clock()
confirmed = True

# varibili per gestire i turni del gioco
turn_number = 0
# whites_turn = True

pygame.display.set_caption("Analog Chess")

draw_line_round_corners_polygon(
    see_through, (120, 120), (220, 220), RED_HIGHLIGHT, 0.7 * 640 / 8
)
grabbed_piece = None

for piece in board.get_pieces():
    piece.calc_paths(board.get_pieces())
          

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        # turno del giocatore e cioè il bianco (in seguito fare che si sceglie il colore durante la creazione della partita)
        if board.is_white_turn():
            if event.type == pygame.MOUSEBUTTONDOWN:
                for piece in board.get_pieces():

                    if board.is_white_turn():
                        if piece.color == white:
                            piece.try_grab(to_game_coords(pygame.mouse.get_pos()))
                    else:
                        if piece.color != white:
                            piece.try_grab(to_game_coords(pygame.mouse.get_pos()))
                            
                    
            elif event.type == pygame.MOUSEMOTION:
                for piece in board.get_pieces():
                    piece.drag(to_game_coords(pygame.mouse.get_pos()), board.get_pieces())

            elif event.type == pygame.MOUSEBUTTONUP:

                new_pieces = []

                for piece in board.get_pieces():
                    sol = piece.ungrab(board.get_pieces())

                    if sol != None:
                        if sol == True:
                            board.set_turn(not board.is_white_turn())

                    if piece.can_promote():
                        new_pieces.append(Queen(piece.x, piece.y, piece.color))
                    else:
                        new_pieces.append(piece)

                board.set_pieces(new_pieces)

                for piece in board.get_pieces():
                    if piece.deleted and piece.id == king:
                        done = True
                        font = pygame.font.SysFont("oldenglishtext", int(80))
                        confirm_text = font.render("Wiiiiiiin", True, black)
                        draw_center_text(confirm_text)
                        pygame.display.flip()


                for piece in board.get_pieces():
                    piece.calc_paths(board.get_pieces())
            
            # giocatore nero e cioè l'IA (in seguito fare che si sceglie il colore durante la creazione della partita)
            if not board.is_white_turn():

                best_move = ia.get_best_move(board)

                # alphabeta_move = ia.alpha_beta_search(board, 1, whites_turn)
                board.apply_move(best_move)
                
                board.set_turn(True)
            

    
    # ia.set_turn(whites_turn)

    draw_checkers()


    prev_grabbed_piece = grabbed_piece
    grabbed_piece = None
    for piece in board.get_pieces():
        if piece.grabbed:
            grabbed_piece = piece   
    
    if grabbed_piece:
        for piece in board.get_pieces():
            if piece.color != grabbed_piece.color:
                piece.draw_paths(board.get_pieces())
    if grabbed_piece:
        grabbed_piece.draw_moves(board.get_pieces())

    screen.blit(see_through, (0, 0))

    screen.blit(see_through2, (0, 0))

    for piece in board.get_pieces():
        piece.draw()

    # draw grabbed piece last so it will show up on top
    if grabbed_piece:
        grabbed_piece.draw()

    pygame.display.flip()
    clock.tick(30)

    see_through.fill((0, 0, 0, 0))

    see_through2.fill((0, 0, 0, 0))

    