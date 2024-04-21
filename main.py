import gymnasium as gym
import env

envw = gym.envs.make('TicTacToe-v0', pieces=3, pieces_to_win=3)

observation, info = envw.reset()

for i in range(100):
    action = envw.action_space.sample()
    observation, reward, terminated, truncated, info = envw.step(action)
    envw.render()
    print('----')
    if terminated or truncated:
        print(f'reward: {reward}')
        observation, info = envw.reset()

envw.close()
