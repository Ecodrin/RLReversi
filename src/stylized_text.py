import pygame


class StylizedText:
    def __init__(self, content: str = 'Hello world', Rect: pygame.Rect = (), TextColour: tuple = (0, 0, 0),
                 FontFamily: str = 'Arial', FontSize: int = 24, FontStyle: int = 0) -> None:
        """
        :param content: Содержимое текста
        :param Rect: Позиция кнопки
        :param TextColour: Цвет текста
        :param FontFamily: Шрифт текста
        :param FontSize: Размер текста
        :param FontStyle: Стиль текста
        :return:
        """

        self.content = content
        self.Rect = Rect
        self.TextColour = TextColour
        self.FontFamily = FontFamily
        self.FontSize = FontSize
        self.FontStyle = FontStyle

    def __Is_bold(self):
        """
        :return: Будет ли шрифт жирным
        """
        return self.FontSize % 10

    def __Is_italic(self):
        """
        :return: Будет ли шрифт курсивным
        """
        return self.FontSize / 10 % 10

    def render(self, screen) -> None:
        """
        Отображает текст с заданным стилем и позицией
        :param screen: разрешение экрана
        """
        bold = self.__Is_bold()
        italic = self.__Is_italic()
        font = pygame.font.SysFont(self.FontFamily, self.FontSize, bold=bold, italic=italic)
        text_surface = font.render(self.content, True, self.TextColour)
        screen.blit(text_surface, self.Rect)

    def __repr__(self):
        return (f'StylizedText({self.content}, {self.Rect} ,{self.TextColour}, '
                f'{self.FontFamily}, {self.FontSize}, {self.FontStyle})')

    def __str__(self):
        return f'("{self.content}", {self.FontSize}, {self.TextColour})'
