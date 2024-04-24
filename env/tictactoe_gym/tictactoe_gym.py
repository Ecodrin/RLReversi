from typing import SupportsFloat, Any
import random

import gymnasium
import numpy as np
from gymnasium import spaces
from gymnasium.core import ActType, ObsType

from src.board import Board
from src.manager import Adversary
from src.tictactoe import TicTacToeManager


class TicTacToeEnv(gymnasium.Env):
    def __init__(self, size: int = 3, pieces_to_win: int = 3, depth: int = 1):
        self.depth = depth
        self.size = size
        self.manager: TicTacToeManager = TicTacToeManager(Board(size), pieces_to_win)
        self.adversary: Adversary = Adversary(self.manager)
        self.action_space: ActType = MoveSpace(self.manager.find_legal_moves())
        self.observation_space: ObsType = gymnasium.spaces.Box(low=-1, high=1, shape=(self.size ** 2,), dtype=np.int8)

    def reset(self, seed: int | None = None, options: dict[str, Any] | None = None) -> tuple[ObsType, dict[str, Any]]:
        self.manager.reset_board()
        self.action_space.legal_moves = self.manager.find_legal_moves()
        return self.manager.board.board, {}

    def step(self, action: ActType) -> tuple[ObsType, SupportsFloat, bool, bool, dict[str, Any]]:
        """
        :param action: Клетка, куда ходит модель
        :return: (поле, оценка, победа(bool), False, информация о шаге)
        """
        self.manager.make_move(action)
        reward = self.manager.has_game_ended()
        if reward is not None:
            return self.manager.board.board, reward, True, False, {'step': action, 'win': False, 'reward': reward}
        # Умный ход ботяры(глубина выбирается по тому, что вам нужно)
        self.manager.make_move(self.adversary.search_root(self.depth))
        self.action_space.legal_moves = self.manager.find_legal_moves()
        reward = self.manager.has_game_ended()
        terminated = True if reward is not None else False
        return (self.manager.board.board, reward, terminated, False,
                {'step': action, 'win': terminated, 'reward': reward})

    def render(self, mode='human') -> None:
        match mode:
            case 'human':
                display(self.manager.board.board, self.size)
            case _:
                raise TypeError(f'Mode "{mode}" is not supported.')

    def close(self):
        return 0


class MoveSpace(spaces.Space):
    def __init__(self, legal_moves: list[int]):
        super().__init__()
        self.legal_moves = legal_moves

    def sample(self, mask: Any | None = None) -> int:
        move = random.choice(self.legal_moves)
        return move


def display(board: list[int], size: int = 3) -> None:
    """
    Display board.
    :param board: board
    :param size: size of the board
    :return:
    """
    for i in range(size):
        for j in range(size):
            print(f'{board[i * int(len(board) ** 0.5) + j]: >2} ', end='')
        print()
