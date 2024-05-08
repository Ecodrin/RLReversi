# StylizedText Class
## Attributes:
- `position`: `pygame.Rect` object representing the position of the text.
- `content`: String content of the text.
- `text_colour`: Color of the text.
- `font_family`: Font family of the text.
- `font_size`: Font size of the text.
- `font_style`: Style of the text (bold, italic, underline).

## Methods:
- `__init__`: Initializes the StylizedText object.
- `render`: Renders the text on the screen.
- `__repr__`: Returns a string representation of the StylizedText object.
- `__str__`: Returns a string representation of the StylizedText object.

# Button Class (inherits from Clickable)
## Attributes:
- `onClick`: Callback function when the button is clicked.
- `hitbox`: Rectangular hitbox of the button.
- `inner_text`: StylizedText object representing the text on the button.
- `default_texture`: Default color or image texture of the button.
- `hover_texture`: Color or image texture when the button is hovered.
- `click_texture`: Color or image texture when the button is clicked.
- `border_radius`: Border radius of the button.

## Methods:
- `__init__`: Initializes the Button object.
- `hover_click`: Changes the button color based on user interaction.
- `render`: Renders the button on the screen.
- `__setattr__`: Sets an attribute of the Button object.
- `__getattr__`: Gets an attribute of the Button object.
- `__repr__`: Returns a string representation of the Button object.
- `__str__`: Returns a string representation of the Button object.

# GroupObjectClass Class
## Attributes:
- `content`: List or tuple of objects to be grouped.
- `position`: Position of the block of objects.
- `direction`: Direction of arrangement (vertical or horizontal).
- `margins`: Margins between objects.

## Methods:
- `__init__`: Initializes the GroupObjectClass object.
- `insert`: Inserts an object into the block at a specific index.
- `append`: Appends an object to the block.
- `pop`: Removes and returns an object from the block.
- `hover_click`: Handles user interactions for all objects in the group.
- `render`: Renders all objects in the group.
- `__repr__`: Returns a string representation of the GroupObjectClass object.
- `__str__`: Returns a string representation of the GroupObjectClass object.

This code provides classes for creating stylized text, buttons with interactive functionalities, and grouping objects for graphical user interface development using Pygame library.