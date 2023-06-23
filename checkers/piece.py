class Piece:
    def __init__(self, name):
        self.name = name
        self.has_eaten = False

    def get_name(self):
        return self.name

    def get_position(self):
        return self.name[:-2]

    def get_color(self):
        return self.name[-2]

    def get_has_eaten(self):
        return self.has_eaten

    def is_dame(self):
        return True if self.name[-1] == "Y" else False

    def set_position(self, new_position):
        position_index = 1 if len(self.name) == 3 else 2
        self.name = str(new_position) + self.name[position_index:]

    def set_is_dame(self, dame):
        is_dame = "Y" if dame else "N"
        self.name = self.name[:-1] + is_dame

    def set_has_eaten(self, has_eaten):
        self.has_eaten = has_eaten

    def get_adjacent_squares(self, board):
        current_col = board.get_col_number(int(self.get_position()))
        current_row = board.get_row_number(int(self.get_position()))

        if self.is_dame():
            all_coords = [
                (current_row - 1, current_col - 1),
                (current_row - 1, current_col + 1),
                (current_row + 1, current_col - 1),
                (current_row + 1, current_col + 1),
            ]
        else:
            if board.get_color_up() == self.get_color():
                all_coords = [
                    (current_row - 1, current_col - 1),
                    (current_row - 1, current_col + 1),
                ]
            else:
                all_coords = [
                    (current_row + 1, current_col - 1),
                    (current_row + 1, current_col + 1),
                ]

        return list(
            filter(
                lambda coords: coords[0] != -1
                and coords[0] != 8
                and coords[1] != -1
                and coords[1] != 8,
                all_coords,
            )
        )

    def get_moves(self, board):
        def get_eat_position(piece, coords):
            if (piece.get_color() == own_color) or (coords[0] in (0, 7)) or (coords[1] in (0, 7)):
                return None

            if coords[1] > current_col:
                position_to_eat = (coords[0] + (coords[0] - current_row), coords[1] + 1)
            else:
                position_to_eat = (coords[0] + (coords[0] - current_row), coords[1] - 1)

            position_num = Piece.get_position_with_row_col(position_to_eat[0], position_to_eat[1])

            return None if board.has_piece(position_num) else position_num

        current_col = board.get_col_number(int(self.get_position()))
        current_row = board.get_row_number(int(self.get_position()))
        possible_moves = []
        own_color = self.get_color()

        possible_coords = self.get_adjacent_squares(board)

        close_squares = board.get_pieces_by_coords(*possible_coords)
        empty_squares = []

        for index, square in enumerate(close_squares):
            if square is None:
                empty_squares.append(index)
            else:
                position_to_eat = get_eat_position(square, possible_coords[index])
                if position_to_eat is None:
                    continue

                possible_moves.append({"position": str(position_to_eat), "eats_piece": True})

        if len(possible_moves) == 0:
            for index in empty_squares:
                new_position = Piece.get_position_with_row_col(
                    possible_coords[index][0], possible_coords[index][1]
                )
                possible_moves.append({"position": str(new_position), "eats_piece": False})

        return possible_moves

    @staticmethod
    def get_position_with_row_col(row, col):
        return row * 4 + col // 2
