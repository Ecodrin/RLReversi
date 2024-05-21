import os
import pygame
import constants as const

from agent import TicTacToeAgent
from gui_elements import Button, StylizedText, ClickableCell, GroupObjectClass, NumberField
from typing import Callable, Any

from board import Board
from tictactoe import TicTacToeManager
from manager import Adversary


class HomePage:

    def __init__(self,  screen: pygame.display, title: str = const.TITLE, crosses_player: int = 0, zeros_player: int = 1) -> None:
        """
        :param screen: Экран для отображения игры.
        :param title: Имя вкладки с игрой.
        :param depth: Глубина анализа.
        :param crosses_player: Кто играет за крестики.
        :param zeros_player: Кто играет за нолики.
        :return:
        """
        self.crosses_player: int = crosses_player
        self.zeros_player: int = zeros_player
        self.running: int = True
        self.size = 0
        self.page: int = 0
        self.rendered_pages: list[Any] = []
        self.screen: pygame.display = screen
        self.objects_on_the_screen: list = []
        self.title: str = title

    def run(self) -> None:
        """
        Функция, отвечающая за визуализацию cтраниц игры.
        Разделена на 2 части - создание объектов, их рэндер и обработка действий.
        :return:
        """
        pygame.init()
        self.rendered_pages.append(self)
        self.page_create()
        pygame.display.set_caption(self.title)
        self.screen.fill(const.SCREEN_COLOR)

        while self.running:
            # Рэндер объектов в Зависимости от текущей страницы
            self.rendered_pages[self.page].processes()
            self.rendered_pages[self.page].render()
            pygame.display.flip()

# ------------------------CОЗДАНИЕ--------------------------------------------------
    # Создание всех страниц
    def page_create(self) -> None:
        """
        Функция создаёт гланую страницу и страницу с игрой 3 на 3
        :return:
        """
        self.create_home_page()
        self.create_game_page()

    def create_home_page(self) -> None:
        """
        Создаёт главную страницу с игрой
        :return:
        """
        self.objects_on_the_screen.append(
            pygame.image.load(const.START_IMAGE_PATH))
        self.create_generate_button()
        self.create_group_of_buttons()

    def create_game_page(self, size: int = 3, pieces_to_win: int = 3) -> None:
        """
        Создаёт страницу с игрой с необходимыми данными и добавляет её в массив созданных страниц
        :param size: Размер изначального поля
        :param pieces_to_win: Количество в ряд для победы
        :return:
        """
        classic_game_page = GamePage(
            self, size=size, pieces_to_win=pieces_to_win, crosses_player=self.crosses_player, zeros_player=self.zeros_player)
        self.rendered_pages.append(classic_game_page)

    def create_group_of_buttons(self) -> None:
        """
        Создание группы кнопок на начальной странице и добавление их в словарь со всеми объектами.
        :return:
        """
        buttons = []
        buttons.append(Button(self.open_game_page, hitbox=const.BUTTON_THREE_HITBOX,
                       inner_text=const.BUTTON_THREE_CONTENT, default_texture=const.BUTTON_DEFAULT_DEFAULT_TEXTURE, hover_texture=const.BUTTON_DEFAULT_HOVER_TEXTURE,
                       click_texture=const.BUTTON_DEFAULT_CLICK_TEXTURE, border_radius=const.BUTTON_BACK_BOARDER_RADIUS))
        buttons.append(Button(self.open_game_page, 4, 3, hitbox=const.BUTTON_FOUR_HITBOX,
                              inner_text=const.BUTTON_FOUR_CONTENT, default_texture=const.BUTTON_DEFAULT_DEFAULT_TEXTURE, hover_texture=const.BUTTON_DEFAULT_HOVER_TEXTURE,
                              click_texture=const.BUTTON_DEFAULT_CLICK_TEXTURE, border_radius=const.BUTTON_BACK_BOARDER_RADIUS))
        group_of_buttons = GroupObjectClass(
            buttons, const.START_GROUP_OF_BUTTONS_HITBOX, 'vertical', const.START_GROUP_OF_BUTTONS_MARGINS)
        self.objects_on_the_screen.append(group_of_buttons)

    def create_generate_button(self) -> None:
        """
        Создание кнопки и текстовых полей для генерации поля пользователем
        :return:
        """
        size_text = StylizedText(const.NUMBERFIELD_FOR_SIZE_HITBOX, const.NUMBERFIELD_FOR_SIZE_CONTENT,
                                 const.NUMBERFIELD_FOR_SIZE_COLOR, const.NUMBERFIELD_FOR_SIZE_FONT_FAMILY, const.NUMBERFIELD_FOR_SIZE_FONT_SIZE)
        win_text = StylizedText(const.NUMBERFIELD_FOR_WIN_HITBOX, const.NUMBERFIELD_FOR_WIN_CONTENT,
                                const.NUMBERFIELD_FOR_WIN_COLOR, const.NUMBERFIELD_FOR_WIN_FONT_FAMILY, const.NUMBERFIELD_FOR_WIN_FONT_SIZE)
        size_block = NumberField(const.SIZE_BLOCK_HITBOX, background_text=size_text,
                                 background_texture=const.SCREEN_COLOR)
        win_block = NumberField(const.WIN_BLOCK_HITBOX, background_text=win_text,
                                background_texture=const.SCREEN_COLOR)
        self.objects_on_the_screen.append(size_block)
        self.objects_on_the_screen.append(win_block)
        generative_button = Button(self.user_game, size_block, win_block, hitbox=const.BUTTON_GENERATE_HITBOX,
                                   inner_text=const.BUTTON_GENERATE_CONTENT, default_texture=const.BUTTON_GENERATE_DEFAULT_TEXTURE,
                                   hover_texture=const.BUTTON_GENERATE_HOVER_TEXTURE, click_texture=const.BUTTON_GENERATE_CLICK_TEXTURE, border_radius=const.BUTTON_GENERATE_BOARDER_RADIUS)
        self.objects_on_the_screen.append(generative_button)

# ------------------------РЭНДЕР-----------------------------------------------------
    def render(self) -> None:
        """
        Oтображение главной страницы.
        :return: None
        """
        for object in self.objects_on_the_screen:
            if isinstance(object, pygame.Surface):
                self.screen.blit(
                    object, const.START_IMAGE_COORDS)
            else:
                object.render(self.screen)

# ---------------------------------ОБРАБОТКА ДЕЙСТВИЙ-------------------------------------------
    def processes(self) -> None:
        """
        Обработка действий пользователя.
        :return:
        """
        for event in pygame.event.get():
            for object in self.objects_on_the_screen:
                if not (isinstance(object, pygame.Surface)):
                    object.hover_click(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                self.running = False

    def open_game_page(self, size: int = 3, pieces_to_win: int = 3) -> None:
        """
        Проверяет Создана ли страница с такими параметрами. Если создана, то открывает ёё, иначе создаёт
        :param size: Размер поля
        :param pieces_to_win: Колличество ячеек в ряд для победы
        :return:
        """
        self.screen.fill(const.SCREEN_COLOR)
        index_of_page = -1
        for page in self.rendered_pages:
            index_of_page += 1
            if page.size == size and page.pieces_to_win == pieces_to_win:
                self.page = index_of_page
                if self.crosses_player == 1 and self.zeros_player == 0:
                    self.rendered_pages[index_of_page].make_move(
                        crosses_player=1, zeros_player=0)
                break
        else:
            self.create_game_page(size, pieces_to_win)
            if self.crosses_player == 1 and self.zeros_player == 0:
                self.rendered_pages[-1].make_move(
                    crosses_player=1, zeros_player=0)
            self.page = -1

    def user_game(self, size_field: NumberField, win_field: NumberField) -> None:
        """
        Проверяет корректные ли данные введены Пользователем. Если верные, то открывает необходимую страницу
        :param size_field: объект, отвечающий за ввод размеров поля
        :param win_field: объект, отвечающий за ввод колличества клеток для победы
        :return:
        """
        if size_field.is_text_correct and win_field.is_text_correct and int(win_field.text.content) <= int(size_field.text.content):
            self.open_game_page(size=int(size_field.text.content),
                                pieces_to_win=int(win_field.text.content))

    def __str__(self) -> str:
        return f'HomePage with: screen {self.screen} and title {self.title}'

    def __repr__(self) -> str:
        return f'HomePage(screen={self.screen}, title={self.title}, crosses_player={self.crosses_player}, zeros_player={self.zeros_player})'


class GamePage():

    def __init__(self, home_page: HomePage, size: int = 3, pieces_to_win: int = 0, crosses_player: int = 0, zeros_player: int = 1) -> None:
        """
        Класс создаёт игровую страницу по введенным данным.
        :param home_page: ссылка на главную страницу
        :param size: размер доски
        :param pieces_to_win: Колличество клеток в ряд для победы
        :param crosses_player: Кто играет за крестиков
        :param zeros_player: Кто играет за ноликов
        """
        self.crosses_player: int = crosses_player
        self.zeros_player: int = zeros_player
        self.zero_texture: os.PathLike = const.ZEROS_TEXTURE
        self.cross_texture: os.PathLike = const.CROSSES_TEXTURE
        self.moves: list[int] = []
        self.size: int = size
        if pieces_to_win == 0:
            self.pieces_to_win: int = self.size
        else:
            self.pieces_to_win: int = pieces_to_win
        logic_board: Board = Board(size)
        self.logic: TicTacToeManager = TicTacToeManager(
            logic_board, self.pieces_to_win)
        # Временно функцию нейронки выполняет Adwersary
        self.computer: Adversary = Adversary(self.logic)
        # self.agent = TicTacToeAgent.load('agent10_1.5m_d3')
        self.visual_board: list[Button] = []
        self.home_page: HomePage = home_page
        self.objects_on_the_screen: dict = {}
        self.create_game_page()

# ------------------------ СОЗДАНИЕ СТРАНИЦЫ С ИГРОЙ ---------------------------------
    def create_game_page(self) -> None:
        """
        Создаёт все объекты на игровой странице
        """
        self.create_visual_board()
        self.create_sticks()
        self.create_buttons()

    def create_buttons(self) -> None:
        """
        Создаёт кнопки для рестарта игры, взятия хода назад, и возвращения на главную страницу
        :return:
        """
        buttons = []
        buttons.append(Button(self.open_home_page, hitbox=const.BUTTON_BACK_HITBOX, inner_text=const.BUTTON_BACK_CONTENT, default_texture=const.BUTTON_BACK_DEFAULT_TEXTURE,
                       hover_texture=const.BUTTON_BACK_HOVER_TEXTURE, click_texture=const.BUTTON_BACK_CLICK_TEXTURE, border_radius=const.BUTTON_BACK_BOARDER_RADIUS))
        buttons.append(Button(self.restart_game, hitbox=const.BUTTON_RESET_HITBOX, inner_text=const.BUTTON_RESET_CONTENT, default_texture=const.BUTTON_RESET_DEFAULT_TEXTURE,
                              hover_texture=const.BUTTON_RESET_HOVER_TEXTURE, click_texture=const.BUTTON_RESET_CLICK_TEXTURE, border_radius=const.BUTTON_RESET_BOARDER_RADIUS))
        buttons.append(Button(self.move_back, hitbox=const.BUTTON_UNDO_HITBOX,
                              inner_text=const.BUTTON_UNDO_CONTENT, default_texture=const.BUTTON_UNDO_DEFAULT_TEXTURE,
                              hover_texture=const.BUTTON_UNDO_HOVER_TEXTURE, click_texture=const.BUTTON_UNDO_CLICK_TEXTURE, border_radius=const.BUTTON_BACK_BOARDER_RADIUS))
        group_of_buttons = GroupObjectClass(
            buttons, const.GAME_GROUP_OF_BUTTONS_HITBOX, 'horizontal', const.GAME_GROUP_OF_BUTTONS_MARGINS)
        self.objects_on_the_screen['groupOfButtons'] = group_of_buttons

    def create_visual_board(self) -> None:
        """
        Создаёт игровое поле нужных размеров
        :return:
        """
        n_sticks = self.size - 1
        # Числа предназначены для конкретного расположения по центру поля 
        # 710 - размер поля 710 на 710 пикселей, размер палочки - 10 пикселей + отступы слева и справа от палочек итого 20
        # 10 - отступы по 5 пикселей слева и справа
        size_of_cell = (710 - n_sticks * 20 - 10) // self.size
        for y in range(self.size):
            for x in range(self.size):
                crosses = self.crosses_player
                zeros = self.zeros_player
                number_of_button = self.size * y + x
                # 90 - отступ слева 10 - размер палочки + 5 пикселей отступы между клеткой и панками = 10 + 5 * 2 = 20
                # 25 - отступ сверху
                hitbox = pygame.Rect(90 + x * (20 + size_of_cell), 25 + y * (20 + size_of_cell), size_of_cell, size_of_cell)
                if self.crosses_player == self.zeros_player == 1:                           
                    board_cell = ClickableCell(hitbox, self.print_number, default_texture=pygame.color.Color(  
                        const.SCREEN_COLOR), hover_texture=const.SCREEN_COLOR)
                    self.objects_on_the_screen[number_of_button] = board_cell
                else:
                    board_cell = ClickableCell(hitbox, self.make_move, number_of_button, crosses, zeros, default_texture=pygame.color.Color(
                        const.SCREEN_COLOR), hover_texture=const.SCREEN_COLOR)
                    self.objects_on_the_screen[number_of_button] = board_cell
                self.visual_board.append(
                    self.objects_on_the_screen[number_of_button])

    def create_sticks(self) -> None:
        """
        Создаёт решетку поля.
        :return:
        """
        n_sticks = self.size - 1
        # числа нужны для корректной отцентровки
        # 710 - размер всего поля - 20 отступы между палками и клетками, суммарные отступы по краям
        size_of_cell = (710 - n_sticks * 20 - 10) // self.size
        # 85 - отступ слева 10 * i отступ в зависимости от колличества клеток слева, 10 * (i - 1) - отступ в зависимости от кол-ва палок слева
        # 20 координата по y, 10 - нирина палки, 710 - высота палка
        for i in range(1, self.size):
            coords_vertical = (85 + size_of_cell * i + 10 * i + 10 * (i - 1), 20, 10, 710)
            self.objects_on_the_screen[f'vert{i}'] = pygame.Rect(coords_vertical)
            # 85 - отступ слева, 10 * i отступ в зависимости от колличества клеток сыерху, 10 * (i - 1) - отступ в зависимости от кол-ва палок сверху
            coords_horizontal = (85, 20 + size_of_cell * i + 10 * i + 10 * (i - 1), 710, 10)
            self.objects_on_the_screen[f'hor{i}'] = pygame.Rect(coords_horizontal)

# -------------------------- Рэндер страницы с классической игрой -----------------
    def render(self) -> None:
        """
        Отображение объектов на странице.
        :return:
        """
        for object in self.objects_on_the_screen.values():
            if isinstance(object, pygame.Rect):
                pygame.draw.rect(self.home_page.screen,
                                 const.INNER_BOARDERS_COLOR, object)
            else:
                object.render(self.home_page.screen)

# -------------------- ТРИГЕР ДЕЙСТВИЙ НА СТРАНИЦЕ--------------------------
    def processes(self) -> None:
        """
        Обработка действий  над объектами на странице
        :return:
        """
        if self.crosses_player == 1 == self.zeros_player and self.is_game_continue():
            self.make_move()
        for event in pygame.event.get():
            for object in self.objects_on_the_screen.values():
                if not isinstance(object, pygame.Rect):
                    object.hover_click(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                self.home_page.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                self.home_page.running = False

# ----------------------- РАБОТА С ДЕЙСТВИЯМИ НА СТРАНИЦЕ ----------------------
    def is_move_available(self, number: int) -> bool:
        """
        Проверка на возможность хода в клетку
        :param number: номер клетки
        """
        if len(self.moves) == 0:
            return True
        if self.is_game_continue():
            return number in self.logic.find_legal_moves()
        return False

    def zeros_move(self, number: int) -> None:
        """
        Делает ход ноликов в нужную клетку, если это возможно.
        :param number: номер клетки
        :return:
        """
        if self.is_move_available(number):
            self.logic.make_move(number)
            self.moves.append(number)
            self.visual_board[number].default_texture = self.zero_texture
            self.visual_board[number].hover_texture = self.zero_texture
            self.visual_board[number].click_texture = self.zero_texture
            self.visual_board[number].onClick = self.print_number

    def move_back(self) -> None:
        """
        Делает ход назад, если это возможно.
        :return:
        """
        if (len(self.moves) > 0 and not (self.crosses_player == 1 and self.zeros_player == 0)) or self.crosses_player == 1 and self.zeros_player == 0 and len(self.moves) > 1:
            last_move = self.moves[-1]
            self.logic.unmake_move(last_move)
            last_cell = self.visual_board[last_move]
            last_cell.default_texture = const.SCREEN_COLOR
            last_cell.hover_texture = const.SCREEN_COLOR
            last_cell.onClick = self.make_move
            self.moves.remove(last_move)

    def is_game_continue(self) -> bool:
        """
        Проверяет продолжается игра или завершен.
        :return: bool
        """
        winner = self.logic.check_win()
        if winner is None:
            return True
        else:
            # text = ['Ничья', 'Крестики', 'Нолики'] Для будущего
            return False

    def make_move(self, number: int = -1, crosses_player: int = 1, zeros_player=1) -> None:
        """
        Делает ход в нужную клетку. Также в случае если игра закончилась, не дает возможности делать ходы
        :return:
        """
        if not self.is_game_continue():  # Если игра закончилась, то ход делать не надо
            for сell in self.visual_board:
                сell.onClick = self.print_number
        elif len(self.moves) % 2:  # Если ход ноликов
            match zeros_player:  # Определение того, кто играет за ноликов
                case 0:
                    self.zeros_move(number)
                case 1:
                    computers_turn = self.computer.search_root(const.DEPTH)
                    self.zeros_move(computers_turn)
                case 2:
                    computers_turn = self.agent.predict(
                        self.logic.board.get_uid(), self.logic.find_legal_moves())[1]
                    self.zeros_move(computers_turn)
            if crosses_player == 1:  # если противник компъютер, то вызываем его ход
                self.make_move(crosses_player=crosses_player,
                               zeros_player=zeros_player)
        else:  # Если ход крестиков
            match crosses_player:
                case 0:
                    self.crosses_move(number)
                case 1:
                    computers_turn = self.computer.search_root(const.DEPTH)
                    self.crosses_move(computers_turn)
                case 2:
                    computers_turn = self.agent.predict(
                        self.logic.board.get_uid(), self.logic.find_legal_moves())[1]
                    self.zeros_move(computers_turn)
            if zeros_player == 1:  # если противник компъютер, то вызываем его ход
                self.make_move(crosses_player=crosses_player,
                               zeros_player=zeros_player)

    def crosses_move(self, number: int) -> None:
        """
        Делает ход крестиков в нужную клетку, если это возможно.
        :param number: номер клетки
        :return:
        """
        if self.is_move_available(number):
            self.logic.make_move(number)
            self.moves.append(number)
            self.visual_board[number].default_texture = self.cross_texture
            self.visual_board[number].hover_texture = self.cross_texture
            self.visual_board[number].click_texture = self.cross_texture
            self.visual_board[number].onClick = self.print_number

    def restart_game(self) -> None:
        """
        Перезапускает игру.
        :return:
        """
        self.logic.reset_board()
        for сell in self.visual_board:
            сell.click_texture = const.SCREEN_COLOR
            сell.default_texture = const.SCREEN_COLOR
            сell.hover_texture = const.SCREEN_COLOR
            сell.onClick = self.make_move
        self.moves = []
        if self.crosses_player == 1 and self.zeros_player == 0:
            self.make_move(crosses_player=1, zeros_player=0)

    def open_home_page(self) -> None:
        """
        Открывает главную страницу.
        :return:
        """
        self.logic.reset_board()
        for сell in self.visual_board:
            сell.click_texture = const.SCREEN_COLOR
            сell.default_texture = const.SCREEN_COLOR
            сell.hover_texture = const.SCREEN_COLOR
            сell.onClick = self.make_move
        self.moves = []
        self.render()
        self.home_page.screen.fill(const.SCREEN_COLOR)
        self.home_page.page = 0

    def print_number(self, *args) -> None:
        """
        Функция, без действий, бедет применяться при обучении.
        :return:
        """
        print(args[0])

    def __str__(self) -> str:
        return f'GamePage with size {self.size}, pieces_to_win {self.pieces_to_win}, crosses_player {self.crosses_player} and zeros_player {self.zeros_player}'

    def __repr__(self) -> str:
        return f'GamePage(home_page={self.home_page}, size={self.size}, pieces_to_win={self.pieces_to_win}, crosses_player={self.crosses_player}, zeros_palyer={self.zeros_player})'


def main():
    start = HomePage(pygame.display.set_mode((880, 880)),
                     crosses_player=0, zeros_player=1)
    start.run()


if __name__ == '__main__':
    main()
