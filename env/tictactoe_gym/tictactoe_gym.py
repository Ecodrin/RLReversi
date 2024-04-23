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
    def __init__(self, size: int = 3, pieces_to_win: int = 3, depht: int = 1):
        self.depht = depht
        self.size = size
        self.manager: TicTacToeManager = TicTacToeManager(Board(size), pieces_to_win)
        self.adversary: Adversary = Adversary(self.manager)
        self.action_space: ActType = ActionSpaceLegalMoves(self.manager.find_legal_moves())
        self.observation_space = gymnasium.spaces.Box(low=-1, high=1, shape=(1, self.size ** 2), dtype=np.int8)

    def reset(self, seed: int | None = None, options: dict[str, Any] | None = None) -> tuple[ObsType, dict[str, Any]]:
        self.manager.reset_board()
        self.action_space.legal_moves = self.manager.find_legal_moves()
        self.observation_space = gymnasium.spaces.Box(low=-1, high=1, shape=(1, self.size ** 2), dtype=np.int8)
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
        self.manager.make_move(self.adversary.search_root(self.depht))
        self.action_space.legal_moves = self.manager.find_legal_moves()
        reward = self.manager.has_game_ended()
        terminated = True if reward is not None else False
        return (self.manager.board.board, reward, terminated, False,
                {'step': action, 'win': terminated, 'reward': reward})

    def render(self, mode='human') -> None:
        match mode:
            case 'human':
                display(self.manager.board.board)
            case _:
                raise TypeError(f'mode {mode} not supported')

    def close(self):
        return 0


class ActionSpaceLegalMoves(spaces.Space):
    def __init__(self, legal_moves: list[int]):
        super().__init__()
        self.legal_moves = legal_moves

    def sample(self, mask: Any | None = None) -> int:
        move = random.choice(self.legal_moves)
        return move


def display(board: list[int]) -> None:
    for i in range(int(len(board) ** 0.5)):
        for j in range(int(len(board) ** 0.5)):
            print(f'{board[i * int(len(board) ** 0.5) + j]: >2} ', end='')
        print()
