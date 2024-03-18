from pygame.locals import Rect
import pygame
from typing import Callable


class Coord:
    def __init__(self, x: int = 0, y: int = 0) -> None:
        self.x, self.y = x, y

    def __str__(self):
        return f'({self.x}, {self.y})'

    def __add__(self, other):
        new_x = self.x + other.x
        new_y = self.y + other.y
        return Coord(new_x, new_y)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y

    def __sub__(self, other):
        new_x = self.x - other.x
        new_y = self.y - other.y
        return Coord(new_x, new_y)

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y


class Cell:
    def __init__(self, content: int = 0, weight: int = 0, coord: Coord = Coord()) -> None:
        """

        :param content Content in the cell:
        :param weight:
        :param coord Coordinates of the cell:
        """
        self.position = coord.x, coord.y
        self.content = content
        self.weight = weight
        self.index = coord.x + coord.y * 8
        self.possible_moves = []


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
