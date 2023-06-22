from .piece import Piece
from .board import Board
from .GUI import GUI
from .hold import Hold


class GameLogic:
    def __init__(self, player):
        self.player = player
        self.winner = None
        self.board = None
        self.gui = None
        self.hold = None

    def get_player(self):
        return self.player

    def get_winner(self):
        return self.winner

    def setup(self):
        pieces = []

        for piece in range(12):
            pieces.append(Piece(str(piece)+"BN"))

        for piece in range(20, 32):
            pieces.append(Piece(str(piece)+"RN"))

        self.board = Board(pieces, self.player)
        self.gui = GUI(self.board)
        pass

    def screen(self, surface):
        self.gui.place_board(surface)
        self.gui.place_pieces(surface)
        if self.hold is not None:
            self.hold.place_piece(surface)

    def hold_piece(self, mouse):
        click = self.gui.get_piece_with_mouse(mouse)
        pieces_on_board = self.board.get_pieces()
        is_take_possible = False

        if click is None:
            return

        if click["piece"]["color"] != self.player:
            return

        for piece in pieces_on_board:
            for move in piece.get_moves(self.board):
                if move["take"]:
                    if piece.get_color() == click["piece"]["color"]:
                        is_take_possible = True
            else:
                continue
            break
