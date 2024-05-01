import pygame
from gui_elements import Button, StylizedText
from typing import Callable, Any
from board import Board
from tictactoe import TicTacToeManager
import pathlib
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
        self.page: int = 0
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
        self.create_home_page()
        self.create_classic_game_page()

    # Создание главной страницы
    def create_home_page(self) -> None:
        self.create_image('start_image', 'Start Desk.png', (165, 10))
        self.create_button("classic_game", self.open_classic_game, hitbox=pygame.Rect((165, 300, 270, 60)),
                           inner_text='3 × 3', default_texture=pygame.color.Color((105, 103, 209)),
                           hover_texture=pygame.color.Color(103, 145, 209), click_texture=pygame.color.Color((103, 171, 209)), border_radius=32)
        self.create_button("four_game", self.open_classic_game, hitbox=pygame.Rect((165, 380, 270, 60)),
                           inner_text='4 × 4', default_texture=pygame.color.Color((105, 103, 209)),
                           hover_texture=pygame.color.Color(103, 145, 209), click_texture=pygame.color.Color((103, 171, 209)), border_radius=32)
        self.create_button("user_game", self.open_classic_game, hitbox=pygame.Rect((165, 460, 270, 60)),
                           inner_text='...×...   0', default_texture=pygame.color.Color((105, 103, 209)),
                           hover_texture=pygame.color.Color(103, 145, 209), click_texture=pygame.color.Color((103, 171, 209)), border_radius=32)
    # Создание главной страницы

    def create_classic_game_page(self) -> None:
        classic_game_page = ClassicGamePage(
            self, self.crosses_player, self.zeros_player)
        self.rendered_pages.append(classic_game_page)

    # Создание объектов на главной странице
    def create_button(self, name_of_object: str, function_on_click: Callable, *args, hitbox: pygame.Rect = pygame.Rect((165, 300, 270, 60)),
                      inner_text: str = 'NO TEKST', text_colour: pygame.color.Color = pygame.color.Color(255, 255, 255), font_family: str = 'arial',
                      font_size: int = 24, font_style: int = 0, default_texture=pygame.color.Color((105, 103, 209)),
                      hover_texture=pygame.color.Color(103, 145, 209), click_texture=pygame.color.Color((103, 171, 209)), border_radius: int = 0) -> None:
        """
        :param function_on_click (callback function):
        :param *args (arguments for callback function):
        :param hitbox (rectangular):
        :param inner_text: str = 'NO TEKST'
        :param text_colour: Цвет.
        :param font_family: Шрифт текста.
        :param font_size: Размер текста.
        :param font_style: Стиль текста. Задаётся битовой маской: 0b001 - жирный, 0b010 - курсив, 0b100 - подчёркивание.
        :return:
        :param default_texture: Стандартная текстура кнопки.
        :param hover_texture: Текстура при наведении курсора.
        :param click_texture: Текстура при клике.
        :param border_radius: Радиус округления.
        """
        classic_text = StylizedText(hitbox, inner_text)
        button_classic = Button(function_on_click, hitbox=hitbox, inner_text=classic_text,
                                default_texture=default_texture, hover_texture=hover_texture,
                                click_texture=click_texture, border_radius=32)
        self.objects_on_the_screen[name_of_object] = button_classic

    def create_image(self, name: str, file_with_image: str, coords_of_image: tuple) -> None:
        self.objects_on_the_screen[name] = pygame.image.load(file_with_image)
        self.coordinates_of_images[name] = coords_of_image

 # ------------------------РЭНДЕР------------------------------------------------------
    # Определение страницы для рэндера
    def page_render(self) -> None:
        if self.page == 0:
            self.render_homepage()
        if self.page == 1:
            self.screen.fill((255, 255, 224))
            self.rendered_pages[0].classic_game_render()

    # Отображение главной страницы
    def render_homepage(self) -> None:
        for name in self.objects_on_the_screen:
            if isinstance(self.objects_on_the_screen[name], Button):
                self.render_button(self.objects_on_the_screen[name])
            if isinstance(self.objects_on_the_screen[name], pygame.Surface):
                self.render_image(name)

    def render_button(self, button_to_render: Button) -> None:
        button_to_render.render(self.screen)

    def render_image(self, name_image_to_render: str) -> None:
        self.screen.blit(
            self.objects_on_the_screen[name_image_to_render], self.coordinates_of_images[name_image_to_render])

# ---------------------------------ОБРАБОТКА ДЕЙСТВИЙ-------------------------------------------
    # Функция для определения какая страница должна прогоняться на действия
    def page_processes(self) -> None:
        if self.page == 0:
            self.home_page_processes()
        if self.page == 1:
            self.rendered_pages[0].classic_game_processes()

    def home_page_processes(self) -> None:
        for event in pygame.event.get():
            for name in self.objects_on_the_screen:
                if isinstance(self.objects_on_the_screen[name], Button):
                    self.objects_on_the_screen[name].hover_click(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                self.running = 0
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    self.running = 0

    def open_classic_game(self) -> None:
        if self.crosses_player == 1 and self.zeros_player == 0:
            self.rendered_pages[0].make_move(crosses_player=1, zeros_player=0)
        self.page = 1


class ClassicGamePage():

    def __init__(self, home_page: HomePage, crosses_player: int = 0, zeros_player: int = 1) -> None:
        self.crosses_player = crosses_player
        self.zeros_player = zeros_player
        self.zero_texture = pathlib.Path("Frame 1.png")
        self.cross_texture = pathlib.Path("Group 16.png")
        self.moves = []
        self.size = 3
        self.logic_board = Board(3)
        self.logic = TicTacToeManager()
        self.AI = Adversary(self.logic)
        # Временно функцию нейронки выполняет AI
        self.Neiro = Adversary(self.logic)
        self.visual_board: list[Button] = []
        self.home_page = home_page
        self.objects_on_the_screen = {}
        self.create_classic_game_page()

# ------------------------ СОЗДАНИЕ СТРАНИЦЫ С ИГРОЙ ---------------------------------
    def create_classic_game_page(self) -> None:
        self.create_visual_board()
        self.create_button("Back", self.open_home_page, hitbox=pygame.Rect((65, 474, 130, 60)),
                           inner_text="Back", default_texture=pygame.color.Color((105, 103, 209)),
                           hover_texture=pygame.color.Color(103, 145, 209), click_texture=pygame.color.Color((103, 171, 209)), border_radius=32)
        self.create_button("Reset", self.restart_game, hitbox=pygame.Rect((235, 474, 130, 60)),
                           inner_text="Reset", default_texture=pygame.color.Color((105, 103, 209)),
                           hover_texture=pygame.color.Color(103, 145, 209), click_texture=pygame.color.Color((103, 171, 209)), border_radius=32)
        self.create_button("Undo", self.move_back, hitbox=pygame.Rect((405, 474, 130, 60)),
                           inner_text="Undo", default_texture=pygame.color.Color((105, 103, 209)),
                           hover_texture=pygame.color.Color(103, 145, 209), click_texture=pygame.color.Color((103, 171, 209)), border_radius=32)
    # Создание кнопки

    def create_button(self, name_of_object: str, function_on_click: Callable, *args,
                      hitbox: pygame.Rect = pygame.Rect((165, 300, 270, 60)), inner_text: str = '',
                      default_texture=(255, 255, 224), hover_texture=pygame.color.Color(103, 145, 209),
                      click_texture=pygame.color.Color((103, 171, 209)), border_radius: int = 0) -> None:
        classic_text = StylizedText(hitbox, inner_text)
        button_classic = Button(function_on_click, *args, hitbox=hitbox, inner_text=classic_text,
                                default_texture=default_texture, hover_texture=hover_texture,
                                click_texture=click_texture, border_radius=0)
        self.objects_on_the_screen[name_of_object] = button_classic

    def create_visual_board(self):
        for y in range(self.size):
            for x in range(self.size):
                c = self.crosses_player
                z = self.zeros_player
                number_of_button = 3 * y + x
                hitbox = pygame.Rect(112 + x * 131, 40 + y * 131, 122, 122)
                if self.crosses_player == self.zeros_player == 1:
                    self.create_button(str(number_of_button), self.number_printer, number_of_button, hitbox=hitbox,
                                       default_texture=pygame.color.Color(255, 255, 224), hover_texture=pygame.color.Color((255, 255, 224)),
                                       click_texture=pygame.color.Color(255, 255, 224))
                else:
                    self.create_button(str(number_of_button), self.make_move, number_of_button, c, z, hitbox=hitbox,
                                       default_texture=pygame.color.Color(255, 255, 224), hover_texture=pygame.color.Color((255, 255, 224)),
                                       click_texture=pygame.color.Color(255, 255, 224))
                self.visual_board.append(
                    self.objects_on_the_screen[str(number_of_button)])

# -------------------------- Рэндер страницы с классической игрой -----------------
    def classic_game_render(self) -> None:
        pygame.draw.line(self.home_page.screen, (133, 116, 115),
                         (368, 26), (368, 438), 6)  # правая
        pygame.draw.line(self.home_page.screen, (133, 116, 115),
                         (237, 26), (237, 438), 6)  # левая
        pygame.draw.line(self.home_page.screen, (133, 116, 115),
                         (97, 165), (509, 165), 6)  # верхняя
        pygame.draw.line(self.home_page.screen, (133, 116, 115),
                         (97, 296), (509, 296), 6)  # нижняя
        for name in self.objects_on_the_screen:
            if isinstance(self.objects_on_the_screen[name], Button):
                self.render_button(self.objects_on_the_screen[name])
            if isinstance(self.objects_on_the_screen[name], pygame.Surface):
                self.render_image(name)

    def render_button(self, button_to_render: Button) -> None:
        button_to_render.render(self.home_page.screen)

# -------------------- ТРИГЕР ДЕЙСТВИЙ НА СТРАНИЦЕ--------------------------
    def classic_game_processes(self) -> None:
        if (self.crosses_player == 1) and (self.zeros_player == 1):
            if self.is_game_continue():
                self.make_move()
        for event in pygame.event.get():
            for name in self.objects_on_the_screen:
                if isinstance(self.objects_on_the_screen[name], Button):
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
        if self.is_game_continue():
            if len(self.moves) % 2 == 0:
                if crosses_player == 0:
                    self.crosses_move(number)
                    self.make_move(crosses_player=crosses_player,
                                   zeros_player=zeros_player)
                if crosses_player == 1:
                    computers_turn = self.AI.search_root(8)
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
                    computers_turn = self.AI.search_root(8)
                    self.zeros_move(computers_turn)
                if zeros_player == 2:
                    computers_turn = self.Neiro.search_root(8)
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
        winner = self.logic.has_game_ended()
        if winner is None:
            return True
        else:
            text = ['Ничья', "Крестики", "Нолики"]
            return False

    def move_back(self) -> None:
        if len(self.moves) > 1 or not (self.crosses_player == 1 and self.zeros_player == 0):
            last_move = self.moves[-1]
            self.logic.unmake_move(last_move)
            last_cell = self.visual_board[last_move]
            last_cell.click_texture = pygame.color.Color(255, 255, 224)
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
    start = HomePage(pygame.display.set_mode((600, 600)),
                     crosses_player='Игрок', zeros_player='Комп')
    start.run()


if __name__ == '__main__':
    main()
