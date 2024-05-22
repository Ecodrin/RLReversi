# TicTacToeAgent Documentation

This documentation provides an overview of the `TicTacToeAgent` class, which is an implementation of a reinforcement learning agent for the Tic Tac Toe game. The agent uses the Q-Learning algorithm to learn the optimal policy for the game.

## Imported Modules

The `TicTacToeAgent` class relies on several Python modules:

- `collections`: Provides alternative container data types.
- `os`: Provides a portable way of using operating system dependent functionality.
- `pickle`: Implements binary protocols for serializing and de-serializing a Python object structure.
- `random`: Generates pseudo-random numbers.
- `matplotlib.pyplot`: Provides a MATLAB-like plotting framework.
- `gymnasium`: A standard API for reinforcement learning and a diverse set of reference environments.
- `numpy`: Support for large, multi-dimensional arrays and matrices, along with a large collection of high-level mathematical functions to operate on these arrays.
- `tqdm`: Fast, extensible progress bar for Python and CLI.

## Class: TicTacToeAgent

### Constructor: `__init__`

Initializes the `TicTacToeAgent` with the given parameters.

**Parameters:**

- `env` (`gym.Env`): The environment in which the agent operates.
- `learning_rate` (`float`, optional): The learning rate for the Q-Learning algorithm. Defaults to `0.01`.
- `initial_epsilon` (`float`, optional): The initial exploration rate. Defaults to `1`.
- `epsilon_decay` (`float`, optional): The decay rate for the exploration rate. Defaults to `None`.
- `final_epsilon` (`float`, optional): The final exploration rate. Defaults to `0.1`.
- `discount_factor` (`float`, optional): The discount factor for future rewards. Defaults to `0.95`.

### Method: `get_action`

Returns the best action with probability `(1 - epsilon)`, otherwise a random action with probability `epsilon` to ensure exploration.

**Parameters:**

- `obs` (`int`): The current observation (board state).

**Returns:**

- `int`: The chosen action.

### Method: `update`

Updates the Q-values based on the observed reward and the next observation.

**Parameters:**

- `obs` (`int`): The current observation (board state).
- `action` (`int`): The action taken.
- `reward` (`float`): The reward received.
- `terminated` (`bool`): Whether the episode has ended.
- `next_obs` (`int`): The next observation (board state).

### Method: `decay_epsilon`

Decreases the exploration rate.

### Method: `learn`

Trains the agent by playing multiple episodes and updating the Q-values accordingly.

**Parameters:**

- `total_episodes` (`int`, optional): The total number of episodes to train for. Defaults to `50_000`.

### Method: `predict`

Predicts the best action to take given the current observation and a mask of legal moves.

**Parameters:**

- `obs` (`int`): The current observation (board state).
- `mask` (`list[int]`): A list of legal moves.

**Returns:**

- `tuple[np.ndarray, float]`: The evaluation of the steps and the best step.

### Method: `save`

Saves the agent to a file.

**Parameters:**

- `path` (`os.PathLike | str`): The path to the file where the agent will be saved.

### Method: `load`

Loads an agent from a file.

**Parameters:**

- `path` (`os.PathLike | str`): The path to the file from which the agent will be loaded.

**Returns:**

- `TicTacToeAgent`: The loaded agent instance.
