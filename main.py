import gymnasium as gym
import env

envw = gym.envs.make('TicTacToe-v0')

observation, info = envw.reset()

for i in range(100):
    action = envw.action_space.sample()  # agent policy that uses the observation and info
    observation, reward, terminated, truncated, info = envw.step(action)
    envw.render()
    print('----')
    if terminated or truncated:
        print(f'reward: {reward}')
        envw.render()
        observation, info = envw.reset()

envw.close()
