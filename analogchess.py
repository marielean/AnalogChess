import pygame, time, random
from differentfiles.pieces import *
from differentfiles.ia import IA
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
from differentfiles.heuristics import custom_heuristic_0, custom_heuristic_1

pygame.init()

ia = IA(utility=custom_heuristic_0, algorithm = 'Random', depth = 4)
board = Board(pieces=True, granularity=20)

done = False
clock = pygame.time.Clock()
confirmed = True

turn_number = 0

pygame.display.set_caption("Analog Chess")

draw_line_round_corners_polygon(
    see_through, (120, 120), (220, 220), RED_HIGHLIGHT, 0.7 * 640 / 8
)
grabbed_piece = None

for piece in board.get_pieces():
    piece.calc_paths(board.get_pieces())
          
just_played = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        # turno del giocatore e cioè il bianco
        if board.is_white_turn():
            if event.type == pygame.MOUSEBUTTONDOWN:
                for piece in board.get_pieces():

                    if piece.color == white:
                        piece.try_grab(to_game_coords(pygame.mouse.get_pos()))
                    
            elif event.type == pygame.MOUSEMOTION:
                for piece in board.get_pieces():
                    piece.drag(to_game_coords(pygame.mouse.get_pos()), board.get_pieces())

            elif event.type == pygame.MOUSEBUTTONUP:

                new_pieces = []
                new_new_pieces = []

                for piece in board.get_pieces():
                    sol = piece.ungrab(board.get_pieces())

                    if sol != None:
                        if sol == True:
                            board.set_turn(not board.is_white_turn())
                            just_played = True

                    if piece.can_promote() and not piece.deleted:
                        new_pieces.append(Queen(piece.x, piece.y, piece.color))
                    elif not piece.deleted:
                        new_pieces.append(piece)

                board.set_pieces(new_pieces)

                if board.is_terminal():
                    print("This is the end...")
                    done = True
                    font = pygame.font.SysFont("oldenglishtext", int(80))
                    confirm_text = font.render("Wiiiiiiin", True, black)
                    draw_center_text(confirm_text)
                    pygame.display.flip()

                for piece in board.get_pieces():
                    piece.calc_paths(board.get_pieces())
            

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

    # Il giocatore nero gioca solamente quando il bianco ha appena finito di giocare
    if just_played:

        # print("Before:\n",board.get_chess_board_status())

        best_move = ia.get_best_move(board)

        board.apply_move(best_move)

        print("Mossa selezionata: ", best_move)
        print("Pezzo giocato dal computer", best_move[0])
        # print("After:\n", board.get_chess_board_status())
        _, black_pieces = board.get_chess_board_status()
        print("pieces: ", black_pieces)
        
        board.set_turn(True)
        just_played = False
        if board.is_terminal():
            print("This is the end...")
            done = True
            font = pygame.font.SysFont("oldenglishtext", int(80))
            confirm_text = font.render("Wiiiiiiin", True, black)
            draw_center_text(confirm_text)
            pygame.display.flip()

