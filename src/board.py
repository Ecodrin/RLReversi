#from Cell import Coord, Cell
from pygame.locals import Rect


class Board:
    def __init__(self, white_amount=0, black_amount=0):
        self.white_amount = white_amount
        self.black_amount = black_amount
        self.board = []

    def create_board(self) -> None:
        """
        Созданеи массива заполненного объектами типа
        :return:
        """
        for y in range(8):
            for x in range(8):
                self.board(Cell(Coord(x, 7 - y)))
