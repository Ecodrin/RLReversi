import pygame
import pathlib

from gui_elements import Button, StylizedText, ClicableCell, GroupObjectClass
from typing import Callable, Any

from board import Board
from tictactoe import TicTacToeManager
from manager import Adversary


class HomePage:

    def __init__(self,  screen: pygame.display, title: str = 'Tic-Tac-Toe', depth: int = 8, crosses_player: str = 'Игрок', zeros_player: str = "Комп") -> None:
        """
        :param screen: Экран для отображения игры.
        :param title: Имя вкладки с игрой.
        :param depth: Глубина анализа.
        :param crosses_player: Кто играет за крестики.
        :param zeros_player: Кто играет за нолики.
        """
        players = {'Игрок': 0, "Комп": 1, 'Нейронка': 2}
        self.crosses_player: int = players[crosses_player]
        self.zeros_player: int = players[zeros_player]
        self.depth: int = depth
        self.running: int = 1
        self.size = 0
        self.page: int = 1
        self.rendered_pages: list[Any] = []
        self.screen: pygame.display = screen
        self.objects_on_the_screen: dict = {}
        self.coordinates_of_images: dict = {}  # создали экран
        self.title: str = title

    def run(self) -> None:
        """
        Функция, отвечающая за визуализацию Страниц игры.
        Разделена на 2 части - создание объектов, их рэндер и обработка действий.
        """
        pygame.init()
        self.rendered_pages.append(self)
        self.page_create()
        pygame.display.set_caption(self.title)
        self.screen.fill((255, 255, 224))

        while self.running:
            # Рэндер объектов в Зависимости от текущей страницы
            self.page_processes()
            self.page_render()
            pygame.display.flip()

# ------------------------CОЗДАНИЕ--------------------------------------------------
    # Создание всех страниц
    def page_create(self) -> None:
        """
        Функция создаёт гланую страницу и страницу с игрой 3 на 3
        """
        self.create_home_page()
        self.create_game_page()

    # Создание главной страницы
    def create_home_page(self) -> None:
        self.create_image('start_image', 'Start Desk.png', (245, 15))
        self.create_group_of_buttons()
    # Создание главной страницы

    def create_game_page(self, size: int = 3, pieces_to_win: int = 3) -> None:
        classic_game_page = GamePage(
            self, size=size, pieces_to_win=pieces_to_win, crosses_player=self.crosses_player, zeros_player=self.zeros_player)
        self.rendered_pages.append(classic_game_page)

    # Создание объектов на главной странице
    def create_button(self, name_of_object: str, function_on_click: Callable, *args, hitbox: pygame.Rect = pygame.Rect((165, 300, 270, 60)),
                      inner_text: str = 'NO TEKST', text_colour: pygame.color.Color = pygame.color.Color(255, 255, 255), font_family: str = 'arial',
                      font_size: int = 24, font_style: int = 0, default_texture=pygame.color.Color((105, 103, 209)),
                      hover_texture=pygame.color.Color(103, 145, 209), click_texture=pygame.color.Color((103, 171, 209)), border_radius: int = 0) -> None:
        """
        :param function_on_click (callback function):
        :param args (arguments for callback function):
        :param hitbox (rectangular):
        :param inner_text: str = 'NO TEKST'
        :param text_colour: Цвет.
        :param font_family: Шрифт текста.
        :param font_size: Размер текста.
        :param font_style: Стиль текста. Задаётся битовой маской: 0b001 - жирный, 0b010 - курсив, 0b100 - подчёркивание.
        :param default_texture: Стандартная текстура кнопки.
        :param hover_texture: Текстура при наведении курсора.
        :param click_texture: Текстура при клике.
        :param border_radius: Радиус округления.
        """
        button_text = StylizedText(hitbox, inner_text, text_colour=text_colour,
                                   font_family=font_family, font_size=font_size, font_style=font_style)
        button = Button(function_on_click, *args, hitbox=hitbox, inner_text=button_text,
                        default_texture=default_texture, hover_texture=hover_texture,
                        click_texture=click_texture, border_radius=32)
        return button

    def create_group_of_buttons(self):
        buttons = []
        buttons.append(self.create_button("classic_game", self.open_game_page, hitbox=pygame.Rect((165, 400, 400, 90)),
                                          inner_text='3 × 3', default_texture=pygame.color.Color((105, 103, 209)),
                                          hover_texture=pygame.color.Color(103, 145, 209), click_texture=pygame.color.Color((103, 171, 209)), border_radius=32))
        buttons.append(self.create_button("four_game", self.open_game_page, 4, 3, hitbox=pygame.Rect((165, 380, 400, 90)),
                                          inner_text='4 × 4', default_texture=pygame.color.Color((105, 103, 209)),
                                          hover_texture=pygame.color.Color(103, 145, 209), click_texture=pygame.color.Color((103, 171, 209)), border_radius=32))
        buttons.append(self.create_button("user_game", self.open_game_page, 8, 5, hitbox=pygame.Rect((165, 460, 400, 90)),
                                          inner_text='...×...   0', default_texture=pygame.color.Color((105, 103, 209)),
                                          hover_texture=pygame.color.Color(103, 145, 209), click_texture=pygame.color.Color((103, 171, 209)), border_radius=32))
        group_of_buttons = GroupObjectClass(
            buttons, pygame.Rect(242, 438, 400, 332), 'vertical', (20, 20))
        self.objects_on_the_screen["GroupOfButtons"] = group_of_buttons

    def create_image(self, name: str, file_with_image: str, coords_of_image: tuple) -> None:
        """
        :param name: Название объекта
        :param file_with_image: Путь до файла с изображением
        :param coords_of_image: координаты изображения
        """
        self.objects_on_the_screen[name] = pygame.image.load(file_with_image)
        self.coordinates_of_images[name] = coords_of_image

 # ------------------------РЭНДЕР------------------------------------------------------
    # Определение страницы для рэндера
    def page_render(self) -> None:
        if self.page == 0:
            self.render()
        else:
            self.rendered_pages[self.page].classic_game_render()

    # Отображение главной страницы

    def render(self) -> None:
        for name in self.objects_on_the_screen:
            if isinstance(self.objects_on_the_screen[name], pygame.Surface):
                self.render_image(name)
            if isinstance(self.objects_on_the_screen[name], GroupObjectClass):
                print("Yes")
                self.objects_on_the_screen[name].render(self.screen)

    def render_image(self, name_image_to_render: str) -> None:
        self.screen.blit(
            self.objects_on_the_screen[name_image_to_render], self.coordinates_of_images[name_image_to_render])

# ---------------------------------ОБРАБОТКА ДЕЙСТВИЙ-------------------------------------------
    # Функция для определения какая страница должна прогоняться на действия
    def page_processes(self) -> None:
        self.rendered_pages[self.page].processes()

    def processes(self) -> None:
        for event in pygame.event.get():
            for name in self.objects_on_the_screen:
                if isinstance(self.objects_on_the_screen[name], Button):
                    self.objects_on_the_screen[name].hover_click(event)
                if isinstance(self.objects_on_the_screen[name], GroupObjectClass):
                    self.objects_on_the_screen[name].hover_click(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                self.running = 0
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    self.running = 0

    def open_game_page(self, size: int = 3, pieces_to_win: int = 3) -> None:
        print(size)
        self.screen.fill((255, 255, 224))
        index = -1
        for i in self.rendered_pages:
            index += 1
            if i.size == size:
                if self.crosses_player == 1 and self.zeros_player == 0:
                    self.rendered_pages[0].make_move(
                        crosses_player=1, zeros_player=0)
                self.page = index
                break
        else:
            self.create_game_page(size, pieces_to_win)
            self.page = -1

    def open_four_game(self) -> None:
        if self.crosses_player == 1 and self.zeros_player == 0:
            self.rendered_pages[0].make_move(crosses_player=1, zeros_player=0)


class GamePage():

    def __init__(self, home_page: HomePage, size: int = 3, pieces_to_win: int = 0, crosses_player: int = 0, zeros_player: int = 1) -> None:
        self.crosses_player = crosses_player
        self.zeros_player = zeros_player
        self.zero_texture = pathlib.Path("Subtract.png")
        self.cross_texture = pathlib.Path("Union.png")
        self.moves = []
        self.size = size
        if pieces_to_win == 0:
            self.pieceses_to_win: int = self.size
        else:
            self.pieceses_to_win: int = pieces_to_win
        logic_board = Board(size)
        self.logic = TicTacToeManager(logic_board, self.pieceses_to_win)
        self.computer = Adversary(self.logic)
        # Временно функцию нейронки выполняет AI
        self.Neiro = Adversary(self.logic)
        self.visual_board: list[Button] = []
        self.home_page = home_page
        self.objects_on_the_screen = {}
        self.create_game_page()

# ------------------------ СОЗДАНИЕ СТРАНИЦЫ С ИГРОЙ ---------------------------------
    def create_game_page(self) -> None:
        self.create_visual_board()
        self.create_sticks()
        self.create_buttons()
    # Создание кнопки

    def create_button(self, name_of_object: str, function_on_click: Callable, *args,
                      hitbox: pygame.Rect = pygame.Rect((165, 300, 270, 60)), inner_text: str = '',
                      default_texture=(255, 255, 224), hover_texture=pygame.color.Color(103, 145, 209),
                      click_texture=pygame.color.Color((103, 171, 209)), border_radius: int = 0) -> None:
        text = StylizedText(hitbox, inner_text)
        button = Button(function_on_click, *args, hitbox=hitbox, inner_text=text,
                        default_texture=default_texture, hover_texture=hover_texture,
                        click_texture=click_texture, border_radius=0)
        return button

    def create_buttons(self):
        buttons = []
        buttons.append(self.create_button("Back", self.open_home_page, hitbox=pygame.Rect((65, 474, 190, 90)), inner_text="Back", default_texture=pygame.color.Color(
            (105, 103, 209)), hover_texture=pygame.color.Color(103, 145, 209), click_texture=pygame.color.Color((103, 171, 209)), border_radius=32))
        buttons.append(self.create_button("Reset", self.restart_game, hitbox=pygame.Rect((235, 474, 190, 90)), inner_text="Reset", default_texture=pygame.color.Color((105, 103, 209)),
                                          hover_texture=pygame.color.Color(103, 145, 209), click_texture=pygame.color.Color((103, 171, 209)), border_radius=32))
        buttons.append(self.create_button("Undo", self.move_back, hitbox=pygame.Rect((405, 474, 190, 90)),
                                          inner_text="Undo", default_texture=pygame.color.Color((105, 103, 209)),
                                          hover_texture=pygame.color.Color(103, 145, 209), click_texture=pygame.color.Color((103, 171, 209)), border_radius=32))
        group_of_buttons = GroupObjectClass(
            buttons, pygame.Rect(26, 765, 700, 90), 'horizontal', (64, 64))
        self.objects_on_the_screen['groupOfButtons'] = group_of_buttons

    def create_visual_board(self):
        amount_of_sticks = self.size - 1
        size_of_cell = (710 - amount_of_sticks * 20 - 10) // self.size
        for y in range(self.size):
            for x in range(self.size):
                crosses = self.crosses_player
                zeros = self.zeros_player
                number_of_button = self.size * y + x
                hitbox = pygame.Rect(90 + x * (20 + size_of_cell), 25 +
                                     y * (20 + size_of_cell), size_of_cell, size_of_cell)
                if self.crosses_player == self.zeros_player == 1:
                    cell = ClicableCell(hitbox, self.number_printer, default_texture=pygame.color.Color(
                        255, 255, 224), hover_texture=pygame.color.Color(255, 255, 224))
                    self.objects_on_the_screen[number_of_button] = cell
                else:
                    cell = ClicableCell(hitbox, self.make_move, number_of_button, crosses, zeros, default_texture=pygame.color.Color(
                        255, 255, 224), hover_texture=pygame.color.Color(255, 255, 224))
                    self.objects_on_the_screen[number_of_button] = cell
                self.visual_board.append(
                    self.objects_on_the_screen[number_of_button])

    def create_sticks(self):
        amount_of_sticks = self.size - 1
        size_of_cell = (710 - amount_of_sticks * 20 - 10) // self.size
        for i in range(1, self.size):
            coords_vertical = (85 + size_of_cell * i + 10 *
                               i + 10 * (i - 1), 20, 10, 710)
            self.objects_on_the_screen[f"vert{
                i}"] = pygame.Rect(coords_vertical)
            coords_horizontal = (85, 20 + size_of_cell *
                                 i + 10 * i + 10 * (i - 1), 710, 10)
            self.objects_on_the_screen[f"hor{
                i}"] = pygame.Rect(coords_horizontal)

# -------------------------- Рэндер страницы с классической игрой -----------------
    def classic_game_render(self) -> None:
        for name in self.objects_on_the_screen:
            if isinstance(self.objects_on_the_screen[name], Button):
                self.objects_on_the_screen[name].render(self.home_page.screen)
            if isinstance(self.objects_on_the_screen[name], GroupObjectClass):
                self.objects_on_the_screen[name].render(self.home_page.screen)
            if isinstance(self.objects_on_the_screen[name], pygame.Surface):
                self.render_image(name)
            if isinstance(self.objects_on_the_screen[name], pygame.Rect):
                pygame.draw.rect(self.home_page.screen, (133, 116, 115),
                                 self.objects_on_the_screen[name], 0, 10)
            else:
                self.objects_on_the_screen[name].render(self.home_page.screen)

# -------------------- ТРИГЕР ДЕЙСТВИЙ НА СТРАНИЦЕ--------------------------
    def processes(self) -> None:
        if (self.crosses_player == 1) and (self.zeros_player == 1):

            if self.is_game_continue():
                self.make_move()
        for event in pygame.event.get():
            for name in self.objects_on_the_screen:
                if isinstance(self.objects_on_the_screen[name], Button):
                    self.objects_on_the_screen[name].hover_click(event)
                if isinstance(self.objects_on_the_screen[name], GroupObjectClass):
                    self.objects_on_the_screen[name].hover_click(event)
                if isinstance(self.objects_on_the_screen[name], ClicableCell):
                    self.objects_on_the_screen[name].hover_click(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                self.home_page.running = 0
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    self.home_page.running = 0

# ----------------------- РАБОТА С ДЕЙСТВИЯМИ НА СТРАНИЦЕ ----------------------
    def is_move_available(self, number: int):
        if len(self.moves) == 0:
            return True
        if self.is_game_continue():
            return number in self.logic.find_legal_moves()
        return False

    def make_move(self, number: int = -1, crosses_player: int = 1, zeros_player=1) -> None:
        print(number)
        if self.is_game_continue():
            if len(self.moves) % 2 == 0:
                if crosses_player == 0:
                    self.crosses_move(number)
                    self.make_move(crosses_player=crosses_player,
                                   zeros_player=zeros_player)
                if crosses_player == 1:
                    computers_turn = self.computer.search_root(8)
                    self.crosses_move(computers_turn)
                    if zeros_player == 1:
                        self.make_move(crosses_player=crosses_player,
                                       zeros_player=zeros_player)
                if crosses_player == 2:
                    computers_turn = self.Neiro.search_root(8)
                    self.crosses_move(computers_turn)
                    if zeros_player == 1:
                        self.make_move(crosses_player=crosses_player,
                                       zeros_player=zeros_player)

            else:
                if zeros_player == 0:
                    self.zeros_move(number)
                    self.make_move(crosses_player=crosses_player,
                                   zeros_player=zeros_player)
                if zeros_player == 1:
                    computers_turn = self.computer.search_root(3)
                    self.zeros_move(computers_turn)
                if zeros_player == 2:
                    computers_turn = self.Neiro.search_root(3)
                    self.zeros_move(computers_turn)
        else:
            for Cell in self.visual_board:
                Cell.onClick = self.number_printer

    def crosses_move(self, number):
        if self.is_move_available(number):
            self.logic.make_move(number)
            self.moves.append(number)
            self.visual_board[number].default_texture = self.cross_texture
            self.visual_board[number].hover_texture = self.cross_texture
            self.visual_board[number].click_texture = self.cross_texture
            self.visual_board[number].onClick = self.number_printer

    def zeros_move(self, number):
        if self.is_move_available(number):
            self.logic.make_move(number)
            self.moves.append(number)
            self.visual_board[number].default_texture = self.zero_texture
            self.visual_board[number].hover_texture = self.zero_texture
            self.visual_board[number].click_texture = self.zero_texture
            self.visual_board[number].onClick = self.number_printer

    def is_game_continue(self):
        winner = self.logic.check_win()
        if winner is None:
            return True
        else:
            text = ['Ничья', "Крестики", "Нолики"]
            return False

    def move_back(self) -> None:
        if len(self.moves) > 0 and not (self.crosses_player == 1 and self.zeros_player == 0):
            last_move = self.moves[-1]
            self.logic.unmake_move(last_move)
            last_cell = self.visual_board[last_move]
            last_cell.default_texture = pygame.color.Color(255, 255, 224)
            last_cell.hover_texture = pygame.color.Color(255, 255, 224)
            last_cell.onClick = self.make_move
            self.moves.remove(last_move)

    def restart_game(self) -> None:
        if len(self.moves) > 0:
            self.logic.reset_board()
            for Cell in self.visual_board:
                Cell.click_texture = pygame.color.Color(255, 255, 224)
                Cell.default_texture = pygame.color.Color(255, 255, 224)
                Cell.hover_texture = pygame.color.Color(255, 255, 224)
                Cell.onClick = self.make_move
            self.moves = []
            if self.crosses_player == 1 and self.zeros_player == 0:
                self.make_move(crosses_player=1, zeros_player=0)

    def open_home_page(self) -> None:
        self.restart_game()
        self.classic_game_render()
        self.home_page.screen.fill((255, 255, 224))
        self.home_page.page = 0

    def number_printer(self, *args):
        print(args[0])


def main():
    start = HomePage(pygame.display.set_mode((880, 880)),
                     crosses_player='Игрок', zeros_player='Комп')
    start.run()


if __name__ == '__main__':
    main()
