# TicTacToeManager Class

This class manages the Tic-Tac-Toe game board and the game logic.

## Methods

### __init__(self, board: Board = Board(3), pieces_to_win: int = None)
- Constructor for the TicTacToeManager class.
- Parameters:
    - board: Board object representing the game board.
    - pieces_to_win: Integer representing the number of pieces required to win.
- If pieces_to_win is not provided, it defaults to the size of the board.
- Initializes the board, crosses, noughts, turn, and pieces_to_win attributes.

### reset_board(self)
- Resets the game board by creating a new board.

### make_move(self, cell: int)
- Makes a move on the board at the specified cell for the current player (crosses or noughts).
- Updates the board state and changes the turn to the next player.

### unmake_move(self, cell: int)
- Reverts the move made at the specified cell.
- Removes the move from the player's list and updates the board state.

### find_legal_moves(self) -> list[int]
- Returns a list of legal moves (empty cells) on the board.

### check_win(self) -> int
- Checks if the current player has won the game.
- Returns 1 if the player wins, 0 if no one wins yet.

### is_game_ended(self) -> int
- Checks if the game has ended.
- Returns 1 if crosses win, -1 if noughts win, 0 for a draw, None if the game is ongoing.

# Adversary Class

This class represents an AI opponent for the Tic-Tac-Toe game.

## Methods

### __init__(self, manager)
- Constructor for the Adversary class.
- Initializes the adversary with a TicTacToeManager object.

### search(self, depth: int, alpha=float('-infinity'), beta=float('+infinity')) -> int
- Performs a search to evaluate the position.
- Returns the evaluation score for the current position.

### search_root(self, depth: int) -> int
- Finds the best move for the current player.
- Returns the best move to make.