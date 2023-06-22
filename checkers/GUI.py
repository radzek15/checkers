import pygame as pg
from .piece import Piece

BLACK_PAWN = pg.image.load("images/black_pawn.png")
RED_PAWN = pg.image.load("images/red_pawn.png")
BLACK_DAME = pg.image.load("images/black_dame.png")
RED_DAME = pg.image.load("images/red_dame.png")
BOARD = pg.image.load("images/board.svg")
MARK = pg.image.load("images/mark.png")

DIST = 100
TOP_LEFT = (0, 0)


class GUI:
    def __init__(self, board):
        self.pieces = self.get_piece_details(board)
        self.del_piece = -1
        self.moves = []

    def set_pieces(self, all_pieces):
        self.pieces = all_pieces

    def get_piece_details(self, board):
        starting_pieces = board.get_pieces()
        pieces = []

        for p in starting_pieces:
            p_pos = int(p.get_position())
            p_row = board.get_row(p_pos)
            p_col = board.get_col(p_pos)
            p_details = {
                "rect": pg.Rect(GUI.get_GUI_position((p_row, p_col), DIST, TOP_LEFT), (50, 50)),
                "color": p.get_color(),
                "is_dame": p.is_dame()
            }

            pieces.append(p_details)

        return pieces

    def get_single_piece(self, index):
        return self.pieces[index]

    def delete_piece(self, index):
        self.del_piece = index

    def load_piece(self):
        loaded_piece = self.del_piece
        self.del_piece = -1
        return loaded_piece

    def place_pieces(self, surface):
        for i, piece in enumerate(self.pieces):
            if i == self.del_piece:
                continue

            if piece["is_dame"]:
                surface.blit(BLACK_DAME if piece["color"] == 'B' else RED_DAME, piece["rect"])
            else:
                surface.blit(BLACK_PAWN if piece["color"] == 'B' else RED_PAWN, piece["rect"])

    def get_moves(self):
        return self.moves

    def set_moves(self, all_pos):
        if len(all_pos) == 0:
            self.moves = []

        for pos in all_pos:
            self.moves.append(pg.Rect(GUI.get_GUI_position((pos[0], pos[1]), DIST, TOP_LEFT), (50, 50)))

    def place_board(self, surface):
        surface.blit(BOARD, (0, 0))

        if len(self.moves) != 0:
            for pos in self.moves:
                surface.blit(MARK, pos)

    def get_piece_with_mouse(self, mouse):
        for i, piece in enumerate(self.pieces):
            if piece["rect"].collidepoint(mouse):
                return {"index": i, "piece": piece}
        return None

    @staticmethod
    def get_position_with_rect(rect):
        return GUI.get_piece_position((rect.x, rect.y), DIST, TOP_LEFT)

    @staticmethod
    def get_surface(piece):
        surfaces = [BLACK_DAME, RED_DAME] if piece.is_dame() else [BLACK_PAWN, RED_PAWN]
        return surfaces[0] if piece.get_color() == 'B' else surfaces[1]

    @staticmethod
    def get_GUI_position(pos, dist, top_left):
        x_pos = top_left[0] + 2*dist*(pos[1]//2) if pos[0] % 2 == 0 else top_left[0] + 2*dist*(pos[1]//2) + dist
        y_pos = top_left[1] + dist * pos[0]

        return x_pos, y_pos

    @staticmethod
    def get_piece_position(pos, dist, top_left):
        row = (pos[0] - top_left[0]) // dist
        col = (pos[1] - top_left[1]) // dist

        return Piece.get_row_col(row, col)
