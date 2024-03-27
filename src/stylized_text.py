import pygame


class StylizedText:
    def __init__(self, content: str = 'Hello world', position: pygame.Rect = (), text_colour: pygame.color = (0, 0, 0),
                 font_family: str = 'Arial', font_size: int = 24, font_style: int = 0) -> None:
        """
        :param content: Содержимое текста
        :param position: Позиция текст
        :param text_colour: Цвет текста
        :param font_family: Шрифт текста
        :param font_size: Размер текста
        :param font_style: Стиль текста
        :return:
        """

        self.content = content
        self.position = position
        self.text_colour = text_colour
        self.font_family = font_family
        self.font_size = font_size
        self.font_style = font_style

    def __styles_determinate(self):
        mask = self.font_style & 0b11
        match mask:
            case 0:
                return False, False
            case 1:
                return True, False
            case 2:
                return False, True
            case 3:
                return True, True

    def render(self, screen: pygame.display) -> None:
        """
        Отображает текст с заданным стилем и позицией
        :param screen: разрешение экрана
        """
        bold, italic = self.__styles_determinate()
        font = pygame.font.SysFont(self.font_family, self.font_size, bold=bold, italic=italic)
        text_surface = font.render(self.content, True, self.text_colour)
        screen.blit(text_surface, self.position)

    def __repr__(self):
        return (f'StylizedText({self.content}, {self.position} ,{self.text_colour}, '
                f'{self.font_family}, {self.font_size}, {self.font_style})')

    def __str__(self):
        return f'("{self.content}", {self.font_size}, {self.text_colour})'
