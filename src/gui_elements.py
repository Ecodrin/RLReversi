import os
import pygame
from typing import Callable
from pygame.locals import Rect
from gui_utility import center_relative_to
from сell import Clickable


class StylizedText:
    def __init__(self, position: pygame.Rect, borders: pygame.Rect, content: str = '',
                 text_colour: pygame.color.Color = pygame.color.Color(255, 255, 255),
                 font_family: str = 'arial', font_size: int = 24,
                 font_style: int = 0) -> None:
        """
        :param content: Содержимое.
        :param position: Позиция.
        :param text_colour: Цвет.
        :param font_family: Шрифт текста.
        :param font_size: Размер текста.
        :param font_style: Стиль текста. Задаётся битовой маской: 0b01 - жирный, 0b10 - курсив.
        :param borders: Границы Кнопки (special for button).
        :return:
        """
        self.position: pygame.Rect = position
        self.content: str = content
        self.text_colour: pygame.color.Color = text_colour
        self.font_family: str = font_family
        self.font_size: int = font_size
        self.font_style: int = font_style
        self.borders: pygame.Rect = borders

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

    def render(self, screen: pygame.display) -> None:
        """
        Отображает текст с заданным стилем и позицией.
        :param screen: Разрешение выводимого окна.
        """

        bold, italic = self.__is_bold(), self.__is_italic()
        if self.font_family in pygame.font.get_fonts():
            font = pygame.font.SysFont(self.font_family, self.font_size, italic=italic, bold=bold)
        else:
            font = pygame.font.Font(self.font_family, self.font_size)
            font.set_bold(bold == 1)
            font.set_italic(italic == 2)

        words = self.content.split()
        lines = []
        line = ''
        line_width = 0

        for word in words:
            word_surface = font.render(word, True, self.text_colour)
            word_width = word_surface.get_width()
            if line_width + word_width >= self.borders[2]:
                lines.append(line)
                line = word + ' '
                line_width = word_width
            else:
                line += word + ' '
                line_width += word_width
            print(line)
        lines.append(line)

        y_offset = self.position[1] + (self.borders[3] - len(lines) * self.font_size) // 2
        for line in lines:
            text_surface = font.render(line, True, self.text_colour)
            text_rect = text_surface.get_rect(center=(self.position[0] + self.position[2] // 2,
                                                      y_offset + self.font_size // 2))
            screen.blit(text_surface, text_rect)
            y_offset += self.font_size

    def __repr__(self):
        return (f'StylizedText("{self.content}", {self.position} ,{self.text_colour}, '
                f'{self.font_family}, {self.font_size}, {self.font_style})')

    def __str__(self):
        return f'("{self.content}", {self.font_size}, {self.text_colour})'


class Button(Clickable):

    def __init__(self, onClick: Callable, *args,
                 hitbox: Rect, inner_text: StylizedText,
                 default_texture: pygame.color.Color | os.PathLike = pygame.color.Color(255, 255, 255),
                 hover_texture: pygame.color.Color | os.PathLike = pygame.color.Color(160, 160, 160),
                 click_texture: pygame.color.Color | os.PathLike = pygame.color.Color(64, 64, 64),
                 border_radius: int = 0) -> None:

        """
        :param onClick (callback function):
        :param *args (arguments for callback function):
        :param  hitbox (rectangular):
        :param inner_text: Текст на кнопке.
        :param default_texture: Стандартная текстура кнопки.
        :param hover_texture: Текстура при наведении курсора.
        :param click_texture: Текстура при клике.
        :param border_radius: Радиус округления.
        """
        super().__init__(onClick, *args, hitbox=hitbox)
        self.inner_text: StylizedText = inner_text
        self.default_texture: pygame.color.Color | os.PathLike = default_texture
        self.hover_texture: pygame.color.Color | os.PathLike = hover_texture
        self.click_texture: pygame.color.Color | os.PathLike = click_texture
        self.button_texture: pygame.color.Color | os.PathLike = self.default_texture
        self.border_radius: int = border_radius

    def hover_click(self, event: pygame.event) -> None:
        """
        Красит кнопку в нужный цвет.
        :param event: Действия пользователя
        """
        collide = super().check_collision()
        if collide:
            self.button_texture = self.hover_texture
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.button_texture = self.click_texture
            elif event.type == pygame.MOUSEBUTTONUP:
                self.button_texture = self.hover_texture

        else:
            self.button_texture = self.default_texture

    def render(self, screen: pygame.display) -> None:
        """
        Выводит кнопку на экран.
        :param screen: Разрешение выводимого окна
        """
        center_relative_to(self.inner_text.position, self.hitbox)
        if isinstance(self.button_texture, pygame.color.Color):
            pygame.draw.rect(screen, self.button_texture, self.hitbox, 0, border_radius=self.border_radius)
        elif isinstance(self.button_texture, os.PathLike):
            img = pygame.image.load(self.button_texture)
            img = pygame.transform.scale(img, (self.hitbox[2], self.hitbox[3]))
            screen.blit(img, self.hitbox)
        else:
            raise TypeError('Invalid texture type')
        self.inner_text.render(screen)

    def __repr__(self):
        return (f'Button("{self.inner_text}", {self.hitbox},{self.default_texture}, {self.hover_texture},'
                f'{self.click_texture}, {self.onClick} {self.args})')

    def __str__(self):
        return f'"{self.inner_text}", {self.hitbox}, {self.default_texture}, {self.hover_texture}, {self.click_texture}'
