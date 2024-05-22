import collections
import os
import pickle
import random
import matplotlib.pyplot as plt

from collections import defaultdict

import gymnasium as gym
import numpy as np

from tqdm import tqdm


class TicTacToeAgent:

    def __init__(
            self,
            env: gym.Env,
            learning_rate: float = 0.01,
            initial_epsilon: float = 1,
            epsilon_decay: float = None,
            final_epsilon: float = 0.1,
            discount_factor: float = 0.95) -> None:
        self.env: gym.Env = env
        self.q_values: collections.defaultdict = defaultdict(self.npzeros)

        self.lr: float = learning_rate
        self.discount_factor: float = discount_factor

        self.epsilon: float = initial_epsilon
        self.epsilon_decay: float = epsilon_decay
        self.final_epsilon: float = final_epsilon

        self.training_error: list = []

    def npzeros(self):
        return np.zeros(self.env.action_space.n)

    def get_action(self, obs: int) -> int:
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

    def update(
            self,
            obs: int,
            action: int,
            reward: float,
            terminated: bool,
            next_obs: int,
    ) -> None:
        """
        Update q_tables.
        :param obs: board.get_uid()
        :param action: step's man.
        :param reward: reward.
        :param terminated: win?
        :param next_obs: next board.get_uid()
        :return:
        """

        future_q_value = (not terminated) * np.max(self.q_values[next_obs])
        temporal_difference = (
                reward + self.discount_factor * future_q_value - self.q_values[obs][action]
        )

        self.q_values[obs][action] = (
                self.q_values[obs][action] + self.lr * temporal_difference
        )
        self.training_error.append(temporal_difference)

    def decay_epsilon(self) -> None:
        self.epsilon = max(self.final_epsilon, self.epsilon - self.epsilon_decay)

    def learn(self, total_episodes=50_000) -> None:
        victories = [0]
        losses = [0]
        if self.epsilon_decay is None:
            self.epsilon_decay = self.epsilon / (total_episodes / 2)
            # print(self.epsilon_decay)
        for episode in tqdm(range(total_episodes)):
            obs, info = self.env.reset()
            done = False
            while not done:
                action = self.get_action(obs)

                next_obs, reward, terminated, truncated, info = self.env.step(action)
                # update the agent
                self.update(obs, action, reward, terminated, next_obs)

                # update if the environment is done and the current obs
                done = terminated or truncated
                obs = next_obs
                if done and reward == -10:
                    losses.append(losses[-1] + 1)
                    victories.append(victories[-1])
                if done and reward == 10:
                    victories.append(victories[-1] + 1)
                    losses.append(losses[-1])
            self.decay_epsilon()
        plt.plot(victories)
        plt.show()
        plt.plot(losses, color='red')
        plt.show()

    def predict(self, obs: int, mask: list[int]) -> tuple[np.ndarray, float]:
        """
        :param obs: board.get_uid()
        :param mask: Is a list of current legal moves.
        :return: eval of steps, the best step.
        """
        # artificially remove illegal moves and randomly choose one of the best moves
        temp = self.q_values[obs].copy()
        print(temp, mask)
        temp[mask] += 10
        return temp, random.choice(np.where(temp.max() == temp)[0])

    def save(self, path: os.PathLike | str) -> None:
        """
        Save agent.
        :param path: path to agent.
        :return:
        """
        with open(path, 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def load(path: os.PathLike | str):
        with open(path, 'rb') as f:
            instance = pickle.load(f)
            instance.q_values = defaultdict(instance.npzeros, instance.q_values)
            return instance
