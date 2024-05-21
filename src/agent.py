import os
import pickle
import random

import gymnasium as gym
import numpy as np

from collections import defaultdict

from tqdm import tqdm
from numpy import zeros


class TicTacToeAgent:

    def __init__(
            self,
            env: gym.Env,
            learning_rate: float = 0.01,
            initial_epsilon: float = 1,
            epsilon_decay: float = None,
            final_epsilon: float = 0.1,
            discount_factor: float = 0.95
    ):
        self.env = env
        self.q_values = defaultdict(self.npzeros)

        self.lr = learning_rate
        self.discount_factor = discount_factor

        self.epsilon = initial_epsilon
        self.epsilon_decay = epsilon_decay
        self.final_epsilon = final_epsilon

    def npzeros(self):
        return np.zeros(self.env.action_space.n)

    def _get_action(self, obs: int) -> int:
        """
        Returns the best action with probability (1 - epsilon)
        otherwise a random action with probability epsilon to ensure exploration.
        """
        # with probability epsilon return a random action to explore the environment
        if np.random.random() < self.epsilon:
            return self.env.action_space.sample()
        # with probability (1 - epsilon) act greedily (exploit)
        else:
            return int(np.argmax(self.q_values[obs]))

    def _update(
            self,
            obs: int,
            action: int,
            reward: float,
            next_obs: int,
    ):

        future_q_value = (self.q_values[next_obs]).max()
        temporal_difference = (
            reward + self.discount_factor *
            future_q_value - self.q_values[obs][action]
        )

        self.q_values[obs][action] = (self.q_values[obs][action] + self.lr * temporal_difference
        )

    def _decay_epsilon(self):
        self.epsilon = max(self.final_epsilon,
                           self.epsilon - self.epsilon_decay)

    def learn(self, total_episodes: int = 50_000) -> None:
        if self.epsilon_decay is None:
            self.epsilon_decay = self.epsilon / (total_episodes / 2)

        for episode in tqdm(range(total_episodes)):
            obs, info = self.env.reset()
            done = False

            # play one episode
            while not done:
                action: int = self._get_action(obs)
                next_obs, reward, terminated, truncated, info = self.env.step(
                    action)

                # update the agent
                self._update(obs, action, reward, next_obs)

                # update if the environment is done and the current obs
                done: bool = terminated or truncated
                obs = next_obs

            self._decay_epsilon()

    # mask is a list of current legal moves
    def predict(self, obs: int, mask: list[int]) -> tuple[np.ndarray, int]:
        # artificially remove illegal moves and randomly choose one of the best moves
        temp: np.ndarray = self.q_values[obs].copy()
        temp[mask] += 10
        return temp, random.choice(np.where(temp.max() == temp)[0])

    def save(self, path: os.PathLike | str) -> None:
        with open(path, 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def load(path: os.PathLike | str):
        with open(path, 'rb') as f:
            instance: TicTacToeAgent = pickle.load(f)
            instance._q_values = defaultdict(
                instance.npzeros, instance.q_values)
            return instance
