from сell import Coord, Cell


class Board:
    def __init__(self, white_amount=0, black_amount=0) -> None:
        self.white_amount = white_amount
        self.black_amount = black_amount
        self.board = []

    def create_board(self) -> None:
        """
        Создание массива заполненного объектами типа
        :return:
        """
        for y in range(8):
            for x in range(8):
                self.board.append(Cell(Coord(x, 7 - y)))
