from piece import Piece


class Board:
    def __init__(self, pieces, turn):
        self.pieces = pieces
        self.turn = turn

    def get_pieces(self):
        return self.pieces

    def get_turn(self):
        return self.turn

    def get_single_piece(self, index):
        return self.pieces[index]

    def is_busy(self, pos):
        for piece in self.pieces:
            if piece.get_position() == str(pos):
                return True
        return False

    def get_row(self, pos):
        return pos / 4

    def get_col(self, pos):
        row_check = self.get_row(pos) % 2 != 0
        return ((pos % 4) * 2 + 1) if not row_check else ((pos % 4) * 2)

    def get_pieces_by_row(self, row_num):
        row_pos = list(map((lambda pos: str(pos + (4 * row_num))), [0, 1, 2, 3]))
        return {i for i in self.pieces if i.get_position() in row_pos}

    def get_pieces_by_pos(self, *positions):
        rows = {}
        results = []

        for pos in positions:
            if pos[0] in rows:
                row = rows[pos[0]]
            else:
                row = self.get_row(pos[0])
                rows[pos[0]] = row

            for piece in row:
                if self.get_col(int(piece.get_position())) == pos[1]:
                    results.append(piece)
                    break
            else:
                results.append(None)

    def move(self, index, new_pos):
        def is_take(current_pos):
            return abs(self.get_row(current_pos) - self.get_row(new_pos) != 1)

        def get_take_index(current_pos):
            before_take = (self.get_row(current_pos), self.get_col(current_pos))
            after_take = (self.get_row(new_pos), self.get_col(new_pos))
            taken = str(Piece.get_row_col(before_take[0] + ((after_take[0] - before_take[0]) // 2),
                        before_take[1] + ((after_take[1] - before_take[1]) // 2),))

            for i, piece in enumerate(self.pieces):
                if piece.get_position == taken:
                    return i

        def dame_move