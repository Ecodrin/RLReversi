import os

import pygame

from typing import Callable, Any

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
        :param font_style: Стиль текста. Задаётся битовой маской: 0b001 - жирный, 0b010 - курсив, 0b100 - подчёркивание.
        :return:
        """
        self._position: pygame.Rect = position
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
        if not isinstance(text, str):
            raise TypeError('Content must be a string type')

        self._content = text
        self.__text = self.__create_text()

    @property
    def position(self) -> pygame.Rect:
        return self._position

    @position.setter
    def position(self, pos: pygame.Rect) -> None:
        if not isinstance(pos, pygame.Rect):
            raise TypeError('Pos must be a RectType')
        self._position = pos
        self.__text = self.__create_text()

    def __is_bold(self) -> int:
        """
        :return: Разряд отвечающий за жирность.
        """
        return self.font_style & 0b001

    def __is_italic(self) -> int:
        """
        :return: Разряд отвечающий за курсив.
        """
        return self.font_style & 0b010

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
                line = ''
                line_width = 0

            line += word + ' '
            line_width += word_width

        lines.append(line)

        # Вычисление начального смещения по y для центрирования текста по вертикали.
        y_offset = self.position[1] + (self.position[3] - len(lines) * self.font_size) // 2
        surfaces = []
        for text_line in lines:
            # requires antialiasing: bool
            text_surface = font.render(text_line, True, self.text_colour)
            # Вычисление центра текстуры.
            center = (self.position[0] + self.position[2] // 2, y_offset + font.size(text_line)[1] // 2)
            text_rect = text_surface.get_rect(center=center)
            surfaces.append((text_surface, text_rect))
            # Обновление смещения по y для следующей строки текста.
            y_offset += self.font_size

        return surfaces

    def render(self, screen: pygame.display) -> None:
        """
        Отображает текст с заданным стилем и позицией.
        :param screen: Объект дисплея для обновления содержимого.
        """
        for surface, position in self.__text:
            screen.blit(surface, position)

    def __repr__(self) -> str:
        return (f'StylizedText("{self._content}", {self.position}, {self.text_colour}, '
                f'"{self.font_family}", {self.font_size}, {self.font_style})')

    def __str__(self) -> str:
        return f'"Text {self._content}, Size {self.font_size}, Colour {self.text_colour}'


class Button(Clickable):

    def __init__(self, onClick: Callable, *args,
                 hitbox: pygame.Rect, inner_text: StylizedText,
                 default_texture: pygame.color.Color | os.PathLike = pygame.color.Color(255, 255, 255),
                 hover_texture: pygame.color.Color | os.PathLike = pygame.color.Color(160, 160, 160),
                 click_texture: pygame.color.Color | os.PathLike = pygame.color.Color(64, 64, 64),
                 border_radius: int = 0) -> None:

        """
        :param onClick (callback function):
        :param *args (arguments for callback function):
        :param hitbox (rectangular):
        :param inner_text: Текст на кнопке.
        :param default_texture: Стандартная текстура кнопки.
        :param hover_texture: Текстура при наведении курсора.
        :param click_texture: Текстура при клике.
        :param border_radius: Радиус округления.
        """

        super().__init__(hitbox, onClick, *args)
        self.inner_text: StylizedText = inner_text
        self.default_texture: pygame.color.Color | os.PathLike = default_texture
        self.hover_texture: pygame.color.Color | os.PathLike = hover_texture
        self.click_texture: pygame.color.Color | os.PathLike = click_texture
        self.button_texture: pygame.color.Color | os.PathLike = self.default_texture
        self.border_radius: int = border_radius
        self._image_cache: pygame.SurfaceType = pygame.Surface((800, 600))

    def hover_click(self, event: pygame.event) -> None:
        """
        Красит кнопку в нужный цвет.
        :param event: Действия пользователя
        """
        collide = super().check_collision()
        # Проверка на коллизию мышки с кнопкой.
        if collide:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.button_texture = self.click_texture
            else:
                self.button_texture = self.hover_texture

        else:
            self.button_texture = self.default_texture

    def render(self, screen: pygame.surface) -> None:
        """
        Выводит кнопку на экран.
        :param screen: Объект дисплея для обновления содержимого.
        """
        if isinstance(self.button_texture, pygame.color.Color):
            pygame.draw.rect(screen, self.button_texture, self.hitbox, width=0,
                             border_radius=self.border_radius)
        elif isinstance(self.button_texture, os.PathLike):
            # Кэшировние изображений, которые уже были зарендерены.
            if self.button_texture != pygame.SurfaceType:
                img = pygame.image.load(self.button_texture).convert_alpha()
                if img.get_size() != (self.hitbox[2], self.hitbox[3]):
                    img = pygame.transform.smoothscale(img, (self.hitbox[2], self.hitbox[3]))
                self._image_cache = img
            else:
                img = self._image_cache

            screen.blit(img, self.hitbox)
        else:
            raise TypeError('Invalid texture type')

        self.inner_text.render(screen)

    def __setattr__(self, key, value):
        if key == 'hitbox' and isinstance(value, pygame.Rect) and self._image_cache:
            self.inner_text.position = center_relative_to(self.inner_text.position, value)
        else:
            object.__setattr__(self, key, value)

    def __getattr__(self, item):
        if item in object.__dict__.keys():
            return object.__getattribute__(self, item)
        return None

    def __repr__(self):
        return f"Button(hitbox={self.hitbox}, inner_text={self.inner_text}, " \
               f"default_texture={self.default_texture}, hover_texture={self.hover_texture}, " \
               f"click_texture={self.click_texture}, border_radius={self.border_radius})"

    def __str__(self):
        return f"Button with text '{self.inner_text}' and hitbox {self.hitbox}"


class GroupObjectClass:
    def __init__(self, content: list[Any] | tuple[Any],
                 position: pygame.Rect,
                 direction: str = 'horizontal',
                 margin: tuple[int, int] | list[int, int] = (0, 0)) -> None:
        """
        Класс для отрисовки группы объектов в ряд с заданными отступами.
        :param content: Объекты
        :param position: Позиция блока
        :param direction: vertical/horizontal
        :param margin: Количество пикселей между объектами
        """
        self.__content: list[Any] | tuple[Any] = content
        self.__position: pygame.Rect = position
        self.__direction: str = direction
        self.__margin: tuple[int, int] | list[int, int] = margin
        self.__count_draw_object: int = 0
        self.__create_block()

    @property
    def count_draw_object(self) -> int:
        return self.__count_draw_object

    @property
    def margin(self):
        return self.__margin

    @margin.setter
    def margin(self, value):
        if not isinstance(value, tuple | list):
            raise TypeError('Не тот тип данных')
        self.__margin = value
        self.__create_block()

    @property
    def direction(self):
        return self.__direction

    @direction.setter
    def direction(self, value):
        if not isinstance(value, str):
            raise TypeError('Не тот тип данных')
        self.__direction = value
        self.__create_block()

    def insert(self, pos: int, obj: Any) -> None:
        """
        Вставка объекта в блок
        :param pos: его позиция в блоке
        :param obj: объект
        :return: None
        """
        self.__content.insert(pos, obj)
        self.__create_block()

    def append(self, obj) -> None:
        """
        Append object to the list
        :param obj:
        :return:
        """
        self.__content.append(obj)
        self.__create_block()

    def pop(self, pos: int) -> object:
        """
        Удаление объекта из
        :param pos: index
        :return: object
        """
        obj = self.__content.pop(pos)
        self.__create_block()
        return obj

    def __create_block(self) -> None:
        match self.__direction:
            case 'horizontal':
                margin_amendment = self.__position[0] + self.__position[0]
                # if horizontally
                axis = 'vertical'
                amendment = 0
            case 'vertical':
                margin_amendment = self.__position[1] + self.__margin[1]
                # if vertically
                axis = 'horizontal'
                amendment = 1
            case _:
                raise ValueError("Неверное направление блока")
        self.__count_draw_object = 0
        for obj in self.__content:
            # двигаем подвижную координату
            obj.hitbox[amendment] = margin_amendment
            # Центрируем по заданной оси
            obj.hitbox = center_relative_to(element=obj.hitbox, relative_to=self.__position, mode=axis)
            # проверяем, вышло ли за стенку
            if (obj.hitbox[amendment] + obj.hitbox[amendment + 2] > self.__position[amendment] +
                    self.__position[amendment + 2] + self.__margin[amendment]):
                break
            self.__count_draw_object += 1
            # увеличиваем приращение
            margin_amendment += self.__margin[amendment] + obj.hitbox[amendment + 2]

    def hover_click(self, event: pygame.event.Event) -> None:
        """
        Hover click event
        :param event: event
        :return: None
        """
        for ind, obj in enumerate(self.__content, 0):
            if ind >= self.__count_draw_object:
                break
            obj.hover_click(event)

    def render(self, screen: pygame.Surface) -> None:
        """
        Отрисовка всех объектов
        :param Дисплей
        :return:None
        """
        i = 0
        for obj in self.__content:
            if i >= self.__count_draw_object:
                break
            obj.render(screen)
            i += 1

    def __repr__(self) -> str:
        return (f'GroupObjectClass: {list(map(lambda x: repr(x), self.__content))}\n'
                f'position: {self.__position}\ndirection: {self.__direction}\nmargins: {self.__margin}\n')

    def __str__(self) -> str:
        return f'GroupObjectClass: objects: \n{list(self.__content)}\n position{self.__position}'


from gui_utility import center_relative_to
from pygame.locals import Color, Rect
import time

pygame.init()
screen = pygame.display.set_mode((1000, 700))
clock = pygame.time.Clock()

text_content = "Hello, Ivan Iva"
text_position = Rect(100, 100, 200, 200)
text_colour = pygame.color.Color(0, 0, 0)
font_family = "arial"
font_size = 24
font_style = 0
borders = text_position
stylized_text = StylizedText(
    content=text_content,
    position=text_position,
    text_colour=text_colour,
    font_family=font_family,
    font_size=font_size,
    font_style=font_style,
)

button1 = Button(onClick=lambda x: x + 1, hitbox=borders,
                 inner_text=stylized_text,
                 default_texture=pygame.color.Color(255, 0, 0),
                 hover_texture=pygame.color.Color(0, 255, 0),
                 click_texture=pygame.color.Color(0, 0, 255))


text_content = "Hello, ZEk ZEk asddfsadasdasad"
text_position = Rect(400, 400, 200, 200)
text_colour = pygame.color.Color(0, 0, 0)
font_family = "arial"
font_size = 24
font_style = 0
borders = text_position
stylized_text = StylizedText(
    content=text_content,
    position=text_position,
    text_colour=text_colour,
    font_family=font_family,
    font_size=font_size,
    font_style=font_style,
)

button2 = Button(onClick=lambda x: x + 1, hitbox=borders,
                 inner_text=stylized_text,
                 default_texture=pygame.color.Color(255, 0, 0),
                 hover_texture=pygame.color.Color(0, 255, 0),
                 click_texture=pygame.color.Color(0, 0, 255), border_radius=20)


text_content = "Hello, Piddrtrrr"
text_position = Rect(400, 400, 200, 200)
text_colour = pygame.color.Color(0, 0, 0)
font_family = "arial"
font_size = 24
font_style = 0
borders = text_position
stylized_text = StylizedText(
    content=text_content,
    position=text_position,
    text_colour=text_colour,
    font_family=font_family,
    font_size=font_size,
    font_style=font_style,
)

button3 = Button(onClick=lambda x: x + 1, hitbox=borders,
                 inner_text=stylized_text,
                 default_texture=pygame.color.Color(255, 0, 0),
                 hover_texture=pygame.color.Color(0, 255, 0),
                 click_texture=pygame.color.Color(0, 0, 255))

screen.fill((255, 255, 255))
running = True

a = GroupObjectClass([button1, button2, button3], Rect(100, 100, 800, 500), direction="vertical", margin=(20, 20))
pygame.draw.rect(screen, (0, 0, 0), Rect(100, 100, 800, 500), 1)
while running:
    for event in pygame.event.get():
        a.hover_click(event)
        a.render(screen)
        #########
        pygame.display.flip()
        if event.type == pygame.QUIT:
            running = False

    pygame.time.Clock().tick()
pygame.quit()
