import pygame as pg
from pygame.locals import *
from checkers.game_logic import GameLogic
from sys import exit, argv


def main(gamemode):
    pg.init()
    PLAYER_COLOR = "R"
    WHITE = (255, 255, 255)
    DISPLAYSURF = pg.display.set_mode((1000, 800))
    pg.display.set_caption('Checkers')
    fps_clock = pg.time.Clock()

    if gamemode == "cpu":
        game_control = GameLogic(PLAYER_COLOR, True)
    else:
        game_control = GameLogic(PLAYER_COLOR, False)

    main_font = pg.font.SysFont("Arial", 25)
    turn_rect = (820, 26)
    winner_rect = (820, 152)

    while True:
        DISPLAYSURF.fill((0, 0, 0))
        game_control.draw_screen(DISPLAYSURF)

        turn_display_text = "Red's turn" if game_control.get_turn() == "R" else "Black's turn"
        DISPLAYSURF.blit(main_font.render(turn_display_text, True, WHITE), turn_rect)

        if game_control.get_winner() is not None:
            winner_display_text = "Red wins!" if game_control.get_winner() == "R" else "Black wins!"
            DISPLAYSURF.blit(main_font.render(winner_display_text, True, WHITE), winner_rect)

        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                return

            if event.type == MOUSEBUTTONDOWN:
                game_control.hold_piece(event.pos)

            if event.type == MOUSEBUTTONUP:
                game_control.release_piece()

                if game_control.get_turn() != PLAYER_COLOR and gamemode == "cpu":
                    pg.time.set_timer(USEREVENT, 400)

            if event.type == USEREVENT:
                if game_control.get_winner() is not None:
                    continue

                game_control.move_ai()

                if game_control.get_turn() == PLAYER_COLOR:
                    pg.time.set_timer(USEREVENT, 0)

        pg.display.update()
        fps_clock.tick(30)


if __name__ == '__main__':
    if len(argv) != 2:
        print("Please specify the game mode.")
    else:
        if argv[1] in ["cpu", "pvp"]:
            main(argv[1])
        else:
            print("Game mode not found.")

    exit()
