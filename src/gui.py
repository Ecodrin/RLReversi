import sys
import pygame
from gui_elements import Button
from gui_elements import StylizedText
from typing import Callable

class TicTacToe():

    def __init__(self) -> None:
        pass
    
    def run(self, title: str='Tic-Tac-Toe'):
        pygame.init()
        screen = pygame.display.set_mode((600, 600)) #создали экран
        screen.fill((255, 255, 224)) # Задаем цвет фона
        pygame.display.set_caption(title)
    
        image = pygame.image.load("Start Desk.png") # загружаем фото с крестиками
        screen.blit(image, (172, 10))

        classic_text = StylizedText(pygame.Rect((165, 300, 270, 60)), "3 × 3")
        button_classic = Button(self.change_color, hitbox=pygame.Rect((165, 300, 270, 60)), inner_text=classic_text, 
                                default_texture=pygame.color.Color((105, 103, 209)), hover_texture=pygame.color.Color(103, 145, 209), click_texture=pygame.color.Color((103, 171, 209)), border_radius=32)
        while True:
            button_classic.render(screen)
            for event in pygame.event.get():
                button_classic.hover_click(event)
                pygame.display.flip()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                        
            
    def change_color():
        print('YES')

start = TicTacToe()
start.run()