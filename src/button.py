from typing import Callable, Union
import pygame
from pygame.locals import Rect
from сell import Clickable
from stylized_text import StylizedText
from function_Cente_Relative_To import center_relative_to


class Button(Clickable):

    def __init__(self, onClick: Callable, *args,
                 hitbox: Rect = pygame.Rect(0, 0, 0, 0),
                 inner_text: StylizedText = '',
                 default_texture: Union[tuple, str] = (0, 0, 255),
                 hover_texture: Union[tuple, str] = (255, 0, 0),
                 click_texture: Union[tuple, str] = (0, 255, 0)) -> None:

        super().__init__(onClick, *args, hitbox=hitbox)
        self.inner_text: StylizedText = inner_text
        self.default_texture: Union[tuple, str] = default_texture
        self.hover_texture: Union[tuple, str] = hover_texture
        self.click_texture: Union[tuple, str] = click_texture
        self.button_texture: Union[tuple, str] = self.default_texture

    def hover_click(self, event: pygame.event) -> None:
        point = pygame.mouse.get_pos()
        collide = self.hitbox.collidepoint(point)
        if collide:
            self.button_texture = self.hover_texture
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.button_texture = self.click_texture
            elif event.type == pygame.MOUSEBUTTONUP:
                self.button_texture = self.hover_texture

        else:
            self.button_texture = self.default_texture

    def render(self, screen: pygame.display) -> None:
        center_relative_to(self.inner_text.position, self.hitbox)

        if isinstance(self.button_texture, tuple):
            pygame.draw.rect(screen, self.button_texture, self.hitbox)
            self.inner_text.render(screen)
        else:
            img = pygame.image.load(self.button_texture)
            img = pygame.transform.scale(img, (self.hitbox[2], self.hitbox[3]))
            screen.blit(img, self.hitbox)
            self.inner_text.render(screen)

    def __repr__(self):
        return (f'{self.inner_text}, {self.default_texture}, {self.hover_texture},'
                f'{self.click_texture}, {self.onClick}, {self.args}, {self.hitbox}')

    def __str__(self):
        return f'{self.inner_text}, {self.default_texture}, {self.hover_texture}, {self.click_texture}'
