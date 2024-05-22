# TicTacToeManager Documentation

The `TicTacToeManager` class is a concrete implementation of the `GameManager` class for a Tic Tac Toe game. It manages the game board, turns, and game logic specific to Tic Tac Toe.

## Class: TicTacToeManager

### Constructor: `__init__`

Initializes a `TicTacToeManager` object with the specified parameters.

**Parameters:**

- `board` (`Board`, optional): The game board object. Defaults to a 3x3 board.
- `pieces_to_win` (`int`, optional): The number of pieces in a row needed to win. Defaults to the size of the board.

### Attributes:

- `board` (`Board`): The game board object.
- `_crosses` (`list[int]`): A list of cells where crosses (player 1) have been placed.
- `_noughts` (`list[int]`): A list of cells where noughts (player 2) have been placed.
- `_last_move` (`int`): The last move made by the current player.
- `turn` (`int`): The current turn number. 1 for crosses' turn, -1 for noughts' turn.
- `pieces_to_win` (`int`): The number of pieces in a row needed to win.

### Methods:

- `reset_board() -> None`: Resets the game board to its initial state.
- `make_move(cell: int) -> None`: Makes a move on the game board at the specified cell.
- `unmake_move(cell: int) -> None`: Undoes a move on the game board at the specified cell.
- `find_legal_moves() -> list[int]`: Returns a list of all legal moves for the current player.
- `check_win() -> int`: Checks if the game has been won and returns the winner's score.
- `_check_win_at_cell(cell: int) -> int`: Checks if the move at the specified cell results in a win.
- `_check_borders(cell: int, direction: tuple[int, int]) -> bool`: Checks if a move in a certain direction is within the board boundaries.
