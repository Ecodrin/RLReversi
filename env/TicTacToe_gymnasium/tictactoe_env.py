import gymnasium as gym
from gymnasium.spaces import Box, Discrete

from src.board import Board
from src.manager import Adversary
from src.tictactoe import TicTacToeManager


class TicTacToeEnv(gym.Env):
    def __init__(self, dimension: int = 3):
        super().__init__()
        self.size = dimension
        self.action_space = Discrete(dimension ** 2)
        self.observation_space = Box(low=0, high=2, shape=(dimension ** 2,), dtype=int)
        self.manager = TicTacToeManager(Board(dimension))
        self.adversary = Adversary(self.manager)

    def reset(self, *, seed=None, options=None):
        super().reset(seed=seed)
        self.manager.reset_board()
        return self.manager.board.board, {}

    def step(self, action):
        reward = self.manager.has_game_ended()
        if reward is not None:
            return self.manager.board.board, reward, True, False, {'action': action, 'win': reward == 1}

        self.manager.make_move(action)
        reward = self.manager.has_game_ended()
        if reward is not None:
            return self.manager.board.board, reward, True, False, {'action': action, 'win': reward == 1}

        adversary_action = self.adversary.search_root(1)
        self.manager.make_move(adversary_action)
        reward = self.manager.has_game_ended()
        return self.manager.board.board, reward, reward is not None, False, {'action': action, 'win': reward == 1}

    def render(self, mode='human'):
        if mode == 'human':
            for i in range(self.size):
                for j in range(self.size):
                    print(f'{self.manager.board.board[i * self.size + j]:^4}', end='')
                print()
        elif mode == 'ansi':
            output = ''
            for i in range(self.size):
                for j in range(self.size):
                    output += f'{self.manager.board.board[i * self.size + j]:^4}'
                output += '\n'
            return output

    def close(self):
        return None
