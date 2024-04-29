import sys
import pygame
from gui_elements import Button
from gui_elements import StylizedText
from typing import Callable

def test(x: int):
    print(x+1)

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

text_content = "Hello, World! Hello world! Hello world! Hello, World! Hello world! Hello world!"
text_position = pygame.Rect(200, 200, 300, 400)
text_colour = pygame.color.Color(0, 0, 0)
font_family = "arial"
font_size = 24
font_style = 10
stylized_text = StylizedText(
    content=text_content,
    position=text_position,
    text_colour=text_colour,
    font_family=font_family,
    font_size=font_size,
    font_style=font_style,
)

button = Button(test, 2, hitbox=text_position, inner_text=stylized_text,
                default_texture=pygame.color.Color(255, 0, 0),
                hover_texture=pygame.color.Color(0, 255, 0), click_texture=pygame.color.Color(0, 0, 255))

screen.fill((255, 255, 255))
running = True
while running:
    for event in pygame.event.get():
        # print(event)
        button.hover_click(event)
        button.render(screen)
        pygame.display.flip()
        if event.type == pygame.QUIT:
            running = False

    pygame.time.Clock().tick()

pygame.quit()
