import pygame
import pathlib

SCREEN_COLOR = pygame.color.Color(255, 255, 224)

START_IMAGE_PATH = pathlib.Path('Start Desk.png')
START_IMAGE_COORDS = (245, 15)

BUTTON_DEFAULT_HITBOX = pygame.Rect(242, 440, 400, 90)
BUTTON_DEFAULT_TEXT_COLOR = pygame.color.Color(255, 255, 255)
BUTTON_DEFAULT_CONTENT = 'NO TEKST'
BUTTON_DEFAULT_FONT_FAMILY = 'arial'
BUTTON_DEFAULT_FONT_SIZE = 24
BUTTON_DEFAULT_FONT_STYLE = 0
BUTTON_DEFAULT_DEFAULT_TEXTURE = pygame.color.Color(105, 103, 209)
BUTTON_DEFAULT_HOVER_TEXTURE = pygame.color.Color(103, 145, 209)
BUTTON_DEFAULT_CLICK_TEXTURE = pygame.color.Color(103, 171, 209)
BUTTON_DEFAULT_BOARDER_RADIUS = 24

BUTTON_THREE_HITBOX = pygame.Rect(242, 400, 400, 90)
BUTTON_THREE_CONTENT = '3 × 3'

BUTTON_FOUR_HITBOX = pygame.Rect(242, 380, 400, 90)
BUTTON_FOUR_CONTENT = '4 × 4'

BUTTON_GENERATE_HITBOX = pygame.Rect((242, 770, 400, 90))
BUTTON_GENERATE_CONTENT = 'Сгенерировать'
BUTTON_GENERATE_DEFAULT_TEXTURE = pygame.color.Color((105, 103, 209))
BUTTON_GENERATE_HOVER_TEXTURE = pygame.color.Color(103, 145, 209)
BUTTON_GENERATE_CLICK_TEXTURE = pygame.color.Color((103, 171, 209))

BUTTON_BACK_HITBOX = pygame.Rect((65, 474, 190, 90))
BUTTON_BACK_CONTENT = 'Back'
BUTTON_BACK_DEFAULT_TEXTURE = pygame.color.Color((105, 103, 209))
BUTTON_BACK_HOVER_TEXTURE = pygame.color.Color(103, 145, 209)
BUTTON_BACK_CLICK_TEXTURE = pygame.color.Color((103, 171, 209))
BUTTON_BACK_BOARDER_RADIUS = 32

BUTTON_RESET_HITBOX = pygame.Rect((235, 474, 190, 90))
BUTTON_RESET_CONTENT = 'Reset'
BUTTON_RESET_DEFAULT_TEXTURE = pygame.color.Color((105, 103, 209))
BUTTON_RESET_HOVER_TEXTURE = pygame.color.Color(103, 145, 209)
BUTTON_RESET_CLICK_TEXTURE = pygame.color.Color((103, 171, 209))
BUTTON_RESET_BOARDER_RADIUS = 32

BUTTON_UNDO_HITBOX = pygame.Rect((405, 474, 190, 90))
BUTTON_UNDO_CONTENT = 'Undo'
BUTTON_UNDO_DEFAULT_TEXTURE = pygame.color.Color((105, 103, 209))
BUTTON_UNDO_HOVER_TEXTURE = pygame.color.Color(103, 145, 209)
BUTTON_UNDO_CLICK_TEXTURE = pygame.color.Color((103, 171, 209))
BUTTON_UNDO_BOARDER_RADIUS = 32

START_GROUP_OF_BUTTONS_HITBOX = pygame.Rect(242, 438, 400, 230)
START_GROUP_OF_BUTTONS_MARGINS = (30, 30)

GAME_GROUP_OF_BUTTONS_HITBOX = pygame.Rect(26, 765, 700, 90)
GAME_GROUP_OF_BUTTONS_MARGINS = (64, 64)

NUMBERFIELD_FOR_SIZE_HITBOX = pygame.Rect(242, 665, 200, 90)
NUMBERFIELD_FOR_SIZE_CONTENT = 'size'
NUMBERFIELD_FOR_SIZE_COLOR = pygame.color.Color(105, 103, 209)
NUMBERFIELD_FOR_SIZE_FONT_FAMILY = 'arial'
NUMBERFIELD_FOR_SIZE_FONT_STYLE = 'bold'
NUMBERFIELD_FOR_SIZE_FONT_SIZE = 70

NUMBERFIELD_FOR_WIN_HITBOX = pygame.Rect(242, 665, 200, 90)
NUMBERFIELD_FOR_WIN_CONTENT = 'win'
NUMBERFIELD_FOR_WIN_COLOR = pygame.color.Color(105, 103, 209)
NUMBERFIELD_FOR_WIN_FONT_SIZE = 70
NUMBERFIELD_FOR_WIN_FONT_FAMILY = 'arial'

SIZE_BLOCK_HITBOX = pygame.Rect(242, 665, 200, 90)
WIN_BLOCK_HITBOX = pygame.Rect(442, 665, 200, 90)

ZEROS_TEXTURE = pathlib.Path("Frame 4.png")
CROSSES_TEXTURE = pathlib.Path("Union.png")

DEPTH = 6
TITLE = 'Tic-Tac-Toe'
