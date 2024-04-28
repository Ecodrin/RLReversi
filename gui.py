import sys
import pygame
from board import Clickable

class TicTacToe():

    def __init__(self) -> None:
        self.screen = ['open', 'three', 'four', 'user', 'infinity']
    
    def run(self, title: str='Tic-Tac-Toe'):
        pygame.init()
        screen = pygame.display.set_mode((600, 600)) #создали экран
        pygame.display.set_caption(title)
        image = pygame.image.load("Start Desk.png") # загружаем фото с крестиками
        while True:
            screen.fill((255, 255, 224)) # Задаем цвет фона
            screen.blit(image, (172, 10))
            
            pygame.draw.rect(screen, (105, 103, 209), (172, 300, 270, 60), border_radius=32)
            pygame.draw.rect(screen, (105, 103, 209), (172, 380, 270, 60), border_radius=32)
            pygame.draw.rect(screen, (105, 103, 209), (172, 460, 270, 60), border_radius=32)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
start = TicTacToe()
start.run()