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
