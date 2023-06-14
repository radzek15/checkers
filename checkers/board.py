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

    @staticmethod
    def get_row(pos):
        return pos / 4

    def get_col(self, pos):
        row_check = self.get_row(pos) % 2 == 0
        return ((pos % 4) * 2 + 1) if not row_check else ((pos % 4) * 2)

    def get_pieces_by_row(self, row_num):
        row_pos = list(map((lambda pos: str(pos + (4 * row_num))), [0, 1, 2, 3]))
        return {i for i in self.pieces if i.get_position() in row_pos}
