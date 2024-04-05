import os
import pygame
from typing import Callable
from pygame.locals import Rect
from gui_utility import center_relative_to
from cell import Clickable


class StylizedText:
    def __init__(self, position: pygame.Rect, content: str = '',
                 text_colour: pygame.color.Color = pygame.color.Color(255, 255, 255),
                 font_family: str = 'arial', font_size: int = 24,
                 font_style: int = 0) -> None:
        """
        :param content: Содержимое.
        :param position: Позиция.
        :param text_colour: Цвет.
        :param font_family: Шрифт текста.
        :param font_size: Размер текста.
        :param font_style: Стиль текста. Задаётся битовой маской: 0b01 - жирный, 0b10 - курсив, 0b100 - подчёркивание.
        :return:
        """
        self.position: pygame.Rect = position
        self._content: str = content
        self.text_colour: pygame.color.Color = text_colour
        self.font_family: str = font_family
        self.font_size: int = font_size
        self.font_style: int = font_style
        self.__text: list[tuple[pygame.SurfaceType, pygame.Rect]] = self.__create_text()

    @property
    def content(self) -> str:
        return self._content

    @content.setter
    def content(self, text: str) -> None:
        if text is None:
            raise TypeError('content must be str')

        self._content = text
        self.__text = self.__create_text()

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

    def __is_underline(self) -> int:
        """
        :return: Разряд отвечающий за подчёркивание.
        """
        return self.font_style & 0b100

    def __create_font(self) -> pygame.font.Font:
        """
        Создаёт шрифт исходя из входных данных.
        :return Возвращает созданный шрифт.
        """
        bold, italic, underline = self.__is_bold(), self.__is_italic(), self.__is_underline()
        # Если шрифт есть в системных, то он создаётся специальной функцией.
        if self.font_family in pygame.font.get_fonts():
            font = pygame.font.SysFont(self.font_family, self.font_size)
        else:
            font = pygame.font.Font(self.font_family, self.font_size)

        font.set_bold(bold)
        font.set_italic(italic)
        font.set_underline(underline)

        return font

    def __create_text(self) -> list[tuple[pygame.SurfaceType, pygame.Rect]]:
        """
        Создаёт отцентрованный и поделенный на строки текст.
        :return: Список кортежей (контент, позиция).
        """
        words = self._content.split()
        lines = []
        line = ''
        line_width = 0
        font = self.__create_font()
        for word in words:
            word_width = font.size(word + ' ')[0]
            # Проверка на выход за границы позиции.
            if line_width + word_width >= self.position[2]:
                lines.append(line)
                line = word + ' '
                line_width = word_width

            line += word + ' '
            line_width += word_width

        lines.append(line)

        # Изначальное смещение по y.
        y_offset = self.position[1] + (self.position[3] - len(lines) * self.font_size) // 2
        surfaces = []
        for text_line in lines:
            text_surface = font.render(text_line, True, self.text_colour)
            center = (self.position[0] + self.position[2] // 2, y_offset + font.size(text_line)[1] // 2)
            text_rect = text_surface.get_rect(center=center)
            surfaces.append((text_surface, text_rect))
            y_offset += self.font_size

        return surfaces

    def render(self, screen: pygame.display) -> None:
        """
        Отображает текст с заданным стилем и позицией.
        :param screen: Объект дисплея для обновления содержимого.
        """
        for surface, position in self.__text:
            screen.blit(surface, position)

    def __repr__(self):
        return (f'StylizedText("{self._content}", {self.position} ,{self.text_colour}, '
                f'{self.font_family}, {self.font_size}, {self.font_style})')

    def __str__(self):
        return f'("{self._content}", {self.font_size}, {self.text_colour})'


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

    def render(self, screen) -> None:
        """
        Выводит кнопку на экран.
        :param screen: Объект дисплея для обновления содержимого.
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
        return (f'Button("Text{self.inner_text}", Hitbox{self.hitbox}, def_tex{self.default_texture},'
                f'hov_tex{self.hover_texture},'
                f'click_tex{self.click_texture}, func{self.onClick} args{self.args})')

    def __str__(self):
        return (f'("Text{self.inner_text}", Hitbox{self.hitbox}, def_tex{self.default_texture},'
                f'hov_tex{self.hover_texture}, click_tex{self.click_texture})')
