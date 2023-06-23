from .piece import Piece


class Board:
    def __init__(self, pieces, color_up):
        self.pieces = pieces
        self.color_up = color_up

    def get_color_up(self):
        return self.color_up

    def get_pieces(self):
        return self.pieces

    def get_piece_by_index(self, index):
        return self.pieces[index]

    def has_piece(self, position):
        string_pos = str(position)

        for piece in self.pieces:
            if piece.get_position() == string_pos:
                return True

        return False

    def get_row_number(self, position):
        return position // 4

    def get_col_number(self, position):
        remainder = position % 4
        column_position = remainder * 2
        is_row_odd = not (self.get_row_number(position) % 2 == 0)
        return column_position + 1 if is_row_odd else column_position

    def get_row(self, row_number):
        row_pos = [0, 1, 2, 3]
        row_pos = list(map((lambda pos: str(pos + (4 * row_number))), row_pos))
        row = []

        for piece in self.pieces:
            if piece.get_position() in row_pos:
                row.append(piece)

        return set(row)

    def get_pieces_by_coords(self, *coords):
        row_memory = dict()
        results = []

        for coord_pair in coords:
            if coord_pair[0] in row_memory:
                current_row = row_memory[coord_pair[0]]
            else:
                current_row = self.get_row(coord_pair[0])
                row_memory[coord_pair[0]] = current_row

            for piece in current_row:
                if self.get_col_number(int(piece.get_position())) == coord_pair[1]:
                    results.append(piece)
                    break
            else:
                results.append(None)

        return results

    def move_piece(self, moved_index, new_position):
        def is_eat_movement(current_position):
            return abs(self.get_row_number(current_position) - self.get_row_number(new_position)) != 1

        def get_eaten_index(current_position):
            current_coords = [self.get_row_number(current_position), self.get_col_number(current_position)]
            new_coords = [self.get_row_number(new_position), self.get_col_number(new_position)]
            eaten_coords = [current_coords[0], current_coords[1]]

            eaten_coords[0] += (new_coords[0] - current_coords[0]) // 2
            eaten_coords[1] += (new_coords[1] - current_coords[1]) // 2

            eaten_position = str(Piece.get_position_with_row_col(eaten_coords[0], eaten_coords[1]))

            for index, piece in enumerate(self.pieces):
                if piece.get_position() == eaten_position:
                    return index

        def is_king_movement(piece):
            if piece.is_king():
                return False

            end_row = self.get_row_number(new_position)
            piece_color = piece.get_color()
            king_row = 0 if self.color_up == piece_color else 7

            return end_row == king_row

        piece_to_move = self.pieces[moved_index]

        if is_eat_movement(int(piece_to_move.get_position())):
            self.pieces.pop(get_eaten_index(int(piece_to_move.get_position())))
            piece_to_move.set_has_eaten(True)
        else:
            piece_to_move.set_has_eaten(False)

        if is_king_movement(piece_to_move):
            piece_to_move.set_is_king(True)

        piece_to_move.set_position(new_position)

    def get_winner(self):
        current_color = self.pieces[0].get_color()

        for piece in self.pieces:
            if piece.get_color() != current_color:
                break
        else:
            return current_color

        return None
