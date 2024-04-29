import sys
import pygame
from gui_elements import Button
from gui_elements import StylizedText
from typing import Callable
from board import Board

class HomePage:

    def __init__(self,  screen: pygame.display, title: str='Tic-Tac-Toe') -> None:
        self.running = True
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
        print(self.rendered_pages[0].objects_on_the_screen)

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
    def page_render(self) -> None:
        if self.page == 0:
            self.render_homepage()
        if self.page == 1:
            self.screen.fill((255, 255, 224))
            self.rendered_pages[0].classic_game_render()
    
    #отображение главной страницы
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
    def page_processes(self):
        if self.page == 0:
            self.home_page_processes()
        if self.page == 1:
            self.rendered_pages[0].classic_game_processes()

    def home_page_processes(self):
        for event in pygame.event.get():
                for name in self.objects_on_the_screen:
                    if isinstance(self.objects_on_the_screen[name], Button):
                        self.objects_on_the_screen[name].hover_click(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        self.running = False
    
    def open_classic_game(self):
        self.page = 1


class ClassicGamePage():

    def __init__(self, home_page: HomePage):
        self.home_page = home_page
        self.objects_on_the_screen = {}
        self.create_classic_game_page()
    
    def create_classic_game_page(self):
        self.create_button("Back", self.open_home_page, hitbox=pygame.Rect((165, 300, 270, 60)), 
                           inner_text="Back", default_texture=pygame.color.Color((105, 103, 209)), 
                           hover_texture=pygame.color.Color(103, 145, 209), click_texture=pygame.color.Color((103, 171, 209)), border_radius=32)
        self.create_button("Reset", self.open_home_page, hitbox=pygame.Rect((165, 380, 270, 60)), 
                           inner_text="Reset", default_texture=pygame.color.Color((105, 103, 209)), 
                           hover_texture=pygame.color.Color(103, 145, 209), click_texture=pygame.color.Color((103, 171, 209)), border_radius=32)
        self.create_button("Undo", self.open_home_page, hitbox=pygame.Rect((165, 460, 270, 60)), 
                           inner_text="Undo", default_texture=pygame.color.Color((105, 103, 209)), 
                           hover_texture=pygame.color.Color(103, 145, 209), click_texture=pygame.color.Color((103, 171, 209)), border_radius=32)

    def create_button(self, name_of_object: str, function_on_click: Callable, *args, 
                      hitbox: pygame.Rect=pygame.Rect((165, 300, 270, 60)), inner_text: str='NO TEKST', 
                      default_texture=pygame.color.Color((105, 103, 209)), hover_texture=pygame.color.Color(103, 145, 209), 
                      click_texture=pygame.color.Color((103, 171, 209)), border_radius: int=0) -> None:
        classic_text = StylizedText(hitbox, inner_text)
        button_classic = Button(function_on_click, hitbox=hitbox, inner_text=classic_text, 
                                default_texture=default_texture, hover_texture=hover_texture, 
                                click_texture=click_texture, border_radius=32)
        self.objects_on_the_screen[name_of_object] = button_classic
    
    def classic_game_render(self):

        for name in self.objects_on_the_screen:
                if isinstance(self.objects_on_the_screen[name], Button):
                    self.render_button(self.objects_on_the_screen[name])
                if isinstance(self.objects_on_the_screen[name], pygame.Surface):
                     self.render_image(name)
    
    def render_button(self, button_to_render: Button) -> None:
        button_to_render.render(self.home_page.screen)

    def open_home_page(self):
        self.home_page.page = 0
        pygame.display.flip()

    def classic_game_processes(self):
        for event in pygame.event.get():
                for name in self.objects_on_the_screen:
                    if isinstance(self.objects_on_the_screen[name], Button):
                        self.objects_on_the_screen[name].hover_click(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.home_page.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        self.home_page.running = False


start = HomePage(pygame.display.set_mode((600, 600)))
start.run()