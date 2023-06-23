import pygame as pg

from .piece import Piece

BLACK_PAWN = pg.image.load("images/black_pawn.png")
RED_PAWN = pg.image.load("images/red_pawn.png")
BLACK_KING = pg.image.load("images/black_dame.png")
RED_KING = pg.image.load("images/red_dame.png")
BOARD = pg.image.load("images/board.svg")
MARK = pg.image.load("images/mark.png")

SQUARE_DIST = 100
TOPLEFTBORDER = (0, 0)


class GUI:
    def __init__(self, board):
        self.pieces = self.get_piece_properties(board)
        self.hidden_piece = -1
        self.move_marks = []

    def set_pieces(self, piece_list):
        self.pieces = piece_list

    def get_piece_properties(self, board):
        initial_pieces = board.get_pieces()
        pieces = []

        for piece in initial_pieces:
            piece_position = int(piece.get_position())
            piece_row = board.get_row_number(piece_position)
            piece_column = board.get_col_number(piece_position)
            piece_properties = dict()

            piece_properties["rect"] = pg.Rect(
                GUI.get_GUI_position((piece_row, piece_column), SQUARE_DIST, TOPLEFTBORDER),
                (100, 100),
            )
            piece_properties["color"] = piece.get_color()
            piece_properties["is_king"] = piece.is_king()

            pieces.append(piece_properties)

        return pieces

    def get_piece_by_index(self, index):
        return self.pieces[index]

    def hide_piece(self, index):
        self.hidden_piece = index

    def show_piece(self):
        piece_shown = self.hidden_piece
        self.hidden_piece = -1
        return piece_shown

    def draw_pieces(self, display_surface):
        for index, piece in enumerate(self.pieces):
            if index == self.hidden_piece:
                continue

            if piece["is_king"]:
                display_surface.blit(
                    BLACK_KING if piece["color"] == "B" else RED_KING, piece["rect"]
                )
            else:
                display_surface.blit(
                    BLACK_PAWN if piece["color"] == "B" else RED_PAWN, piece["rect"]
                )

    def draw_board(self, display_surface):
        display_surface.blit(BOARD, (0, 0))

        if len(self.move_marks) != 0:
            for rect in self.move_marks:
                display_surface.blit(MARK, rect)

    def get_piece_on_mouse(self, mouse_pos):
        for index, piece in enumerate(self.pieces):
            if piece["rect"].collidepoint(mouse_pos):
                return {"index": index, "piece": piece}

        return None

    def get_surface(self, piece):
        surfaces = [BLACK_PAWN, RED_PAWN, BLACK_KING, RED_KING]
        surfaces = surfaces[2:] if piece.is_king() else surfaces[:2]

        return surfaces[0] if piece.get_color() == "B" else surfaces[1]

    def get_move_marks(self):
        return self.move_marks

    def set_move_marks(self, position_list):
        if len(position_list) == 0:
            self.move_marks = []

        for position in position_list:
            row = position[0]
            column = position[1]
            self.move_marks.append(
                pg.Rect(GUI.get_GUI_position((row, column), SQUARE_DIST, TOPLEFTBORDER), (100, 100))
            )

    def get_position_by_rect(self, rect):
        return GUI.get_piece_position((rect.x, rect.y), SQUARE_DIST, TOPLEFTBORDER)

    @staticmethod
    def get_GUI_position(pos, dist, top_left):
        x_pos = top_left[0] + dist * (pos[1] - (pos[0] % 2) // 2)
        y_pos = top_left[1] + dist * pos[0]

        return x_pos, y_pos

    @staticmethod
    def get_piece_position(pos, dist, top_left):
        row = (pos[1] - top_left[1]) // dist
        col = (pos[0] - top_left[0]) // dist

        return Piece.get_position_with_row_col(row, col)
