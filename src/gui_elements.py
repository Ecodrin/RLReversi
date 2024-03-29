import pygame
from gui_utility import center_relative_to
from сell import Clickable
from typing import Union


class StylizedText:
    def __init__(self, content: str = '', position: pygame.Rect = (), text_colour: tuple = (0, 0, 0),
                 font_family: str = 'Arial', font_size: int = 24, font_style: int = 0) -> None:
        """
        :param content: Содержимое текста.
        :param position: Позиция текста.
        :param text_colour: Цвет текста.
        :param font_family: Шрифт текста.
        :param font_size: Размер текста.
        :param font_style: Стиль текста. Задаётся битовой маской: 0b01 - жирный, 0b10 - курсив.
        :return:
        """
        self.content: str = content
        self.position: pygame.Rect = position
        self.text_colour: tuple = text_colour
        self.font_family: str = font_family
        self.font_size: int = font_size
        self.font_style: int = font_style
        self.text: pygame.SurfaceType = self.text_create()

    def __is_italic(self) -> int:
        """
        :return: Разряд отвечающий за курсив.
        """
        return self.font_style & 0b10

    def __is_bold(self) -> int:
        """
        :return: Разряд отвечающий за жирность.
        """
        return self.font_style & 0b01

    def text_create(self) -> pygame.SurfaceType:
        bold, italic = self.__is_bold(), self.__is_italic()
        font = pygame.font.SysFont(self.font_family, self.font_size, bold=bold, italic=italic)
        text_surface = font.render(self.content, True, self.text_colour)
        self.position[2], self.position[3] = text_surface.get_width(), text_surface.get_height()
        return text_surface

    def render(self, screen: pygame.display) -> None:
        """
        Отображает текст с заданным стилем и позицией
        :param screen: Разрешение выводимого окна.
        """
        screen.blit(self.text, self.position)

    def __repr__(self):
        return (f'StylizedText({self.content}, {self.position} ,{self.text_colour}, '
                f'{self.font_family}, {self.font_size}, {self.font_style})')

    def __str__(self):
        return f'("{self.content}", {self.font_size}, {self.text_colour})'


class Button(Clickable):

    def __init__(self, onClick: Callable, *args,
                 hitbox: Rect = pygame.Rect(0, 0, 0, 0),
                 inner_text: StylizedText = '',
                 default_texture: Union[tuple, str] = (0, 0, 255),
                 hover_texture: Union[tuple, str] = (255, 0, 0),
                 click_texture: Union[tuple, str] = (0, 255, 0)) -> None:

        super().__init__(onClick, *args, hitbox=hitbox)
        self.inner_text: StylizedText = inner_text
        self.default_texture: Union[tuple, str] = default_texture
        self.hover_texture: Union[tuple, str] = hover_texture
        self.click_texture: Union[tuple, str] = click_texture
        self.button_texture: Union[tuple, str] = self.default_texture

    def hover_click(self, event: pygame.event) -> None:
        point = pygame.mouse.get_pos()
        collide = self.hitbox.collidepoint(point)
        if collide:
            self.button_texture = self.hover_texture
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.button_texture = self.click_texture
            elif event.type == pygame.MOUSEBUTTONUP:
                self.button_texture = self.hover_texture

        else:
            self.button_texture = self.default_texture

    def render(self, screen: pygame.display) -> None:
        center_relative_to(self.inner_text.position, self.hitbox)

        if isinstance(self.button_texture, tuple):
            pygame.draw.rect(screen, self.button_texture, self.hitbox)
            self.inner_text.render(screen)
        else:
            img = pygame.image.load(self.button_texture)
            img = pygame.transform.scale(img, (self.hitbox[2], self.hitbox[3]))
            screen.blit(img, self.hitbox)
            self.inner_text.render(screen)

    def __repr__(self):
        return (f'{self.inner_text}, {self.default_texture}, {self.hover_texture},'
                f'{self.click_texture}, {self.onClick}, {self.args}, {self.hitbox}')

    def __str__(self):
        return f'{self.inner_text}, {self.default_texture}, {self.hover_texture}, {self.click_texture}'
