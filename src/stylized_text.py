import pygame


class StylizedText:
    def __init__(self, content: str = '', position: pygame.Rect = (), text_colour: pygame.color = (0, 0, 0),
                 font_family: str = 'Arial', font_size: int = 24, font_style: int = 0) -> None:
        """
        :param content: Содержимое текста
        :param position: Позиция текст
        :param text_colour: Цвет текста
        :param font_family: Шрифт текста
        :param font_size: Размер текста
        :param font_style: Стиль текста. Задаётся битовой маской: 1 - жирный 10 - курсив.
        :return:
        """

        self.content = content
        self.position = position
        self.text_colour = text_colour
        self.font_family = font_family
        self.font_size = font_size
        self.font_style = font_style

    def __is_cursive(self) -> int:
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
        Отображает текст с заданным стилем и позицией
        :param screen: Разрешение выводимого окна.
        """
        bold, italic = self.__is_bold(), self.__is_cursive()
        font = pygame.font.SysFont(self.font_family, self.font_size, bold=bold, italic=italic)
        text_surface = font.render(self.content, True, self.text_colour)
        screen.blit(text_surface, self.position)

    def __repr__(self):
        return (f'StylizedText({self.content}, {self.position} ,{self.text_colour}, '
                f'{self.font_family}, {self.font_size}, {self.font_style})')

    def __str__(self):
        return f'("{self.content}", {self.font_size}, {self.text_colour})'
