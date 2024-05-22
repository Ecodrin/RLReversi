# GameManager Documentation

The `GameManager` class is an abstract base class (ABC) that defines the structure for a game manager. It is responsible for managing the game board, turns, and game logic.

## Class: GameManager

### Constructor: `__init__`

Initializes a `GameManager` object with the specified parameters.

**Parameters:**

- `board` (`Board`): The game board object.

### Abstract Methods:

- `reset_board() -> None`: Resets the game board to its initial state.
- `make_move(move) -> None`: Makes a move on the game board.
- `unmake_move(move) -> None`: Undoes a move on the game board.
- `find_legal_moves() -> list`: Returns a list of all legal moves for the current player.
- `check_win() -> int`: Checks if the game has been won and returns the winner's score.

# Adversary Documentation

The `Adversary` class is responsible for managing the AI opponent in the game. It uses the minimax algorithm with alpha-beta pruning to determine the best move.

## Class: Adversary

### Constructor: `__init__`

Initializes an `Adversary` object with the specified parameters.

**Parameters:**

- `manager` (`GameManager`): The game manager object.

### Methods:

- `search(depth: int, alpha=float('-infinity'), beta=float('+infinity')) -> float`: Performs the minimax search with alpha-beta pruning to determine the best move.
- `search_root(depth: int) -> int`: Finds the best move for the current player by searching the game tree to the specified depth.

Both `search` and `search_root` methods are part of the minimax algorithm with alpha-beta pruning. The `search` method is used to evaluate the game state at a certain depth and the `search_root` method is used to find the best move by searching the game tree to a specified depth.

The `search` method uses the negamax variant of the minimax algorithm, which simplifies the implementation by avoiding the need to switch between maximizing and minimizing players. The `search_root` method is used to find the best move by iterating over all possible moves and choosing the one with the highest evaluation. If there are multiple moves with the same highest evaluation, a random choice is made among them.

The `alpha` and `beta` parameters are used in the alpha-beta pruning optimization to avoid exploring branches that are guaranteed to be worse than previously explored branches.