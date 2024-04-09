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
    def __init__(self, content: list[Any],
                 borders: pygame.Rect,
                 direction: str = 'horizontally',
                 margins: list[int, int] = (0, 0)) -> None:
        """
        Class for draw objects in the box
        :param content: List of objects(ex. button or text)
        :param borders: borders of block and its position
        :param direction: vertically/horizontally
        :param margins: margin: int  of pixels between elements.
        """
        self.__content: list[Any] = content
        self.__borders: pygame.Rect = borders
        self.__direction: str = direction
        self.__margins: list[int, int] = margins
        self.__count_draw_object: int = 0
        self.__create_block()

    @property
    def margins(self):
        return self.__margins

    @margins.setter
    def margins(self, value):
        if isinstance(value, list) == 0:
            raise TypeError('Не тот тип данных')
        self.__margins = value
        self.__create_block()

    @property
    def direction(self):
        return self.__direction

    @direction.setter
    def direction(self, value):
        if isinstance(value, str) == 0:
            raise TypeError('Не тот тип данных')
        self.__direction = value
        self.__create_block()

    @staticmethod
    def __update_block(func: Callable) -> Callable:
        """
        Decorator for updating block
        Decorator causes __create_block in the end every function.
        :param func: function to be decorated
        :return: Callable
        """
        def wrapper(self, *args, **kwargs) -> Any:
            res = func(self, *args, **kwargs)
            self.__create_block()
            return res
        return wrapper

    @__update_block
    def insert(self, pos: int, obj: Any) -> None:
        """
        Insert object at given position
        :param pos: index of object in the list
        :param obj: object to be inserted
        :return: None
        """
        self.__content.insert(pos, obj)

    @__update_block
    def append(self, obj) -> None:
        """
        Append object to the list
        :param obj:
        self.__create_block()
        :return:
        """
        self.__content.append(obj)

    @__update_block
    def pop(self, pos: int) -> object:
        """
        Pop object from the list
        :param pos: index
        :return: object
        """
        obj = self.__content.pop(pos)
        return obj

    def __create_block(self) -> None:
        if self.__direction == 'horizontally':
            margins_amendment = [self.__margins[0] + self.__borders[0], 0]
            # if horizontally
            amendment = 0
        else:
            margins_amendment = [0, self.__margins[1] + self.__borders[1]]
            # if vertically
            amendment = 1
        self.__count_draw_object = 0
        for obj in self.__content:
            # двигаем подвижную координаты
            obj.hitbox[amendment] = margins_amendment[amendment]
            # центруем по заданной оси
            obj.hitbox = center_relative_to(element=obj.hitbox, relative_to=self.__borders, mode=self.__direction)
            # проверяем, вышло ли за стенку
            if obj.hitbox[amendment] + obj.hitbox[amendment + 2] > self.__borders[amendment] + self.__borders[amendment + 2]\
                    + self.__margins[amendment]:
                break
            self.__count_draw_object += 1
            # увеличиваем приращение
            margins_amendment[amendment] += self.__margins[amendment] + obj.hitbox[amendment + 2]

    def hover_click(self, event: pygame.event.Event) -> None:
        """
        Hover click event for all objects in the box
        :param event: Event
        :return: None
        """
        i = 0
        for obj in self.__content:
            if i >= self.__count_draw_object:
                break
            obj.hover_click(event)
            i += 1

    def render(self, screen: pygame.Surface) -> None:
        """
        Draw all objects in the box
        :param screen:Object Display
        :return:None
        """
        i = 0
        for obj in self.__content:
            if i >= self.__count_draw_object:
                break
            obj.render(screen)
            i += 1

    def __str__(self) -> str:
        return f'GroupObjectClass: objects: \n{list(self.__content)}\n Borders{self.__borders}'

    def __repr__(self) -> str:
        return (f'GroupObjectClass: {list(map(lambda x: repr(x), self.__content))}\n'
                f'Borders: {self.__borders}\ndirection: {self.__direction}\nmargins: {self.__margins}\n')
