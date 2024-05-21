import os
import pygame
import constants as const

from typing import Callable, Any
from pygame.locals import Rect

from gui_utility import center_relative_to
from board import Clickable


class StylizedText:
    def __init__(self, position: pygame.Rect, content: str = '', text_colour: pygame.color.Color = const.WHITE,
                 font_family: str = const.BUTTON_DEFAULT_FONT_FAMILY, font_size: int = const.BUTTON_DEFAULT_FONT_SIZE, font_style: int = const.BUTTON_BACK_BOARDER_RADIUS) -> None:
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

    def __is_bold(self) -> bool:
        """
        :return: Разряд отвечающий за жирность.
        """
        return self.font_style & 0b001 > 0

    def __is_italic(self) -> bool:
        """
        :return: Разряд отвечающий за курсив.
        """
        return self.font_style & 0b010 > 0

    def __is_underline(self) -> bool:
        """
        :return: Разряд отвечающий за подчёркивание.
        """
        return self.font_style & 0b100 > 0

    def __create_font(self) -> pygame.font.Font:
        """
        Создаёт шрифт исходя из входных данных.
        :return Возвращает созданный шрифт.
        """
        bold = self.__is_bold()
        italic = self.__is_italic()
        underline = self.__is_underline()
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
        y_offset = self.position[1] + \
            (self.position[3] - len(lines) * self.font_size) // 2
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
                f'{self.font_family}', {self.font_size}, {self.font_style})

    def __str__(self) -> str:
        return f'Text "{self._content}", Size {self.font_size}, Colour {self.text_colour}'


class ClickableCell(Clickable):

    def __init__(self, hitbox: pygame.Rect, onClick: Callable[..., Any], *args,
                 default_texture: pygame.color.Color | os.PathLike = const.WHITE,
                 hover_texture: pygame.color.Color | os.PathLike = const.GREY) -> None:
        super().__init__(hitbox, onClick, *args)
        self.default_texture: pygame.color.Color | os.PathLike = default_texture
        self.hover_texture: pygame.color.Color | os.PathLike = hover_texture
        self.button_texture: pygame.color.Color | os.PathLike = self.default_texture
        self._image_cache: pygame.SurfaceType = pygame.Surface((800, 600))

    def hover_click(self, event: pygame.event) -> None:
        """
        Красит клетку в нужный цвет.
        :param event: Действия пользователя
        """
        collide = super().check_collision()
        # Проверка на коллизию мышки с кнопкой.
        if collide:
            if event.type == pygame.MOUSEBUTTONDOWN:
                super().process()
            else:
                self.button_texture = self.hover_texture

        else:
            self.button_texture = self.default_texture

    def render(self, screen: pygame.Surface) -> None:
        """
        Выводит кнопку на экран.
        :param screen: Объект дисплея для обновления содержимого.
        """
        if isinstance(self.button_texture, pygame.color.Color):
            pygame.draw.rect(screen, self.button_texture, self.hitbox, width=0)
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

    def __repr__(self):
        return f'ClickableCell(hitbox={self.hitbox},\n' \
            f'default_texture={self.default_texture}, hover_texture={self.hover_texture}'

    def __str__(self) -> str:
        return f'ClickableCell with hitbox: {self.hitbox}'


class Button(Clickable):

    def __init__(self, onClick: Callable, *args,
                 hitbox: pygame.Rect, inner_text: StylizedText | str,
                 default_texture: pygame.color.Color | os.PathLike = const.PURPLE,
                 hover_texture: pygame.color.Color | os.PathLike = const.LIGHT_BLUE,
                 click_texture: pygame.color.Color | os.PathLike = const.INDIGO,
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
        self.inner_text: StylizedText | str = inner_text
        if isinstance(inner_text, str):
            self.inner_text = StylizedText(position=hitbox, content=inner_text)
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
                super().process()
            else:
                self.button_texture = self.hover_texture

        else:
            self.button_texture = self.default_texture

    def render(self, screen: pygame.Surface) -> None:
        """
        Выводит кнопку на экран.
        :param screen: Объект дисплея для обновления содержимого.
        """
        if isinstance(self.button_texture, pygame.color.Color):
            pygame.draw.rect(screen, self.button_texture, self.hitbox, width=0, border_radius=self.border_radius)
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
        return f'Button(hitbox={self.hitbox}, inner_text={self.inner_text}, ' \
            f'default_texture={self.default_texture}, hover_texture={self.hover_texture}, ' \
            f'click_texture={self.click_texture}, border_radius={self.border_radius})'

    def __str__(self):
        return f'Button with text "{self.inner_text}" and hitbox {self.hitbox}'


class GroupObjectClass:
    def __init__(self, content: list[Any] | tuple[Any],
                 position: pygame.Rect,
                 direction: str = 'horizontal',
                 margins: tuple[int, int] | list[int, int] = (0, 0)) -> None:
        """
        Класс для отрисовки группы объектов в ряд с заданными отступами.
        :param content: Объекты
        :param position: Позиция блока
        :param direction: vertical/horizontal
        :param margins: Количество пикселей между объектами
        """
        self.content: list[Any] | tuple[Any] = content
        self.__position: pygame.Rect = position
        self.__direction: str = direction
        self.__margins: tuple[int, int] | list[int, int] = margins
        self.__count_draw_object: int = 0
        self.__create_block()

    @property
    def position(self) -> pygame.Rect:
        return self.__position

    @position.setter
    def position(self, position: pygame.Rect):
        if not isinstance(position, pygame.Rect):
            raise TypeError('Position must be pygame.Rect.')
        self.__position = position
        self.__create_block()

    @property
    def margins(self):
        return self.__margins

    @margins.setter
    def margins(self, value):
        if not isinstance(value, tuple | list):
            raise TypeError('Margins must be a list or tuple type.')
        self.__margins = value
        self.__create_block()

    @property
    def direction(self):
        return self.__direction

    @direction.setter
    def direction(self, value):
        if not isinstance(value, str):
            raise TypeError('Direction must be a string type.')
        self.__direction = value
        self.__create_block()

    def insert(self, index: int, item: Any) -> None:
        """
        Вставка объекта в блок.
        :param index: Позиция объекта в блоке
        :param item: Объект для вставки в блок.
        :return: None
        """
        self.content.insert(index, item)
        self.__create_block()

    def append(self, item) -> None:
        """
        Добавление объекта в блок.
        :param item: Объект для вставки в блок.
        :return:
        """
        self.content.append(item)
        self.__create_block()

    def pop(self, position: int) -> object:
        """
        Удаление объекта из блока.
        :param position: Индекс элементы.
        :return: объект.
        """
        item = self.content.pop(position)
        self.__create_block()
        return item

    def __create_block(self) -> None:
        """
        Создаем и фиксируем координаты объектов блока.
        Проходим каждый объект, располагаем его в блоке.
        Изменяются внутренние координаты объекта.
        :return:
        """
        match self.__direction:
            case 'horizontal':
                # Задаем начальный угол для координаты подвижной по Оси(то есть граница + заданное смещение).
                shift = self.__position[0] + self.__margins[0]
                axis = 'vertical'
                shift_index = 0
            case 'vertical':
                # Задаем начальный угол для координаты подвижной по Оси(то есть граница + заданное смещение).
                shift = self.__position[1] + self.__margins[1]
                axis = 'horizontal'
                shift_index = 1
            case _:
                raise ValueError('Direction must be horizontal or vertical.')
        self.__count_draw_object = 0
        for item in self.content:
            # Двигаем объект(из блока) по оси.
            item.hitbox[shift_index] = shift
            # Центрируем объект по противоположной оси.
            item.hitbox = center_relative_to(
                element=item.hitbox, relative_to=self.__position, mode=axis)
            # Проверяем, вышло ли за границу (длина объекта + координата его левого угла >= границы блока).
            # Чтобы получить длину Rect, надо к shift_index прибавить 2.
            if (item.hitbox[shift_index] + item.hitbox[shift_index + 2] >= self.__position[shift_index] +
                    self.__position[shift_index + 2] + self.__margins[shift_index]):
                break
            self.__count_draw_object += 1
            # Увеличиваем приращение. Двигаем левый угол для следующего блока(возможного) Ox: Длина + левый верхний.
            shift += self.__margins[shift_index] + item.hitbox[shift_index + 2]

    def hover_click(self, event: pygame.event.Event) -> None:
        """
        Функция перебирает все объекты и проверяет их состояние в pygame.event.Event. Если функция находит какое-либо
        совпадение, то вызывается внутреняя функция объекта.
        :param event: pygame.event (Bruh moment from dmitriy_senior_pomidorovich).
        :return: None
        """
        for index, item in enumerate(self.content):
            if index >= self.__count_draw_object:
                break
            item.hover_click(event)

    def render(self, screen: pygame.Surface) -> None:
        """
        Отрисовка всех объектов.
        :param screen: Дисплей.
        :return:None
        """
        for index, item in enumerate(self.content):
            if index >= self.__count_draw_object:
                break
            item.render(screen)

    def __repr__(self) -> str:
        return (f'GroupObjectClass: {list(map(lambda x: repr(x), self.content))}\n'
                f'position: {self.__position}\ndirection: {self.__direction}\nmargins: {self.__margins}\n')

    def __str__(self) -> str:
        return f'GroupObjectClass: objects: \n{list(self.content)}\n position{self.__position}'


class NumberField:

    def __init__(self, hitbox: pygame.Rect = const.NUMBERFIELD_FOR_SIZE_HITBOX, background_text: StylizedText | str = const.NUMBERFIELD_FOR_SIZE_CONTENT,
                 background_texture: pygame.color.Color | os.PathLike = const.PURPLE, max_value: int = 15):
        """
        Класс для блока с вводом цифр
        :param hitbox: хитбокс блока с текстом
        :param background_text: текст на блоке по умолчанию
        :param background_texture: задний фон
        :param max_value: максимальное значение, которое может быть в клетке
        """
        self.hitbox: pygame.Rect = hitbox
        self.background_texture: pygame.color.Color | os.PathLike = background_texture
        if isinstance(background_text, str):
            self.background_text: StylizedText = StylizedText(self.hitbox, background_text)
            self.text: StylizedText = StylizedText(self.hitbox, background_text)
        else:
            self.background_text: StylizedText = background_text
            self.text: StylizedText = StylizedText(self.hitbox, background_text.content, background_text.text_colour, background_text.font_family, background_text.font_size, background_text.font_style)
        self.max_value: int = max_value
        self._image_cache: pygame.SurfaceType = pygame.Surface((800, 600))
        self.is_text_correct: bool = False
        self.is_selected: bool = False

    def render(self, screen: pygame.Surface):
        """
        Отображает блок для ввода текста
        :param screen: дисплей для отображения
        """
        if isinstance(self.background_texture, pygame.color.Color):
            pygame.draw.rect(screen, self.background_texture, self.hitbox, width=0)
        elif isinstance(self.background_texture, os.PathLike):
            # Кэшировние изображений, которые уже были зарендерены.
            if self.background_texture != pygame.SurfaceType:
                img = pygame.image.load(self.background_texture).convert_alpha()
                if img.get_size() != (self.hitbox[2], self.hitbox[3]):
                    img = pygame.transform.smoothscale(img, (self.hitbox[2], self.hitbox[3]))
                self._image_cache = img
            else:
                img = self._image_cache

            self.screen.blit(img, self.hitbox)
        else:
            raise TypeError('Invalid texture type')
        self.text.render(screen)  # Белый цвет текста

    def hover_click(self, event):
        """
        Обработка действий над текстом
        """
        match event.type:
            case pygame.MOUSEBUTTONDOWN:
                # Если кликнули на блок, то помечаем это
                if self.hitbox.collidepoint(event.pos) and self.text.content == self.background_text.content:
                    self.is_selected = True
                    self.text.content = ''
                    self.is_text_correct = False
                elif self.hitbox.collidepoint(event.pos):
                    self.is_selected = True
                elif self.is_selected and self.text.content == '':
                    self.is_selected = False
                    self.text.content = self.background_text.content
                else:
                    self.is_selected = False
            case pygame.KEYDOWN:
                if self.is_selected and event.unicode.isdigit() and self.text.content != self.background_text.content:
                    if not self.is_text_correct and event.unicode:
                        self.text.content += event.unicode
                        self.is_text_correct = True
                    elif int(self.text.content + event.unicode) <= self.max_value:
                        self.text.content += event.unicode
                elif self.is_selected and event.key == pygame.K_BACKSPACE and self.text.content == '':
                    self.text.content = self.background_text.content
                    self.is_text_correct = False
                elif self.is_selected and event.key == pygame.K_BACKSPACE and not self.text.content == self.background_text.content:
                    self.text.content = self.text.content[:-1]

    def __str__(self) -> str:
        return f'NumberField with background_text "{self.background_text}" and hitbox {self.hitbox}'

    def __repr__(self) -> str:
        return f'NumberFieldClass: hitbox: {self.hitbox}\nbackground_text: {self.background_text}'
