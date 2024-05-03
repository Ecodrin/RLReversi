import environment

import gymnasium

env = gymnasium.make('TicTacToe-v0', depth=10)
observation, info = env.reset()


while True:
    action = env.action_space.sample()
    observation, reward, done, _, info = env.step(action)
    env.render()
    if done:
        print(f'Reward: {reward}')
        observation, info = env.reset()
        break