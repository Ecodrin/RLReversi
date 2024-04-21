from typing import SupportsFloat, Any
import random

import gymnasium
from gymnasium import spaces
import numpy as np
from gymnasium.core import ActType, ObsType

from src.board import Board
from src.manager import Adversary
from src.tictactoe import TicTacToeManager


class TicTacToeEnv(gymnasium.Env):
    def __init__(self, pieces: int = 3, pieces_to_win: int = 3):
        self.count_cell = pieces
        self.observation_space: spaces.Box = spaces.Box(low=-1, high=1, shape=(pieces, pieces), dtype=np.int8)
        self.manager: TicTacToeManager = TicTacToeManager(Board(pieces), pieces_to_win)
        self.adversary: Adversary = Adversary(self.manager)
        self.action_space: ActType = ActionSpace(self.manager.find_legal_moves())

    def reset(self, seed: int | None = None, options: dict[str, Any] | None = None) -> tuple[ObsType, dict[str, Any]]:
        self.manager.reset_board()
        self.action_space.legal_moves = self.manager.find_legal_moves()
        return self.manager.board.board, {}

    def step(self, action: ActType) -> tuple[ObsType, SupportsFloat, bool, bool, dict[str, Any]]:
        self.manager.make_move(action)
        reward = self.manager.has_game_ended()
        if reward is not None:
            return self.manager.board.board, reward, True, False, {}
        # Умный ход ботяры(глубина выбирается по тому, что вам нужно)
        self.manager.make_move(self.adversary.search_root(1))
        self.action_space.legal_moves = self.manager.find_legal_moves()
        reward = self.manager.has_game_ended()
        terminated = True if reward else False
        return self.manager.board.board, reward, terminated, False, {}

    def render(self, mode='human') -> None:
        if mode == 'human':
            self.display()

    def display(self) -> None:
        for i in range(int(len(self.manager.board.board) ** 0.5)):
            for j in range(int(len(self.manager.board.board) ** 0.5)):
                print(f'{self.manager.board.board[i * int(len(self.manager.board.board) ** 0.5) + j]: >2} ', end='')
            print()

    def close(self):
        return 0


class ActionSpace(spaces.Space[np.ndarray]):
    def __init__(self, legal_moves: list[int]):
        super().__init__()
        self.legal_moves = legal_moves

    def sample(self, mask: Any | None = None) -> int:
        move = random.choice(self.legal_moves)
        return move
