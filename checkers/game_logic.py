from .ai import AI
from .board import Board
from .GUI import GUI
from .hold import Hold
from .piece import Piece


class GameLogic:
    def __init__(self, player_color, is_computer_opponent):
        self.turn = player_color
        self.winner = None
        self.board = None
        self.board_draw = None
        self.held_piece = None
        self.ai_control = None

        if is_computer_opponent:
            self.ai_control = AI("B") if player_color == "R" else AI("R")

        self.setup()

    def get_turn(self):
        return self.turn

    def get_winner(self):
        return self.winner

    def setup(self):
        # Initial setup
        pieces = []

        for opponent_piece in range(0, 12):
            pieces.append(Piece(str(opponent_piece) + "BN"))

        for player_piece in range(20, 32):
            pieces.append(Piece(str(player_piece) + "RN"))

        self.board = Board(pieces, self.turn)
        self.board_draw = GUI(self.board)
        pass

    def draw_screen(self, display_surface):
        self.board_draw.draw_board(display_surface)
        self.board_draw.draw_pieces(display_surface)

        if self.held_piece is not None:
            self.held_piece.place_piece(display_surface)

    def hold_piece(self, mouse_pos):
        piece_clicked = self.board_draw.get_piece_on_mouse(mouse_pos)
        board_pieces = self.board.get_pieces()
        has_jump_restraint = False

        if piece_clicked is None:
            return

        if piece_clicked["piece"]["color"] != self.turn:
            return

        for piece in board_pieces:
            for move in piece.get_moves(self.board):
                if move["eats_piece"]:
                    if piece.get_color() == piece_clicked["piece"]["color"]:
                        has_jump_restraint = True
            else:
                continue

        piece_moves = board_pieces[piece_clicked["index"]].get_moves(self.board)

        if has_jump_restraint:
            piece_moves = list(filter(lambda mv: mv["eats_piece"] is True, piece_moves))

        move_marks = []

        for possible_move in piece_moves:
            row = self.board.get_row_number(int(possible_move["position"]))
            column = self.board.get_col_number(int(possible_move["position"]))
            move_marks.append((row, column))

        self.board_draw.set_move_marks(move_marks)

        self.board_draw.hide_piece(piece_clicked["index"])
        self.set_held_piece(piece_clicked["index"], board_pieces[piece_clicked["index"]], mouse_pos)

    def release_piece(self):
        if self.held_piece is None:
            return

        position_released = self.held_piece.check_collision(self.board_draw.get_move_marks())
        moved_index = self.board_draw.show_piece()
        piece_moved = self.board.get_piece_by_index(moved_index)

        if position_released is not None:
            self.board.move_piece(
                moved_index, self.board_draw.get_position_by_rect(position_released)
            )
            self.board_draw.set_pieces(self.board_draw.get_piece_properties(self.board))
            self.winner = self.board.get_winner()

            jump_moves = list(
                filter(lambda move: move["eats_piece"] is True, piece_moved.get_moves(self.board))
            )

            if len(jump_moves) == 0 or piece_moved.get_has_eaten() is False:
                self.turn = "B" if self.turn == "R" else "R"

        self.held_piece = None
        self.board_draw.set_move_marks([])

    def set_held_piece(self, index, piece, mouse_pos):
        surface = self.board_draw.get_surface(piece)
        offset = GameLogic.get_surface_coords(
            self.board_draw.get_piece_by_index(index)["rect"], mouse_pos
        )
        self.held_piece = Hold(surface, offset)

    def move_ai(self):
        if self.turn == "R":
            return

        optimal_move = self.ai_control.get_move(self.board)

        for index, piece in enumerate(self.board.get_pieces()):
            if piece.get_position() == optimal_move["position_from"]:
                index_moved = index
                piece_moved = piece
                break
        else:
            raise RuntimeError(
                "AI was supposed to return a move from an existing piece but found none."
            )

        self.board.move_piece(index_moved, int(optimal_move["position_to"]))
        self.board_draw.set_pieces(self.board_draw.get_piece_properties(self.board))
        self.winner = self.board.get_winner()

        jump_moves = list(
            filter(lambda move: move["eats_piece"] is True, piece_moved.get_moves(self.board))
        )

        if len(jump_moves) == 0 or piece_moved.get_has_eaten() is False:
            self.turn = "B" if self.turn == "R" else "R"

    @staticmethod
    def get_surface_coords(surface, mouse):
        return surface[0] - mouse[0], surface[1] - mouse[1]
