# StylizedText Documentation

The `StylizedText` class is used to create and manage text objects with customizable styles and positions. It is designed to be used with the Pygame library for rendering text on a Pygame surface.

## Class: StylizedText

### Constructor: `__init__`

Initializes a `StylizedText` object with the specified parameters.

**Parameters:**

- `content` (`str`, optional): The text content. Defaults to an empty string.
- `position` (`pygame.Rect`): The position of the text on the screen.
- `text_colour` (`pygame.color.Color`, optional): The color of the text. Defaults to white.
- `font_family` (`str`, optional): The font family to use. Defaults to 'arial'.
- `font_size` (`int`, optional): The size of the font. Defaults to 24.
- `font_style` (`int`, optional): The style of the font. It is a bitmask where 0b001 is bold, 0b010 is italic, and 0b100 is underline. Defaults to 0 (no style).

### Properties:

- `content` (`str`): The text content.
- `position` (`pygame.Rect`): The position of the text on the screen.

### Methods:

- `render(screen: pygame.display) -> None`: Renders the text on the specified Pygame display.
- `__repr__(self) -> str`: Returns a string representation of the `StylizedText` object.
- `__str__(self) -> str`: Returns a human-readable string representation of the `StylizedText` object.

# Button Documentation

The `Button` class is a subclass of `Clickable` and represents a clickable button with customizable text, textures, and border radius.

## Class: Button

### Constructor: `__init__`

Initializes a `Button` object with the specified parameters.

**Parameters:**

- `onClick` (`Callable`): The callback function to be called when the button is clicked.
- `*args` (`arguments for callback function`): Additional arguments for the callback function.
- `hitbox` (`pygame.Rect`): The rectangular hitbox of the button.
- `inner_text` (`StylizedText`): The text to be displayed on the button.
- `default_texture` (`pygame.color.Color | os.PathLike`, optional): The default texture of the button. Defaults to white.
- `hover_texture` (`pygame.color.Color | os.PathLike`, optional): The texture of the button when hovered over. Defaults to a lighter gray.
- `click_texture` (`pygame.color.Color | os.PathLike`, optional): The texture of the button when clicked. Defaults to a darker gray.
- `border_radius` (`int`, optional): The radius of the button's corners. Defaults to 0 (rectangular button).

### Methods:

- `hover_click(event: pygame.event) -> None`: Changes the button's texture based on the mouse event.
- `render(screen: pygame.surface) -> None`: Renders the button on the specified Pygame surface.
- `__repr__(self) -> str`: Returns a string representation of the `Button` object.
- `__str__(self) -> str`: Returns a human-readable string representation of the `Button` object.

# GroupObjectClass Documentation

The `GroupObjectClass` class is used to manage and render a group of objects in a row with specified margins.

## Class: GroupObjectClass

### Constructor: `__init__`

Initializes a `GroupObjectClass` object with the specified parameters.

**Parameters:**

- `content` (`list[Any] | tuple[Any]`): The list or tuple of objects to be managed.
- `position` (`pygame.Rect`): The position of the group block.
- `direction` (`str`, optional): The direction in which the objects are arranged. Can be 'horizontal' or 'vertical'. Defaults to 'horizontal'.
- `margins` (`tuple[int, int] | list[int, int]`, optional): The margins between the objects. Defaults to (0, 0).

### Properties:

- `position` (`pygame.Rect`): The position of the group block.
- `margins` (`tuple[int, int] | list[int, int]`): The margins between the objects.
- `direction` (`str`): The direction in which the objects are arranged.

### Methods:

- `insert(index: int, item: Any) -> None`: Inserts an object at the specified index in the group block.
- `append(item: Any) -> None`: Appends an object to the end of the group block.
- `pop(position: int) -> object`: Removes and returns the object at the specified position in the group block.
- `hover_click(event: pygame.event.Event) -> None`: Checks the state of the objects in the group block based on the Pygame event.
- `render(screen: pygame.Surface) -> None`: Renders all objects in the group block on the specified Pygame surface.
- `__repr__(self) -> str`: Returns a string representation of the `GroupObjectClass` object.
- `__str__(self) -> str`: Returns a human-readable string representation of the `GroupObjectClass` object.