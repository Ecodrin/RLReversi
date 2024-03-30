import pygame


class StylizedText:
    def __init__(self, content: str = '', position: pygame.Rect = (), text_colour: pygame.color = (0, 0, 0),
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
        self.text_colour: pygame.color = text_colour
        self.font_family: str = font_family
        self.font_size: int = font_size
        self.font_style: int = font_style

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
        Отображает текст с заданным стилем и позицией
        :param screen: Разрешение выводимого окна.
        """
        bold, italic = self.__is_bold(), self.__is_italic()
        font = pygame.font.Font(self.font_family, self.font_size)
        font.set_italic(italic == 2)
        font.set_bold(bold == 1)
        text_surface = font.render(self.content, True, self.text_colour)
        screen.blit(text_surface, self.position)

    def __repr__(self):
        return (f'StylizedText({self.content}, {self.position} ,{self.text_colour}, '
                f'{self.font_family}, {self.font_size}, {self.font_style})')

    def __str__(self):
        return f'("{self.content}", {self.font_size}, {self.text_colour})'




from pygame.locals import *
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
rect = pygame.Rect(300, 200, 200, 100)

text_content = "Hello, World!"
text_position = Rect(100, 100, 100, 100)
text_colour = (0, 0, 0)
font_family = "arial"
font_size = 36
font_style = 3

stylized_text = StylizedText(
    content=text_content,
    position=text_position,
    text_colour=text_colour,
    font_family=font_family,
    font_size=font_size,
    font_style=font_style
)

screen.fill((255, 255, 255))
running = True
stylized_text.render(screen)
pygame.display.flip()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.time.Clock().tick()

pygame.quit()
