class Piece:
    def __init__(self, details):
        self.details = details
        self.take = False

    def get_details(self):
        return self.details

    def get_position(self):
        return self.details[:-2]

    def set_position(self, new_position):
        pos_index = 1 if len(self.details) == 3 else 2
        self.details = str(new_position) + self.details[pos_index:]

    def get_color(self):
        return self.details[-2]

    def is_dame(self):
        return self.details[-1]

    def set_is_dame(self, dame):
        self.details[-1] = True if dame else False

    def get_take(self):
        return self.take

    def set_take(self, take):
        self.take = take

    @staticmethod
    def get_row_col(row, col):
        return row * 4 + col // 2

    def possible_moves(self, board):
        row = board.get_row(int(self.get_position()))
        col = board.get_col(int(self.get_position()))

        if self.is_dame():
            moves = [(row - 1, col - 1), (row - 1, col + 1), (row + 1, col - 1), (row + 1, col + 1)]
        else:
            if self.get_color() == board.get_turn():
                moves = [(row - 1, col - 1), (row - 1, col + 1)]
            else:
                moves = [(row + 1, col - 1), (row + 1, col + 1)]

        return list(filter(lambda squares: -1 < squares[0] < 8 and -1 < squares[1] < 8, moves))

    def get_moves(self, board):
        row = board.get_row(int(self.get_position()))
        col = board.get_col(int(self.get_position()))

        def get_taken_pos(piece, pos):
            if piece.get_color() == self.get_color() or pos[0] in range(8) or pos[1] in range(8):
                return None

            if pos[1] > col:
                is_take = (2 * pos[0] - row, pos[1] + 1)
            else:
                is_take = (2 * pos[0] - row, pos[1] + 1)
            must_take = (Piece.get_row_col(is_take[0], is_take[1]))

            return None if board.is_busy(must_take) else must_take

