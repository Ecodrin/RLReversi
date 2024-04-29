import sys
import pygame
from gui_elements import Button
from gui_elements import StylizedText
from typing import Callable

class TicTacToe():

    def __init__(self,  title: str='Tic-Tac-Toe') -> None:
        self.objects_on_the_screen = {}
        self.screen = pygame.display.set_mode((600, 600)) #создали экран
        self.title = title
        pass
    
    def run(self) -> None:
        pygame.init()
        self.objects_on_the_screen['image_of_game'] = pygame.image.load("Start Desk.png") # загружаем фото с крестиками
        self.create_button("classic_game", self.change_color, hitbox=pygame.Rect((165, 300, 270, 60)), 
                           inner_text='3 × 3', default_texture=pygame.color.Color((105, 103, 209)), 
                           hover_texture=pygame.color.Color(103, 145, 209), click_texture=pygame.color.Color((103, 171, 209)), border_radius=32)
        self.create_button("four_game", self.change_color, hitbox=pygame.Rect((165, 380, 270, 60)), 
                           inner_text='4 × 4', default_texture=pygame.color.Color((105, 103, 209)), 
                           hover_texture=pygame.color.Color(103, 145, 209), click_texture=pygame.color.Color((103, 171, 209)), border_radius=32)
        self.create_button("user_game", self.change_color, hitbox=pygame.Rect((165, 460, 270, 60)), 
                           inner_text='...×...   0', default_texture=pygame.color.Color((105, 103, 209)), 
                           hover_texture=pygame.color.Color(103, 145, 209), click_texture=pygame.color.Color((103, 171, 209)), border_radius=32)

        
        pygame.display.set_caption(self.title)
        self.screen.fill((255, 255, 224)) # Задаем цвет фона

        while True:
            # Цикл для Рэндера объектов
            for name in self.objects_on_the_screen:
                if isinstance(self.objects_on_the_screen[name], Button):
                        self.objects_on_the_screen[name].render(self.screen)
            
            self.screen.blit(self.objects_on_the_screen['image_of_game'], (172, 10))
            
            # Цикл для проверки ивентов на объектах
            for event in pygame.event.get():
                for name in self.objects_on_the_screen:
                    if isinstance(self.objects_on_the_screen[name], Button):
                        self.objects_on_the_screen[name].hover_click(event)
                        self.objects_on_the_screen[name].render(self.screen)
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
                      click_texture=pygame.color.Color((103, 171, 209)), border_radius: int=0):
        classic_text = StylizedText(hitbox, inner_text)
        button_classic = Button(function_on_click, hitbox=hitbox, inner_text=classic_text, 
                                default_texture=default_texture, hover_texture=hover_texture, 
                                click_texture=click_texture, border_radius=32)
        self.objects_on_the_screen[name_of_object] = button_classic
    
    def change_color(self):
        print('YES')

start = TicTacToe()
start.run()