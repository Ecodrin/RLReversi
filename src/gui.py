import sys
import pygame

pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption('Test')

while True:
    # Задаем цвет фона
    screen.fill((255, 255, 224))
    # Обновляем экран
    pygame.display.flip()
    #pygame.draw.line(surface, color, start_point, end_point, width)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()