import pygame
from gui_elements import Button
from gui_elements import StylizedText
from typing import Callable
from board import Board
import pathlib
import os

class HomePage:

    def __init__(self,  screen: pygame.display, title: str='Tic-Tac-Toe') -> None:
        self.running = 1
        self.page = 0
        self.rendered_pages = []
        self.screen = screen
        self.objects_on_the_screen = {}
        self.coordinates_of_images = {} #создали экран
        self.title = title
    
    def run(self) -> None:
        # Создаём объекты
        pygame.init()
        self.page_create()
        
        pygame.display.set_caption(self.title)
        self.screen.fill((255, 255, 224)) # Задаем цвет фона

        while self.running:
            #Рэндер объектов в Зависимости от текущей страницы
            pygame.display.flip()
            self.page_render()
            self.page_processes()
 
 #------------------------CОЗДАНИЕ--------------------------------------------------   
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
        classic_game_page = ClassicGamePage(self)
        self.rendered_pages.append(classic_game_page)

    # Создание объектов на главной странице
    def create_button(self, name_of_object: str, function_on_click: Callable, *args, 
                      hitbox: pygame.Rect=pygame.Rect((165, 300, 270, 60)), inner_text: str='NO TEKST', 
                      default_texture=pygame.color.Color((105, 103, 209)), hover_texture=pygame.color.Color(103, 145, 209), 
                      click_texture=pygame.color.Color((103, 171, 209)), border_radius: int=0) -> None:
        classic_text = StylizedText(hitbox, inner_text)
        button_classic = Button(function_on_click, hitbox=hitbox, inner_text=classic_text, 
                                default_texture=default_texture, hover_texture=hover_texture, 
                                click_texture=click_texture, border_radius=32)
        self.objects_on_the_screen[name_of_object] = button_classic
    
    def create_image(self, name: str, file_with_image: str, coords_of_image: tuple) -> None:
        self.objects_on_the_screen[name] = pygame.image.load(file_with_image)
        self.coordinates_of_images[name] = coords_of_image

 #------------------------РЭНДЕР------------------------------------------------------    
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
        self.screen.blit(self.objects_on_the_screen[name_image_to_render], self.coordinates_of_images[name_image_to_render])

#---------------------------------ОБРАБОТКА ДЕЙСТВИЙ-------------------------------------------   
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
        self.page = 1


class ClassicGamePage():

    def __init__(self, home_page: HomePage) -> None:
        self.turn_number = 0
        self.size = 3
        self.logic_board = Board(3)
        self.visual_board: list[Button] = []
        self.home_page = home_page
        self.objects_on_the_screen = {}
        self.create_classic_game_page()

#------------------------ СОЗДАНИЕ СТРАНИЦЫ С ИГРОЙ ---------------------------------
    def create_classic_game_page(self) -> None:
        self.create_visual_board()
        self.create_button("Back", self.open_home_page, hitbox=pygame.Rect((65, 474, 130, 60)), 
                           inner_text="Back", default_texture=pygame.color.Color((105, 103, 209)), 
                           hover_texture=pygame.color.Color(103, 145, 209), click_texture=pygame.color.Color((103, 171, 209)), border_radius=32)
        self.create_button("Reset", self.open_home_page, hitbox=pygame.Rect((235, 474, 130, 60)), 
                           inner_text="Reset", default_texture=pygame.color.Color((105, 103, 209)), 
                           hover_texture=pygame.color.Color(103, 145, 209), click_texture=pygame.color.Color((103, 171, 209)), border_radius=32)
        self.create_button("Undo", self.open_home_page, hitbox=pygame.Rect((405, 474, 130, 60)), 
                           inner_text="Undo", default_texture=pygame.color.Color((105, 103, 209)), 
                           hover_texture=pygame.color.Color(103, 145, 209), click_texture=pygame.color.Color((103, 171, 209)), border_radius=32)
    # Создание кнопки
    def create_button(self, name_of_object: str, function_on_click: Callable, *args, 
                      hitbox: pygame.Rect=pygame.Rect((165, 300, 270, 60)), inner_text: str='', 
                      default_texture=pygame.color.Color((105, 103, 209)), hover_texture=pygame.color.Color(103, 145, 209), 
                      click_texture=pygame.color.Color((103, 171, 209)), border_radius: int=0) -> None:
        classic_text = StylizedText(hitbox, inner_text)
        button_classic = Button(function_on_click, *args, hitbox=hitbox, inner_text=classic_text, 
                                default_texture=default_texture, hover_texture=hover_texture, 
                                click_texture=click_texture, border_radius=0)
        self.objects_on_the_screen[name_of_object] = button_classic

    def create_visual_board(self):
        zero = pathlib.Path("Frame 1.png")
        cross = pathlib.Path("Group 16.png")
        for y in range(self.size):
            for x in range(self.size):
                number_of_button = str(3 * y + x)
                hitbox = pygame.Rect(112 + x * 131, 40 + y * 131, 119, 119) 
                self.create_button(number_of_button, self.make_move, number_of_button, zero, cross, hitbox=hitbox, 
                                   default_texture=pygame.color.Color(218, 96, 96), hover_texture=pygame.color.Color((220, 146, 146)), 
                                   click_texture=pygame.color.Color(218, 96, 96))
                self.visual_board.append(self.objects_on_the_screen[number_of_button])

#-------------------------- Рэндер страницы с классической игрой -----------------   
    def classic_game_render(self) -> None:
        pygame.draw.line(self.home_page.screen, (133, 116, 115), (368, 26), (368, 438), 6) #правая
        pygame.draw.line(self.home_page.screen, (133, 116, 115), (237, 26), (237, 438), 6) #левая
        pygame.draw.line(self.home_page.screen, (133, 116, 115), (97, 165), (509, 165), 6) #верхняя
        pygame.draw.line(self.home_page.screen, (133, 116, 115), (97, 296), (509, 296), 6) #нижняя
        for name in self.objects_on_the_screen:
                if isinstance(self.objects_on_the_screen[name], Button):
                    self.render_button(self.objects_on_the_screen[name])
                if isinstance(self.objects_on_the_screen[name], pygame.Surface):
                     self.render_image(name)
    
    def render_button(self, button_to_render: Button) -> None:
        button_to_render.render(self.home_page.screen)

    def open_home_page(self) -> None:
        self.home_page.screen.fill((255, 255, 224))
        self.home_page.page = 0

    def make_move(self, number: str, zero_texture: os.PathLike, cross_texture: os.PathLike):
        self.turn_number += 1
        if self.turn_number % 2 == 1:
            texture_to_put = cross_texture
        else: 
            texture_to_put = zero_texture
        self.objects_on_the_screen[number].default_texture = texture_to_put
        self.objects_on_the_screen[number].hover_texture = texture_to_put
        print(number)


#-------------------- ТРИГЕР ДЕЙСТВИЙ НА СТРАНИЦЕ--------------------------
    def classic_game_processes(self) -> None:
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


start = HomePage(pygame.display.set_mode((600, 600)))
start.run()