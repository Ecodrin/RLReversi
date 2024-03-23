import pygame


class StylizedText:
    def __int__(self, content: str = 'Hello world', TextColour: tuple = (0, 0, 0),
                FontFamily: pygame.font.Font = None, FontSize: int = 24, FontStyle: str = '') -> None:
        """

        :param content: Содержимое текста
        :param TextColour: Цвет текста
        :param FontFamily: Шрифт текста
        :param FontSize: Размер текста
        :param FontStyle: Стиль текста
        :return:
        """

        self.content = content
        self.TextColour = TextColour
        self.FontFamily = FontFamily
        self.FontSize = FontSize
        self.FontStyle = FontStyle

    def __repr__(self):
        return f'StylizedText({self.content}, {self.TextColour}, {self.FontFamily}, {self.FontSize}, {self.FontStyle})'

    def __str__(self):
        return f'("{self.content}", {self.FontSize}, {self.TextColour})'
