import sys
import pygame
from gui_elements import Button
from gui_elements import StylizedText
from typing import Callable

class HomeScreen():

    def __init__(self,  title: str='Tic-Tac-Toe') -> None:
        self.page = 0
        self.objects_on_the_screen = {}
        self.coordinates_of_images = {}
        self.screen = pygame.display.set_mode((600, 600)) #создали экран
        self.title = title
    
    def run(self) -> None:
        # Создаём объекты
        pygame.init()
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

        
        pygame.display.set_caption(self.title)
        self.screen.fill((255, 255, 224)) # Задаем цвет фона

        while True:
            #Рэндер объектов в Зависимости от текущей страницы
            self.what_page_now()
            
            # проверка ивентов в зависимости от текущей страницы
            for event in pygame.event.get():
                for name in self.objects_on_the_screen:
                    if isinstance(self.objects_on_the_screen[name], Button):
                        self.objects_on_the_screen[name].hover_click(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
            pygame.display.flip()
                        
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
    
    def what_page_now(self) -> None:
        if self.page == 0:
            self.render_homepage()
        if self.page == 1:
            self.render_classic_game()

    def render_button(self, button_to_render: Button) -> None:
        button_to_render.render(self.screen)

    def render_image(self, name_image_to_render: str) -> None:
        self.screen.blit(self.objects_on_the_screen[name_image_to_render], self.coordinates_of_images[name_image_to_render])

    def render_homepage(self) -> None:
        for name in self.objects_on_the_screen:
                if isinstance(self.objects_on_the_screen[name], Button):
                    self.render_button(self.objects_on_the_screen[name])
                if isinstance(self.objects_on_the_screen[name], pygame.Surface):
                     self.render_image(name)

    def render_classic_game(self):
        for name in self.objects_on_the_screen:
                if isinstance(self.objects_on_the_screen[name], pygame.Surface):
                    self.screen.fill((125, 125, 200))
                    self.render_image(name)
    
    def open_classic_game(self):
        self.page = 1

start = HomeScreen()
start.run()