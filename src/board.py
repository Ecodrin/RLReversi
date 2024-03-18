from Cell import Coord, Cell


class Board:
    def __init__(self, white_amount: int = 0, black_amount: int = 0) -> None:
        self.white_amount = white_amount
        self.black_amount = black_amount
        self.board = []
        self.create_board()

    def create_board(self) -> None:
        """
        Очистка и заполнение массива объектами типа Cell
        :return:
        """
        self.board.clear()
        for y in range(8):
            for x in range(8):
                self.board.append(Cell(Coord(x, 7 - y)))
