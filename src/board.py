from pygame.locals import Rect
import pygame
from typing import Callable


class Board:
    def __init__(self, size) -> None:
        self.size = size
        self.board: list[int] = []
        self.create_board()

    def create_board(self) -> None:
        """
        Очистка и заполнение массива объектами типа Cell
        :return:
        """
        self.board.clear()
        for y in range(self.size):
            for x in range(self.size):
                self.board.append(0)

    # Получить уникальный ID доски. Всего возможных ID: (кол-во возможных ходов) в степени (кол-во ячеек). Для 3х3: 3^9
    def get_uid(self) -> int:
        result: int = 0
        # Проходит по каждой ячейке доски, нормализует её (приводит к положительным числам)
        # и выделяет ей свое место в системе счисления, равной размеру доски.
        for i in range(len(self.board)):
            result += self.size ** i * (self.board[i] + 1)
        return result


class Clickable:

    def __init__(self, hitbox: pygame.Rect, onClick: Callable, *args) -> None:
        """
        Clickable (property)
        :param onClick (callback function):
        :param *args (arguments for callback function):
        :param hitbox (rectangular):
        """
        self.hitbox: pygame.Rect = hitbox
        self.onClick: Callable = onClick
        self.args = args

    def check_collision(self) -> bool:
        """
        Checks collision.
        :return: Rect collision with mouse
        """
        point = pygame.mouse.get_pos()
        collide = self.hitbox.collidepoint(point)
        return collide

    def process(self) -> None:
        """
        Calls callback
        """
        if self.check_collision():
            self.onClick(*self.args)
