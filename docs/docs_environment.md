# TicTacToeEnv Documentation

This documentation provides an overview of the `TicTacToeEnv` class, which is a custom environment for the Tic Tac Toe game in the Gymnasium framework. The environment is designed to be compatible with reinforcement learning algorithms.

## Imported Modules

The `TicTacToeEnv` class relies on several Python modules:

- `typing`: Provides support for type hints as introduced by PEP 484.
- `random`: Generates pseudo-random numbers.
- `gymnasium`: A standard API for reinforcement learning and a diverse set of reference environments.
- `numpy`: Support for large, multi-dimensional arrays and matrices, along with a large collection of high-level mathematical functions to operate on these arrays.
- `src.board`: A module that likely contains the `Board` class used to represent the Tic Tac Toe board.
- `src.manager`: A module that likely contains the `Adversary` class and `TicTacToeManager` class, which manage the game logic.
- `src.tictactoe`: A module that likely contains the `TicTacToeManager` class, which manages the game logic.

## Class: TicTacToeEnv

### Constructor: `__init__`

Initializes the `TicTacToeEnv` with the given parameters.

**Parameters:**

- `size` (`int`, optional): The size of the Tic Tac Toe board. Defaults to `3`.
- `pieces_to_win` (`int`, optional): The number of pieces in a row required to win. Defaults to `3`.
- `depth` (`int`, optional): The search depth for the adversary. Defaults to `5`.

### Method: `reset`

Resets the environment to its initial state.

**Parameters:**

- `seed` (`int | None`, optional): The seed for the random number generator. Defaults to `None`.
- `options` (`dict[str, Any] | None`, optional): Additional options for the environment. Defaults to `None`.

**Returns:**

- `tuple[ObsType, dict[str, Any]]`: The initial observation and an empty dictionary.

### Method: `step`

Performs a step in the environment.

**Parameters:**

- `action` (`ActType`): The action to take in the environment.

**Returns:**

- `tuple[ObsType, SupportsFloat, bool, bool, dict[str, Any]]`: The observation, reward, termination flag, truncation flag, and a dictionary with additional information.

### Method: `render`

Renders the environment.

**Parameters:**

- `mode` (`str`, optional): The rendering mode. Defaults to `'human'`.

### Method: `close`

Closes the environment.

**Returns:**

- `int`: Always returns `0`.

## Class: MoveSpace

A custom space for the action space in the environment.

### Constructor: `__init__`

Initializes the `MoveSpace` with the given parameters.

**Parameters:**

- `legal_moves` (`list[int]`): The list of legal moves.

### Method: `sample`

Samples a random legal move and removes it from the list of legal moves.

**Parameters:**

- `mask` (`Any | None`, optional): An optional mask to apply to the legal moves. Defaults to `None`.

**Returns:**

- `int`: The sampled move.

## Function: `display`

Displays the board.

**Parameters:**

- `board` (`list[int]`): The board to display.
- `size` (`int`, optional): The size of the board. Defaults to `3`.
