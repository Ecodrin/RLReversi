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
    def __init__(self, count_cell: int = 3, count_win_cell: int = 3):
        self.observation_space: ObsType = spaces.Box(low=-1, high=1, shape=(count_cell, count_cell), dtype=np.int8)
        self.manager: TicTacToeManager = TicTacToeManager(Board(count_cell), count_win_cell)
        self.adversary: Adversary = Adversary(self.manager)
        self.action_space = ActionSpace(self.manager.find_legal_moves(), self.adversary)
        self.reward: int = 0
        self.current_player: int = 1

    def reset(self, seed: int | None = None, options: dict[str, Any] | None = None) -> tuple[ObsType, dict[str, Any]]:
        self.manager.reset_board()
        self.reward = 0
        return np.array(self.manager.board.board), {}

    def step(self, action: ActType) -> tuple[ObsType, SupportsFloat, bool, bool, dict[str, Any]]:
        if self.manager.board.board[action] != 0:
            print("Error")
        self.manager.make_move(action)
        terminated = True
        match self.manager.has_game_ended():
            case 1:
                self.reward = -1
            case 0:
                self.reward = 0
            case -1:
                self.reward = 1
            case _:
                terminated = False
        self.action_space.legal_moves = self.manager.find_legal_moves()
        return np.array(self.manager.board.board), self.reward, terminated, False, {}

    def render(self, mode='human') -> None:
        self.display()

    def display(self):
        for i in range(int(len(self.manager.board.board) ** 0.5)):
            for j in range(int(len(self.manager.board.board) ** 0.5)):
                print(f'{self.manager.board.board[i * int(len(self.manager.board.board) ** 0.5) + j]: >2} ', end='')
            print()

    def close(self):
        return 0


class ActionSpace(spaces.Space[np.ndarray]):
    def __init__(self, legal_moves: list[int], adversary: Adversary):
        super().__init__()
        self.adversary = adversary
        self.legal_moves = legal_moves

    def sample(self, mask: Any | None = None):
        ln = len(self.legal_moves)
        if ln % 2:
            move = random.choice(self.legal_moves)
        else:
            move = self.adversary.search_root(7)
            print(move)
        return move
