from pygame.locals import Rect
from pygame import mouse


class Coord:
    def __init__(self, x=0, y=0):
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
    def __init__(self, content=0, weight=0, x=0, y=0):
        self.position = x, y
        self.content = content
        self.weight = weight
        self.index = x * 8 + y
        self.possible_moves = []


class Clickable:
    def __init__(self, onClick, *args, hitbox=Rect(0, 0, 0, 0)):
        self.onClick = onClick
        self.args = args
        self.hitbox = hitbox

    def process(self):
        """checks collision and calls callback"""
        mouse_x, mouse_y = mouse.get_pos()
        if self.hitbox[0] <= mouse_x <= self.hitbox[0] + self.hitbox[2] and \
                self.hitbox[1] <= mouse_y <= self.hitbox[1] + self.hitbox[3]:
            self.onClick(self.args)
