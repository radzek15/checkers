from copy import deepcopy
from random import choice

from .board import Board


class AI:
    def __init__(self, color):
        self.color = color

    def minimax(self, board, is_maximizing, depth, turn):
        if depth == 0 or board.get_winner() is not None:
            return self.get_value(board)

        next_turn = "B" if turn == "R" else "R"
        board_color_up = board.get_color_up()
        ai_pieces = board.get_pieces()
        ai_moves = list(
            map(
                lambda piece: piece.get_moves(board) if piece.get_color() == turn else False,
                ai_pieces,
            )
        )

        if is_maximizing:
            maximum = -999
            for index, moves in enumerate(ai_moves):
                if moves is False:
                    continue

                for move in moves:
                    aux_board = Board(deepcopy(ai_pieces), board_color_up)
                    aux_board.move_piece(index, int(move["position"]))
                    maximum = max(self.minimax(aux_board, False, depth - 1, next_turn), maximum)

            return maximum
        else:
            minimum = 999
            for index, moves in enumerate(ai_moves):
                if moves is False:
                    continue

                for move in moves:
                    aux_board = Board(deepcopy(ai_pieces), board_color_up)
                    aux_board.move_piece(index, int(move["position"]))
                    minimum = min(self.minimax(aux_board, True, depth - 1, next_turn), minimum)

            return minimum

    def get_move(self, board):
        board_color_up = board.get_color_up()
        pieces = board.get_pieces()
        next_turn = "R" if self.color == "B" else "B"
        ai_pieces = list(
            map(lambda piece: piece if piece.get_color() == self.color else False, pieces)
        )
        possible_moves = []
        move_scores = []

        for index, piece in enumerate(ai_pieces):
            if piece is False:
                continue

            for move in piece.get_moves(board):
                possible_moves.append({"piece": index, "move": move})

        jump_moves = list(filter(lambda mv: mv["move"]["eats_piece"] is True, possible_moves))

        if len(jump_moves) != 0:
            possible_moves = jump_moves

        for move in possible_moves:
            aux_board = Board(deepcopy(pieces), board_color_up)
            aux_board.move_piece(move["piece"], int(move["move"]["position"]))
            move_scores.append(self.minimax(aux_board, False, 2, next_turn))

        best_score = max(move_scores)
        best_moves = []

        for index, move in enumerate(possible_moves):
            if move_scores[index] == best_score:
                best_moves.append(move)

        move_chosen = choice(best_moves)
        return {
            "position_to": move_chosen["move"]["position"],
            "position_from": ai_pieces[move_chosen["piece"]].get_position(),
        }

    def get_value(self, board):
        board_pieces = board.get_pieces()

        if board.get_winner() is not None:
            if board_pieces[0].get_color() == self.color:
                return 2
            else:
                return -2

        total_pieces = len(board_pieces)
        ai_pieces = len(list(filter(lambda piece: piece.get_color() == self.color, board_pieces)))
        player_pieces = total_pieces - ai_pieces

        if ai_pieces == player_pieces:
            return 0

        return 1 if ai_pieces > player_pieces else -1
