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


class Clickable:
    def __init__(self, onClick: Callable, *args, hitbox: Rect = pygame.Rect(0, 0, 0, 0)) -> None:
        """
        Clickable (property)
        :param onClick (callback function):
        :param *args (arguments for callback function):
        :param  hitbox (rectangular):
        """
        self.onClick = onClick
        self.args = args
        self.hitbox = hitbox

    def process(self) -> None:
        """
        checks collision and calls callback
        """
        point = pygame.mouse.get_pos()
        collide = self.hitbox.collidepoint(point)
        if collide:
            self.onClick(*self.args)
